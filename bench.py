"""
多模型对比测试台
=================
同一个问题 → 多个配置 → 并排对比速度/质量/成本。
works with one API, expandable to more.

运行：streamlit run bench.py
"""

import os
import time
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="模型对比台", page_icon="⚡", layout="wide")
st.title("⚡ 多模型对比测试台")

client = OpenAI(api_key=os.getenv("DEEPSEEK_KEY", ""),
                base_url="https://api.deepseek.com")


def run_test(system_prompt, question, temp, max_tok, model="deepseek-chat"):
    """运行一次测试，返回耗时/token/答案"""
    start = time.time()
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=temp, max_tokens=max_tok
    )
    elapsed = time.time() - start
    usage = r.usage
    return {
        "answer": r.choices[0].message.content,
        "time_ms": int(elapsed * 1000),
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens
    }


# ═══ UI ═══
question = st.text_area("测试问题", height=80,
                         value="用一句话解释什么是 MCP 协议")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("配置 A")
    sys_a = st.text_area("System Prompt", value="简洁回答，不超过50字。",
                         key="a", height=100)
    temp_a = st.slider("Temperature", 0.0, 1.5, 0.3, 0.1, key="ta")
    max_a = st.slider("Max Tokens", 50, 1000, 200, 50, key="ma")

with c2:
    st.subheader("配置 B")
    sys_b = st.text_area("System Prompt", value="你是技术专家，详细解释。",
                         key="b", height=100)
    temp_b = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1, key="tb")
    max_b = st.slider("Max Tokens", 50, 1000, 600, 50, key="mb")

with c3:
    st.subheader("配置 C")
    sys_c = st.text_area("System Prompt", value="用表格形式回答。",
                         key="c", height=100)
    temp_c = st.slider("Temperature", 0.0, 1.5, 0.5, 0.1, key="tc")
    max_c = st.slider("Max Tokens", 50, 1000, 400, 50, key="mc")

if st.button("🚀 开始对比", type="primary"):
    with st.spinner("运行中..."):
        results = {}
        configs = [
            ("A", sys_a, temp_a, max_a),
            ("B", sys_b, temp_b, max_b),
            ("C", sys_c, temp_c, max_c),
        ]
        for label, sys, temp, mx in configs:
            if sys.strip():
                results[label] = run_test(sys, question, temp, mx)

    # ── 指标对比表 ──
    st.divider()
    st.subheader("📊 指标对比")

    cols = st.columns(len(results))
    for i, (label, r) in enumerate(results.items()):
        cols[i].metric(f"配置 {label}", "")
        cols[i].metric("⏱️ 耗时", f"{r['time_ms']}ms")
        cols[i].metric("📝 输出 Token", r['completion_tokens'])
        cols[i].metric("💰 总 Token", r['total_tokens'])

    # ── 答案并排 ──
    st.divider()
    st.subheader("📝 答案并排对比")
    cols = st.columns(len(results))
    for i, (label, r) in enumerate(results.items()):
        with cols[i]:
            st.write(f"**配置 {label}** (t={temp_a if label=='A' else temp_b if label=='B' else temp_c})")
            st.info(r['answer'])
