"""총분석 — Figma 시안 '총분석 — Titanic Analytics'.

선박 배너 → 분석 항목 태그 5개(전체 요약 · 성별 · 등급 · 복합 · 탑승 항구) → 어두운 대시보드 → Footer.
전체 요약은 시안 그대로: 결론 문장 → KPI 카드 3개(전체 생존율 · 성별 격차 · 등급 격차) → 성별 · 객실 등급별 생존율 막대 6줄.
나머지 4개 항목은 같은 카드·막대 모양으로 보여준다 (시안에는 전체 요약만 있다).
숫자는 모두 data/titanic_clean.csv 에서 계산한다. 인사이트에는 데이터로 확인한 사실만 쓰고 원인은 단정하지 않는다.
"""
import pandas as pd
import streamlit as st

from common import (nav_active, CLASSES, group_rows, html_kpis as kpis, html_table as table, html_ul as ul,
                    load_clean, masthead, num, pct, port_names, pp, r1, site_footer, summary, tabs_band, request_scroll_top, scroll_top_if_requested)

nav_active("analysis")
ITEMS = ["전체 요약", "성별 분석", "등급 분석", "복합 분석", "탑승 항구 분석"]
F_COL, M_COL, LOW_COL = "#8fa9ba", "#456d88", "#ff8a5c"          # 여성 · 남성 · 가장 낮음 (Figma)
C_COLS = (F_COL, "#6b8ba1", M_COL)                                # 1·2·3등석
S = summary()
ROWS = group_rows()
RIGHT = ("인원(명)", "생존자(명)", "생존율")


# ---------------------------------------------------------------- 계산
@st.cache_data
def port_data() -> dict:
    """탑승 항구별(C, Q, S) 전체와 객실 등급별 생존자·인원 (정제한 데이터)."""
    df = load_clean()
    out = {}
    for code in "CQS":
        d = df[df["Embarked"] == code]
        by_cls = {c: (int(d[d["Pclass"] == i].Survived.sum()), int((d["Pclass"] == i).sum())) for i, c in enumerate(CLASSES, start=1)}
        out[code] = dict(s=int(d.Survived.sum()), n=len(d), rate=r1(d.Survived.mean() * 100), cls=by_cls)
    return out


def cell(s: int, n: int) -> str:
    return f"{pct(r1(s / n * 100))} ({s}/{n}명)" if n else "-"


def item(label, g, color, low=False):
    return dict(label=label, rate=g["rate"], s=g["s"], n=g["n"], color=color, low=low)


# ---------------------------------------------------------------- 화면 조각 (HTML)
def bars_card(title: str, sub: str, items: list, legend: bool = True) -> str:
    """가로 막대 카드. 막대 오른쪽에 생존율과 (생존자 / 인원), 가장 낮은 집단은 주황색 + 배지."""
    rows = "".join(
        f'<div class="an-row"><span class="n">{x["label"]}</span>'
        f'<span class="trk"><i style="width:{x["rate"]}%;background:{LOW_COL if x["low"] else x["color"]}"></i></span>'
        f'<b class="v{" low" if x["low"] else ""}">{pct(x["rate"])}</b>'
        f'<span class="c">({num(x["s"])} / {num(x["n"])}명)</span>'
        f'<span class="bd">{"<em>가장 낮음</em>" if x["low"] else ""}</span></div>'
        for x in items)
    leg = (f'<div class="lg"><span><i style="background:{F_COL}"></i>여성</span><span><i style="background:{M_COL}"></i>남성</span></div>'
           if legend else "")
    alt = f"{title}: " + ", ".join(f'{x["label"]} {pct(x["rate"])}' for x in items)
    return f"""<div class="an-card an-chart">
  <div class="hd"><div><div class="tt">{title}</div><div class="sb">{sub}</div></div>{leg}</div>
  <div role="img" aria-label="{alt}">{rows}</div>
  <div class="an-scale"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>
</div>"""


