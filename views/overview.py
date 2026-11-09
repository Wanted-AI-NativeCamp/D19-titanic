"""프로젝트 소개 — Figma 시안 '프로젝트 소개 — Ocean Archive'.

선박 배너(TITANIC 로고 · 제목 · 설명) → 어두운 카드 하나(프로젝트 배경 · 분석 목적 · 데이터셋 소개) → Footer.
홈(views/home.py)과는 별도 페이지다. 시안 아래쪽의 '이어서 보기' 카드 2개는 앞서 요청하신 대로 넣지 않았다.
숫자와 '비어 있는 값'은 data/*.csv 에서 계산한다. 칸 뜻은 실습 코드(t1_look.py)의 설명을 그대로 쓴다.
"""
import streamlit as st

from common import GOALS, asset_uri, column_meaning, load_clean, load_raw, nav_active, num, pct, site_footer, summary

nav_active("overview")
S = summary()
raw, clean = load_raw(), load_clean()
missing = raw.isna().sum()
extra_cols = [c for c in clean.columns if c not in raw.columns]      # 정제 때 추가한 칸 (t3_clean.py)
COLUMN_MEANING = column_meaning()

st.html(f"""
<style>
  /* 배너: 로고 이미지 + 제목 + 설명 */
  .oa-mh .ov-eyebrow {{ font-size: 12px; font-weight: 700; letter-spacing: 3px; color: var(--gold); margin: 0 0 10px; }}
  .ov-logo {{ width: 254px; height: 75px; overflow: hidden; position: relative; }}
  .ov-logo img {{ position: absolute; height: 116.94%; left: -1.55%; top: -15.24%; width: 104.02%; max-width: none; }}
  .oa-mh .ov-rule {{ width: 470px; max-width: 100%; height: 1px; background: var(--line); opacity: .65; margin: 16px 0; }}
  .oa-mh .ov-ko {{ font-size: 27px; font-weight: 500; color: var(--white); margin: 0 0 16px; }}
  .oa-mh .ov-d {{ font-size: 17px; line-height: 1.85; color: var(--t2); max-width: 540px; margin: 0; word-break: keep-all; }}

  .st-key-ov-body {{ background: var(--index); padding: 48px 80px 64px; }}
  .st-key-ov-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 48px; }}
  .ov-sec {{ display: flex; gap: 40px; align-items: flex-start; }}
  .ov-id {{ flex: none; width: 220px; display: flex; flex-direction: column; gap: 12px; }}
  .ov-id i {{ font-family: "Playfair Display", serif; font-style: normal; font-size: 36px; line-height: 1; color: #456d88; }}
  .ov-id b {{ font-size: 25px; color: var(--white); white-space: nowrap; }}
  .ov-id span {{ font-family: "Playfair Display", serif; font-size: 13px; letter-spacing: 2px; color: var(--t2); }}
  .ov-txt {{ flex: 1; font-size: 17px; line-height: 1.95; color: var(--t1); margin: 0; word-break: keep-all; }}
  .ov-div {{ height: 1px; background: var(--line); margin: 44px 0; }}
  .ov-qs {{ flex: 1; display: flex; flex-direction: column; gap: 24px; }}
  .ov-qs > p {{ font-size: 17px; line-height: 1.7; color: var(--t1); margin: 0; }}
  .ov-q {{ display: flex; gap: 20px; align-items: flex-start; padding-bottom: 20px; border-bottom: 1px solid var(--line); }}
  .ov-q i {{ flex: none; width: 28px; font-family: "Playfair Display", serif; font-style: normal; font-size: 29px; line-height: 1.1; color: #456d88; }}
  .ov-q b {{ display: block; font-size: 17px; line-height: 1.6; color: var(--white); margin-bottom: 8px; }}
  .ov-q p {{ margin: 0; font-size: 15px; line-height: 1.8; color: var(--t1); word-break: keep-all; }}

  .ov-sum {{ display: flex; background: var(--nav); border: 1px solid var(--line); border-radius: 12px; padding: 28px 0; margin: 28px 0 0; }}
  .ov-sum > div {{ flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
  .ov-sum .k {{ font-size: 14px; color: var(--t2); }}
  .ov-sum .v {{ font-size: 43px; font-weight: 700; color: var(--white); letter-spacing: -2px; line-height: 1.1; }}
  .ov-cap {{ display: flex; justify-content: space-between; align-items: center; margin: 28px 0 16px; }}
  .ov-cap b {{ font-size: 17px; color: var(--white); }}
  .ov-cap span {{ font-family: "JetBrains Mono", monospace; font-size: 11px; letter-spacing: 1px; color: var(--t2); }}
  .ov-dict {{ background: var(--nav); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }}
  .ov-dict .row {{ display: flex; gap: 24px; align-items: center; min-height: 52px; padding: 14px 24px; background: var(--card); border-bottom: 1px solid var(--line); }}
  .ov-dict .row:last-child {{ border-bottom: 0; }}
  .ov-dict .row.na {{ background: var(--nav); }}
  .ov-dict .row.hd {{ background: var(--nav); min-height: 48px; padding: 0 24px; font-size: 13px; font-weight: 700; color: var(--white); }}
  .ov-dict .c1 {{ flex: none; width: 162px; font-family: "JetBrains Mono", monospace; font-size: 14px; color: var(--t1); }}
  .ov-dict .hd .c1 {{ font-family: inherit; font-size: 13px; color: var(--white); }}
  .ov-dict .c2 {{ flex: 1; font-size: 15px; line-height: 1.6; color: var(--t2); }}
  .ov-dict .hd .c2 {{ font-size: 13px; color: var(--white); }}
  .ov-dict .c3 {{ flex: none; width: 118px; text-align: right; font-size: 14px; color: #77858c; }}
  .ov-dict .na .c3 {{ color: var(--t1); font-weight: 700; }}
  .ov-dict .hd .c3 {{ color: var(--white); }}
  .ov-note {{ background: var(--nav); border-left: 2px solid var(--line); padding: 24px; margin-top: 28px; color: var(--t1); }}
  .ov-note .g {{ font-family: "Playfair Display", serif; font-size: 13px; letter-spacing: 2px; margin-bottom: 10px; }}
  .ov-note p {{ margin: 0; font-size: 15px; line-height: 1.9; word-break: keep-all; }}
  .ov-note code {{ font-family: "JetBrains Mono", monospace; font-size: 13px; color: var(--cream); background: transparent; }}
  @media (max-width: 900px) {{
    .st-key-ov-body {{ padding: 24px 20px 40px; }} .st-key-ov-card {{ padding: 24px; }}
    .ov-sec {{ flex-direction: column; gap: 16px; align-items: stretch !important; }} .ov-id {{ width: auto; }} .ov-sum .v {{ font-size: 28px; }}
    .ov-dict .row {{ flex-wrap: wrap; gap: 6px 16px; }} .ov-dict .c1 {{ width: auto; }} .ov-dict .c2 {{ flex-basis: 100%; order: 3; }}
  }}
</style>
<div class="oa-mh oa-mh-b">
  <p class="ov-eyebrow">TITANIC · SURVIVAL ANALYSIS</p>
  <div class="ov-logo"><img src="{asset_uri("logo_titanic.png")}" alt="TITANIC"></div>
  <div class="ov-rule"></div>
  <p class="ov-ko">타이타닉 생존 요인 분석 대시보드</p>
  <p class="ov-d">타이타닉호 승객 {num(S['total'])}명의 기록으로, <br class='nb'>성별과 객실 등급이 생존율에 어떤 차이를 만들었는지 분석했습니다.</p>
  <span class="cap">RMS TITANIC · 1912</span>
</div>
""")

