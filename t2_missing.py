import pandas as pd

# 1) 파일 읽기 (아무것도 고치지 않고 있는 그대로 읽는다)
df = pd.read_csv("data/titanic.csv")
total = len(df)

# 2) "빈 값"을 뜻하는 표시들
#    - 진짜 비어 있는 칸(NaN)은 pandas가 알아서 찾아준다.
#    - 문자로 적힌 표시("-", "없음" 등)는 우리가 목록으로 직접 찾는다.
TEXT_MARKS = ["NaN", "nan", "-", "없음", ""]
NUMBER_MARKS = [0, 999]  # 0, 999는 진짜 값일 수도 있으니 '의심'으로만 센다

# 3) 칸마다 결측 개수 세기
missing_rows = []
for col in df.columns:
    nan_count = df[col].isna().sum()                       # 진짜 빈 칸
    text_count = df[col].isin(TEXT_MARKS).sum()            # 문자 표시("-" 등)
    missing_total = nan_count + text_count
    # 숫자 칸에서만 0, 999가 몇 개인지 따로 센다 (결측으로 합치지 않음)
    if pd.api.types.is_numeric_dtype(df[col]):
        suspect = df[col].isin(NUMBER_MARKS).sum()
    else:
        suspect = 0
    missing_rows.append({
        "칸": col,
        "결측 개수": missing_total,
        "결측 비율(%)": round(missing_total / total * 100, 1),
        "(참고)0 또는 999 개수": suspect,
    })

# 4) 표로 만들고 결측이 많은 순서로 정렬
table = pd.DataFrame(missing_rows).sort_values("결측 개수", ascending=False)

print("=" * 60)
print(f"1. 칸별 결측 개수와 비율 (전체 {total}행)")
print("=" * 60)
print(table.to_string(index=False))

# 5) 결측이 있는 칸마다 비어있는 행 3개씩 보기
print()
print("=" * 60)
print("2. 결측이 있는 칸별 비어있는 행 3개씩")
print("=" * 60)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)
for col in table[table["결측 개수"] > 0]["칸"]:
    is_empty = df[col].isna() | df[col].isin(TEXT_MARKS)  # 빈 칸이거나 "-" 등인 행
    print(f"\n[{col}] 비어있는 행 예시")
    print(df[is_empty].head(3))