def mini(rows: list) -> str:
    """KPI 카드 안의 작은 막대: (이름, 비율, 색)."""
    return '<div class="an-mini">' + "".join(
        f'<div><span class="n">{n}</span><span class="trk"><i style="width:{v}%;background:{c}"></i></span><b>{pct(v)}</b></div>'
        for n, v, c in rows) + "</div>"


def callout(no: int, title: str, text: str) -> str:
    return f'<div class="an-call"><span class="no">{no}</span><div><b>{title}</b><p>{text}</p></div></div>'


def kpi_card(label: str, value: str, unit: str, mini_html: str, call_html: str) -> str:
    return (f'<div class="an-card an-kpi"><div class="k">{label}</div><div class="v">{value}<small>{unit}</small></div>'
            f'{mini_html}{call_html}</div>')


def insights_html(notes: list) -> str:
    return f'<div class="an-card an-note"><div class="tt">주요 인사이트 (데이터로 확인한 사실)</div>{ul(notes)}</div>'


# ---------------------------------------------------------------- 항목별 내용 (전체 요약 외 4개)
def build(name: str) -> dict:
    f, m = S["sex"]["여성"], S["sex"]["남성"]
    c = S["cls"]
    if name == "성별 분석":
        return dict(
            lead="성별에 따라 생존율이 얼마나 달랐는지 비교합니다.",
            kpis=kpis([("여성 생존율", pct(f["rate"])), ("남성 생존율", pct(m["rate"])), ("격차 (여성 − 남성)", pp(S["sex_gap"]))]),
            title="성별 생존율 (%)", sub="2개 집단 비교 · 생존자 / 해당 집단 승객 수",
            items=[item("여성", f, F_COL), item("남성", m, M_COL)],
            table=table(pd.DataFrame({"성별": ["여성", "남성"], "인원(명)": [num(f["n"]), num(m["n"])], "생존자(명)": [num(f["s"]), num(m["s"])],
                                      "생존율": [pct(f["rate"]), pct(m["rate"])]}), right=RIGHT),
            notes=[f"여성의 생존율은 {pct(f['rate'])}({num(f['s'])}명/{num(f['n'])}명), 남성은 {pct(m['rate'])}({num(m['s'])}명/{num(m['n'])}명)입니다.",
                   f"두 집단의 생존율 차이는 {pp(S['sex_gap'])}입니다.",
                   f"승객 수는 남성 {num(m['n'])}명, 여성 {num(f['n'])}명입니다."],
            basis="비교 기준: 여성 집단과 남성 집단의 생존율. 집단 간 차이를 보여줄 뿐 원인을 설명하지는 않습니다.",
        )
    if name == "등급 분석":
        up = c["1등석"]["rate"] > c["2등석"]["rate"] > c["3등석"]["rate"]
        return dict(
            lead="객실 등급에 따라 생존율이 얼마나 달랐는지 비교합니다.",
            kpis=kpis([(f"{k} 생존율", pct(c[k]["rate"])) for k in CLASSES]),
            title="객실 등급별 생존율 (%)", sub="3개 집단 비교 · 생존자 / 해당 집단 승객 수",
            items=[item(k, c[k], col) for k, col in zip(CLASSES, C_COLS)],
            table=table(pd.DataFrame({"객실 등급": CLASSES, "인원(명)": [num(c[k]["n"]) for k in CLASSES], "생존자(명)": [num(c[k]["s"]) for k in CLASSES],
                                      "생존율": [pct(c[k]["rate"]) for k in CLASSES]}), right=RIGHT),
            notes=[f"생존율은 1등석 {pct(c['1등석']['rate'])}, 2등석 {pct(c['2등석']['rate'])}, 3등석 {pct(c['3등석']['rate'])}입니다.",
                   "등급이 높을수록 생존율이 높습니다." if up else "등급과 생존율의 관계가 일정하지 않습니다.",
                   f"1등석과 3등석의 생존율 차이는 {pp(S['cls_gap'])}입니다."],
            basis="비교 기준: 1·2·3등석 집단의 생존율. 집단 간 차이를 보여줄 뿐 원인을 설명하지는 않습니다.",
        )
    if name == "복합 분석":
        hi, lo = max(ROWS, key=lambda r: r["rate"]), min(ROWS, key=lambda r: r["rate"])
        rate = {(r["sex"], r["cls"]): r for r in ROWS}
        all_f = all(rate[("여성", k)]["rate"] > rate[("남성", k)]["rate"] for k in CLASSES)
        gaps = ", ".join(f"{k} {pp(r1(rate[('여성', k)]['rate'] - rate[('남성', k)]['rate']))}" for k in CLASSES)
        pivot = pd.DataFrame({"성별": ["여성", "남성"], **{k: [cell(rate[(sx, k)]["s"], rate[(sx, k)]["n"]) for sx in ("여성", "남성")] for k in CLASSES}})
        return dict(
            lead="성별과 객실 등급을 함께 놓고 6개 집단의 생존율을 비교합니다.",
            kpis=kpis([("가장 높은 집단", f"{hi['sex']} {hi['cls']} {pct(hi['rate'])}"), ("가장 낮은 집단", f"{lo['sex']} {lo['cls']} {pct(lo['rate'])}"),
                       ("최고 − 최저", pp(r1(hi["rate"] - lo["rate"])))]),
            title="성별 · 객실 등급별 생존율 (%)", sub="6개 집단 비교 · 생존자 / 해당 집단 승객 수",
            items=[item(f"{r['sex']} {r['cls']}", r, F_COL if r["sex"] == "여성" else M_COL, low=r is lo) for r in ROWS],
            table=table(pivot, right=CLASSES),
            notes=[f"생존율이 가장 높은 집단은 {hi['sex']} {hi['cls']} {pct(hi['rate'])}({num(hi['s'])}명/{num(hi['n'])}명), 가장 낮은 집단은 {lo['sex']} {lo['cls']} {pct(lo['rate'])}({num(lo['s'])}명/{num(lo['n'])}명)입니다.",
                   ("모든 등급에서 여성의 생존율이 남성보다 높습니다." if all_f else "등급에 따라 여성과 남성의 생존율 순서가 다릅니다.") + f" (여성 − 남성: {gaps})",
                   "집단마다 인원 수가 다르므로 비율과 함께 인원 수를 확인해야 합니다."],
            basis="비교 기준: 성별 × 객실 등급의 6개 집단. 집단 간 차이를 보여줄 뿐 원인을 설명하지는 않습니다.",
        )
    # 탑승 항구 분석
    pd_, names = port_data(), port_names()
    label = lambda k: f"{k} ({names[k]})" if names.get(k) else k
    big = max(pd_, key=lambda k: pd_[k]["n"])
    cross = pd.DataFrame({"탑승 항구": [label(k) for k in "CQS"], "전체": [cell(pd_[k]["s"], pd_[k]["n"]) for k in "CQS"],
                          **{cl: [cell(*pd_[k]["cls"][cl]) for k in "CQS"] for cl in CLASSES}})
    return dict(
        lead="탑승 항구에 따라 생존율이 얼마나 달랐는지 비교합니다. 항구 × 객실 등급 표도 함께 봅니다.",
        kpis=kpis([(f"{label(k)} 생존율", pct(pd_[k]["rate"])) for k in "CQS"]),
        title="탑승 항구별 생존율 (%)", sub="3개 집단 비교 · 생존자 / 해당 집단 승객 수",
        items=[item(label(k), pd_[k], F_COL) for k in "CQS"],
        table=table(cross, right=("전체", *CLASSES)),
        notes=["항구별 생존율은 " + ", ".join(f"{label(k)} {pct(pd_[k]['rate'])}({num(pd_[k]['s'])}명/{num(pd_[k]['n'])}명)" for k in "CQS") + "입니다.",
               f"승객 수는 {label(big)}가 {num(pd_[big]['n'])}명으로 가장 많고, 항구마다 인원 수 차이가 큽니다.",
               "항구와 객실 등급을 함께 보면 칸마다 인원이 적은 집단이 있어, 비율은 인원 수와 함께 읽어야 합니다."],
        basis="비교 기준: 탑승 항구 3곳의 생존율. 집단 간 차이를 보여줄 뿐 원인을 설명하지는 않습니다.",
    )


