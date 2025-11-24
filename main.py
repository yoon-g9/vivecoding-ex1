import streamlit as st

# --- 웹 페이지 설정 ---
st.title("🐾 움직이는 강아지 배경 & 강아지 버튼 앱")

# 움직이는 강아지 배경 GIF URL
ANIMATED_DOG_GIF_URL = "https://media.giphy.com/media/efg6i9yL7i4M8/giphy.gif"
# "입력" 버튼으로 사용할 강아지 아이콘 이미지 URL
DOG_BUTTON_ICON_URL = "https://www.flaticon.com/svg/static/icons/svg/1057/1057088.svg"

# 배경 이미지를 위한 사용자 정의 CSS (HTML 삽입)
background_css = f"""
<style>
.stApp {{
    background-image: url("{ANIMATED_DOG_GIF_URL}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center center;
}}

.stApp > header, .stApp > div:first-child {{
    background-color: rgba(0,0,0,0) !important;
}}

[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.7);
}}

[data-testid="stVerticalBlock"] {{
    background-color: rgba(255, 255, 255, 0.6); /* 투명도를 조금 높여 GIF가 더 잘 보이도록 */
    padding: 10px;
    border-radius: 10px;
}}

h1, h2, h3, h4, .stMarkdown, .stTextInput > label {{
    color: black;
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
}}

/* 강아지 버튼 스타일 */
.stButton > button {{
    background-color: #6A1B9A; /* 보라색 계열로 버튼 배경색 설정 */
    color: white;
    padding: 10px 20px;
    border-radius: 20px; /* 둥근 모서리 */
    border: none;
    cursor: pointer;
    font-size: 18px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px; /* 아이콘과 텍스트 간격 */
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3); /* 버튼 그림자 */
}}

.stButton > button:hover {{
    background-color: #4A148C; /* 호버 시 색상 변경 */
}}

/* 강아지 아이콘을 버튼 안에 넣기 위한 CSS */
.dog-button-icon {{
    width: 24px; /* 아이콘 크기 조절 */
    height: 24px;
    vertical-align: middle;
}}

</style>
"""

st.markdown(background_css, unsafe_allow_html=True)

# --- 사용자 입력 섹션 ---
user_name = st.text_input("당신의 이름을 입력하세요:")

# "입력" 버튼 생성 (강아지 아이콘 포함)
# HTML을 직접 사용하여 버튼 안에 아이콘을 넣습니다.
button_html = f"""
<button style="
    background-color: #4CAF50; /* 버튼 배경색 */
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 20px; /* 둥근 모서리 */
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    gap: 8px; /* 아이콘과 텍스트 사이 간격 */
">
    <img src="{DOG_BUTTON_ICON_URL}" alt="Dog Icon" style="width: 24px; height: 24px; filter: invert(100%);">
    입력
</button>
"""

# Streamlit 버튼 클릭 감지를 위해 st.button을 사용하고, 디자인은 CSS로 오버라이드합니다.
# 하지만 st.button은 내부적으로 자신의 스타일을 강제하기 때문에,
# 실제 HTML 버튼을 직접 만들어 클릭 이벤트를 처리하는 것은 Streamlit의 철학과 맞지 않습니다.
# 대신 st.button의 label에 HTML을 넣어 아이콘을 구현하는 방식으로 접근합니다.

# St.button의 label에 이미지와 텍스트를 포함
if st.button(f'<img src="{DOG_BUTTON_ICON_URL}" class="dog-button-icon" alt="dog"> 입력', unsafe_allow_html=True):
    if user_name:
        st.balloons() # 메시지 출력 시 풍선 효과 추가
        st.success(f"🐶 짠~ **{user_name}**님, 헬로 월드!")
    else:
        st.warning("이름을 입력해 주세요.")
