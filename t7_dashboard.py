"""t7_dashboard.py
data/titanic_clean.csv 를 읽어서 대시보드 홈 화면(index_final.html)을 만든다.
- 숫자(비율, 인원수, 격차, 결론 문장)는 전부 이 파일이 CSV에서 센 값으로 채운다.
- 디자인(라벤더 톤, 카드 안의 카드, 가로 막대)은 TEMPLATE 안의 CSS에 들어 있다.
실행:  python t7_dashboard.py   ->  index_final.html 을 브라우저로 열기
"""
import json
import pandas as pd

# 1) 데이터 읽기, 그룹별로 세기 (인원수 = 분모, 생존자수 = 분자)
df = pd.read_csv("data/titanic_clean.csv")
df["성별"] = df["Sex"].map({"male": "남성", "female": "여성"})
df["등급"] = df["Pclass"].astype(str) + "등석"

g = df.groupby(["성별", "등급"])["Survived"].agg(n="size", s="sum").reset_index()
rows = []
for sex in ["여성", "남성"]:                      # 화면 순서: 여성 -> 남성
    for r in g[g["성별"] == sex].sort_values("등급").itertuples():
        rows.append({"sex": sex, "cls": r.등급, "n": int(r.n), "s": int(r.s)})

# 2) 검산: 그룹을 다 더하면 전체 행수/생존자수와 같아야 한다
assert sum(r["n"] for r in rows) == len(df)
assert sum(r["s"] for r in rows) == int(df["Survived"].sum())

