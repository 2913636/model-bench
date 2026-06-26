# 多模型对比测试台
> 同一问题 → 多配置 → 并排对比速度/质量/成本

## 运行
```bash
pip install streamlit openai
set DEEPSEEK_KEY=你的Key
streamlit run bench.py
```

## 功能
- 3 路并排对比（不同 Prompt / Temperature / Max Tokens）
- 指标：耗时、输出 Token、总 Token
- 答案并排展示
