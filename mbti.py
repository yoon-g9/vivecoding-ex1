import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="MBTI 국가별 통계 (Semantic UI)",
    page_icon="🌏",
    layout="wide"
)

# 2. Semantic UI CDN 주입 (HTML/CSS 로드)
def load_semantic_ui():
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
        <style>
            /* Streamlit 기본 패딩 조정 */
            .main .block-container { padding-top: 2rem; }
            /* 폰트 등 기본 스타일 조정 */
            body { font-family: 'Lato', 'Helvetica Neue', Arial, Helvetica, sans-serif; }
        </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('countriesMBTI_16types.csv')
        return df
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다.")
        return None

mbti_info = {
    "ISTJ": "현실주의자 - 사실에 근거하여 사고하며 행동합니다.",
    "ISFJ": "수호자 - 소중한 이들을 지키고 헌신하는 방어자입니다.",
    "INFJ": "옹호자 - 조용하고 신비로우며 샘솟는 영감으로 타인을 돕습니다.",
    "INTJ": "전략가 - 상상력이 풍부하며 철두철미한 계획을 세웁니다.",
    "ISTP": "장인 - 대담하고 현실적인 성향으로 도구 사용에 능숙합니다.",
    "ISFP": "모험가 - 항시 새로운 경험을 추구하는 유연하고 매력적인 예술가입니다.",
    "INFP": "중재자 - 상냥하고 이타적이며 낭만적인 이상주의자입니다.",
    "INTP": "논리술사 - 끊임없이 새로운 지식에 목말라하는 혁신가입니다.",
    "ESTP": "사업가 - 영리하고 에너지 넘치며 관찰력이 뛰어납니다.",
    "ESFP": "연예인 - 주위에 있으면 인생이 지루할 틈이 없습니다.",
    "ENFP": "활동가 - 창의적이고 항상 웃을 거리를 찾아내는 활발한 사람입니다.",
    "ENTP": "변론가 - 지적인 도전을 두려워하지 않는 똑똑한 호기심 대장입니다.",
    "ESTJ": "경영자 - 사물과 사람을 관리하는 데 뛰어난 능력을 보입니다.",
    "ESFJ": "집정관 - 타인을 돕는 데 열성적인 세심하고 사교적인 사람입니다.",
    "ENFJ": "선도자 - 청중을 사로잡고 의욕을 불어넣는 카리스마 넘치는 리더입니다.",
    "ENTJ": "통솔자 - 대담하고 상상력이 풍부하며 강한 의지의 지도자입니다."
}

def main():
    load_semantic_ui()  # CSS 적용
    df = load_data()

    # --- 헤더 영역 (Semantic UI Header) ---
    st.markdown("""
        <div class="ui center aligned icon header">
            <i class="globe icon"></i>
            <div class="content">
                글로벌 MBTI 매칭 분석기
                <div class="sub header">Semantic UI로 꾸며진 Streamlit 앱입니다.</div>
            </div>
        </div>
        <div class="ui divider"></div>
    """, unsafe_allow_html=True)

    if df is not None:
        # --- 입력 영역 (Streamlit Native Widget 사용) ---
        # 입력 컴포넌트는 Streamlit 고유 기능을 쓰는 것이 기능상 안전합니다.
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mbti_options = ["선택해주세요"] + list(mbti_info.keys())
            selected_mbti = st.selectbox("🔻 아래에서 당신의 MBTI를 선택하세요", mbti_options)

        # 선택 전 대기 화면
        if selected_mbti == "선택해주세요":
            st.markdown("""
                <div class="ui info message">
                    <div class="header">안내</div>
                    <p>MBTI를 선택하시면 전 세계 데이터를 분석해드립니다.</p>
                </div>
            """, unsafe_allow_html=True)
            st.stop()

        else:
            # --- 결과 화면: Semantic UI Card ---
            st.markdown(f"""
                <div class="ui centered card fluid">
                    <div class="content">
                        <div class="header" style="font-size: 1.5em;">{selected_mbti}</div>
                        <div class="meta">Type Description</div>
                        <div class="description">
                            <p style="font-size: 1.2em;">{mbti_info[selected_mbti]}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 데이터 분석
            top_countries = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(5)
            top_countries['Percentage'] = top_countries[selected_mbti].apply(lambda x: x * 100)
            
            best_country = top_countries.iloc[0]
            
            # --- 결과 화면: 통계 및 차트 레이아웃 ---
            st.markdown("<h3 class='ui horizontal divider header'><i class='chart bar icon'></i> 분석 결과 </h3>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 1])

            with c1:
                # Semantic UI Statistics 컴포넌트 활용
                st.markdown(f"""
                    <div class="ui segment">
                        <h4 class="ui header">🏆 1위 국가 정보</h4>
                        <div class="ui center aligned huge statistic">
                            <div class="value">
                                {best_country['Country']}
                            </div>
                            <div class="label">
                                전체 인구의 {best_country['Percentage']:.2f}%
                            </div>
                        </div>
                    </div>
                    
                    <div class="ui positive icon message">
                        <i class="plane departure icon"></i>
                        <div class="content">
                            <div class="header">
                                여행 추천
                            </div>
                            <p><b>{selected_mbti}</b> 성향이 가장 많은 나라는 <b>{best_country['Country']}</b>입니다.<br>
                            비슷한 친구들을 만나러 떠나보세요!</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with c2:
                # 차트는 Streamlit 기능을 쓰되, Semantic UI Segment로 감싸서 디자인 통일
                st.markdown('<div class="ui segment"><h4 class="ui header">📊 Top 5 국가 비교</h4>', unsafe_allow_html=True)
                st.bar_chart(top_countries.set_index('Country')['Percentage'])
                st.markdown('</div>', unsafe_allow_html=True)

            # 전체 데이터 테이블 (Accordion 스타일)
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📑 전체 통계 데이터 확인하기"):
                st.dataframe(df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
