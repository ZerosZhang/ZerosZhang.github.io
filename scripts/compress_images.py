#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客图片自动压缩脚本
====================

功能：
  - 扫描 content/ 下所有文章图片（封面 cover.jpg 及正文截图）
  - 封面图：压缩到最大宽度 COVER_MAX_W，目标 ≤ COVER_TARGET
  - 截图：  压缩到最大宽度 OTHER_MAX_W，目标 ≤ OTHER_TARGET
  - GIF 动图自动跳过（避免损坏动画）
  - 幂等：已达标（≤目标大小）的图片跳过不动，可反复运行

用法：
  python scripts/compress_images.py            # 实际压缩
  python scripts/compress_images.py --dry-run  # 只预览会改哪些，不写盘

自定义阈值（可选）：
  python scripts/compress_images.py --cover-max-w 1200 --cover-target 300
  python scripts/compress_images.py --other-max-w 1600 --other-target 1000

依赖：pip install Pillow
"""

import argparse
import io
import os

from PIL import Image

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")

DEFAULTS = {
    "cover_max_w": 1200,
    "cover_target_kb": 300,
    "other_max_w": 1600,
    "other_target_kb": 1000,
    "min_quality": 40,
}


def human(n):
    if n >= 1024 * 1024:
        return f"{n / 1024 / 1024:.1f}MB"
    return f"{n / 1024:.0f}KB"


def compress_to_target(base_size, img, max_w, target, is_png):
    """压缩图像到目标大小以下；无法做到时返回 None。"""
    img = img.convert("RGB") if not is_png else img
    w, h = img.size
    if w > max_w:
        img = img.resize((max_w, int(h * max_w / w)), Image.LANCZOS)

    if is_png:
        buf = encode(img, "PNG", optimize=True)
        return buf if len(buf) <= target else None

    for q in (85, 80, 75, 70, 65, 60, 55, 50, 45, 40):
        buf = encode(img, "JPEG", quality=q, optimize=True, progressive=True)
        if len(buf) <= target:
            return buf
    buf = encode(img, "JPEG", quality=40, optimize=True, progressive=True)
    if len(buf) < base_size:
        return buf
    return None


def encode(img, fmt, **kw):
    b = io.BytesIO()
    img.save(b, fmt, **kw)
    return b.getvalue()


def iter_target_files(args):
    if getattr(args, "paths", None):
        for p in args.paths:
            abspath = os.path.abspath(p)
            if not os.path.isfile(abspath):
                print(f"WARN 不存在: {p}")
                continue
            yield abspath
        return
    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        for fn in filenames:
            yield os.path.join(dirpath, fn)


def process(args):
    total_before = total_after = 0
    changed = skipped = 0
    for path in iter_target_files(args):
        ext = os.path.splitext(path)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png"):
            continue

        try:
            size = os.path.getsize(path)
        except OSError:
            continue
        is_cover = os.path.basename(path).lower() == "cover.jpg"
        max_w = args.cover_max_w if is_cover else args.other_max_w
        target = args.cover_target_kb * 1024 if is_cover else args.other_target_kb * 1024

        if size <= target:
            skipped += 1
            continue

        total_before += size
        try:
            img = Image.open(path)
            img.load()
            if getattr(img, "is_animated", False):
                print(f"SKIP  (动图)  {path} ({human(size)})")
                continue
            buf = compress_to_target(size, img, max_w, target, ext == ".png")
        except Exception as e:
            print(f"ERROR {path}: {e}")
            continue

        if buf is None:
            print(f"KEEP  (压不动)  {path} ({human(size)})")
            continue

        if args.dry_run:
            print(f"DRY   {path}: {human(size)} -> ~{human(len(buf))}")
        else:
            with open(path, "wb") as f:
                f.write(buf)
            print(f"OK    {path}: {human(size)} -> {human(len(buf))}")
        total_after += len(buf)
        changed += 1

    print("\n=== 统计 ===")
    print(f"已处理 {changed} 张（已达标跳过 {skipped} 张）")
    if changed:
        print(f"总体积: {human(total_before)} -> {human(total_after)} (节省 {human(total_before - total_after)})")
    if args.dry_run:
        print("(dry-run 模式，未实际写盘)")


def main():
    ap = argparse.ArgumentParser(description="Hugo 博客图片压缩")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写盘")
    ap.add_argument("--cover-max-w", type=int, default=DEFAULTS["cover_max_w"])
    ap.add_argument("--cover-target", dest="cover_target_kb", type=int, default=DEFAULTS["cover_target_kb"], metavar="KB")
    ap.add_argument("--other-max-w", type=int, default=DEFAULTS["other_max_w"])
    ap.add_argument("--other-target", dest="other_target_kb", type=int, default=DEFAULTS["other_target_kb"], metavar="KB")
    ap.add_argument("--paths", nargs="+", metavar="FILE",
                    help="只处理指定文件（供 git hook 使用）；缺省扫描整个 content/")
    args = ap.parse_args()

    if not os.path.isdir(BASE_DIR):
        print(f"未找到 content 目录: {BASE_DIR}")
        return
    process(args)


if __name__ == "__main__":
    main()
