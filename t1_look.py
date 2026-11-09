import pandas as pd

# 데이터 불러오기
df = pd.read_csv("data/titanic.csv")

# 1. 몇 행, 몇 칸인지
print("=" * 50)
print("1. 데이터 크기")
print("=" * 50)
rows, cols = df.shape
print(f"행(승객 수): {rows}개, 칸(항목 수): {cols}개")

# 2. 위 5줄
print()
print("=" * 50)
print("2. 맨 위 5줄")
print("=" * 50)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)
print(df.head())

# 3. 필드명 설명
print()
print("=" * 50)
print("3. 각 필드(칸 이름)의 의미")
print("=" * 50)
descriptions = {
    "PassengerId": "승객 번호 (1부터 순서대로 붙인 고유 번호)",
    "Survived": "생존 여부 (0 = 사망, 1 = 생존)",
    "Pclass": "객실 등급 (1 = 1등석, 2 = 2등석, 3 = 3등석)",
    "Name": "승객 이름",
    "Sex": "성별 (male = 남성, female = 여성)",
    "Age": "나이",
    "SibSp": "함께 탄 형제자매/배우자 수",
    "Parch": "함께 탄 부모/자녀 수",
    "Ticket": "티켓 번호",
    "Fare": "요금 (티켓 가격)",
    "Cabin": "객실 번호",
    "Embarked": "탑승한 항구 (C = 셰르부르, Q = 퀸스타운, S = 사우샘프턴)",
}
for col in df.columns:
    print(f"- {col}: {descriptions.get(col, '(설명 없음)')}")

# 4. 각 칸마다 비어있지 않은 개수와 자료형
print()
print("=" * 50)
print("4. 칸별 채워진 개수와 자료형")
print("=" * 50)
info = pd.DataFrame({
    "비어있지 않은 개수": df.notna().sum(),
    "비어있는 개수": df.isna().sum(),
    "자료형": df.dtypes,
})
print(info)
