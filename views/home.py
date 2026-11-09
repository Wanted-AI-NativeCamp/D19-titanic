"""홈 — Figma 시안 '홈 — Titanic Analytics'.

선박 사진 Hero(제목 · 설명 · 버튼 3개) → 이동 카드 3개(프로젝트 소개 / 분석 방법 소개 / 총분석) → Footer.
이미지는 assets/ 에 있고, 이 페이지에만 쓰는 스타일은 아래 CSS 에 둔다.
"""
import streamlit as st

from common import asset_uri, site_footer

ARROW_C = asset_uri("arrow_circle.svg")

st.html(f"""
<style>
  /* Hero: 사진 + 왼쪽에서 오른쪽으로 옅어지는 어두운 막 */
  .st-key-hm-hero {{ position: relative; min-height: 670px; padding: 65px 80px 44px; gap: 22px; overflow: hidden;
    background-color: var(--nav);
    background-image: linear-gradient(90deg, rgba(4,21,31,.95) 0%, rgba(4,21,31,.65) 44%, rgba(4,21,31,0) 100%), url({asset_uri("hero_figma.jpg")});
    background-size: 100% 100%, cover; background-position: 0 0, 100% 0; background-repeat: no-repeat; }}
  .hm-eyebrow {{ font-size: 12px; font-weight: 700; letter-spacing: 3px; color: var(--gold); margin: 0 0 10px; }}
  .hm-logo {{ width: 323px; height: 85px; overflow: hidden; position: relative; }}
  .hm-logo img {{ position: absolute; height: 132.07%; left: -1.55%; top: -16.62%; width: 104.02%; max-width: none; }}
  .hm-ko {{ font-size: 27px; font-weight: 700; color: var(--white); margin: 22px 0 0; }}
  .hm-desc {{ font-size: 17px; line-height: 1.9; color: var(--t1); margin: 22px 0 0; }}

  /* 이동 카드 */
  .st-key-hm-index {{ background: var(--index); padding: 35px 80px 64px; gap: 20px; }}
  [class*="st-key-hm-card-"] {{ position: relative; height: 190px; background: var(--card); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }}
  [class*="st-key-hm-card-"]::before {{ content: ""; position: absolute; top: 0; right: 0; width: 510px; height: 100%;
      background: var(--img) center/cover no-repeat; }}
  [class*="st-key-hm-card-"]::after {{ content: ""; position: absolute; top: 0; right: 0; width: 510px; height: 100%;
      background: linear-gradient(90deg, var(--card) 0%, rgba(0,17,27,0) 38%); pointer-events: none; }}
  .st-key-hm-card-1 {{ --img: url({asset_uri("card_project.jpg")}); }}
  .st-key-hm-card-2 {{ --img: url({asset_uri("card_process.jpg")}); }}
  .st-key-hm-card-3 {{ --img: url({asset_uri("card_analysis.jpg")}); }}
  .hm-card {{ display: flex; gap: 30px; align-items: flex-start; padding: 28px 32px; position: relative; z-index: 1; }}
  .hm-card .n {{ font-family: "Playfair Display", serif; font-size: 37px; line-height: 16px; color: var(--t1); padding-top: 4px; }}
  .hm-card .en {{ font-family: "Playfair Display", serif; font-size: 12px; letter-spacing: 2px; color: var(--t1); margin-bottom: 8px; }}
  .hm-card .ko {{ font-size: 25px; font-weight: 700; color: var(--white); margin-bottom: 8px; }}
  .hm-card .ds {{ font-size: 14px; line-height: 1.8; color: var(--t2); width: 650px; max-width: 100%; }}
  .hm-card .go {{ position: absolute; right: 35px; top: 76px; width: 36px; height: 36px; border-radius: 100px; border: 1px solid var(--t1);
      background: #0b243c url({ARROW_C}) center/19px no-repeat; }}
  /* 카드 전체를 누를 수 있게 링크 상자를 카드 위에 덮는다 (눈에는 보이지 않는다) */
  [class*="st-key-hm-card-"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"]) {{ position: absolute; inset: 0; z-index: 2; width: 100%; height: 100%; }}
  [class*="st-key-hm-card-"] [data-testid="stPageLink"], [class*="st-key-hm-card-"] [data-testid="stPageLink"] > div {{ width: 100%; height: 100%; }}
  [class*="st-key-hm-card-"] [data-testid="stPageLink-NavLink"] {{ width: 100%; height: 100%; padding: 0; opacity: 0; cursor: pointer; }}
  [class*="st-key-hm-card-"]:hover {{ border-color: rgba(255,255,255,.45); }}
  @media (max-width: 900px) {{
    .st-key-hm-hero {{ padding: 40px 20px; min-height: 520px; align-items: center; justify-content: center; text-align: center;
      background-image: linear-gradient(180deg, rgba(4,21,31,.85) 0%, rgba(4,21,31,.6) 100%), url({asset_uri("hero_ship_night.jpg")});
      background-position: 0 0, 72% 50%; }} .st-key-hm-index {{ padding: 24px 20px 40px; }}
    .st-key-hm-hero [data-testid="stElementContainer"], .st-key-hm-hero [data-testid="stMarkdownContainer"] {{ width: 100%; text-align: center; }}
    .hm-logo {{ margin: 0 auto; max-width: 100%; }}
    .hm-card .ds {{ width: auto; }} [class*="st-key-hm-card-"]::before, [class*="st-key-hm-card-"]::after {{ opacity: .35; }}
  }}
</style>
""")

with st.container(key="hm-hero"):
    st.html(f"""
<p class="hm-eyebrow">TITANIC · SURVIVAL ANALYSIS</p>
<div class="hm-logo"><img src="{asset_uri("logo_titanic.png")}" alt="TITANIC"></div>
<div class="hm-ko">타이타닉 생존 요인 분석 대시보드</div>
<p class="hm-desc">타이타닉호 승객 891명의 기록으로, <br class='nb'>데이터로 어떤 차이가 있었는지 분석했습니다.</p>
""")

CARDS = [
    ("1", "views/overview.py", "01", "PROJECT", "프로젝트 소개",
     "891명의 승객 기록에서 시작하는 질문. <br class='nb'>분석의 배경과 데이터, 그리고 우리가 살펴볼 생존 요인을 소개합니다."),
    ("2", "views/method.py", "02", "PROCESS", "분석 방법 소개",
     "데이터 탐색부터 결측 처리, 그룹 비교와 시각화까지. <br class='nb'>여덟 단계의 분석 과정을 기록으로 확인하세요."),
    ("3", "views/analysis.py", "03", "ANALYSIS", "총분석",
     "성별·객실 등급·탑승 항구별 생존율을 비교합니다. <br class='nb'>개별 요인과 복합 집단을 함께 읽는 최종 대시보드입니다."),
]
with st.container(key="hm-index"):
    for k, page, n, en, ko, ds in CARDS:
        with st.container(key=f"hm-card-{k}"):
            st.html(f'<div class="hm-card"><div class="n">{n}</div><div><div class="en">{en}</div>'
                    f'<div class="ko">{ko}</div><div class="ds">{ds}</div></div><div class="go"></div></div>')
            st.page_link(page, label=ko)

site_footer()
