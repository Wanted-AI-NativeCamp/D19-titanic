"""공유 부품: Ocean Archive 디자인 CSS, 데이터 계산.

- 숫자는 모두 data/*.csv 에서 계산한다 (손으로 쓰지 않는다).
- 디자인 기준: md/design.md (Ocean Archive). 색은 아래 CSS 변수(--navy-900 …)로만 쓴다.
"""
import ast
import base64
import html
import math
import re
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ASSETS = ROOT / "assets"


# ---------------------------------------------------------------- 표기 도우미
def r1(v: float) -> float:
    return math.floor(v * 10 + 0.5) / 10          # 소수 첫째 자리, 반올림(0.5는 올림)


def pct(v: float) -> str:
    return f"{v:.1f}%"


def num(v) -> str:
    return f"{int(v):,}"


def pp(v: float) -> str:
    """두 비율의 차이는 %p 로 표기한다 (예: 55.3%p)."""
    return f"{v:.1f}%p"


# ---------------------------------------------------------------- HTML 조각 (흰 카드 안에서 쓰는 표 · KPI · 목록)
esc = html.escape


def html_table(df, right: tuple = ()) -> str:
    head = "".join(f'<th class="{"r" if c in right else ""}">{esc(str(c))}</th>' for c in df.columns)
    body = "".join(
        "<tr>" + "".join(f'<td class="{"r" if c in right else ""}">{esc(str(v))}</td>' for c, v in zip(df.columns, row)) + "</tr>"
        for row in df.itertuples(index=False)
    )
    return f'<table class="oa-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def html_kpis(items: list) -> str:
    return '<div class="oa-kpi-w">' + "".join(
        f'<div><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div></div>' for k, v in items) + "</div>"


def html_ul(items: list) -> str:
    return '<ul class="oa-ul">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def html_caption(text: str) -> str:
    return f'<div class="oa-cap">{esc(text)}</div>'


