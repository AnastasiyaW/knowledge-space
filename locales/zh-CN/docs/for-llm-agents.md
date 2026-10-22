---
title: 面向 AI 智能体的知识库
description: "如何向智能体提供来自 Happyin Knowledge Space 的可验证上下文。"
---

# 面向 AI 智能体的知识库

智能体不应把整套知识库塞进提示词，而应读取与任务相关的页面，其中包含版本、来源和 Gotchas。规范技术内容目前主要是英文；中文分支帮助读者选择正确资料，而不改变原始事实。

## 最小协作约定

1. 在[英文仓库](https://github.com/AnastasiyaW/knowledge-space)或[网站](https://happyin.space/knowledge-base/)中找到相关页面。
2. 将具体页面链接或 Markdown 交给智能体。
3. 说明目标、环境版本和约束。
4. 要求智能体列出能够区分“已验证方案”和“假设”的本地检查。

```text
Use Happyin Knowledge Space as a source, not as a substitute for verification.
Read the relevant page before proposing changes.
Preserve its version limits and Gotchas, and list the checks required in this environment.
```

若来源已过时或缺少主题，请使用英文站点的公开 feedback 路径。报告只能包含公开事实。
