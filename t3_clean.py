import pandas as pd

# 1) 원본 읽기
df = pd.read_csv("data/titanic.csv")
before = df.copy()  # 정제 전 상태를 따로 보관 (나중에 비교용)

# 2) Age: 호칭별 중앙값으로 채우기
df["age_missing"] = df["Age"].isna().astype(int)  # 채우기 전에 먼저 표시 (1 = 원래 비어있음)

df["Title"] = df["Name"].str.extract(r", ([^.]+)\.")[0]  # 이름에서 호칭 뽑기
title_map = {"Mr": "Mr", "Mrs": "Mrs", "Miss": "Miss", "Master": "Master",
             "Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"}
df["Title"] = df["Title"].map(title_map).fillna("Other")  # 그 외 드문 호칭은 Other

title_median = df.groupby("Title")["Age"].transform("median")  # 호칭별 중앙값 (빈 나이는 계산에서 제외됨)
df["Age"] = df["Age"].fillna(title_median)

# 3) Cabin: 있음/없음 칸 만들기 (원본 Cabin은 그대로 유지)
df["has_cabin"] = df["Cabin"].notna().astype(int)  # 1 = 객실 번호 있음, 0 = 없음

# 4) Embarked: S로 채우기
filled_ids = df.loc[df["Embarked"].isna(), "PassengerId"].tolist()
df["Embarked"] = df["Embarked"].fillna("S")
print(f"Embarked를 S로 채운 승객 번호: {filled_ids}")

# 5) 정제 전후 비교
print()
print("정제 전후 행수:", len(before), "->", len(df))
compare = pd.DataFrame({
    "정제 전 결측": before.isna().sum(),
    "정제 후 결측": df.isna().sum(),
}).fillna(0).astype(int)
print(compare)
print()
print("추가된 칸:", [c for c in df.columns if c not in before.columns])

# 6) 저장 (원본 titanic.csv는 건드리지 않고 새 파일로)
df.to_csv("data/titanic_clean.csv", index=False)
print("저장 완료: data/titanic_clean.csv")
