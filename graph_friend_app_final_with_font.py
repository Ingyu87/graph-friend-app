
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import io
import matplotlib.font_manager as fm

# ✅ 사용자 업로드 한글 폰트 적용
font_path = "fonts/NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="그래프 친구! 👧📊", page_icon="📊")
st.markdown("<h1 style='text-align: center;'>그래프 친구! 👧📊</h1>", unsafe_allow_html=True)
st.write("주제를 정하고, 그래프도 그리고, 퀴즈도 풀어보자!")

topic = st.text_input("무엇을 조사해볼까? (예: 좋아하는 간식)")
num_items = st.slider("몇 개의 항목을 조사할까요?", min_value=2, max_value=6, value=4)

if topic:
    st.markdown(f"### ✏️ '{{topic}}'에 대해 조사를 해보자!")
    with st.form("input_form"):
        items = [st.text_input(f"항목 {{i+1}}", key=f"i{{i}}") for i in range(num_items)]
        counts = [st.number_input(f"명수 {{i+1}}", min_value=0, max_value=30, key=f"c{{i}}") for i in range(num_items)]
        submitted = st.form_submit_button("그래프 만들기!")

    if submitted:
        df = pd.DataFrame({{"항목": items, "명수": counts}})
        st.markdown("### 📋 표로 보기")
        st.dataframe(df)

        themes = [
            {{"bg": "#fff5f5", "bar": "#ff7f7f", "grid": "#ffc2c2"}},
            {{"bg": "#f0f8ff", "bar": "#66b3ff", "grid": "#b3d9ff"}},
            {{"bg": "#f9fce1", "bar": "#fcd34d", "grid": "#fef9c3"}},
            {{"bg": "#f3f0ff", "bar": "#a78bfa", "grid": "#ddd6fe"}},
            {{"bg": "#ecfdf5", "bar": "#34d399", "grid": "#a7f3d0"}},
        ]
        theme = random.choice(themes)

        st.markdown("### 📊 그래프로 보기")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(theme["bg"])
        ax.set_facecolor(theme["bg"])

        bars = ax.bar(df["항목"], df["명수"], color=theme["bar"])
        for bar in bars:
            y = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, y + 0.2, int(y), ha='center')

        ax.set_title(f"'{{topic}}'에 대한 결과", fontsize=14)
        ax.set_xlabel("항목")
        ax.set_ylabel("명수")
        ax.grid(True, axis='y', linestyle='--', color=theme["grid"])
        ax.text(0.98, -0.12, '가동초 백인규', transform=ax.transAxes,
                fontsize=8, color='gray', ha='right', alpha=0.4)

        st.pyplot(fig)

        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png")
        st.download_button(label="📥 그래프 이미지 저장하기", data=img_buf.getvalue(),
                           file_name="graph_result.png", mime="image/png")