# ---------------------------------------------------------------- 스타일 (이 페이지 전용)
st.html("""
<style>
  .st-key-tabs-band { border-bottom: 1px solid var(--line); }
  .st-key-an-body { background: var(--index); padding: 0 80px 48px; gap: 20px; }
  .an-card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; }
  .an-head { padding: 36px 0 32px; }
  .an-head .h { font-size: 34px; font-weight: 700; line-height: 1.85; color: #edf3f7; margin: 0; word-break: keep-all; }
  .an-head .h mark { background: #edf3f7; color: #061c29; border-radius: 10px; padding: 5px 14px; margin: 0 6px; }
  .an-head .s { font-size: 15px; line-height: 1.6; color: var(--t2); margin: 14px 0 0; }
  .an-head .eyebrow { font-family: "Playfair Display", serif; font-size: 12px; letter-spacing: 2px; color: var(--t2); margin-bottom: 8px; }

  .an-kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .an-kpi { padding: 24px; display: flex; flex-direction: column; gap: 14px; }
  .an-kpi .k { font-size: 13px; color: var(--t2); }
  .an-kpi .v { font-size: 42px; font-weight: 700; color: var(--white); letter-spacing: -2px; line-height: 1.2; font-variant-numeric: tabular-nums; }
  .an-kpi .v small { font-size: 20px; letter-spacing: -1px; margin-left: 2px; }
  .an-mini { display: flex; flex-direction: column; gap: 6px; }
  .an-mini > div { display: grid; grid-template-columns: 64px 1fr 40px; gap: 8px; align-items: center; font-size: 11px; color: var(--t1); }
  .an-mini .trk, .an-row .trk { background: var(--nav); border-radius: 4px; overflow: hidden; display: block; }
  .an-mini .trk { height: 8px; }
  .an-mini .trk i, .an-row .trk i { display: block; height: 100%; border-radius: 2px; }
  .an-mini b { text-align: right; color: var(--white); font-weight: 700; font-variant-numeric: tabular-nums; }
  .an-call { background: var(--nav); border: 1px solid var(--line); border-radius: 10px; padding: 20px; display: flex; gap: 12px; align-items: flex-start; }
  .an-call .no { flex: none; width: 28px; height: 28px; border-radius: 100px; background: #8fa9ba; color: #061c29; font-weight: 700; font-size: 13px;
                 display: flex; align-items: center; justify-content: center; }
  .an-call b { display: block; font-size: 14px; color: var(--white); margin-bottom: 5px; }
  .an-call p { margin: 0; font-size: 12px; line-height: 1.7; color: #8fa9ba; word-break: keep-all; }

  .an-chart { padding: 30px; display: flex; flex-direction: column; gap: 22px; }
  .an-chart .hd { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
  .an-chart .tt, .an-note .tt { font-size: 19px; font-weight: 700; color: var(--white); }
  .an-chart .sb { font-size: 13px; color: var(--t1); margin-top: 6px; }
  .an-chart .lg { display: flex; gap: 16px; font-size: 12px; color: var(--t1); }
  .an-chart .lg i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; }
  .an-row { display: grid; grid-template-columns: 80px 1fr 52px 90px 75px; gap: 12px; align-items: center; margin-bottom: 14px; }
  .an-row:last-child { margin-bottom: 0; }
  .an-row .n { font-size: 13px; color: var(--t1); }
  .an-row .trk { height: 22px; border-radius: 2px; }
  .an-row .v { text-align: right; font-size: 15px; color: var(--white); font-variant-numeric: tabular-nums; }
  .an-row .v.low { color: #ff8a58; }
  .an-row .c { text-align: right; font-size: 12px; color: #8fa9ba; white-space: nowrap; }
  .an-row .bd em { font-style: normal; font-size: 11px; font-weight: 700; color: #ff8a58; background: #3a2219; border-radius: 100px; padding: 3px 10px; white-space: nowrap; }
  .an-scale { display: flex; justify-content: space-between; font-size: 10px; color: var(--t2); margin: -8px 234px 0 92px; }

  .an-note { padding: 28px 30px; }
  .an-note .oa-ul { margin: 14px 0 0; padding-left: 20px; }
  .an-note .oa-ul li { font-size: 14px; line-height: 1.9; color: var(--t1); word-break: keep-all; }
  .an-cap { font-size: 13px; color: var(--t2); margin: 2px 0 0; }
  .an-table { padding: 26px 30px; }
  .an-table .tt { font-size: 16px; font-weight: 700; color: var(--white); margin-bottom: 14px; }
  .an-body-wrap .oa-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .an-body-wrap .oa-table th { text-align: left; color: var(--white); font-weight: 700; padding: 12px 18px; border-bottom: 1px solid var(--line); }
  .an-body-wrap .oa-table td { color: var(--t1); padding: 12px 18px; border-bottom: 1px solid var(--line); }
  .an-body-wrap .oa-table tr:last-child td { border-bottom: 0; }
  .an-body-wrap .oa-table .r { text-align: right; }
  .an-body-wrap .oa-kpi-w { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 0; }
  .an-body-wrap .oa-kpi-w > div { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 24px; }
  .an-body-wrap .oa-kpi-w .k { font-size: 13px; color: var(--t2); }
  .an-body-wrap .oa-kpi-w .v { font-size: 34px; font-weight: 700; color: var(--white); margin-top: 12px; letter-spacing: -1px; }

  /* 이전 · 다음 버튼: 외곽선 알약 */
  .st-key-an-nav [data-testid^="stBaseButton"] { background: transparent; border: 1px solid var(--t1); border-radius: 100px; padding: 10px 24px; }
  .st-key-an-nav [data-testid^="stBaseButton"], .st-key-an-nav [data-testid^="stBaseButton"] * { color: var(--white); font-weight: 700; font-size: 14px; }
  .st-key-an-nav [data-testid^="stBaseButton"]:hover { border-color: var(--white); background: rgba(255,255,255,.08); }
  .st-key-an-nav { padding-top: 8px; }

  @media (max-width: 900px) {
    .st-key-an-body { padding: 0 20px 40px; }
    .an-kpis, .an-body-wrap .oa-kpi-w { grid-template-columns: 1fr; }
    .an-head .h { font-size: 24px; }
    .an-row { grid-template-columns: 70px 1fr 48px; } .an-row .c, .an-row .bd { grid-column: 2 / -1; text-align: left; }
    .an-scale { margin: -8px 0 0 82px; }
  }
</style>
""")

