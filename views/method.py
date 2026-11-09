"""분석 방법 소개 — Figma 시안 '분석 방법 소개 — Titanic Analytics' (실습 8단계).

선박 배너 → 8개 단계 태그 → 선택한 단계의 상세 기록 카드 → 이전·다음 → Footer.
상세 카드 순서: 번호 · 제목 · 목적 → 주요 활동 | 사용 도구 → 코드 예시 | 결과 → 해석 → 이전·다음.
내용은 실제 실습(t1~t7 스크립트, data/*.csv)에서만 가져온다. 숫자는 모두 데이터에서 계산하고,
'해석'에는 데이터로 확인한 사실만 쓴다.
"""
import pandas as pd
import streamlit as st

from common import asset_uri, masthead, nav_active, ROOT, STEP_TITLES, esc, load_clean, load_raw, num, pct, pp, r1, site_footer, summary, tabs_band, request_scroll_top, scroll_top_if_requested
from common import html_caption as caption, html_kpis as kpis, html_table as table, html_ul as ul

nav_active("method")
TITLE_MAP = {"Mr": "Mr", "Mrs": "Mrs", "Miss": "Miss", "Master": "Master", "Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"}
AGE_BINS = [0, 13, 20, 40, 60, float("inf")]
AGE_LABELS = ["어린이(0~12)", "10대(13~19)", "청년(20~39)", "중년(40~59)", "노년(60+)"]