TEMPLATE = r'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>타이타닉 생존 분석</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap">
<style>
  /* 색은 여기 변수만 쓴다. 라벤더 톤, 카드 안의 카드, 인디고 강조 */
  :root{
    --ink:#10233a; --ink-muted:#4b5b6b; --hairline:#d9d4c7;
    --surface:#ffffff; --indigo:#4f46e5; --indigo-soft:#eef0ff; --indigo-mid:#9a96f0;
    --alert:#b93c0a; --alert-soft:#fdece3; --wash-top:#f1f1ff; --wash-bottom:#fcfcff;
    --shadow:0 8px 32px rgba(79,70,229,.08);
    --font:"Noto Sans KR",system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    color-scheme:light;
  }
  *{box-sizing:border-box}
  h1,.sub,.row span,.s{word-break:keep-all}
  body{margin:0;font-family:var(--font);color:var(--ink);
    background:radial-gradient(520px 260px at 8% 12%,rgba(255,238,220,.7),transparent 70%),linear-gradient(180deg,var(--wash-top) 0%,var(--wash-bottom) 55%,var(--surface) 100%) fixed,var(--wash-bottom);
    padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  nav{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;max-width:1120px;margin:0 auto;padding-block:16px}
  .logo{font-size:20px;font-weight:800;letter-spacing:-.02em}
  .logo b{color:var(--indigo)}
  .pill{display:inline-block;font-size:12px;font-weight:700;line-height:18px;padding:2px 10px;border-radius:999px;background:var(--indigo-soft);color:var(--indigo)}
  .pill.warn{background:var(--alert-soft);color:var(--alert)}
  main{max-width:1120px;margin:0 auto;padding-bottom:32px;display:flex;flex-direction:column;gap:16px}
  .hero{text-align:left;padding-top:16px}
  h1{margin:0;font-size:clamp(28px,4.4vw,44px);line-height:1.3;font-weight:800;letter-spacing:-.02em;text-wrap:balance}
  .hl{background:var(--indigo);color:#fff;padding:0 .4em;border-radius:999px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
  .sub{margin:10px 0 0;font-size:16px;line-height:24px}
  .pair{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:8px}
  .panel{background:var(--surface);border-radius:28px;box-shadow:var(--shadow)}

  /* 바깥 카드(.c3) 안에 지표 카드(.k) + 결론(.cc) */
  .c3{display:flex;flex-direction:column;gap:12px;min-width:0;background:var(--surface);border-radius:28px;box-shadow:var(--shadow);padding:14px}
  .c3 .k{flex:1;border-radius:20px;background:var(--wash-top);padding:22px 28px;display:flex;flex-direction:column;justify-content:center;min-width:0;min-height:116px}
  .k .l{font-size:14px;font-weight:700;color:var(--ink-muted)}
  .k .n{font-size:44px;line-height:1.1;font-weight:800;margin:2px 0;font-variant-numeric:tabular-nums}
  .cmp{display:grid;gap:6px;margin-top:10px}
  .cr{display:grid;grid-template-columns:72px 1fr 48px;align-items:center;gap:8px;font-size:13px;color:var(--ink-muted)}
  .ct{height:14px;background:var(--surface);border-radius:7px;overflow:hidden}
  .cb{display:block;height:100%;border-radius:7px;background:var(--indigo)}
  .cb.lo{background:var(--indigo-mid)}
  .cv{font-weight:800;color:var(--ink);text-align:right;font-variant-numeric:tabular-nums}
  .hrow{display:flex;align-items:center;justify-content:space-between;gap:12px}
  .donut{width:84px;height:84px;flex:none;transform:rotate(-90deg)}
  .donut circle{fill:none;stroke-width:14}
  .dt{stroke:var(--surface)} .dv{stroke:var(--indigo)}
  .lg{display:flex;gap:12px;flex-wrap:nowrap;font-size:12px;color:var(--ink-muted);margin-top:8px}
  .lg span{white-space:nowrap}
  .lg i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:-1px}
  .cc{padding:8px 8px 6px}
  .row{display:flex;gap:14px;align-items:flex-start;font-size:15px;line-height:22px;color:var(--ink-muted);font-weight:500}
  .row i{flex:none;width:28px;height:28px;border-radius:10px;background:var(--indigo-soft);color:var(--indigo);font-style:normal;font-size:15px;font-weight:800;display:grid;place-items:center}
  .row b{display:block;color:var(--ink);font-weight:800;font-size:17px;line-height:24px}
  .row em{font-style:normal}

  /* 가로 막대 차트 */
  .chart{padding:24px 32px 18px}
  .ch h2{margin:0 0 12px;font-size:18px;font-weight:800}
  .hr{display:grid;grid-template-columns:112px 1fr 188px 64px;align-items:center;gap:14px;padding:7px 0}
  .hn{font-size:15px;font-weight:700;color:var(--ink)}
  .hn span{font-weight:500;color:var(--ink-muted);margin-left:6px}
  .tr{height:22px;background:var(--indigo-soft);border-radius:11px;overflow:hidden}
  .br{height:100%;background:var(--indigo);border-radius:11px}
  .br.low{background:var(--alert)}
  .hv{font-size:15px;font-weight:800;font-variant-numeric:tabular-nums;white-space:nowrap}
  .hv small{font-size:13px;font-weight:500;color:var(--ink-muted);margin-left:4px}
  .hv.low{color:var(--alert)}
  .tg{text-align:right;white-space:nowrap}
  .foot{text-align:center;font-size:12px;color:var(--ink-muted)}
  @media (max-width:760px){
    .hr{grid-template-columns:1fr auto auto}
    .tg:empty{display:none}
    .hr .tr{grid-column:1/-1;order:3}
    .pair{grid-template-columns:1fr}
    .chart{padding:20px 16px 14px}
  }
</style>
</head>
<body>
<nav><span class="logo">Titanic<b>.</b>Dashboard</span><span class="pill" id="note"></span></nav>
<main>
  <section class="hero">
    <h1 id="h1"></h1>
    <p class="sub">승객 그룹별 생존율을 비교해, 가장 큰 차이를 만든 요인을 한눈에 보여줍니다</p>
  </section>

  <section class="pair" aria-label="핵심 숫자와 결론">
    <div class="c3">
      <div class="k"><div class="l">전체 생존율</div>
        <div class="hrow"><div class="n" id="k1n"></div>
          <svg class="donut" id="donut" viewBox="0 0 100 100" role="img"><circle class="dt" cx="50" cy="50" r="40"/><circle class="dv" id="donut-v" cx="50" cy="50" r="40"/></svg></div>
        <div class="lg"><span><i style="background:var(--indigo)"></i><span id="lg1"></span></span><span><i style="background:var(--surface);box-shadow:inset 0 0 0 1.5px var(--indigo-mid)"></i><span id="lg2"></span></span></div></div>
      <div class="cc"><div class="row"><i>1</i><span><b id="c1h"></b><em id="c1t"></em></span></div></div>
    </div>
    <div class="c3">
      <div class="k"><div class="l">성별 격차</div><div class="n" id="k2n"></div><div class="cmp" id="cmp2"></div></div>
      <div class="cc"><div class="row"><i>2</i><span><b id="c2h"></b><em id="c2t"></em></span></div></div>
    </div>
    <div class="c3">
      <div class="k"><div class="l">등급 격차</div><div class="n" id="k3n"></div><div class="cmp" id="cmp3"></div></div>
      <div class="cc"><div class="row"><i>3</i><span><b id="c3h"></b><em id="c3t"></em></span></div></div>
    </div>
  </section>

  <section class="panel chart" aria-label="성별 · 객실 등급별 생존율">
    <div class="ch"><h2>성별 · 객실 등급별 생존율 (%)</h2></div>
    <div id="plot"></div>
  </section>
  <p class="foot">data/titanic_clean.csv 기준 (결측치 처리 후 891명) · t7_dashboard.py 가 계산</p>
</main>

<script>
  // 아래 d 는 t7_dashboard.py 가 CSV에서 센 값: n = 승객 수(분모), s = 생존자 수
  const d = __DATA__;

  const sum = (rows, k) => rows.reduce((a, r) => a + r[k], 0);
  const rate = (rows) => sum(rows, 's') / sum(rows, 'n') * 100;
  const r1 = (v) => Math.round(v * 10) / 10;
  const pct = (v) => v.toFixed(1) + '%';
  const num = (v) => v.toLocaleString('ko-KR');
  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, t) => { const e = document.createElement(tag); if (cls) e.className = cls; if (t !== undefined) e.textContent = t; return e; };

  // ---- 계산 ----
  const total = sum(d, 'n'), alive = sum(d, 's'), dead = total - alive;
  const by = (k, v) => d.filter((r) => r[k] === v);
  const allRate = r1(rate(d));
  const female = r1(rate(by('sex', '여성'))), male = r1(rate(by('sex', '남성')));
  const c1 = r1(rate(by('cls', '1등석'))), c2 = r1(rate(by('cls', '2등석'))), c3 = r1(rate(by('cls', '3등석')));
  const sexGap = r1(female - male), clsGap = r1(c1 - c3);          // 화면에 보이는 값끼리 뺀다
  const bars = d.map((r) => ({ ...r, rate: r1(r.s / r.n * 100) }));
  const low = bars.reduce((a, b) => (b.rate < a.rate ? b : a));
  const rateOf = (sx, c) => bars.find((b) => b.sex === sx && b.cls === c).rate;
  const classes = ['1등석', '2등석', '3등석'];

  // 큰 제목은 데이터가 뒷받침할 때만 쓴다
  const femaleHigher = classes.every((c) => rateOf('여성', c) > rateOf('남성', c));
  const classUp = c1 > c2 && c2 > c3;

  // ---- 머리글 ----
  $('note').textContent = `실제 데이터 · 탑승객 ${num(total)}명`;
  $('h1').innerHTML = (femaleHigher && classUp)
    ? '타이타닉 생존 분석,<br><span class="hl">여성</span>이거나 <span class="hl">객실 등급이 높을수록</span> 생존율이 올라갔다.'
    : '타이타닉 생존 분석,<br>성별과 객실 등급에 따라 생존율이 달랐다.';

  // ---- 1열: 전체 생존율 ----
  $('k1n').textContent = pct(allRate);
  const circ = 2 * Math.PI * 40;
  $('donut-v').setAttribute('stroke-dasharray', `${(allRate / 100 * circ).toFixed(1)} ${circ.toFixed(1)}`);
  $('donut').setAttribute('aria-label', `생존 ${pct(allRate)}, 사망 ${pct(r1(100 - allRate))}`);
  $('lg1').textContent = `생존 ${num(alive)}명 (${pct(allRate)})`;
  $('lg2').textContent = `사망 ${num(dead)}명 (${pct(r1(dead / total * 100))})`;
  const tenth = Math.round(allRate / 10);
  $('c1h').textContent = `전체 10명 중 ${tenth}명${tenth <= 5 ? '만' : ''} 생존`;
  $('c1t').textContent = `${num(total)}명 중 ${num(alive)}명(${pct(allRate)})이 살아남았습니다`;

  // ---- 2, 3열: 비교 막대 ----
  const cmp = (id, a, b) => {
    a.forEach((_, i) => {});
    [a, b].forEach((x, i) => {
      const row = el('div', 'cr');
      const t = el('span', 'ct'); const bar = el('span', 'cb' + (i ? ' lo' : '')); bar.style.width = x[1] + '%'; t.appendChild(bar);
      row.append(el('span', '', x[0]), t, el('span', 'cv', pct(x[1])));
      $(id).appendChild(row);
    });
  };
  $('k2n').textContent = pct(sexGap);  cmp('cmp2', ['여성', female], ['남성', male]);
  $('k3n').textContent = pct(clsGap);  cmp('cmp3', ['1등석', c1], ['3등석', c3]);
  $('c2h').textContent = sexGap >= clsGap ? '성별이 가장 큰 변수' : '성별 격차는 등급 격차보다 작다';
  $('c2t').textContent = `여성 생존율 ${pct(female)}, 남성은 ${pct(male)}`;
  $('c3h').textContent = classUp ? '등급이 높을수록 생존율 상승' : '등급과 생존율의 관계가 일정하지 않다';
  $('c3t').textContent = `1등석 ${pct(c1)}, 3등석 ${pct(c3)}`;

  // ---- 가로 막대 차트 (가로축 0~100%, 0에서 시작) ----
  bars.forEach((b) => {
    const isLow = b === low;
    const row = el('div', 'hr');
    const hn = el('div', 'hn', b.sex); hn.appendChild(el('span', '', b.cls));
    const tr = el('div', 'tr'); const br = el('div', 'br' + (isLow ? ' low' : '')); br.style.width = b.rate + '%'; tr.appendChild(br);
    const hv = el('div', 'hv' + (isLow ? ' low' : ''), pct(b.rate)); hv.appendChild(el('small', '', `(${num(b.s)}명/${num(b.n)}명)`));
    const tg = el('div', 'tg'); if (isLow) tg.appendChild(el('span', 'pill warn', '가장 낮음'));
    row.append(hn, tr, hv, tg);
    $('plot').appendChild(row);
  });
</script>
</body>
</html>
'''

html = TEMPLATE.replace("__DATA__", json.dumps(rows, ensure_ascii=False))
with open("index_final.html", "w", encoding="utf-8") as f:
    f.write(html)

# 3) 결과 확인용 출력
print("전체:", len(df), "명 중", int(df["Survived"].sum()), "명 생존")
for r in rows:
    print(f'{r["sex"]} {r["cls"]}: {r["s"]/r["n"]*100:.1f}% ({r["s"]}명/{r["n"]}명)')
print("저장 완료: index_final.html")
