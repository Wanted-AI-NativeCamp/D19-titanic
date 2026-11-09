import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

# 원본에서 시작 (t3_clean.py 결과가 아니라 결측이 그대로 있는 데이터)
raw = pd.read_csv("data/titanic.csv")

# 호칭 뽑기 (방법 3에서 사용)
title = raw["Name"].str.extract(r", ([^.]+)\.")[0]
title_map = {"Mr": "Mr", "Mrs": "Mrs", "Miss": "Miss", "Master": "Master",
             "Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"}
raw["Title"] = title.map(title_map).fillna("Other")

# 처리 방법 4가지: 각각 Age가 다르게 처리된 표를 만든다
methods = {}
methods["1.지우기"] = raw.dropna(subset=["Age"]).copy()

m2 = raw.copy()
m2["Age"] = m2["Age"].fillna(raw["Age"].median())
methods["2.전체중앙값"] = m2

m3 = raw.copy()
m3["Age"] = m3["Age"].fillna(raw.groupby("Title")["Age"].transform("median"))
methods["3.호칭별중앙값"] = m3

m4 = raw.copy()
m4["Age"] = m4["Age"].fillna(0)
methods["4.0으로채움"] = m4

# 나이대 나누기 (왼쪽 포함, 오른쪽 미포함: 12.5세는 어린이로 본다)
bins = [0, 13, 20, 40, 60, float("inf")]
labels = ["어린이(0~12)", "10대(13~19)", "청년(20~39)", "중년(40~59)", "노년(60+)"]

rate_tables = []
count_tables = []
for name, d in methods.items():
    d["나이대"] = pd.cut(d["Age"], bins=bins, labels=labels, right=False)
    g = d.groupby("나이대", observed=False)["Survived"]
    rate_tables.append((g.mean() * 100).round(1).rename(name))
    count_tables.append(g.size().rename(name))

rates = pd.concat(rate_tables, axis=1)
counts = pd.concat(count_tables, axis=1)

print("=" * 70)
print("1. 나이대별 인원 수 (명)")
print("=" * 70)
print(counts)
print("합계:", counts.sum().to_dict())

print()
print("=" * 70)
print("2. 나이대별 생존율 (%)")
print("=" * 70)
print(rates)

# 방법 1(지우기)과 비교해서 얼마나 달라졌는지 (%p)
print()
print("=" * 70)
print("3. 방법 1(지우기) 대비 생존율 차이 (%p)")
print("=" * 70)
diff = rates.sub(rates["1.지우기"], axis=0).drop(columns="1.지우기").round(1)
print(diff)

# 가장 크게 달라진 칸
biggest = diff.abs().stack().idxmax()
print()
print(f"가장 크게 달라진 칸: {biggest[0]} / {biggest[1]} "
      f"(차이 {diff.loc[biggest]:+.1f}%p)")
print(f"  -> 지우기 {rates.loc[biggest[0], '1.지우기']}%, "
      f"{biggest[1]} {rates.loc[biggest[0], biggest[1]]}%")
