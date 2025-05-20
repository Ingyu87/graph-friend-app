
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "fonts/NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()

st.set_page_config(page_title="그래프 친구", page_icon="📊")

st.title("📊 그래프 친구! 😎")

# 탭으로 인터페이스 구분
tab1, tab2 = st.tabs(["📥 입력하기", "📈 그래프 & 퀴즈"])

with tab1:
    st.header("📝 주제와 항목을 입력해줘!")
    topic = st.text_input("조사할 주제를 써보자! (예: 좋아하는 간식)")
    num_items = st.selectbox("항목 개수를 선택해줘!", options=[2, 3, 4, 5, 6, 7, 8])

    item_inputs = []
    count_inputs = []
    if topic:
        cols = st.columns(2)
        for i in range(num_items):
            with cols[0]:
                item = st.text_input(f"항목 {i+1}", key=f"item_{i}")
                item_inputs.append(item)
            with cols[1]:
                count = st.number_input(f"명수 {i+1}", min_value=0, max_value=20, key=f"count_{i}")
                count_inputs.append(count)

# 그래프 및 퀴즈 탭
with tab2:
    if topic and all(item_inputs) and len(item_inputs) == num_items:
        df = pd.DataFrame({"항목": item_inputs, "명수": count_inputs})

        st.subheader("📊 그래프로 보기")
        color_bg = random.choice(["#f9f9f9", "#eef2ff", "#fff7e6", "#f3f3fc"])
        color_bar = random.choice(["#ff9999", "#ffcc99", "#99ccff", "#c2c2f0"])

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(color_bg)
        bars = ax.bar(df["항목"], df["명수"], color=color_bar)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, height, f"{int(height)}", ha='center', va='bottom')
        ax.set_xlabel("항목")
        ax.set_ylabel("명수")
        ax.set_title(f"'{topic}'에 대한 결과", pad=15)
        st.pyplot(fig)

        st.divider()
        st.subheader("🧠 퀴즈를 풀어보자!")

        with st.form("quiz_form"):
            q1 = st.radio("1️⃣ 그래프에서 가장 많은 항목은 무엇일까?", df["항목"], key="q1")
            q2 = st.radio("2️⃣ 가장 적은 사람 수는 어떤 항목일까?", df["항목"], key="q2")
            delta = int(df["명수"].max() - df["명수"].min())
            delta_item = df.loc[df["명수"].idxmax(), "항목"]
            target_item = df.loc[df["명수"].idxmin(), "항목"]
            q3 = st.radio(f"3️⃣ '{delta_item}'은(는) '{target_item}'보다 몇 명 많을까?", [delta, delta+1, delta+2], key="q3")
            submitted = st.form_submit_button("정답 확인")

        if submitted:
            correct1 = df.loc[df["명수"].idxmax(), "항목"]
            correct2 = df.loc[df["명수"].idxmin(), "항목"]

            st.markdown("### 🧩 정답 확인 결과")
            if q1 == correct1:
                st.success("1번 정답이야! 🥳")
            else:
                st.error(f"1번 아쉬워~ 정답은 '{correct1}'였어.")

            if q2 == correct2:
                st.success("2번 정답이야! 🎉")
            else:
                st.error(f"2번 정답은 '{correct2}'였어.")

            if int(q3) == delta:
                st.success("3번도 정답! 완벽해요 💯")
                st.balloons()
            else:
                st.error(f"3번은 아쉬워요. 정답은 {delta}명이에요.")
    else:
        st.warning("먼저 주제와 항목을 모두 입력해줘!")
