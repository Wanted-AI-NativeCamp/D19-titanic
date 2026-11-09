"""타이타닉 대시보드 — 진입점.

실행:  streamlit run app.py
페이지: 홈 → 프로젝트 소개 → 분석 방법 소개 → 종합 분석 (views/ 폴더)
상단 메뉴는 시안(image/)처럼 로고 + 메뉴 3개를 직접 그린다. 홈은 로고를 눌러 돌아간다.
"""
import streamlit as st

from common import inject_css

st.set_page_config(page_title="Titanic Analytics — Survival Analysis", layout="wide")
inject_css()

home = st.Page("views/home.py", title="홈", default=True)
overview = st.Page("views/overview.py", title="프로젝트 소개")
method = st.Page("views/method.py", title="분석 방법 소개")
analysis = st.Page("views/analysis.py", title="총분석")

pg = st.navigation([home, overview, method, analysis], position="hidden")


def site_header() -> None:
    with st.container(key="site-header"):
        brand, nav = st.columns([1, 1], vertical_alignment="center")
        with brand:
            with st.container(key="site-brand", horizontal=True, vertical_alignment="center", gap="small"):
                with st.container(key="site-logo", width="content"):
                    st.page_link(home, label="Titanic Analytics")
                st.html('<div class="oa-tagline">1912 Survival Data Analysis</div>')
        with nav:
            with st.container(key="site-nav", horizontal=True):
                st.page_link(overview)
                st.page_link(method)
                st.page_link(analysis)


site_header()
pg.run()
