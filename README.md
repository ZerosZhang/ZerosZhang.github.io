# Zeros遇见的作品集合

基于 [Hugo](https://gohugo.io/) + [Stack 主题](https://github.com/CaiJimmy/hugo-theme-stack) 构建的静态个人博客。

## 技术栈

- Hugo（extended 版，本地 `hugo.exe`，v0.165.0）
- Hugo Theme Stack v4.0.3（`themes/` 内嵌）
- SCSS / TypeScript（由 Hugo Pipes 编译，无需 Node.js）

## 目录结构

```
├── hugo.toml          # 站点全部配置（含主题参数）
├── content/
│   ├── post/          # 文章（Page Bundle，每篇一个文件夹）
│   └── page/          # 独立页面（about、archives、search、projects 等）
├── themes/
│   └── hugo-theme-stack-4.0.3/   # Stack 主题（内嵌，可自定义）
├── static/            # 静态资源（avatar 等）
└── public/            # 构建输出（部署用，已 gitignore）
```

## 常用命令

```bash
# 本地预览（含草稿）
./hugo.exe server -D

# 构建站点（输出到 public/）
./hugo.exe

# 新建文章
./hugo.exe new post/主题名称/index.md
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

`public/` 目录是一个独立的 Git 仓库，remote 指向 GitHub Pages 仓库，构建后推送即可部署。
