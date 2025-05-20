
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib import font_manager

# 한글 폰트 설정
font_path = "fonts/NanumGothic.ttf"
fontprop = font_manager.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = fontprop.get_name()

# 제목
st.set_page_config(page_title="그래프 친구!", page_icon="📊")
st.title("그래프 친구! 📊🧡")

# 입력 단계
topic = st.text_input("무엇을 조사해볼까? (예: 좋아하는 간식)", key="topic")

if topic:
    st.subheader(f"✏️ '{topic}'에 대해 조사해보자!")

    with st.form(key="main_form"):
        num_items = 4
        items = [st.text_input(f"항목 {i+1}", key=f"item_{i}_{topic}") for i in range(num_items)]
        counts = [st.number_input(f"명수 {i+1}", min_value=0, max_value=20, key=f"count_{i}_{topic}") for i in range(num_items)]
        submitted = st.form_submit_button("그래프 만들기!")

    if submitted:
        df = pd.DataFrame({'항목': items, '명수': counts})
        st.subheader("📋 표로 보기")
        st.dataframe(df)

        # 랜덤 스타일
        colors = ['#F4A261', '#2A9D8F', '#E76F51', '#9C89B8', '#8ECAE6']
        bg_color = random.choice(colors)
        bar_color = random.choice([c for c in colors if c != bg_color])
        grid_style = '--' if bg_color != '#8ECAE6' else '-.'

        # 그래프
        st.subheader("📊 그래프로 보기")
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar(df["항목"], df["명수"], color=bar_color)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, int(yval), ha='center', fontproperties=fontprop)
        ax.set_facecolor(bg_color)
        ax.set_xlabel("항목", fontproperties=fontprop)
        ax.set_ylabel("명수", fontproperties=fontprop)
        ax.set_title(f"'{topic}'에 대한 결과", fontproperties=fontprop)
        ax.grid(True, linestyle=grid_style, alpha=0.4)
        st.pyplot(fig)

        # 퀴즈
        st.subheader("🧠 퀴즈를 풀어보자!")

        max_idx = df["명수"].idxmax()
        min_idx = df["명수"].idxmin()

        q1 = st.radio("1️⃣ 그래프에서 가장 많은 항목은 무엇일까?", df["항목"].tolist(), key="q1")
        if st.button("정답 확인", key="btn_q1"):
            if q1 == df["항목"][max_idx]:
                st.success("정답이에요! 🎉")
                st.balloons()
            else:
                st.error(f"아쉬워요~ 정답은 '{df['항목'][max_idx]}'였어요.")
            st.markdown(f"🔍 해설: 그래프에서 막대가 가장 높은 항목이 바로 '{df['항목'][max_idx]}'이에요.")

        q2 = st.radio("2️⃣ 가장 적은 사람 수는 어떤 항목일까?", df["항목"].tolist(), key="q2")
        if st.button("정답 확인", key="btn_q2"):
            if q2 == df["항목"][min_idx]:
                st.success("정답이에요! 👍")
            else:
                st.error(f"틀렸어요 😢 정답은 '{df['항목'][min_idx]}'였어요.")
            st.markdown("🔍 해설: 제일 막대가 짧은 항목이 가장 적어요!")

        diff = int(df["명수"][max_idx]) - int(df["명수"][min_idx])
        q3 = st.radio(f"3️⃣ '{df['항목'][max_idx]}'은(는) '{df['항목'][min_idx]}'보다 몇 명 많을까?", [diff - 1, diff, diff + 1], key="q3")
        if st.button("정답 확인", key="btn_q3"):
            if q3 == diff:
                st.success("완벽해요! 👏")
            else:
                st.error(f"정답은 {diff}명이었어요.")
            st.markdown("🔍 해설: 가장 큰 수에서 가장 작은 수를 빼면 돼요!")

        # 워터마크
        st.markdown("<div style='text-align:right; font-size:10px; color:gray;'>가동초 백인규</div>", unsafe_allow_html=True)