# ---------------------------------------------------------------- 화면
masthead("FINAL ANALYSIS", "총분석", "주요 요인별 생존율을 비교하고, 성별과 객실 등급을 함께 살펴봅니다. <br class='nb'>"
         f"{num(S['total'])}명의 기록에서 관측한 차이를 한눈에 확인하세요.")

def go_item(delta: int) -> None:
    request_scroll_top()
    st.session_state["item"] = ITEMS[ITEMS.index(st.session_state["item"]) + delta]


idx = tabs_band(ITEMS, "item", "분석 항목")


def card_nav() -> None:
    with st.container(key="an-nav"):
        prev_col, next_col = st.columns(2)
        with prev_col:
            if idx == 0:
                if st.button("← 분석 방법 소개", key="prev_item"):
                    st.switch_page("views/method.py")
            else:
                st.button(f"← 이전: {ITEMS[idx - 1]}", key="prev_item", on_click=go_item, args=(-1,))
        with next_col:
            with st.container(key="next-wrap", horizontal=True, horizontal_alignment="right"):
                if idx == len(ITEMS) - 1:
                    if st.button("처음으로: 프로젝트 소개 →", key="next_item"):
                        st.switch_page("views/overview.py")
                else:
                    st.button(f"다음: {ITEMS[idx + 1]} →", key="next_item", on_click=go_item, args=(1,))


