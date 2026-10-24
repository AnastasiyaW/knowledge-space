---
title: 隐私
description: "Happyin Knowledge Space 如何使用数据、cookie 和广告。"
---

# 隐私

简体中文分支不会增加独立的数据收集系统；它使用与英文知识库相同的页面和规则。

## 无 cookie 统计

访问量由 Cloudflare Web Analytics 统计，不使用 cookie，也不进行浏览器指纹识别。匿名回访计数和“加星”按钮计数只在浏览器本地存储中保留记录；详情和开关见[英文政策](https://happyin.space/privacy/)。

## Google Analytics 与 Google 广告

在站点所有者完成配置后，页面会加载 Google Analytics 4，并在文章页面展示 Google AdSense 广告。Google 如何使用这些数据，请参阅[《Google 如何使用使用其服务的网站或应用中的信息》](https://policies.google.com/technologies/partner-sites?hl=zh-CN)以及 [Google 广告 cookie 说明](https://policies.google.com/technologies/ads?hl=zh-CN)。

**同意模式（Consent Mode v2）** 在任何 Google 脚本加载之前设置：

- **在欧洲经济区、英国和瑞士**，分析和广告存储默认关闭。你会看到提示，只有在选择“允许”后才会使用 Google Analytics cookie。在此之前，Google 可能收到不含 cookie 和广告标识符的信号（例如某个页面被浏览）。启用广告后，这些国家的个性化广告同意由 Google 认证的同意消息收集；未同意时广告不进行个性化。
- **在其他地区**，这些设置默认开启，Google 可能设置分析和广告 cookie。你可以随时关闭。
- **Global Privacy Control 或 Do Not Track** 会关闭全部选项：不加载 Google Analytics 标签，广告不基于 cookie 进行个性化。

**你的选择。** 每个页面页脚的“隐私选项”链接和下方按钮都会重新打开提示。选择“拒绝”会在此浏览器中将四个同意模式信号全部设为拒绝，停止我们的分析事件，并删除本站的 Google cookie（`_ga`、`_ga_*`、`__gads`、`__gpi`、`__eoi`）。你的选择保存在浏览器本地存储（`ks_consent_v2`）中。为判断是否需要提示，页面会请求本站的 `/api/consent-region`；它只根据 Cloudflare 从 IP 地址推断的国家回答“需要 / 不需要”，不保存国家信息。

**我们测量的内容。** 仅聚合行为：页面和文章浏览、搜索使用和结果打开、代码复制、GitHub 跳转和成功订阅。我们不会在事件中发送搜索词、提示词、电子邮箱、反馈文本、URL query string 或广告标识符；我们的分析关闭了 Google 信号和广告个性化。

**广告** 只出现在文章页面：不会出现在首页、本页以及“关于”和“联系”页面。你可以在 [Google 我的广告中心](https://myadcenter.google.com/)管理个性化广告。广告标有“广告”字样，不影响文章内容。

<p class="ks-counter-switch"><span data-ks-analytics-state>此开关需要 JavaScript。</span> <button type="button" class="md-button" data-ks-analytics-preferences hidden>隐私选项</button></p>

## Cookie

- **Google Analytics**（`_ga`、`_ga_*`，最长 2 年）和 **Google 广告 cookie**（本域名上的 `__gads`、`__gpi`、`__eoi`，以及 Google 域名上的 Google 自有 cookie）——仅按上文所述使用。
- **Cloudflare** 可能出于安全目的设置必要 cookie。
- **本地存储**（非 cookie）：回访计数、你的同意选择，以及订阅提示是否已关闭。

## 联系

隐私相关问题请通过 [GitHub Issues](https://github.com/AnastasiyaW/knowledge-space/issues) 或 [Telegram 频道](https://t.me/happyin_space)联系；详见[联系页面](contact.md)。请勿在公开 issue 中发布个人数据。

## 完整政策

完整的规范政策（订阅、问题报告、第三方服务）见[英文页面](https://happyin.space/privacy/)。在翻译完成独立法律审查前，如有差异，以英文文本为准。