goals_html = "".join(
    f'<div class="ov-q"><i>{i}</i><div><b>{g}</b><p>{d}</p></div></div>'
    for i, (g, d) in enumerate(GOALS, start=1)
)
rows_html = "".join(
    f'<div class="row{" na" if missing[c] else ""}"><span class="c1">{c}</span><span class="c2">{COLUMN_MEANING.get(c, "")}</span>'
    f'<span class="c3">{(num(missing[c]) + "명") if missing[c] else "없음"}</span></div>'
    for c in raw.columns
)
extra_html = ", ".join(f"<code>{c}</code>" for c in extra_cols)

with st.container(key="ov-body"):
    with st.container(key="ov-card"):
        st.html(f"""
<div class="ov-sec" style="align-items:center">
  <div class="ov-id"><i>01</i><b>프로젝트 배경</b><span>BACKGROUND</span></div>
  <p class="ov-txt">이 프로젝트는 데이터 분석 실습의 하나로, Kaggle에 공개된 1912년 타이타닉 승객 데이터를 사용했습니다.
  승객의 성별, 나이, 객실 등급, 탑승 항구 같은 기록과 생존 여부가 함께 담겨 있어, 어떤 승객이 살아남았는지를 데이터로 확인할 수 있습니다.</p>
</div>
<div class="ov-div"></div>
<div class="ov-sec">
  <div class="ov-id"><i>02</i><b>분석 목적</b><span>RESEARCH QUESTIONS</span></div>
  <div class="ov-qs"><p>누가 살아남았는지를 세 가지 질문으로 나누어 확인했습니다.</p>{goals_html}</div>
</div>
<div class="ov-div"></div>
<div class="ov-sec" style="align-items:center">
  <div class="ov-id"><i>03</i><b>데이터셋 소개</b><span>THE DATASET</span></div>
  <p class="ov-txt">승객 한 명이 한 행이고, 칸마다 승객의 기록 하나가 들어 있습니다.</p>
</div>
<div class="ov-sum">
  <div><span class="k">승객 수</span><span class="v">{num(S['total'])}명</span></div>
  <div><span class="k">칸 수</span><span class="v">{raw.shape[1]}개</span></div>
  <div><span class="k">전체 생존율</span><span class="v">{pct(S['rate'])}</span></div>
</div>
<div class="ov-cap"><b>전체 데이터 사전</b><span>DATA DICTIONARY / {raw.shape[1]} FIELDS</span></div>
<div class="ov-dict">
  <div class="row hd"><span class="c1">칸</span><span class="c2">뜻</span><span class="c3">비어 있는 값</span></div>
  {rows_html}
</div>
<div class="ov-note"><div class="g">ARCHIVE NOTE / CLEANING RECORD</div>
  <p>정제 과정에서 {extra_html} 칸을 추가했습니다. 원본 파일은 그대로 두고 새 파일(<code>titanic_clean.csv</code>)에 저장했습니다.</p></div>
""")

site_footer()