with st.container(key="an-body"):
    if idx == 0:
        f, m, cl = S["sex"]["여성"], S["sex"]["남성"], S["cls"]
        up = cl["1등석"]["rate"] > cl["2등석"]["rate"] > cl["3등석"]["rate"]
        hi, lo = max(ROWS, key=lambda r: r["rate"]), min(ROWS, key=lambda r: r["rate"])
        dead = S["total"] - S["alive"]
        k1 = kpi_card("전체 생존율", f"{S['rate']:.1f}", "%",
                      mini([(f"생존 {num(S['alive'])}명", S["rate"], F_COL), (f"사망 {num(dead)}명", r1(100 - S["rate"]), M_COL)]),
                      callout(1, f"전체 10명 중 {round(S['rate'] / 10)}명만 생존",
                              f"{num(S['total'])}명 중 {num(S['alive'])}명({pct(S['rate'])})이 살아남았습니다"))
        k2 = kpi_card("성별 격차", f"{S['sex_gap']:.1f}", "%p",
                      mini([("여성", f["rate"], F_COL), ("남성", m["rate"], M_COL)]),
                      callout(2, "성별 격차가 등급 격차보다 큼" if S["sex_gap"] > S["cls_gap"] else "등급 격차가 성별 격차보다 큼",
                              f"여성 생존율 {pct(f['rate'])}, 남성은 {pct(m['rate'])}"))
        k3 = kpi_card("등급 격차", f"{S['cls_gap']:.1f}", "%p",
                      mini([("1등석", cl["1등석"]["rate"], F_COL), ("3등석", cl["3등석"]["rate"], M_COL)]),
                      callout(3, "등급이 높을수록 생존율 상승" if up else "등급과 생존율의 관계가 일정하지 않음",
                              f"1등석 {pct(cl['1등석']['rate'])}, 3등석 {pct(cl['3등석']['rate'])}"))
        notes = [
            f"여성의 생존율({pct(f['rate'])})이 남성({pct(m['rate'])})보다 {pp(S['sex_gap'])} 높습니다.",
            ("객실 등급이 높을수록 생존율이 높았습니다. " if up else "객실 등급과 생존율의 관계가 일정하지 않았습니다. ")
            + f"1등석 {pct(cl['1등석']['rate'])}, 2등석 {pct(cl['2등석']['rate'])}, 3등석 {pct(cl['3등석']['rate'])}.",
            f"두 기준을 함께 보면 가장 높은 집단은 {hi['sex']} {hi['cls']}({pct(hi['rate'])}), 가장 낮은 집단은 {lo['sex']} {lo['cls']}({pct(lo['rate'])})입니다.",
        ]
        items = [item(f"{r['sex']} {r['cls']}", r, F_COL if r["sex"] == "여성" else M_COL, low=r is lo) for r in ROWS]
        st.html(f"""
<div class="an-body-wrap">
  <div class="an-head">
    <div class="eyebrow">ANALYSIS 01</div>
    <p class="h"><mark>여성</mark>이거나 <mark>객실 등급이 높을수록</mark> 생존율이 올라갔다.</p>
    <p class="s">승객 그룹별 생존율을 비교해, 가장 큰 차이를 만든 요인을 한눈에 보여줍니다.</p>
  </div>
  <div class="an-kpis">{k1}{k2}{k3}</div>
  <div style="height:20px"></div>
  {bars_card("성별 · 객실 등급별 생존율 (%)", "6개 집단 비교 · 생존자 / 해당 집단 승객 수", items)}
  <div style="height:20px"></div>
  {insights_html(notes)}
</div>""")
    else:
        c = build(ITEMS[idx])
        st.html(f"""
<div class="an-body-wrap">
  <div class="an-head">
    <div class="eyebrow">ANALYSIS {idx + 1:02d}</div>
    <p class="h">{ITEMS[idx]}</p>
    <p class="s">{c['lead']}</p>
    <p class="an-cap" style="margin-top:10px">{c['basis']}</p>
  </div>
  {c['kpis']}
  <div style="height:20px"></div>
  {bars_card(c['title'], c['sub'], c['items'], legend=False)}
  <div style="height:20px"></div>
  <div class="an-card an-table"><div class="tt">데이터 표</div>{c['table']}</div>
  <div style="height:20px"></div>
  {insights_html(c['notes'])}
</div>""")
    card_nav()

scroll_top_if_requested()
site_footer()
