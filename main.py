import streamlit as st

# --- 웹 페이지 설정 ---
# 페이지 제목 설정
st.title("🐱 이름 입력 및 헬로 월드 출력 앱")

# 배경 이미지 URL (고양이 이미지)
# 실제 고양이 이미지 URL로 대체하거나, 로컬 파일을 사용할 수 있습니다.
# 여기서는 예시로 Placeholder 이미지를 사용합니다.
CAT_IMAGE_URL = "https://cdn2.thecatapi.com/images/MTU0MzI1OQ.gif" 

# 배경 이미지를 위한 사용자 정의 CSS (HTML 삽입)
background_css = f"""
<style>
.stApp {{
    /* 배경 이미지를 설정하고, 화면을 꽉 채우며, 반복되지 않도록 합니다. */
    background-image: url("{CAT_IMAGE_URL}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed; /* 스크롤해도 배경 고정 */
    background-position: center center;
    /* 텍스트가 잘 보이도록 대비를 위한 약간의 투명한 배경을 컨텐츠 영역에 적용할 수도 있습니다. */
}}

/* Streamlit의 메인 컨텐츠 영역의 배경을 투명하게 만듭니다. */
/* 이렇게 해야 배경 이미지가 보입니다. */
.stApp > header, .stApp > div:first-child {{
    background-color: rgba(0,0,0,0) !important;
}}

/* sidebar 배경 투명 설정 */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.7); /* 사이드바는 가독성을 위해 흰색 반투명으로 */
}}

/* 텍스트 컨텐츠 자체의 가독성을 높이기 위해 배경색을 약간 조절 */
[data-testid="stVerticalBlock"] {{
    background-color: rgba(255, 255, 255, 0.5); 
    padding: 10px;
    border-radius: 10px;
}}

h1, h2, h3, h4, .stMarkdown, .stTextInput > label, .stButton > button {{
    color: black; /* 텍스트 색상을 검은색으로 설정 (배경 이미지에 따라 조정 가능) */
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8); /* 가독성을 위한 그림자 */
}}

</style>
"""

# HTML을 사용하여 Streamlit 앱에 CSS 삽입
st.markdown(background_css, unsafe_allow_html=True)

# --- 사용자 입력 섹션 ---
# 사용자 이름 입력 필드 생성
user_name = st.text_input("당신의 이름을 입력하세요:")

# "입력" 버튼 생성
if st.button("입력"):
    # 버튼이 클릭되었을 때 실행되는 로직
    if user_name:
        # 입력된 이름과 함께 메시지 출력
        st.success(f"짠~ **{user_name}**님, 헬로 월드!")
    else:
        # 이름이 입력되지 않았을 경우 안내 메시지 출력
        st.warning("이름을 입력해 주세요.")
        
# --- 이미지 시각화 (선택적) ---
# st.image(CAT_IMAGE_URL, caption="사랑스러운 고양이", width=300)
