# 多模型对比测试台

> 同一问题 -> 多模型/多配置 -> 并排对比速度/质量/成本。

## 快速开始

```bash
pip install openai streamlit
set DEEPSEEK_KEY=sk-your-key

# Streamlit UI
streamlit run bench.py

# CLI 批量（3 种配置自动对比）
py bench.py --cli "什么是 MCP 协议？"
```

## 功能

- 3 路并排对比（不同 Prompt / Temperature / Model）
- 指标：耗时、Token、成本（美元）
- Streamlit UI + CLI 两种模式
- 结果自动保存 JSON
- 预设模型：DeepSeek V3 / DeepSeek R1

## 面试价值

- 多模型实践经验
- 成本意识（每次调用计算费用）
- 参数对比 + 批量测试