# ---------------------------------------------------------------- 계산 (t1~t5 스크립트와 같은 방법)
@st.cache_data
def stats() -> dict:
    raw, clean = load_raw(), load_clean()
    o = {}
    o["rows"], o["cols"] = raw.shape
    o["rate"] = r1(raw["Survived"].mean() * 100)
    o["age_mean"], o["age_median"] = round(raw["Age"].mean(), 1), round(raw["Age"].median(), 1)
    o["fare_min"], o["fare_max"], o["fare0"] = raw["Fare"].min(), round(raw["Fare"].max(), 1), int((raw["Fare"] == 0).sum())

    # 02 결측
    miss = raw.isna().sum().sort_values(ascending=False)
    o["missing"] = pd.DataFrame({
        "칸": miss.index, "결측 개수": miss.values.astype(int),
        "결측 비율(%)": (miss.values / len(raw) * 100).round(1),
    })
    o["missing"] = o["missing"][o["missing"]["결측 개수"] > 0]

    # 03 왜 비었을까
    has, na = raw[raw["Age"].notna()]["Survived"], raw[raw["Age"].isna()]["Survived"]
    o["age_has"] = (r1(has.mean() * 100), len(has))
    o["age_na"] = (r1(na.mean() * 100), len(na))
    cab = raw.groupby("Pclass")["Cabin"].agg(empty=lambda s: int(s.isna().sum()), n="size")
    # 주의: r.empty 는 pandas 기본 속성이므로 반드시 r["empty"] 로 읽는다
    o["cabin"] = [(f"{c}등석", r1(r["empty"] / r["n"] * 100), int(r["empty"]), int(r["n"])) for c, r in cab.iterrows()]
    o["emb_rows"] = raw[raw["Embarked"].isna()][["Name", "Pclass", "Ticket"]].rename(
        columns={"Name": "이름", "Pclass": "객실 등급", "Ticket": "티켓 번호"})

    # 04 결측 처리
    o["filled_age"] = int(clean["age_missing"].sum())
    o["cabin_yes"], o["cabin_no"] = int((clean["has_cabin"] == 1).sum()), int((clean["has_cabin"] == 0).sum())
    o["filled_emb"] = int(raw["Embarked"].isna().sum())
    title = raw["Name"].str.extract(r", ([^.]+)\.")[0].map(TITLE_MAP).fillna("Other")
    tm = raw.assign(호칭=title).groupby("호칭")["Age"].agg(중앙값="median", 나이있는_인원="count").reset_index()
    tm["중앙값"] = tm["중앙값"].round(1)
    o["title_median"] = tm.rename(columns={"나이있는_인원": "나이가 있던 인원(명)", "중앙값": "중앙값 나이(세)"})
    o["clean_rows"] = len(clean)

    # 05 처리 방법 실험
    r = raw.assign(Title=title)
    methods = {
        "① 지우기": r.dropna(subset=["Age"]),
        "② 전체 중앙값": r.assign(Age=r["Age"].fillna(r["Age"].median())),
        "③ 호칭별 중앙값": r.assign(Age=r["Age"].fillna(r.groupby("Title")["Age"].transform("median"))),
        "④ 0으로 채움": r.assign(Age=r["Age"].fillna(0)),
    }
    rates, counts = {}, {}
    for name, d in methods.items():
        g = d.assign(나이대=pd.cut(d["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=False)).groupby("나이대", observed=False)["Survived"]
        rates[name], counts[name] = (g.mean() * 100).round(1), g.size()
    rt, ct = pd.DataFrame(rates), pd.DataFrame(counts)
    exp = pd.DataFrame({c: [f"{rt.loc[i, c]:.1f}% ({int(ct.loc[i, c])}명)" for i in rt.index] for c in rt.columns})
    exp.insert(0, "나이대", list(rt.index))
    o["exp"] = exp
    diff = rt.sub(rt["① 지우기"], axis=0).drop(columns="① 지우기").round(1)
    big = diff.abs().stack().idxmax()
    o["exp_big"] = dict(age=big[0], method=big[1], diff=float(diff.loc[big]),
                        base=float(rt.loc[big[0], "① 지우기"]), val=float(rt.loc[big[0], big[1]]))

    # 06 그룹별 생존율
    def by(col, label, labels=None):
        g = clean.groupby(col)["Survived"].agg(n="size", s="sum")
        return pd.DataFrame({
            label: [labels.get(i, i) if labels else i for i in g.index],
            "생존율": [pct(r1(s / n * 100)) for s, n in zip(g["s"], g["n"])],
            "생존자 / 전체(명)": [f"{num(s)} / {num(n)}" for s, n in zip(g["s"], g["n"])],
        })
    o["by_sex"] = by("Sex", "성별", {"female": "여성", "male": "남성"})
    o["by_cls"] = by("Pclass", "객실 등급", {1: "1등석", 2: "2등석", 3: "3등석"})
    o["by_emb"] = by("Embarked", "탑승 항구")

    # 07 시각화: chart 폴더에 실제로 저장된 파일
    o["charts"] = sorted(p.name for p in (ROOT / "chart").glob("*.html"))
    return o


# ---------------------------------------------------------------- 화면 조각 (HTML)
def read_code(name: str, upto: str | None = None) -> str:
    text = (ROOT / name).read_text(encoding="utf-8")
    if upto and upto in text:
        text = text.split(upto)[0].rstrip() + "\n\n# ... (이하 HTML 템플릿과 저장 부분은 생략)"
    return text.strip() + "\n"


# ---------------------------------------------------------------- 단계별 내용
def build(i: int, o: dict, S: dict) -> dict:
    """한 단계의 내용: purpose, acts(주요 활동), tools(사용 도구), result(HTML), code(파일, 자를 곳), notes(해석)."""
    if i == 0:
        return dict(
            purpose="어떤 데이터인지, 칸마다 무슨 뜻인지, 이상한 값은 없는지 확인한다.",
            acts=["행과 칸의 개수, 위 5줄 확인", "칸마다 어떤 데이터를 뜻하는지 정리", "칸마다 비어 있지 않은 개수와 자료형 확인",
                  "생존 칸의 평균, 나이의 평균과 중앙값, 운임의 최소·최대값 확인"],
            tools=["t1_look.py", "pandas"],
            result=kpis([("승객 수", f"{num(o['rows'])}명"), ("칸 수", f"{o['cols']}개"), ("전체 생존율", pct(o["rate"]))]),
            code=("t1_look.py", None),
            notes=[f"나이의 평균은 {o['age_mean']}세, 중앙값은 {o['age_median']}세로 두 값이 다르다.",
                   f"운임(Fare)은 최소 {o['fare_min']:.0f}, 최대 {o['fare_max']:,}이고, 운임이 0인 승객이 {o['fare0']}명 있다."],
        )
    if i == 1:
        m = o["missing"]
        top = ", ".join(f"{r['칸']} {num(r['결측 개수'])}명({r['결측 비율(%)']}%)" for _, r in m.iterrows())
        return dict(
            purpose="비어 있는 칸을 찾아 칸마다 개수와 비율을 센다. 이 단계에서는 아무것도 고치거나 채우지 않는다.",
            acts=["칸마다 결측 개수와 비율을 많은 순서로 정리", "결측이 있는 칸마다 비어 있는 행 3개씩 확인",
                  "문자로 적힌 빈 값 표시(&quot;-&quot;, &quot;없음&quot; 등)와 의심되는 숫자(0, 999)도 함께 확인"],
            tools=["t2_missing.py", "pandas"],
            result=caption("칸별 결측 개수와 비율") + table(m, right=("결측 개수", "결측 비율(%)")),
            code=("t2_missing.py", None),
            notes=[f"비어 있는 칸은 {len(m)}개이고, {top}이다."],
        )
    if i == 2:
        cab = o["cabin"]
        cabin_txt = ", ".join(f"{c} {pct(p)}" for c, p, _, _ in cab)
        tickets = ", ".join(str(t) for t in o["emb_rows"]["티켓 번호"])
        return dict(
            purpose="비어 있는 칸마다 왜 비었는지 데이터로 확인한다.",
            acts=["Age: 나이가 빈 승객과 있는 승객의 생존율 비교", "Cabin: 객실 등급별로 비어 있는 비율 확인",
                  "Embarked: 비어 있는 승객의 티켓 번호와 객실 확인", "Fare가 0인 승객이 몇 명인지 확인"],
            tools=["pandas"],
            result=(kpis([("나이가 있는 승객의 생존율", pct(o["age_has"][0])), ("나이가 빈 승객의 생존율", pct(o["age_na"][0])),
                          ("운임이 0인 승객", f"{o['fare0']}명")])
                    + caption("객실 등급별 Cabin(객실 번호)이 빈 비율")
                    + table(pd.DataFrame([(c, pct(p), f"{num(e)} / {num(n)}") for c, p, e, n in cab],
                                         columns=["객실 등급", "빈 비율", "빈 승객 / 전체(명)"]), right=("빈 비율", "빈 승객 / 전체(명)"))
                    + caption("Embarked(탑승 항구)가 빈 승객") + table(o["emb_rows"])),
            code=None,
            notes=[f"나이가 있는 승객 {num(o['age_has'][1])}명의 생존율은 {pct(o['age_has'][0])}, 빈 승객 {num(o['age_na'][1])}명은 {pct(o['age_na'][0])}이다.",
                   f"Cabin이 빈 비율은 {cabin_txt}이다.",
                   f"Embarked가 빈 승객은 {len(o['emb_rows'])}명이고 티켓 번호는 {tickets}이다."],
        )
    if i == 3:
        n_titles = len(o["title_median"])
        return dict(
            purpose="칸마다 정한 방법으로 결측치를 처리한다. 원본 파일은 그대로 두고 새 파일에 저장한다.",
            acts=["Age: 이름에 들어 있는 호칭별 중앙값으로 채우고, 원래 비어 있었는지는 <code>age_missing</code> 칸에 표시",
                  "Cabin: 객실 번호가 있는지 없는지를 <code>has_cabin</code> 칸으로 바꾸고 원본 Cabin은 유지",
                  "Embarked: 비어 있던 값을 S로 채움", "정제한 결과를 <code>data/titanic_clean.csv</code>로 저장"],
            tools=["t3_clean.py", "pandas"],
            result=(kpis([("정제 전 → 후 행 수", f"{num(o['rows'])} → {num(o['clean_rows'])}"),
                          ("나이를 채운 승객", f"{num(o['filled_age'])}명"), ("항구를 채운 승객", f"{o['filled_emb']}명")])
                    + caption("호칭별 중앙값 나이") + table(o["title_median"], right=("중앙값 나이(세)", "나이가 있던 인원(명)"))),
            code=("t3_clean.py", None),
            notes=[f"정제 전후 행 수는 {num(o['rows'])} → {num(o['clean_rows'])}로 같다. 행을 지우지 않았다.",
                   f"나이를 채운 승객은 {num(o['filled_age'])}명이고, 호칭 {n_titles}가지의 중앙값을 사용했다.",
                   f"Cabin은 있음 {num(o['cabin_yes'])}명, 없음 {num(o['cabin_no'])}명으로 나뉜다."],
        )
    if i == 4:
        b = o["exp_big"]
        return dict(
            purpose="나이의 결측치를 처리하는 방법에 따라 나이대별 생존율이 달라지는지 실험한다.",
            acts=["나이 빈 행 지우기", "전체 중앙값으로 채우기", "호칭별 중앙값으로 채우기", "0으로 채우기",
                  "나이대(어린이·10대·청년·중년·노년)마다 생존율과 인원 수를 방법별로 나란히 비교"],
            tools=["t4_experiment.py", "pandas"],
            result=caption("나이대별 생존율 (인원 수)") + table(o["exp"]),
            code=("t4_experiment.py", None),
            notes=[f"가장 크게 달라진 칸은 {esc(b['age'])} / {esc(b['method'])}이다. 지우기 {pct(b['base'])}에서 {pct(b['val'])}로 {b['diff']:+.1f}%p 바뀌었다."],
        )
    if i == 5:
        f, m = S["sex"]["여성"], S["sex"]["남성"]
        c = S["cls"]
        emb = o["by_emb"]
        emb_txt = ", ".join(f"{r['탑승 항구']} {r['생존율']}" for _, r in emb.iterrows())
        return dict(
            purpose="정제한 데이터로 그룹별 생존율과 인원 수를 센다.",
            acts=["성별 생존율과 인원 수", "객실 등급별 생존율과 인원 수", "성별 × 등급 생존율", "탑승 항구별, 항구 × 등급 생존율"],
            tools=["t5_groupby.py", "pandas"],
            result=(caption("성별") + table(o["by_sex"], right=("생존율", "생존자 / 전체(명)"))
                    + caption("객실 등급") + table(o["by_cls"], right=("생존율", "생존자 / 전체(명)"))
                    + caption("탑승 항구") + table(o["by_emb"], right=("생존율", "생존자 / 전체(명)"))),
            code=("t5_groupby.py", None),
            notes=[f"성별 생존율은 여성 {pct(f['rate'])}({num(f['s'])}명/{num(f['n'])}명), 남성 {pct(m['rate'])}({num(m['s'])}명/{num(m['n'])}명)이다.",
                   f"객실 등급별 생존율은 1등석 {pct(c['1등석']['rate'])}, 2등석 {pct(c['2등석']['rate'])}, 3등석 {pct(c['3등석']['rate'])}이다.",
                   f"탑승 항구별 생존율은 {emb_txt}이다."],
        )
    if i == 6:
        kinds = ["등급별 생존율 막대", "성별 × 등급 생존율 묶음 막대", "나이 분포 히스토그램 (원본 vs 중앙값으로 채운 버전)", "등급별 운임 박스 차트"]
        files = o["charts"]
        chart_df = pd.DataFrame({"차트": kinds[:len(files)], "저장 파일": files})
        return dict(
            purpose="분석 결과를 차트로 그리고, 차트마다 같은 규칙을 지킨다.",
            acts=["Plotly로 차트 4개를 그려 <code>chart</code> 폴더에 HTML 파일로 저장", "차트 제목은 결론 문장으로 정할 수 있게 비워 두고 후보를 제안받음",
                  "축 이름은 한글로, 비율은 %로 표시"],
            tools=["t6_charts.py", "pandas", "Plotly"],
            result=(caption("저장된 차트") + table(chart_df)
                    + caption("차트 규칙")
                    + ul(["제목은 결론 문장으로 쓴다", "비율 막대에는 인원(분모)을 같이 표시한다", "막대 차트의 세로축은 0에서 시작한다",
                          "색은 뜻이 있을 때만 쓴다", "축 이름은 한글로, 단위(%, 원, 명)를 붙인다"])),
            code=("t6_charts.py", None),
            notes=[f"차트는 chart 폴더의 HTML 파일 {len(files)}개로 저장되어 있다."],
        )
    return dict(
        purpose="정제한 데이터에서 성별·등급별 생존율을 계산해 한 화면의 대시보드로 만든다.",
        acts=["정제한 데이터(<code>titanic_clean.csv</code>)에서 성별 × 등급 생존율과 인원 수 계산", "계산한 숫자로 대시보드 화면(HTML) 생성",
              "비율 옆에는 항상 인원 수를 함께 표시"],
        tools=["t7_dashboard.py", "pandas"],
        result=kpis([("전체 생존율", pct(S["rate"])), ("성별 격차 (여성 − 남성)", pp(S["sex_gap"])), ("등급 격차 (1등석 − 3등석)", pp(S["cls_gap"]))]),
        code=("t7_dashboard.py", "TEMPLATE = r'''"),
        notes=[f"전체 {num(S['total'])}명 중 {num(S['alive'])}명({pct(S['rate'])})이 생존했다.",
               "같은 계산 결과를 종합 분석 페이지에서 확인할 수 있다."],
    )


# ---------------------------------------------------------------- 화면
st.html(f"""
<style>
  .st-key-md-body {{ background: var(--index); padding: 0 80px 56px; gap: 28px; }}
  .md-num {{ font-family: "Playfair Display", serif; font-size: 37px; line-height: 1; color: var(--t1); }}
  .md-head {{ display: flex; gap: 22px; align-items: flex-start; }}
  .md-head .t {{ font-size: 28px; font-weight: 700; color: var(--white); line-height: 1.3; margin-bottom: 8px; }}
  .md-head .p {{ font-size: 15px; line-height: 1.7; color: var(--t2); margin: 0; word-break: keep-all; }}
  .md-h {{ font-size: 17px; font-weight: 700; color: var(--white); margin: 0 0 13px; }}
  .md-h.s {{ font-size: 16px; margin-bottom: 12px; }}
  .md-acts {{ list-style: none; margin: 0; padding: 0; }}
  .md-acts li {{ display: flex; gap: 10px; align-items: flex-start; font-size: 14px; line-height: 1.7; color: var(--t1); margin-bottom: 8px; word-break: keep-all; }}
  .md-acts li::before {{ content: ""; flex: none; width: 17px; height: 17px; margin-top: 4px; background: url({asset_uri("icon_check.svg")}) center/contain no-repeat; }}
  .md-tools {{ font-size: 15px; color: var(--t1); }}
  .md-res {{ overflow-x: auto; }}
  .md-note {{ display: flex; gap: 14px; align-items: flex-start; padding: 6px 0 0; }}
  .md-note::before {{ content: ""; flex: none; width: 22px; height: 22px; background: url({asset_uri("icon_bulb.svg")}) center/contain no-repeat; }}
  .md-note ul {{ margin: 0; padding-left: 18px; }}
  .md-note li {{ font-size: 14px; line-height: 1.8; color: var(--t1); word-break: keep-all; }}
  .md-two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  .md-jh {{ display: flex; justify-content: space-between; align-items: baseline; padding-top: 12px; }}
  .md-jh b {{ font-size: 23px; color: var(--white); }}
  .md-jh span {{ font-family: "Playfair Display", serif; font-size: 13px; letter-spacing: 2px; color: var(--t2); }}
  .md-recs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .md-rec {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 26px; display: flex; flex-direction: column; gap: 14px; }}
  .md-rec .h {{ display: flex; gap: 15px; align-items: center; }}
  .md-rec .h i {{ font-family: "Playfair Display", serif; font-style: normal; font-size: 37px; line-height: 1; color: #456d88; }}
  .md-rec .h b {{ font-size: 19px; color: var(--white); }}
  .md-rec .g {{ font-size: 10px; font-weight: 700; letter-spacing: 1.5px; color: #285d77; }}
  .md-rec p {{ margin: 0; font-size: 14px; line-height: 1.85; color: var(--t2); word-break: keep-all; }}
  .md-int {{ background: var(--card); border-radius: 12px; padding: 26px; display: flex; flex-direction: column; gap: 15px; }}
  .md-int .g {{ font-family: "Playfair Display", serif; font-size: 12px; letter-spacing: 2px; color: var(--t2); }}
  .md-int b {{ font-size: 19px; color: var(--white); }}
  .md-int p {{ margin: 0; font-size: 14px; line-height: 1.9; color: var(--t1); white-space: pre-wrap; }}

  /* 상세 카드: 어두운 카드, 안의 코드 · 표 · 숫자 상자도 어둡게 */
  .st-key-md-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 40px; gap: 0; }}
  .st-key-md-card [data-testid="stCode"], .st-key-md-card [data-testid="stCode"] pre {{ background: #000 !important; border-radius: 6px; }}
  .st-key-md-card [data-testid="stCode"] code, .st-key-md-card [data-testid="stCode"] code * {{ color: var(--t1) !important; font-family: "JetBrains Mono", monospace; font-size: 13px; }}
  .dk .oa-table {{ width: 100%; border-collapse: collapse; font-size: 13px; border: 1px solid var(--line); border-radius: 6px; }}
  .dk .oa-table th {{ text-align: left; color: var(--white); font-weight: 700; padding: 11px 18px; border-bottom: 1px solid var(--line); }}
  .dk .oa-table td {{ color: var(--t1); padding: 11px 18px; border-bottom: 1px solid var(--line); }}
  .dk .oa-table tr:last-child td {{ border-bottom: 0; }}
  .dk .oa-table .r {{ text-align: right; }}
  .dk .oa-table code {{ background: transparent; color: var(--t1); font-size: 12px; }}
  .dk .oa-kpi-w {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 0 0 12px; }}
  .dk .oa-kpi-w > div {{ background: var(--nav); border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; }}
  .dk .oa-kpi-w .k {{ font-size: 12px; color: var(--t2); }}
  .dk .oa-kpi-w .v {{ font-size: 22px; font-weight: 700; color: var(--white); margin-top: 6px; }}
  .dk .oa-cap {{ font-size: 13px; color: var(--t2); margin: 14px 0 8px; }}
  .dk .oa-ul {{ margin: 0; padding-left: 18px; }}  .dk .oa-ul li {{ font-size: 14px; color: var(--t1); line-height: 1.8; }}
  .dk code {{ font-family: "JetBrains Mono", monospace; font-size: 12px; color: var(--cream); }}

  /* 이전 · 다음 버튼 */
  .st-key-md-nav [data-testid^="stBaseButton"] {{ background: transparent; border: 1px solid var(--t1); border-radius: 100px; padding: 10px 24px; }}
  .st-key-md-nav [data-testid^="stBaseButton"], .st-key-md-nav [data-testid^="stBaseButton"] * {{ color: var(--white); font-weight: 700; font-size: 14px; }}
  .st-key-md-nav [data-testid^="stBaseButton"]:hover {{ border-color: var(--white); background: rgba(255,255,255,.08); }}
  @media (max-width: 900px) {{ .st-key-md-body {{ padding: 0 20px 40px; }} .md-two, .md-recs {{ grid-template-columns: 1fr; }} .dk .oa-kpi-w {{ grid-template-columns: 1fr; }} }}
</style>
""")

masthead("ANALYSIS PROCESS", "분석 방법 소개",
         "891명의 기록을 살펴보고, 정리하고, 비교하기까지. <br class='nb'>데이터에서 인사이트로 이어지는 여덟 단계의 분석 기록이다.", variant="b")

def go(delta: int) -> None:
    request_scroll_top()
    st.session_state["step"] = STEP_TITLES[STEP_TITLES.index(st.session_state["step"]) + delta]


i = tabs_band(STEP_TITLES, "step", "분석 단계")
o, S = stats(), summary()
c = build(i, o, S)
last = len(STEP_TITLES) - 1

with st.container(key="md-body"):
    # ---- 선택한 단계의 상세 기록 카드
    with st.container(key="md-card"):
        st.html(f"""
<div class="dk">
<div class="md-head"><div class="md-num">{i + 1:02d}</div><div><div class="t">{esc(STEP_TITLES[i][3:])}</div><p class="p">{c['purpose']}</p></div></div>
<div class="md-two" style="margin-top:30px">
  <div><div class="md-h">주요 활동</div><ul class="md-acts">{''.join(f'<li>{a}</li>' for a in c['acts'])}</ul></div>
  <div><div class="md-h">사용 도구</div><div class="md-tools">{' · '.join(esc(t) for t in c['tools'])}</div></div>
</div></div>
""")
        left, right = st.columns(2, gap="large")
        with left:
            st.html('<div class="md-h s" style="margin-top:30px">코드 예시</div>')
            if c["code"]:
                st.code(read_code(*c["code"]), language=None, line_numbers=False, height=360)
            else:
                st.html('<div class="dk"><div class="md-tools">이 단계는 별도 스크립트 파일 없이 데이터를 조회해서 확인했다.</div></div>')
        with right:
            st.html(f'<div class="dk"><div class="md-h s" style="margin-top:30px">결과 예시</div><div class="md-res">{c["result"]}</div></div>')
        st.html(f"""
<div class="dk" style="margin-top:30px"><div class="md-note"><div>
  <div class="md-h s">해석 (데이터로 확인한 사실)</div>{ul(c['notes'])}</div></div></div>
""")

    with st.container(key="md-nav"):
        prev_col, next_col = st.columns(2)
        with prev_col:
            if i == 0:
                if st.button("← 프로젝트 소개", key="prev"):
                    st.switch_page("views/overview.py")
            else:
                st.button(f"← 이전: {STEP_TITLES[i - 1][3:]}", key="prev", on_click=go, args=(-1,))
        with next_col:
            with st.container(key="next-wrap", horizontal=True, horizontal_alignment="right"):
                if i == last:
                    if st.button("다음: 총분석 →", key="next"):
                        st.switch_page("views/analysis.py")
                else:
                    st.button(f"다음: {STEP_TITLES[i + 1][3:]} →", key="next", on_click=go, args=(1,))

scroll_top_if_requested()
site_footer()
