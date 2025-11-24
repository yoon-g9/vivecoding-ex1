import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# --- 1. 페이지 설정 및 Custom CSS (비주얼 강화) ---
st.set_page_config(
    page_title="MBTI Global Insight",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: 그라디언트 배경, 카드 스타일, 폰트 조정
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background: linear-gradient(to right bottom, #1e1e2f, #252540);
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* 카드 스타일 컨테이너 */
    .css-card {
        border-radius: 20px;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* 텍스트 하이라이트 */
    .highlight {
        background: -webkit-linear-gradient(45deg, #FF512F, #DD2476);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    /* 메트릭 스타일 */
    div[data-testid="stMetricValue"] {
        color: #00d2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 헬퍼 함수: 데이터 로드 및 애니메이션 ---

@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

def load_lottieurl(url: str):
    try:
        # LottieFiles API는 외부 접근을 막을 수 있으므로 안정적인 URL 사용 및 타임아웃 설정
        r = requests.get(url, timeout=5) 
        if r.status_code != 200:
            # 403 Forbidden 에러 발생 시 경고 메시지 출력 후 None 반환
            st.warning(f"Lottie URL 접근 실패 (Status: {r.status_code}). 애니메이션이 표시되지 않을 수 있습니다.")
            return None
        return r.json()
    except requests.exceptions.RequestException as e:
        # 네트워크 연결 자체의 문제일 경우 처리
        st.warning(f"Lottie URL 로드 중 네트워크 오류 발생: {e}")
        return None

# MBTI 설명 및 메타데이터 (이전과 동일)
mbti_info = {
    "INTJ": {"name": "용의주도한 전략가", "desc": "상상력이 풍부하며 철두철미한 계획을 세우는 전략가형.", "icon": "♟️", "color": "#663399"},
    "INTP": {"name": "논리적인 사색가", "desc": "끊임없이 새로운 지식을 갈구하는 혁신가형.", "icon": "🧪", "color": "#3399ff"},
    "ENTJ": {"name": "대담한 통솔자", "desc": "대담하면서도 상상력이 풍부한 강한 의지의 지도자형.", "icon": "🎤", "color": "#cc3300"},
    "ENTP": {"name": "뜨거운 논쟁을 즐기는 변론가", "desc": "지적인 도전을 두려워하지 않는 똑똑한 호기심형.", "icon": "🔥", "color": "#ff6600"},
    "INFJ": {"name": "선의의 옹호자", "desc": "조용하고 신비로우며 샘솟는 영감으로 지칠 줄 모르는 이상주의자.", "icon": "🧙", "color": "#33cc33"},
    "INFP": {"name": "열정적인 중재자", "desc": "상냥하고 이타적이며 낭만적인 이상주의자.", "icon": "🌻", "color": "#99cc00"},
    "ENFJ": {"name": "정의로운 사회운동가", "desc": "넘치는 카리스마와 영향력으로 청중을 압도하는 리더형.", "icon": "🤝", "color": "#00cc99"},
    "ENFP": {"name": "재기발랄한 활동가", "desc": "창의적이고 항상 웃을 거리를 찾아다니는 활발한 성격.", "icon": "🎉", "color": "#ffcc00"},
    "ISTJ": {"name": "청렴결백한 논리주의자", "desc": "사실에 근거하여 사고하며 이성적으로 행동하는 유형.", "icon": "📋", "color": "#0099cc"},
    "ISFJ": {"name": "용감한 수호자", "desc": "소중한 이들을 수호하는 데 심혈을 기울이는 성실한 방어자형.", "icon": "🛡️", "color": "#6699ff"},
    "ESTJ": {"name": "엄격한 관리자", "desc": "사물과 사람을 관리하는 데 타의 추종을 불허하는 관리자형.", "icon": "⚖️", "color": "#3366cc"},
    "ESFJ": {"name": "사교적인 외교관", "desc": "타인을 향한 세심한 관심과 사교적인 성향으로 인기가 많음.", "icon": "🍰", "color": "#ff99cc"},
    "ISTP": {"name": "만능 재주꾼", "desc": "대담하고 현실적인 성향으로 다양한 도구 사용에 능숙함.", "icon": "🔧", "color": "#ffcc33"},
    "ISFP": {"name": "호기심 많은 예술가", "desc": "항상 새로운 것을 찾아 시도하거나 도전할 준비가 된 예술가형.", "icon": "🎨", "color": "#ffcc66"},
    "ESTP": {"name": "모험을 즐기는 사업가", "desc": "위험을 기꺼이 감수하며 영리하고 에너지가 넘치는 활동가형.", "icon": "🚀", "color": "#ff3300"},
    "ESFP": {"name": "자유로운 영혼의 연예인", "desc": "주위 사람을 즐겁게 해주며 에너지가 넘치는 연예인형.", "icon": "💃", "color": "#ff6699"},
}

# --- 3. 사이드바: 로고 및 선택 ---
with st.sidebar:
    st.title("🧬 Personality Lab")
    st.markdown("---")
    
    # Lottie 애니메이션 (뇌/생각)
    lottie_brain = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_SkhtL8.json")
    
    if lottie_brain:
        st_lottie(lottie_brain, height=150, key="brain_sidebar")
    
    st.markdown("### 🎯 Select Your MBTI")
    
    # 옵션 생성 (아이콘 포함)
    mbti_options = ["선택해주세요"] + list(mbti_info.keys())
    selected_mbti = st.selectbox("당신의 MBTI 유형은 무엇인가요?", mbti_options)
    
    st.markdown("---")
    st.info("💡 이 앱은 16가지 성격 유형의 전 세계 분포 데이터를 3D 시각화와 함께 제공합니다.")

# --- 4. 메인 콘텐츠 로직 ---

df = load_data()

if selected_mbti == "선택해주세요":
    # 초기 화면 (선택 전)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<h1 style='font-size: 3.5rem;'>Welcome to the <br><span class='highlight'>MBTI Universe</span></h1>", unsafe_allow_html=True)
        st.write("### 전 세계 데이터로 보는 나의 성격 유형 분석")
        st.write("왼쪽 사이드바에서 당신의 **MBTI**를 선택하여 시작하세요. 당신의 성격 유형이 전 세계 어디에서 가장 흔한지, 어떤 특징을 가지고 있는지 화려한 시각화로 보여드립니다.")
        st.write("---")
        st.write("👉 **Tip:** 차트는 마우스로 회전하고 확대/축소할 수 있습니다.")
        
    with col2:
        # ✅ URL 변경: 403 에러가 발생하던 URL을 다른 것으로 교체
        lottie_welcome = load_lottieurl("https://lottie.host/791c5e7b-c5e3-4f9e-a61b-94c65369c762/jLq9oH2D2y.json")
        
        if lottie_welcome:
            st_lottie(lottie_welcome, height=400, key="welcome")
        else:
            st.warning("애니메이션 로딩에 실패했습니다. (외부 URL 접근 문제)")

else:
    # --- 선택 후 화면 ---
    info = mbti_info[selected_mbti]
    
    # 1. 헤더 섹션
    st.markdown(f"""
    <div class='css-card'>
        <h1>{info['icon']} {selected_mbti} <span style='font-size:20px; color:#bbb'>: {info['name']}</span></h1>
        <p style='font-size: 1.2rem; font-style: italic;'>"{info['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. 통계 분석 및 멘트 생성
    try:
        # 해당 MBTI 컬럼 데이터 가져오기
        df_sorted = df.sort_values(by=selected_mbti, ascending=False)
        
        top_country = df_sorted.iloc[0]['Country']
        top_val = df_sorted.iloc[0][selected_mbti]
        
        korea_row = df_sorted[df_sorted['Country'] == 'South Korea']
        my_val = korea_row[selected_mbti].values[0] if not korea_row.empty else 0
        
        # 통계 요약 카드 (Metrics)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="🌏 가장 인기 있는 나라", value=top_country)
        with col2:
            st.metric(label="🔥 최고 비율", value=f"{top_val:.2%}")
        with col3:
            st.metric(label="🇰🇷 한국 내 비율", value=f"{my_val:.2%}")
        with col4:
            # 한국 순위 계산 (index는 0부터 시작하므로 1을 더함)
            rank = korea_row.index[0] + 1 if not korea_row.empty else "N/A"
            st.metric(label="🏆 한국 순위 (vs 전세계)", value=f"{rank}위" if rank != "N/A" else "N/A")

        # 맞춤형 멘트
        st.markdown(f"""
        <div class='css-card' style='text-align: center;'>
            <h3>📢 AI Insight</h3>
            <p style='font-size: 1.1rem;'>
                당신은 <b>{top_country}</b>에 가면 마음이 맞는 친구를 가장 많이 만날 수 있습니다! <br>
                전 세계적으로 {selected_mbti} 유형은 독특한 매력을 가지고 있으며, 
                특히 {top_country} 인구의 약 {top_val*100:.1f}%가 당신과 같은 성향을 공유합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. 시각화 섹션 (탭으로 구분)
        tab1, tab2 = st.tabs(["🌍 Global Map (2D)", "🌌 MBTI Galaxy (3D)"])
        
        with tab1:
            st.subheader(f"🗺️️ 전 세계 {selected_mbti} 분포도")
            # Choropleth Map
            fig_map = px.choropleth(
                df,
                locations="Country",
                locationmode="country names",
                color=selected_mbti,
                hover_name="Country",
                color_continuous_scale=px.colors.sequential.Plasma,
                projection="natural earth",
                title=f"World Distribution of {selected_mbti}"
            )
            fig_map.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                geo=dict(bgcolor= 'rgba(0,0,0,0)', showlakes=True, lakecolor='rgba(0,191,255,0.2)'),
                font=dict(color="white"),
                margin={"r":0,"t":30,"l":0,"b":0}
            )
            st.plotly_chart(fig_map, use_container_width=True)

        with tab2:
            st.subheader("🌌 3D 성격 성향 분석")
            st.write(f"{selected_mbti}와 다른 유형(가장 반대되는 유형 등) 간의 국가별 상관관계를 3D로 탐색합니다.")
            
            # 3D 축 설정을 위한 비교 MBTI 유형 선택
            compare_x = selected_mbti
            compare_y = "ESTP" if selected_mbti != "ESTP" else "INFJ"
            compare_z = "INFP" if selected_mbti != "INFP" else "ESTJ"

            fig_3d = px.scatter_3d(
                df,
                x=compare_x,
                y=compare_y,
                z=compare_z,
                color="Country",
                size=selected_mbti, # 선택된 MBTI 비율이 높을수록 점이 큼
                hover_name="Country",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                opacity=0.8,
                title=f"3D Cluster: {compare_x} vs {compare_y} vs {compare_z}"
            )
            fig_3d.update_layout(
                scene = dict(
                    xaxis = dict(backgroundcolor="rgba(0,0,0,0)", title=f"{compare_x} (You)"),
                    yaxis = dict(backgroundcolor="rgba(0,0,0,0)", title=f"{compare_y}"),
                    zaxis = dict(backgroundcolor="rgba(0,0,0,0)", title=f"{compare_z}"),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                margin={"r":0,"t":30,"l":0,"b":0},
                height=600
            )
            st.plotly_chart(fig_3d, use_container_width=True)

    except Exception as e:
        st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")
        st.write("CSV 파일의 형식이나 Streamlit 버전 호환성을 확인해주세요.")

# 푸터
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Created with ❤️ by Streamlit & AI | Data Source: Kaggle/User Upload</div>", unsafe_allow_html=True)
