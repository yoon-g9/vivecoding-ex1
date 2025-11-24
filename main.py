import streamlit as st
import requests
import time
from PIL import Image
from io import BytesIO

# 1. 페이지 설정 및 강아지 사진 API 정의
# Dog API: 랜덤 강아지 이미지 URL을 제공합니다.
DOG_API_URL = "https://dog.ceo/api/breeds/image/random"
# st.set_page_config(layout="wide") # 전체 화면 사용 시 주석 해제

def fetch_dog_image_url():
    """Dog API에서 랜덤 강아지 이미지 URL을 가져옵니다."""
    try:
        response = requests.get(DOG_API_URL)
        response.raise_for_status() # HTTP 오류가 있으면 예외 발생
        data = response.json()
        return data.get("message")
    except Exception as e:
        st.error(f"강아지 이미지 API 호출 중 오류 발생: {e}")
        return None

def set_initial_state():
    """세션 상태를 초기화합니다."""
    if 'dog_image_url' not in st.session_state:
        st.session_state.dog_image_url = fetch_dog_image_url()
        st.session_state.last_update_time = time.time()
    if 'show_message' not in st.session_state:
        st.session_state.show_message = False

def update_dog_image():
    """10초마다 강아지 이미지를 업데이트합니다."""
    current_time = time.time()
    # 10초가 지났으면 이미지 업데이트
    if current_time - st.session_state.last_update_time >= 10:
        new_url = fetch_dog_image_url()
        if new_url:
            st.session_state.dog_image_url = new_url
            st.session_state.last_update_time = current_time

set_initial_state()
update_dog_image()

## 2. 웹앱 스타일 (배경 이미지 설정)
# 배경에 강아지 이미지를 넣기 위해 st.markdown과 CSS를 사용합니다.
# 이미지를 10초마다 변경하려면 URL을 동적으로 업데이트해야 합니다.
background_image_url = st.session_state.dog_image_url
if background_image_url:
    # CSS를 사용하여 배경 이미지를 설정하고, 새로고침(rerun) 시마다 URL을 업데이트합니다.
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover; /* 화면을 채우도록 설정 */
            background-repeat: no-repeat;
            background-attachment: fixed; /* 스크롤 시 이미지 고정 */
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

## 3. 메인 기능 구현 (이름 입력 및 메시지 출력)
st.title("🐾 헬로 월드 강아지 앱")
st.subheader("Streamlit으로 만드는 간단한 웹 애플리케이션")

# 사용자 이름 입력 필드
name = st.text_input("당신의 이름은 무엇인가요?", "이름을 입력하세요")

# 이름 입력 후 버튼을 누르면 메시지를 출력하는 콜백 함수
def display_message():
    """버튼 클릭 시 메시지 출력 상태를 True로 설정합니다."""
    st.session_state.show_message = True

# 입력 버튼 옆에 강아지 발바닥 이모티콘 추가: st.columns와 icon 매개변수를 활용합니다.
col1, col2 = st.columns([1, 10]) # 버튼 영역과 나머지 영역 분리

with col1:
    # st.button의 icon 매개변수는 버튼 내에 아이콘을 넣을 수 있지만,
    # '옆에' 강아지 발바닥을 넣으려면 컬럼을 사용하는 것이 일반적입니다.
    # 하지만 st.button 자체에 이모지 아이콘을 사용하여 발바닥을 '버튼 내부'에 넣는 것이 더 간단하고 효과적입니다.
    
    # st.button: 버튼 클릭 시 display_message 함수 실행
    if st.button("입력 🐾", on_click=display_message, help="이름을 입력하고 클릭하세요"):
        # 버튼이 클릭되면 Streamlit은 앱을 다시 실행합니다.
        pass

# 메시지 출력 로직
if st.session_state.show_message:
    # 이름을 사용하여 '헬로 월드' 메시지 출력
    if name and name != "이름을 입력하세요":
        st.success(f"짠~!! **헬로 월드, {name}님!**")
    else:
        st.warning("이름을 입력해주세요!")
    
    # 메시지 출력 후 다음 상호 작용을 위해 상태 초기화 (옵션)
    # st.session_state.show_message = False

## 4. 강아지 이미지 표시 (확인용)
# 배경에 이미지를 설정했으므로, 여기서는 현재 배경 이미지를 확인하는 용도로만 사용합니다.
if st.session_state.dog_image_url:
    st.markdown("---")
    st.write("### 현재 배경 강아지 이미지 (10초마다 변경)")
    
    # 강아지 이미지를 다운로드하여 표시 (배경 이미지는 CSS로 설정됨)
    try:
        response = requests.get(st.session_state.dog_image_url)
        img = Image.open(BytesIO(response.content))
        # st.image(img, caption="랜덤 강아지 사진", use_column_width=True)
    except Exception as e:
        # st.error(f"이미지 표시 오류: {e}")
        pass

# Streamlit 앱을 1초마다 다시 실행하여 10초 업데이트 로직이 작동하도록 합니다.
# 실제 프로덕션 환경에서는 이보다 효율적인 방법을 고려해야 하지만,
# Streamlit의 간단한 타이머 기능을 구현하는 데 유용합니다.
time.sleep(1)
st.rerun()
