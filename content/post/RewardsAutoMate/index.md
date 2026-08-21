---
title: 'Microsoft Rewards 自动获取助手'
description: 用于每天调用 Bing 搜索，以达到获取 Reward 的功能。
date: 2025-02-06T15:44:39+08:00
image: assets/cover.jpg
categories:
    - 项目
tags:
    - 软件
---

## 关于 Microsoft Rewards

![](assets/ZMicrosoftRewards-1748076929110-5.png)

`Microsoft Rewards` 是微软出品的一款软件，可以通过搜索 `Bing` 来获取奖励，奖励的种类有很多，包括现金、积分、礼品等。但是我老是忘记搜索 `Bing`，因此就实现了一个软件，帮助我每天自动搜索 `Bing`。

我并没有将该功能添加到 `ZerosTodo` 中，因为我并不希望该功能影响我正常使用电脑，所以我拿了一个老笔记本安装了 `Windows Server 2016`，当作我的服务器。

另外，`Rewards` 也有手机端的搜索任务，但是手机我是随身带着，所以我并没有实现安卓端的软件，直接使用油猴脚本进行替代。

## 关于 RewardsAutoMate

1. 自动搜索功能

该软件用于在 PC 端获取随机的搜索关键词，自动搜索 `Bing`，每天搜索 40 次，每隔 12 个小时执行一次任务。如果当天已经完成了任务，则不会继续执行。

![](assets/ZAutoSearch-1748076929110-6.png)

2. 热力图功能

为了记录每天的搜索情况，该软件会生成如 `Github` 的热力图，用于记录每天的搜索情况。

![该图片使用随机数据](assets/ZHeatMap-1748076929110-7.png)

3. 自动登录功能

`Rewards` 和微软账号相关，所以在打开 `EdgeDriver` 时，要调用本地的账户信息进行登录。

项目代码上传到此处：[RewardsAutoMate](https://gitee.com/Zeros_Zhang/rewards-auto-mate)

## 更新记录

    - 2025年4月18日 更新：通过 `UserAgent` 伪装成移动设备，这样可以在 `PC` 端实现移动端的搜索。