# ---------------------------------------------------------------- 실습 코드(t1_look.py)에서 읽어 오는 설명
def column_meaning() -> dict:
    """칸 이름 → 뜻. 실습 코드 t1_look.py 의 descriptions 를 그대로 읽어 온다."""
    tree = ast.parse((ROOT / "t1_look.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "descriptions" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def port_names() -> dict:
    """항구 코드 → 이름 (예: C → 셰르부르). Embarked 설명(C = …, Q = …, S = …)에서 읽는다."""
    text = column_meaning().get("Embarked", "")
    found = dict(re.findall(r"([CQS]) = ([^,)]+)", text))
    return {k: found.get(k, "").strip() for k in "CQS"}


# ---------------------------------------------------------------- 데이터
SEX_KO = {"male": "남성", "female": "여성"}
CLASSES = ["1등석", "2등석", "3등석"]


@st.cache_data
def load_clean() -> pd.DataFrame:
    return pd.read_csv(DATA / "titanic_clean.csv")


@st.cache_data
def load_raw() -> pd.DataFrame:
    return pd.read_csv(DATA / "titanic.csv")


@st.cache_data
def group_rows() -> list[dict]:
    """성별 × 객실 등급 6행: 여성 1·2·3등석, 남성 1·2·3등석 순서. n = 승객 수(분모), s = 생존자 수."""
    df = load_clean()
    d = df.assign(sex=df["Sex"].map(SEX_KO), cls=df["Pclass"].astype(str) + "등석")
    g = d.groupby(["sex", "cls"])["Survived"].agg(n="size", s="sum")
    rows = []
    for sx in ["여성", "남성"]:
        for c in CLASSES:
            n, s = int(g.loc[(sx, c), "n"]), int(g.loc[(sx, c), "s"])
            rows.append(dict(sex=sx, cls=c, n=n, s=s, rate=r1(s / n * 100)))
    return rows


@st.cache_data
def summary() -> dict:
    rows = group_rows()

    def pool(**kw):
        sel = [r for r in rows if all(r[k] == v for k, v in kw.items())]
        n, s = sum(r["n"] for r in sel), sum(r["s"] for r in sel)
        return dict(n=n, s=s, rate=r1(s / n * 100))

    allp = pool()
    out = dict(
        total=allp["n"], alive=allp["s"], dead=allp["n"] - allp["s"], rate=allp["rate"],
        sex={sx: pool(sex=sx) for sx in ["여성", "남성"]},
        cls={c: pool(cls=c) for c in CLASSES},
    )
    out["sex_gap"] = r1(out["sex"]["여성"]["rate"] - out["sex"]["남성"]["rate"])
    out["cls_gap"] = r1(out["cls"]["1등석"]["rate"] - out["cls"]["3등석"]["rate"])
    return out


# 분석 방법 페이지의 단계 태그 (t1~t7 스크립트 순서).
STEP_TITLES = [
    "01 데이터 살펴보기", "02 결측치 찾기", "03 왜 비었을까", "04 결측 처리",
    "05 처리 방법 실험", "06 그룹별 생존율", "07 시각화", "08 대시보드",
]


# 프로젝트 목표 3개 (랜딩 F2, 프로젝트 소개 상세에서 같이 쓴다)
GOALS = [
    ("데이터를 살펴보고 정리하다.", "비어 있는 값을 찾고, 왜 비었는지 확인한 뒤 처리했습니다."),
    ("처리 방법에 따라 결과가 달라지는지 실험하다.", "빈 나이를 4가지 방법으로 처리해 생존율을 비교했습니다."),
    ("그룹별로 생존율을 비교하다.", "성별, 객실 등급, 탑승 항구별 생존율을 인원수와 함께 봤습니다."),
]


# ---------------------------------------------------------------- Hero 이미지
# assets/titanic.(jpg|jpeg|png|webp) 가 있으면 그 사진(흑백 처리), 없으면 선박 실루엣 자리표시.
_SHIP_SVG = """
<svg viewBox="0 0 640 400" role="img" aria-label="타이타닉 선박 실루엣 (자리표시 이미지)" xmlns="http://www.w3.org/2000/svg">
  <rect width="640" height="400" fill="#102A40"/>
  <g stroke="#B5B5B5" stroke-width="1.5" fill="#071B2D">
    <line x1="150" y1="130" x2="150" y2="256" stroke-width="2"/>
    <line x1="548" y1="150" x2="548" y2="256" stroke-width="2"/>
    <g fill="#E5E5E5" stroke="none">
      <rect x="205" y="130" width="34" height="74"/><rect x="255" y="130" width="34" height="74"/>
      <rect x="305" y="130" width="34" height="74"/><rect x="355" y="130" width="34" height="74"/>
    </g>
    <g fill="#071B2D" stroke="none">
      <rect x="205" y="142" width="34" height="10"/><rect x="255" y="142" width="34" height="10"/>
      <rect x="305" y="142" width="34" height="10"/><rect x="355" y="142" width="34" height="10"/>
    </g>
    <rect x="236" y="186" width="180" height="18"/>
    <rect x="190" y="204" width="270" height="22"/>
    <rect x="150" y="226" width="360" height="30"/>
    <path d="M70 256 H580 L616 234 L592 306 H100 Z"/>
  </g>
  <line x1="105" y1="278" x2="565" y2="278" stroke="#B5B5B5" stroke-width="3" stroke-dasharray="3 15" opacity=".6"/>
  <g stroke="#FFFFFF" stroke-opacity=".18" stroke-width="1">
    <line x1="90" y1="322" x2="580" y2="322"/><line x1="130" y1="336" x2="540" y2="336"/><line x1="180" y1="350" x2="490" y2="350"/>
  </g>
</svg>
"""


# ---------------------------------------------------------------- 홈 블루프린트 이미지 (선박 측면도 + 갑판 평면도)
def _blueprint_svg() -> str:
    L = "#CFE0F1"
    out = [f'<svg viewBox="0 0 900 430" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="{L}" stroke-width="1.2" stroke-linecap="round">']
    # 측면도: 선체
    out.append('<path d="M20 205 H730 L752 188 L772 232 Q700 248 650 252 H70 Q40 240 20 205 Z" stroke-width="1.6"/>')
    out.append('<path d="M20 205 Q40 240 70 252" opacity=".6"/><line x1="40" y1="222" x2="745" y2="222" opacity=".5"/>')
    out.append('<line x1="30" y1="262" x2="760" y2="262" opacity=".35" stroke-dasharray="2 8"/>')
    # 현창 두 줄
    out.append(f'<line x1="70" y1="212" x2="715" y2="212" stroke-width="3" stroke-dasharray="2 6" opacity=".65"/>')
    out.append(f'<line x1="80" y1="232" x2="690" y2="232" stroke-width="3" stroke-dasharray="2 8" opacity=".5"/>')
    # 상부 구조
    out.append('<rect x="150" y="170" width="480" height="35"/><rect x="200" y="148" width="380" height="22"/><rect x="250" y="130" width="280" height="18"/>')
    out.append('<line x1="150" y1="180" x2="630" y2="180" opacity=".5"/><line x1="200" y1="158" x2="580" y2="158" opacity=".5"/>')
    # 굴뚝 4개
    for x in (250, 340, 430, 520):
        out.append(f'<path d="M{x} 130 L{x+4} 58 H{x+46} L{x+50} 130 Z" stroke-width="1.5"/><line x1="{x+4}" y1="78" x2="{x+46}" y2="78" opacity=".7"/><line x1="{x+3}" y1="104" x2="{x+47}" y2="104" opacity=".5"/>')
    # 돛대와 삭구
    out.append('<line x1="130" y1="205" x2="130" y2="30" stroke-width="1.6"/><line x1="660" y1="205" x2="660" y2="10" stroke-width="1.6"/>')
    out.append('<line x1="130" y1="40" x2="22" y2="198" opacity=".7"/><line x1="130" y1="40" x2="250" y2="132" opacity=".5"/>')
    out.append('<line x1="660" y1="22" x2="575" y2="132" opacity=".5"/><line x1="660" y1="22" x2="760" y2="200" opacity=".7"/><line x1="130" y1="34" x2="660" y2="16" opacity=".6"/>')
    # 평면도
    out.append('<path d="M40 350 Q60 312 130 306 H700 Q780 318 800 350 Q780 382 700 394 H130 Q60 388 40 350 Z" stroke-width="1.6"/>')
    out.append('<path d="M70 350 Q85 326 140 320 H690 Q752 328 772 350 Q752 372 690 380 H140 Q85 374 70 350 Z" opacity=".5"/>')
    for x in range(150, 700, 62):
        out.append(f'<rect x="{x}" y="326" width="52" height="48" opacity=".55"/><line x1="{x}" y1="350" x2="{x+52}" y2="350" opacity=".35"/>')
    for x in (250, 340, 430, 520):
        out.append(f'<ellipse cx="{x+25}" cy="350" rx="20" ry="14"/>')
    out.append('<line x1="40" y1="350" x2="800" y2="350" opacity=".25" stroke-dasharray="6 6"/>')
    out.append('</svg>')
    return "".join(out)


def blueprint_art() -> str:
    b64 = base64.b64encode(_blueprint_svg().encode()).decode()
    return (f'<img class="hm-blueprint" src="data:image/svg+xml;base64,{b64}" '
            'alt="타이타닉호 측면도와 갑판 평면도를 그린 청사진 스타일 도면">')


def hero_art() -> str:
    """Hero 오른쪽 이미지 HTML. 사진 파일이 있으면 사진, 없으면 자리표시 실루엣."""
    for name, mime in (("titanic.jpg", "image/jpeg"), ("titanic.jpeg", "image/jpeg"),
                       ("titanic.png", "image/png"), ("titanic.webp", "image/webp")):
        p = ASSETS / name
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            return f'<div class="oa-art"><img class="oa-photo" src="data:{mime};base64,{b64}" alt="타이타닉 선박 사진"></div>'
    # <svg> 태그는 st.html 이 걸러내므로 data URI 이미지로 넣는다
    b64 = base64.b64encode(_SHIP_SVG.strip().encode()).decode()
    return f'<div class="oa-art"><img src="data:image/svg+xml;base64,{b64}" alt="타이타닉 선박 실루엣 (자리표시 이미지)"></div>'


def nav_active(path: str) -> None:
    """상단 메뉴에서 지금 보고 있는 페이지(링크 주소 path)를 굵게, 크림색으로 표시한다."""
    st.html(f'<style>.st-key-site-nav a[href="{path}"], .st-key-site-nav a[href="{path}"] * '
            '{ color: var(--cream) !important; font-weight: 700 !important; }</style>')


def asset_uri(name: str) -> str:
    """assets/ 의 이미지를 data URI 로 바꾼다 (CSS url() 과 <img> 에 쓴다)."""
    p = ASSETS / name
    mime = {".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml"}[p.suffix]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def tabs_band(options: list, key: str, label: str) -> int:
    """분석 항목 · 단계 태그 줄. 넓은 화면에서는 태그가 한 줄에 모두 보이고,
    좁은 화면에서는 선택한 태그만 보이며 양 끝 < > 버튼으로 이전 · 다음 태그로 넘어간다. 선택한 번호(0부터)를 돌려준다."""
    st.session_state.setdefault(key, options[0])

    def move(delta: int) -> None:
        st.session_state[key] = options[options.index(st.session_state[key]) + delta]

    cur = options.index(st.session_state[key])
    with st.container(key="tabs-band"):
        with st.container(key="tabs-row", horizontal=True, vertical_alignment="center"):
            st.button("‹", key=f"tabs-{key}_tprev", on_click=move, args=(-1,), disabled=cur == 0, help="이전")
            st.pills(label, options, key=key, required=True, label_visibility="collapsed")
            st.button("›", key=f"tabs-{key}_tnext", on_click=move, args=(1,), disabled=cur == len(options) - 1, help="다음")
    return options.index(st.session_state[key])


def request_scroll_top() -> None:
    """이전 · 다음 버튼의 on_click 에서 부른다: 다음 화면을 그릴 때 페이지 맨 위로 올린다."""
    st.session_state["_to_top"] = True


def scroll_top_if_requested() -> None:
    """페이지 맨 아래에서 부른다. request_scroll_top() 이 불렸을 때만 화면을 맨 위로 올린다."""
    if st.session_state.pop("_to_top", False):
        n = st.session_state["_top_n"] = st.session_state.get("_top_n", 0) + 1     # 같은 내용이면 다시 실행되지 않으므로 번호를 붙인다
        st.html(f"<script>/* {n} */ setTimeout(function () {{ var m = document.querySelector('[data-testid=\"stMain\"]'); "
                "if (m) m.scrollTo(0, 0); window.scrollTo(0, 0); }, 60);</script>", unsafe_allow_javascript=True)


def masthead(label: str, title: str, desc: str, variant: str = "a") -> None:
    """페이지 상단 선박 배너 (Figma: Ship masthead). variant a = 총분석, b = 분석 방법 소개."""
    st.html(f'<div class="oa-mh oa-mh-{variant}"><p class="l">{label}</p><div class="t">{title}</div>'
            f'<p class="d">{desc}</p><span class="cap">RMS TITANIC · 1912</span></div>')


def site_footer() -> None:
    """모든 페이지 맨 아래 Footer (Figma: Archive footer)."""
    S = summary()
    st.html(f"""
<div class="oa-ft">
  <div class="oa-ft-cols">
    <div><b>DATA SOURCE</b><span>Kaggle Titanic · 승객 {num(S['total'])}명</span></div>
    <div><b>TECHNOLOGY</b><span>Python · pandas · Altair · Streamlit</span></div>
    <div><b>PROJECT</b><span>Titanic Analytics — Ocean Archive</span></div>
  </div>
  <div class="oa-ft-rule"></div>
  <div class="oa-ft-sig"><i>A record of lives. A study in survival.</i><span>TITANIC ANALYTICS / DIGITAL ARCHIVE</span></div>
</div>
""")


def page_hero(label: str, title: str, desc: str) -> None:
    """상세 페이지 공통 Hero (design.md 3): 왼쪽에 영문 레이블 · 제목 · 설명, 오른쪽에 같은 선박 이미지."""
    left, right = st.columns([1.1, 1], gap="large", vertical_alignment="center")
    with left:
        st.html(f'<div class="oa-label">{label}</div><h1 class="oa-page-title">{title}</h1><p class="oa-desc">{desc}</p>')
    with right:
        st.html(hero_art())


# ---------------------------------------------------------------- 공통 CSS
def inject_css() -> None:
    """모든 페이지 공통: 색 변수, 폭, 로고, Hero, 버튼 + 아직 새 디자인으로 바꾸지 않은 페이지용 호환 스타일."""
    st.html(CSS)
    st.html(f'''<style>
  @import url("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400&display=swap");
  .oa-mh {{ --mh-img: url({asset_uri("masthead_analysis.jpg")}); }}
  .st-key-site-logo [data-testid="stPageLink-NavLink"] {{ background-image: url({asset_uri("logo_titanic.png")}); }}
</style>''')


CSS = """
<style>
  @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap");   /* 영문·숫자용 (config 에는 폰트 1개씩만 넣을 수 있다) */
  /* Ocean Archive 토큰 (md/design.md 2.3) */
  [data-testid="stApp"] {
    --navy-900: #071B2D; --navy-800: #102A40;
    --white: #FFFFFF; --off-white: #F7F7F7; --gray-200: #E5E5E5; --gray-400: #B5B5B5;
    --gray-600: #777777; --charcoal: #242424; --black: #111111; --text-secondary: #595959;
  }

  /* ---------------- Figma 시안 토큰 ---------------- */
  [data-testid="stApp"] {
    --bg: #061c29; --nav: #04151f; --index: #031520; --card: #00111b; --line: rgba(255, 255, 255, .19);
    --t1: #c9d5dc; --t2: #b6c6d0; --gold: #c3b099; --cream: #ece8e0; --accent: #ff8a5c;
  }
  [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: var(--bg); color: var(--white); }

  /* 가로 전체 폭 레이아웃: 구역마다 안쪽 여백 80px 을 직접 둔다 */
  [data-testid="stMainBlockContainer"] { max-width: none; padding: 0; }
  [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] { gap: 0; }
  [data-testid="stHeader"] { display: none; }

  /* 상단 메뉴 (88px): 로고 · 구분선 · 영문 설명 / 오른쪽 메뉴 3개 */
  .st-key-site-header { background: var(--nav); border-bottom: 1px solid var(--line); height: 88px !important; min-height: 88px; padding: 0 80px; align-items: center; justify-content: center; flex-shrink: 0; }
  .st-key-site-header [data-testid="stHorizontalBlock"] { align-items: center; gap: 0; }
  .st-key-site-logo, .st-key-site-logo [data-testid="stPageLink"] { width: 96px; }
  .st-key-site-header .st-key-site-logo [data-testid="stPageLink-NavLink"] { width: 96px; height: 32px; padding: 0; background-size: contain; background-repeat: no-repeat; background-position: center; }
  .st-key-site-logo [data-testid="stPageLink-NavLink"] * { display: none; }
  .oa-tagline { font-family: "Cormorant Garamond", "Playfair Display", serif; font-size: 15px; letter-spacing: 5px; color: var(--cream);
                border-left: 1px solid var(--line); padding-left: 14px; line-height: 20px; white-space: nowrap; }
  .st-key-site-nav { justify-content: flex-end; gap: 36px !important; }
  .st-key-site-header [data-testid="stPageLink-NavLink"] { background: transparent; border-radius: 0; padding: 0; width: fit-content; }
  .st-key-site-nav [data-testid="stPageLink-NavLink"], .st-key-site-nav [data-testid="stPageLink-NavLink"] * { color: var(--t2); font-size: 15px; font-weight: 400; }
  .st-key-site-nav [data-testid="stPageLink-NavLink"]:hover, .st-key-site-nav [data-testid="stPageLink-NavLink"]:hover * { color: var(--white); background: transparent; }
  /* 상단 메뉴(gnb)와 태그 줄(lnb) 고정: 스크롤해도 화면 위에 남는다. lnb 는 gnb 바로 아래에 붙는다 */
  [data-testid="stApp"] { --gnb-h: 88px; }
  [data-testid="stLayoutWrapper"]:has(> .st-key-site-header) { position: sticky; top: 0; z-index: 1000; }
  [data-testid="stLayoutWrapper"]:has(> .st-key-tabs-band) { position: sticky; top: var(--gnb-h); z-index: 900; }
  @media (max-width: 900px) { [data-testid="stApp"] { --gnb-h: 72px; } }

  /* 이전 · 다음 버튼 줄: 좁은 화면에서도 두 줄로 쌓이지 않고 한 줄에 나란히 */
  @media (max-width: 900px) {
    .st-key-md-nav [data-testid="stHorizontalBlock"], .st-key-an-nav [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 8px !important; }
    .st-key-md-nav [data-testid="stColumn"], .st-key-an-nav [data-testid="stColumn"] { min-width: 0 !important; width: auto !important; flex: 1 1 0 !important; }
    .st-key-md-nav [data-testid^="stBaseButton"], .st-key-an-nav [data-testid^="stBaseButton"] { padding: 8px 12px !important; max-width: 100%; }
    .st-key-md-nav [data-testid^="stBaseButton"] *, .st-key-an-nav [data-testid^="stBaseButton"] * { font-size: 13px !important; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  }

  /* 좁은 화면: 설명 문구의 강제 줄바꿈(br.nb)을 없애고 자연스럽게 이어 쓴다 */
  @media (max-width: 900px) { br.nb { display: none; } }

  /* 좁은 화면: 로고와 메뉴가 두 줄로 나뉘지 않고 한 줄에 머물도록 로고를 줄인다 */
  .st-key-site-brand { flex-wrap: nowrap !important; }
  @media (max-width: 1100px) { .oa-tagline { display: none; } }
  @media (max-width: 900px) {
    .st-key-site-header { padding: 0 20px; height: 72px !important; min-height: 72px; }
    .st-key-site-header [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; }
    .st-key-site-header [data-testid="stColumn"] { min-width: 0 !important; width: auto !important; flex: 0 0 auto !important; }
    .st-key-site-header [data-testid="stColumn"]:last-child { flex: 1 1 auto !important; }
    .st-key-site-logo, .st-key-site-logo [data-testid="stPageLink"] { width: 76px; }
    .st-key-site-header .st-key-site-logo [data-testid="stPageLink-NavLink"] { width: 76px; height: 25px; }
    .st-key-site-nav { gap: 18px !important; flex-wrap: nowrap; }
    .st-key-site-nav [data-testid="stPageLink-NavLink"], .st-key-site-nav [data-testid="stPageLink-NavLink"] * { font-size: 14px; white-space: nowrap; }
  }
  @media (max-width: 520px) {
    .st-key-site-header { padding: 0 14px; }
    .st-key-site-logo, .st-key-site-logo [data-testid="stPageLink"] { width: 60px; }
    .st-key-site-header .st-key-site-logo [data-testid="stPageLink-NavLink"] { width: 60px; height: 20px; }
    .st-key-site-nav { gap: 12px !important; }
    .st-key-site-nav [data-testid="stPageLink-NavLink"], .st-key-site-nav [data-testid="stPageLink-NavLink"] * { font-size: 12px; }
  }

  /* 공통 Footer */
  .oa-ft { background: var(--nav); padding: 38px 80px 28px; }
  .oa-ft-cols { display: flex; gap: 56px; }
  .oa-ft-cols > div { flex: 1; }
  .oa-ft-cols b { display: block; font-family: "Playfair Display", serif; font-weight: 400; font-size: 12px; letter-spacing: 1.8px; color: var(--t2); margin-bottom: 10px; }
  .oa-ft-cols span { font-size: 14px; color: var(--t1); }
  .oa-ft-rule { height: 1px; background: var(--line); margin: 28px 0; }
  .oa-ft-sig { display: flex; justify-content: space-between; align-items: baseline; }
  .oa-ft-sig i { font-family: "Playfair Display", serif; font-style: normal; font-size: 15px; color: var(--t1); }
  .oa-ft-sig span { font-size: 11px; letter-spacing: 1px; color: var(--t2); }
  @media (max-width: 760px) { .oa-ft { padding: 32px 20px 24px; } .oa-ft-cols { flex-direction: column; gap: 20px; } }

  /* ---------------- 공통 Hero (design.md 3) ---------------- */
  .oa-label { font-family: Inter, sans-serif; font-size: 13px; font-weight: 500; letter-spacing: .28em;
              text-transform: uppercase; color: var(--gray-400); }
  .oa-title { font-family: "Playfair Display", serif; font-weight: 700; color: var(--white);
              font-size: clamp(64px, 9vw, 112px); line-height: 1; letter-spacing: .01em; margin: 20px 0 8px; padding: 0; }
  .oa-sub   { font-family: Inter, sans-serif; font-size: 16px; font-weight: 500; letter-spacing: .32em;
              text-transform: uppercase; color: var(--gray-200); }
  .oa-desc  { font-size: 18px; line-height: 1.75; color: var(--gray-200); max-width: 32em; margin: 28px 0 8px; word-break: keep-all; }
  .oa-art   { border: 1px solid rgba(255, 255, 255, .16); border-radius: 12px; overflow: hidden; }
  .oa-art svg, .oa-art img { display: block; width: 100%; height: auto; }
  .oa-art img.oa-photo { filter: grayscale(1) contrast(1.05); aspect-ratio: 8 / 5; object-fit: cover; }

  .oa-page-title { font-family: "Playfair Display", "Noto Sans KR", serif; font-weight: 600; color: var(--white);
                   font-size: clamp(34px, 4.2vw, 48px); line-height: 1.2; letter-spacing: -.005em; margin: 18px 0 0; padding: 0; }

  /* ---------------- 상세 페이지 흰 콘텐츠 카드 (design.md 4): 어두운 배경 위에 독립된 카드 ---------------- */
  [class*="st-key-page-card"] {
    background: var(--white); border: 1px solid var(--gray-200); border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .06); padding: 40px; margin-top: 32px;
  }
  @media (max-width: 760px) { [class*="st-key-page-card"] { padding: 24px; } }
  [class*="st-key-page-card"], [class*="st-key-page-card"] * { color: var(--black); }
  .oa-sec-num   { font-family: Inter, sans-serif; font-size: 12px; font-weight: 600; letter-spacing: .24em; color: var(--gray-600); }
  .oa-sec-title { font-family: "Noto Sans KR", sans-serif; font-weight: 700; font-size: 24px; line-height: 1.4; margin: 10px 0 14px; padding: 0; color: var(--black); }
  .oa-body      { font-size: 16px; line-height: 1.8; color: var(--black); word-break: keep-all; margin: 0 0 12px; }
  .oa-rule      { border: 0; border-top: 1px solid var(--gray-200); margin: 44px 0; }
  .oa-table     { width: 100%; border-collapse: collapse; font-size: 14px; }
  .oa-table th  { text-align: left; font-weight: 600; color: var(--text-secondary); padding: 10px 12px; border-bottom: 1px solid var(--gray-400); }
  .oa-table td  { padding: 10px 12px; border-bottom: 1px solid var(--gray-200); color: var(--black); vertical-align: top; word-break: keep-all; }
  .oa-table .r  { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .oa-table code{ font-family: "JetBrains Mono", monospace; font-size: 13px; color: var(--charcoal); background: var(--off-white); padding: 1px 6px; border-radius: 4px; }
  .oa-kpi-w     { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 4px 0 28px; }
  .oa-kpi-w > div { background: var(--off-white); border-radius: 12px; padding: 18px 20px; }
  .oa-kpi-w .k  { font-size: 13px; color: var(--text-secondary); }
  .oa-kpi-w .v  { font-family: Inter, sans-serif; font-size: 40px; font-weight: 600; line-height: 1.1; margin-top: 6px; color: var(--black); font-variant-numeric: tabular-nums; }
  .oa-goal-w    { display: grid; grid-template-columns: 36px 1fr; gap: 12px; padding: 16px 0; border-top: 1px solid var(--gray-200); }
  .oa-goal-w:first-child { border-top: 0; padding-top: 0; }
  .oa-goal-w .n { font-family: Inter, sans-serif; font-size: 13px; font-weight: 600; letter-spacing: .12em; color: var(--gray-600); padding-top: 4px; }
  .oa-goal-w b  { display: block; font-size: 17px; font-weight: 700; line-height: 1.5; color: var(--black); }
  .oa-goal-w p  { margin: 4px 0 0; font-size: 15px; line-height: 1.7; color: var(--text-secondary); word-break: keep-all; }
  .oa-sub-label { font-family: "Noto Sans KR", sans-serif; font-size: 13px; font-weight: 700; letter-spacing: .08em; color: var(--gray-600); margin: 34px 0 10px; }
  .oa-ul        { margin: 0 0 8px; padding-left: 20px; }
  .oa-ul li     { font-size: 16px; line-height: 1.8; color: var(--black); word-break: keep-all; }
  .oa-chip      { display: inline-block; font-family: "JetBrains Mono", monospace; font-size: 13px; color: var(--charcoal); background: var(--off-white);
                  border: 1px solid var(--gray-200); border-radius: 6px; padding: 3px 10px; margin: 0 8px 6px 0; }
  .oa-note      { background: var(--off-white); border-radius: 12px; padding: 20px 24px; }
  .oa-note .oa-ul { margin-bottom: 0; }
  .oa-cap       { font-size: 13px; font-weight: 600; color: var(--text-secondary); margin: 22px 0 8px; }

  /* ---------------- 카드 안 요소: 번호 배지 · 2열 상자 · 대시보드 패널 ---------------- */
  .oa-head      { display: flex; gap: 18px; align-items: center; margin-bottom: 6px; }
  .oa-badge     { flex: none; width: 52px; height: 52px; border-radius: 50%; background: var(--off-white); border: 1px solid var(--gray-200);
                  display: flex; align-items: center; justify-content: center; font-family: Inter, sans-serif; font-size: 20px; font-weight: 600; color: var(--black); }
  .oa-head .oa-sec-title { margin: 0; }
  .oa-head .en  { font-family: "Playfair Display", serif; font-size: 18px; font-weight: 400; color: var(--text-secondary); margin-left: 8px; }
  .oa-two       { display: grid; grid-template-columns: 1.3fr 1fr; gap: 16px; margin: 8px 0 4px; }
  .oa-two > div { border: 1px solid var(--gray-200); border-radius: 12px; padding: 18px 22px; }
  .oa-two .t    { font-size: 14px; font-weight: 700; color: var(--black); margin-bottom: 8px; }
  .oa-two .oa-ul li { font-size: 15px; line-height: 1.7; }
  @media (max-width: 760px) { .oa-two { grid-template-columns: 1fr; } }
  .oa-flow      { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: 4px; }
  .oa-flow a    { color: var(--black); }
  /* 코드 영역: Off White 바탕, JetBrains Mono, 긴 코드는 가로 스크롤 */
  [class*="st-key-page-card"] [data-testid="stCode"], [class*="st-key-page-card"] [data-testid="stCode"] pre {
    background: var(--off-white) !important; border-radius: 8px; }
  [class*="st-key-page-card"] [data-testid="stCode"] code, [class*="st-key-page-card"] [data-testid="stCode"] code * {
    color: var(--charcoal) !important; font-family: "JetBrains Mono", monospace; font-size: 13px; }
  /* 카드 안 버튼(이전·다음): White Card 위 주요 버튼 = 검정 바탕 흰 글자, 모서리 6px */
  [class*="st-key-page-card"] [data-testid^="stBaseButton"] { background: var(--black); border: 1px solid var(--black); border-radius: 6px; padding: 8px 20px; }
  [class*="st-key-page-card"] [data-testid^="stBaseButton"], [class*="st-key-page-card"] [data-testid^="stBaseButton"] * { color: var(--white); font-weight: 600; }
  [class*="st-key-page-card"] [data-testid^="stBaseButton"]:hover:not(:disabled) { background: var(--charcoal); }
  [class*="st-key-page-card"] [data-testid^="stBaseButton"]:disabled { opacity: .3; }
  [class*="st-key-page-card"] [data-testid="stPageLink-NavLink"] { background: var(--black); border-radius: 6px; padding: 8px 20px; width: fit-content; }
  [class*="st-key-page-card"] [data-testid="stPageLink-NavLink"], [class*="st-key-page-card"] [data-testid="stPageLink-NavLink"] * { color: var(--white); font-weight: 600; }
  [class*="st-key-page-card"] [data-testid="stPageLink-NavLink"]:hover { background: var(--charcoal); }

  /* ---------------- 버튼 (design.md 10): 어두운 배경 위 ---------------- */
  .st-key-cta-primary, .st-key-cta-secondary { flex: 0 0 auto; width: auto; }
  [class*="st-key-cta-"] [data-testid="stPageLink-NavLink"] {
    border-radius: 999px; padding: 10px 26px; width: fit-content; transition: background .18s, border-color .18s;
  }
  [class*="st-key-cta-"] [data-testid="stPageLink-NavLink"] p { font-size: 15px; font-weight: 600; }
  .st-key-cta-primary [data-testid="stPageLink-NavLink"] { background: var(--white); border: 1px solid var(--white); }
  .st-key-cta-primary [data-testid="stPageLink-NavLink"], .st-key-cta-primary [data-testid="stPageLink-NavLink"] * { color: var(--navy-900); }
  .st-key-cta-primary [data-testid="stPageLink-NavLink"]:hover { background: var(--gray-200); border-color: var(--gray-200); }
  .st-key-cta-secondary [data-testid="stPageLink-NavLink"] { background: transparent; border: 1px solid rgba(255, 255, 255, .45); }
  .st-key-cta-secondary [data-testid="stPageLink-NavLink"], .st-key-cta-secondary [data-testid="stPageLink-NavLink"] * { color: var(--white); }
  .st-key-cta-secondary [data-testid="stPageLink-NavLink"]:hover { border-color: var(--white); background: rgba(255, 255, 255, .08); }

  /* 한글은 단어 단위로 줄 바꿈 */
  [data-testid="stMarkdownContainer"] p { word-break: keep-all; }

  /* 단계·항목 태그(st.pills): 한 줄에 같은 너비로 꽉 채운다. 선택 = 밝은 바탕 + 어두운 글자 (Figma: Analysis tabs / Step chip) */
  .st-key-tabs-band { background: var(--index); padding: 18px 80px 26px; }
  .st-key-tabs-band [data-testid="stElementContainer"], .st-key-tabs-band [data-testid="stButtonGroup"], .st-key-tabs-band [role="radiogroup"] { width: 100%; }
  .st-key-tabs-band [role="radiogroup"] { display: flex; flex-wrap: nowrap; gap: 10px; max-width: none; }
  .st-key-tabs-band button[role="radio"] { flex: 1 1 0; min-width: 0; height: 49px; border-radius: 100px; padding: 0 6px; background: var(--card);
      border: 1px solid var(--line); justify-content: center; }
  .st-key-tabs-band button[role="radio"], .st-key-tabs-band button[role="radio"] * { color: var(--t1); font-size: 14px; font-weight: 400; white-space: nowrap; }
  .st-key-tabs-band button[role="radio"]:hover { border-color: rgba(255, 255, 255, .5); }
  .st-key-tabs-band button[role="radio"][aria-checked="true"] { background: var(--tab-on, #edf3f7); border-color: var(--tab-on, #edf3f7); }
  .st-key-tabs-band button[role="radio"][aria-checked="true"], .st-key-tabs-band button[role="radio"][aria-checked="true"] * { color: #061c29; font-weight: 700; }
  .st-key-tabs-row { align-items: center; gap: 10px; flex-wrap: nowrap; }
  .st-key-tabs-row > [data-testid="stElementContainer"]:has([role="radiogroup"]) { flex: 1 1 0; min-width: 0; }
  [class*="st-key-tabs-"][class*="_tprev"], [class*="st-key-tabs-"][class*="_tnext"] { display: none; flex: none; width: auto; }
  .st-key-tabs-row [data-testid^="stBaseButton"] { width: 49px; height: 49px; min-height: 49px; padding: 0; border-radius: 100px; background: var(--card); border: 1px solid var(--line); }
  .st-key-tabs-row [data-testid^="stBaseButton"], .st-key-tabs-row [data-testid^="stBaseButton"] * { color: var(--white); font-size: 22px; font-weight: 400; line-height: 1; }
  .st-key-tabs-row [data-testid^="stBaseButton"]:hover:not(:disabled) { border-color: rgba(255, 255, 255, .5); }
  .st-key-tabs-row [data-testid^="stBaseButton"]:disabled { opacity: .35; }
  /* 화면이 좁으면: 가로 스크롤 없이 선택한 태그 하나만 보이고, 양 끝 < > 버튼으로 이전·다음 태그로 이동 */
  @media (max-width: 1280px) {
    .st-key-tabs-band { padding: 14px 20px 20px; }
    [class*="st-key-tabs-"][class*="_tprev"], [class*="st-key-tabs-"][class*="_tnext"] { display: block; }
    .st-key-tabs-band button[role="radio"]:not([aria-checked="true"]) { display: none; }
    .st-key-tabs-band button[role="radio"][aria-checked="true"] { flex: 1 1 100%; }
    /* < 선택한 태그 > 를 가운데에 모으고, 태그 폭은 규격(최대 420px) 안에 둔다 */
    .st-key-tabs-row { justify-content: center; }
    .st-key-tabs-row > [data-testid="stElementContainer"]:has([role="radiogroup"]) { flex: 0 1 420px; }
  }

  /* 페이지 상단 선박 배너 (Figma: Ship masthead, 340px) */
  .oa-mh { position: relative; height: 340px; padding: 62px 80px 40px; overflow: hidden; background-color: var(--nav);
           background-size: cover; background-position: center top; }
  .oa-mh-a { background-image: linear-gradient(90deg, #04151f 0%, rgba(4,21,31,.91) 56%, rgba(4,21,31,.06) 100%), var(--mh-img); }
  .oa-mh-b { background-image: linear-gradient(90deg, rgba(4,21,31,.95) 0%, rgba(4,21,31,.65) 44%, rgba(4,21,31,0) 100%), var(--mh-img); }
  .oa-mh .l { font-family: "Playfair Display", serif; font-size: 15px; letter-spacing: 3px; color: var(--t1); margin: 0 0 18px; }
  .oa-mh .t { font-size: 43px; font-weight: 700; color: var(--white); line-height: 1.2; margin: 0 0 18px; }
  .oa-mh .d { font-size: 17px; line-height: 1.85; color: var(--t1); max-width: 660px; margin: 0; word-break: keep-all; }
  .oa-mh .cap { position: absolute; right: 80px; bottom: 50px; font-family: "Playfair Display", serif; font-size: 12px; letter-spacing: 2px; color: var(--t1); }
  @media (max-width: 760px) { .oa-mh { padding: 40px 20px; height: auto; min-height: 300px; } .oa-mh .t { font-size: 32px; } .oa-mh .cap { display: none; } }
</style>
"""
