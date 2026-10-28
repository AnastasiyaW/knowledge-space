---
title: Contact
description: "How to reach the maintainers of Happyin Knowledge Space: GitHub issues for corrections and requests, Telegram for news and questions."
---

# Contact

## Corrections, questions and article requests

Open an issue in the public GitHub repository: [github.com/AnastasiyaW/knowledge-space/issues](https://github.com/AnastasiyaW/knowledge-space/issues). This is the fastest way to report a wrong or outdated page, ask for a topic, or raise a privacy question. Issues are public, so please do not include personal data; if you need to share something private, say so in the issue and we will arrange a private channel.

Pull requests are welcome too: [How to contribute](contributing/index.md).

## Telegram

News about the knowledge base and a place for questions: [t.me/happyin_space](https://t.me/happyin_space).

## Reports from AI assistants and scripts

An AI assistant or a script can report an outdated article or a missing topic with one request, no account needed. A plain GET works, so any fetch tool can send it:

```text
https://happyin.space/api/feedback/report?kind=gap&topic=<what you looked for>&agent=<your client name>
https://happyin.space/api/feedback/report?kind=outdated&article=<domain/slug>&detail=<what changed>
```

Scripts can also POST the same fields as JSON to `https://happyin.space/api/feedback`; a GET on that address returns the full list of fields. The reply carries a status link that shows what happens to the report. Send only what you would put in a public issue: no personal data, private code or secrets.

## Advertising and partnerships

Ads on this site are served by Google AdSense; we do not sell ad placements directly. For other partnership questions, open a GitHub issue or write in Telegram.
