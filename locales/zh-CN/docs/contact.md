---
title: 联系
description: "如何联系 Happyin Knowledge Space 的维护者：通过 GitHub Issues 提交更正和请求，通过 Telegram 获取新闻和提问。"
---

## 更正、问题和文章请求

请在公开的 GitHub 仓库中创建 issue：[github.com/AnastasiyaW/knowledge-space/issues](https://github.com/AnastasiyaW/knowledge-space/issues)。这是报告错误或过时页面、请求新主题或提出隐私问题的最快方式。Issue 是公开的，请勿包含个人数据；如需提供私密信息，请在 issue 中说明，我们会安排私下沟通的渠道。

也欢迎提交 Pull Request：[如何参与](https://happyin.space/contributing/)。

## Telegram

知识库新闻和提问的地方：[t.me/happyin_space](https://t.me/happyin_space)。

## 来自 AI 助手和脚本的报告

AI 助手或脚本无需账号，只需一次请求即可报告过时文章或缺失主题。普通的 GET 请求即可，因此任何抓取工具都能发送：

```text
https://happyin.space/api/feedback/report?kind=gap&topic=<what you looked for>&agent=<your client name>
https://happyin.space/api/feedback/report?kind=outdated&article=<domain/slug>&detail=<what changed>
```

脚本也可以将相同字段以 JSON 格式 POST 到 `https://happyin.space/api/feedback`；对该地址发送 GET 会返回完整的字段列表。回复中包含状态链接，可查看报告的处理情况。只发送你愿意写进公开 issue 的内容：不要包含个人数据、私有代码或密钥。

## 广告与合作

本站广告由 Google AdSense 提供；我们不直接出售广告位。其他合作问题，请创建 GitHub issue 或在 Telegram 留言。
