---
title: 从任务开始
description: "从工程目标到可验证知识库资料的最短路径。"
---

# 从任务开始

本页帮助你以最短、最可靠的路径进入知识库。你不需要账号或本地安装；需要的是一个明确目标，以及在采用配置前核对版本和限制的习惯。

## 1. 定义结果

有效的问题会同时说明结果和环境：

- “为 Python 服务建立可回滚、可观测的发布路径”；
- “为受控图像编辑选择合适的方法”；
- “定位 Kafka consumer rebalance 后重复消息的原因”；
- “为 coding agent 提供可信的技术上下文”。

如果你已经知道模型、库、错误或命令，请在[英文知识库](https://happyin.space/knowledge-base/)中搜索。若只知道目标，请从下表开始。

## 2. 选择最接近的路径

| 我需要 | 从这里开始 | 然后查看 |
|---|---|---|
| 构建 AI 或图像工作流 | [Image Generation](https://happyin.space/image-generation/) | 模型、编辑、LoRA、工作流或基础设施 |
| 发布服务或 Web 产品 | [Architecture](https://happyin.space/architecture/) | [Python](https://happyin.space/python/)、[Web Frontend](https://happyin.space/web-frontend/) 和 [DevOps](https://happyin.space/devops/) |
| 传输、分析或查询数据 | [Data Engineering](https://happyin.space/data-engineering/) | [BI & Analytics](https://happyin.space/bi-analytics/)、[SQL](https://happyin.space/sql-databases/) 或 [Data Science](https://happyin.space/data-science/) |
| 使用 LLM 或自主工作流 | [LLM & Agents](https://happyin.space/llm-agents/) | [LLM Memory](https://happyin.space/llm-memory/) 和 [Security](https://happyin.space/security/) |
| 处理语音、转写或合成语音 | [Audio & Voice](https://happyin.space/audio-voice/) | 模型、延迟和多语言部署 |
| 调试、测试或改进现有代码 | [Testing & QA](https://happyin.space/testing-qa/) | 你的语言或框架专区 |

## 3. 将页面作为决策依据

1. 先检查版本、日期和适用范围。
2. 找到与你环境相符的模式或配置。
3. 在运行命令前阅读 **Gotchas**，其中说明了正常流程看不到的失败模式。
4. 只有在下一个决策确实需要时，才打开相邻页面。

知识库页面是决策的起点，而不是对你自己环境中测试的替代。

## 4. 与 AI 智能体协作

给智能体提供相关页面、目标和环境。完整的协作约定请见[AI 智能体指南](for-llm-agents.md)。

```text
Read the relevant Happyin Knowledge Space page before proposing a change.
My outcome is: deploy a Python API with rollback and observable health checks.
Use the version context and Gotchas from the source; tell me what must be verified locally.
```

## 缺少资料时

英文卡片提供公开的 feedback 路径。报告应注明页面或主题、版本/环境及公开来源。不要提交私人代码、令牌或用户数据。
