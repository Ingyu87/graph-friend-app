
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib import font_manager

# NanumGothic 폰트 적용
font_path = "fonts/NanumGothic.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()

st.set_page_config(page_title="그래프 친구!", page_icon="📊")

st.title("📊 그래프로 보기")

# 주제 입력
topic = st.text_input("조사할 주제를 입력해줘! (예: 좋아하는 운동)")

# 항목 수 고르기
num_items = st.slider("항목은 몇 개 조사할까?", min_value=2, max_value=8, value=4)

if topic:
    st.subheader(f"✏️ '{topic}'에 대해 조사해보자!")
    items = []
    counts = []

    with st.form(key="input_form"):
        for i in range(num_items):
            item = st.text_input(f"항목 {i+1}", key=f"item_{i}")
            count = st.number_input(f"명수 {i+1}", min_value=0, max_value=20, key=f"count_{i}")
            items.append(item)
            counts.append(count)

        submitted = st.form_submit_button("그래프 만들기!")

    if submitted:
        df = pd.DataFrame({"항목": items, "명수": counts})

        # 색상 랜덤 지정
        colors = ["#ffb347", "#87cefa", "#90ee90", "#f08080", "#dda0dd"]
        bg_colors = ["#f5f5ff", "#eef6ff", "#fdf5f5", "#f4fff4"]
        main_color = random.choice(colors)
        bg_color = random.choice(bg_colors)

        # 그래프
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor(bg_color)
        bars = plt.bar(df["항목"], df["명수"], color=main_color, alpha=0.7)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, '%d' % int(height), ha='center')
        plt.xlabel("항목")
        plt.ylabel("명수")
        plt.title(f"'{topic}'에 대한 결과")
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("🧠 퀴즈를 풀어보자!")

        max_item = df.loc[df['명수'].idxmax(), '항목']
        min_item = df.loc[df['명수'].idxmin(), '항목']
        diff_val = int(df['명수'].max() - df['명수'].min())

        # 퀴즈
        q1 = st.radio("1️⃣ 그래프에서 가장 많은 항목은 무엇일까?", df["항목"].tolist(), key="q1")
        if st.button("정답 확인", key="a1"):
            if q1 == max_item:
                st.success("정답이야! 잘했어~ ✅")
            else:
                st.error(f"아쉽다~ 정답은 '{max_item}'이었어")

        q2 = st.radio("2️⃣ 가장 적은 사람 수는 어떤 항목일까?", df["항목"].tolist(), key="q2")
        if st.button("정답 확인", key="a2"):
            if q2 == min_item:
                st.success("맞았어! 똑똑한걸? 😄")
            else:
                st.error(f"틀렸어! 정답은 '{min_item}'이야")

        q3 = st.radio(f"3️⃣ '{max_item}'은(는) '{min_item}'보다 몇 명 많을까?", [diff_val, diff_val+1, diff_val+2], key="q3")
        if st.button("정답 확인", key="a3"):
            if q3 == diff_val:
                st.success("정답! 잘 분석했어! 👏")
            else:
                st.error(f"정답은 {diff_val}명이야!")
