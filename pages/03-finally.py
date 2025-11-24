import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
import time

# --- 1. 페이지 설정 & 스타일링 (삐까번쩍 모드) ---
st.set_page_config(
    page_title="Global MBTI Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS: 그라디언트, 폰트, 카드 스타일링
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .main {
        background-color: #0e1117;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 타이틀 스타일링 */
    h1 {
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        padding-bottom: 10px;
    }
    
    /* 카드 박스 효과 */
    .css-1r6slb0, .stMetric {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .stMetric:hover {
        transform: scale(1.02);
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 로드 및 전처리 ---
@st.cache_data
def load_data():
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

df = load_data()

# --- 3. MBTI 데이터 사전 (설명 및 별명) ---
mbti_info = {
    "INTJ": {"name": "용의주도한 전략가", "icon": "♟️", "desc": "상상력이 풍부하며 철두철미한 계획을 세우는 전략가형입니다."},
    "INTP": {"name": "논리적인 사색가", "icon": "🧪", "desc": "끊임없이 새로운 지식에 목말라하는 혁신가형입니다."},
    "ENTJ": {"name": "대담한 통솔자", "icon": "🦁", "desc": "대담하고 상상력이 풍부하며 강한 의지의 지도자형입니다."},
    "ENTP": {"name": "뜨거운 논쟁을 즐기는 변론가", "icon": "🔥", "desc": "지적인 도전을 두려워하지 않는 똑똑한 호기심형입니다."},
    "INFJ": {"name": "선의의 옹호자", "icon": "🧙‍♂️", "desc": "조용하고 신비로우며 샘솟는 영감으로 타인을 돕는 이상주의자입니다."},
    "INFP": {"name": "열정적인 중재자", "icon": "🌿", "desc": "상냥하고 이타적이며 낭만적인 성향을 가진 중재자형입니다."},
    "ENFJ": {"name": "정의로운 사회운동가", "icon": "🗣️", "desc": "넘치는 카리스마와 영향력으로 청중을 압도하는 리더형입니다."},
    "ENFP": {"name": "재기발랄한 활동가", "icon": "🎉", "desc": "창의적이며 항상 웃을 거리를 찾아다니는 활발한 활동가형입니다."},
    "ISTJ": {"name": "청렴결백한 논리주의자", "icon": "📊", "desc": "사실에 근거하여 사고하며 현실 감각이 뛰어난 모범생형입니다."},
    "ISFJ": {"name": "용감한 수호자", "icon": "🛡️", "desc": "소중한 이들을 지키기 위해 헌신하는 성실한 방어자형입니다."},
    "ESTJ": {"name": "엄격한 관리자", "icon": "⚖️", "desc": "사물과 사람을 관리하는 데 타의 추종을 불허하는 관리자형입니다."},
    "ESFJ": {"name": "사교적인 외교관", "icon": "🤝", "desc": "타인을 향한 세심한 관심과 사교적인 성향을 가진 마당발형입니다."},
    "ISTP": {"name": "만능 재주꾼", "icon": "🛠️", "desc": "대담하고 현실적인 성향으로 다양한 도구 사용에 능숙한 탐험가형입니다."},
    "ISFP": {"name": "호기심 많은 예술가", "icon": "🎨", "desc": "항상 새로운 것을 찾아 시도하거나 도전할 준비가 된 융통성 있는 성향입니다."},
    "ESTP": {"name": "모험을 즐기는 사업가", "icon": "🚀", "desc": "위험을 기꺼이 감수하며 영리하고 에너지 넘치는 사업가형입니다."},
    "ESFP": {"name": "자유로운 영혼의 연예인", "icon": "💃", "desc": "주위에 있으면 인생이 지루할 새가 없을 정도로 즉흥적인 연예인형입니다."}
}

# Lottie 애니메이션 URL
lottie_welcome = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_puciaact.json")
lottie_analysis = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_w51pcehl.json")

# --- 4. 사이드바 UI ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
    st.title("MBTI Selector")
    st.markdown("---")
    
    # 초기 상태: 선택 안됨
    options = ["선택해주세요"] + list(mbti_info.keys())
    selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", options)
    
    st.markdown("---")
    st.info("💡 이 앱은 전 세계 MBTI 분포 데이터를 기반으로 분석합니다.")
    st.caption("Created with Streamlit & Plotly")

# --- 5. 메인 로직 ---

if selected_mbti == "선택해주세요":
    # --- 초기 화면 (Landing Page) ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("Welcome to\nGlobal MBTI World! 🌍")
        st.markdown("### 당신의 성격 유형은\n### 전 세계 어디에서 가장 흔할까요?")
        st.markdown("👈 **왼쪽 사이드바**에서 당신의 MBTI를 선택하고\n놀라운 통계를 확인해보세요!")
        st.markdown("---")
        st.success("✨ 준비되셨나요? 바로 시작해보세요!")
    
    with col2:
        if lottie_welcome:
            st_lottie(lottie_welcome, height=400, key="welcome")

else:
    # --- 분석 결과 화면 ---
    
    # 1. 헤더 섹션
    info = mbti_info[selected_mbti]
    
    # 애니메이션과 타이틀
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title(f"{info['icon']} {selected_mbti}")
        st.subheader(f"**{info['name']}**")
        st.write(f"> *{info['desc']}*")
    with col_h2:
        if lottie_analysis:
            st_lottie(lottie_analysis, height=150, key="analysis")

    st.markdown("---")

    # 2. 데이터 분석
    # 해당 MBTI 컬럼 데이터 추출 및 정렬
    target_col = selected_mbti
    
    # 상위 5개 국가 추출
    top_countries = df[['Country', target_col]].sort_values(by=target_col, ascending=False).head(5)
    top_country_name = top_countries.iloc[0]['Country']
    top_country_val = top_countries.iloc[0][target_col]
    
    # 평균 계산
    global_avg = df[target_col].mean()

    # 3. 핵심 지표 (Metrics)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="전 세계 평균 비율", value=f"{global_avg:.2%}")
    with m2:
        st.metric(label="가장 인기 있는 나라", value=f"{top_country_name}")
    with m3:
        st.metric(label="최고 비율", value=f"{top_country_val:.2%}", delta=f"+{(top_country_val-global_avg):.2%} (평균 대비)")

    st.markdown("### 🗺️ Global Distribution Map")
    
    # 4. 지도 시각화 (Plotly Choropleth) - 삐까번쩍 포인트
    fig_map = px.choropleth(
        df,
        locations="Country",
        locationmode='country names',
        color=target_col,
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma, # 화려한 컬러 스케일
        title=f"전 세계 {selected_mbti} 분포도",
        projection="natural earth"
    )
    fig_map.update_layout(
        paper_bgcolor="#0e1117", # 스트림릿 다크모드 배경색 일치
        geo=dict(bgcolor="#0e1117"),
        font=dict(color="white"),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # 5. 상위 국가 바 차트 & 맞춤형 멘트
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### 🏆 Top 5 Countries")
        fig_bar = px.bar(
            top_countries, 
            x='Country', 
            y=target_col,
            color=target_col,
            color_continuous_scale='Viridis',
            text_auto='.2%'
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            xaxis_title="",
            yaxis_title="비율",
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown(f"### 💌 To. {selected_mbti}")
        st.info(f"""
        **{info['name']}님!**
        
        데이터에 따르면 당신과 같은 성향의 사람들은 **{top_country_name}**에 가장 많이 살고 있어요!
        전 세계 평균보다 무려 **{(top_country_val-global_avg)*100:.1f}% 포인트**나 더 높은 수치죠.
        
        혹시 여행을 계획 중이라면, 당신의 소울(Soul)이 가득한
        **{top_country_name}** (으)로 떠나보는 건 어떨까요? ✈️
        
        그곳에 가면 마음이 맞는 친구들을 더 쉽게 만날 수 있을지도 몰라요!
        """)
        st.progress(float(top_country_val), text=f"{top_country_name}에서의 {selected_mbti} 포화도")

    # Footer
    st.markdown("---")
    st.caption("Data Source: World MBTI Stats | Visualization by Streamlit")
