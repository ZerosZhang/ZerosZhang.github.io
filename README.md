# Zeros遇见的作品集合

基于 [Hugo](https://gohugo.io/) + [Stack 主题](https://github.com/CaiJimmy/hugo-theme-stack) 构建的静态个人博客。

**博客地址：https://zeroszhang.github.io/**

## 技术栈

- Hugo（extended 版，本地 `hugo.exe`，v0.165.0）
- Hugo Theme Stack v4.0.3（`themes/` 内嵌）

## 目录结构

```
├── hugo.toml          # 站点全部配置（含主题参数）
├── hugo.exe           # 下载的 hugo 程序（自行下载）
├── content/
│   ├── post/          # 文章（Page Bundle，每篇一个文件夹）
│   └── page/          # 独立页面（about、archives、search、projects 等）
├── themes/            # 主题文件夹（内嵌，可自定义）
```

## 常用命令

```bash
# 新建文章
./hugo new post/主题名称/index.md

# 本地预览
./hugo server -D

# 构建站点（输出到 public/，已使用 github action 自动完成）
./hugo
```

## 侧边栏菜单

| 菜单 | 指向 | 定义位置 |
|---|---|---|
| 主页 | `/` | `hugo.toml` |
| 随笔 | `/categories/随笔/` | `hugo.toml` |
| 项目 | `/categories/项目/` | `hugo.toml` |
| 归档 | `/archives/` | `content/page/archives` |
| 关于 | `/关于/` | `content/page/about` |

## 文章规范

- 每篇文章一个文件夹（Page Bundle），标题图统一放在 `assets/cover.jpg`
- front matter 字段：`title`、`description`、`date`、`image`、`categories`、`tags`
- 分类通过 `categories` 字段自动聚合（随笔、项目等）

## 部署

推送到 `main` 分支后，[GitHub Actions](.github/workflows/deploy.yml) 自动构建并部署到 `gh-pages` 分支。

由 GitHub Pages 发布到 https://zeroszhang.github.io/

## 图片压缩

写文章时图片可能过大（截图、封面动辄几 MB），仓库体积会膨胀。项目内置了自动压缩工具：

- **压缩脚本**：`.github/scripts/compress_images.py`（依赖 Pillow，`pip install Pillow`）
- **git hook**：`.github/hooks/pre-commit`，每次 `git commit` 时自动压缩本次暂存的图片（封面 ≤300KB/宽 1200px，截图 ≤1MB/宽 1600px，GIF 跳过）

新电脑 clone 后需配置一次 hook

```bash
git config core.hooksPath .github/hooks
```
