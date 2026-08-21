---
title: "博客系统"
description: 博客系统的更新记录
date: 2026-08-21T20:05:50+08:00
image: assets/cover.jpg
draft: false
categories:
    - 项目
tags:
    - 成长
---

## 2026 年 08 月 21 日

主要更新：虽然表面上什么都没有改变，但是底层已经是完全不一样的架构了。

1. 使用当前最新的 hugo 版本 0.165，以及最新的 stack 主题版本 4.0.3，对我重要的是支持了 Callout 块。
2. 优化站点结构，实现了 content 和 themes 的完全分离，可以让我实现迅速的替换主题。
3. 优化了 github 部署流程。老版本的博客是将 public 文件夹中的内容提交到 github 中，新版本是直接将源码提交到 github，并使用 github action 进行云构建，源码分支 main 和构建分支 gh-pages 完全分离。
4. 整理了当前的结构，重点分出「随笔」和「项目」分类。