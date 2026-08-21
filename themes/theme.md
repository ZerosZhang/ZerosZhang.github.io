# 主题说明与更换指南

本文件记录本站使用的主题信息，以及修改主题 / 更换主题的完整操作步骤。

## 当前使用的主题

| 项目 | 信息 |
|---|---|
| 主题名称 | Hugo Theme Stack |
| 当前版本 | v4.0.3 |
| 主题目录 | `themes/hugo-theme-stack-4.0.3/` |
| 主题作者 | Jimmy Cai |
| GitHub 仓库 | https://github.com/CaiJimmy/hugo-theme-stack |
| 主题文档 | https://stack.jimmycai.com/ |
| 演示站点 | https://demo.stack.jimmycai.com/ |

## 主题的加载方式

本站使用 Hugo 的 **themes 目录方式**：主题源码直接复制在 `themes/hugo-theme-stack-4.0.3/` 下，与站点源码一起提交到 Git。

```toml
# hugo.toml 中指定主题
theme = 'hugo-theme-stack-4.0.3'
```

## 更换主题的完整流程

本站使用 Hugo 0.165，**主题目录内的 `config/` 和 `hugo.toml` 不会被 Hugo 加载**，所有配置一律以站点根目录的 `hugo.toml` 为准。

### 核心思路：每个主题自带一份配置

**每个主题目录下都保存一份该主题当前生效的完整 `hugo.toml`**。换主题时，把对应主题目录里的 `hugo.toml` 复制到站点根目录即可生效，无需任何额外调整。
