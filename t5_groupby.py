import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

df = pd.read_csv("data/titanic_clean.csv")

# 성별을 한글로 (보기 편하게)
df["Sex"] = df["Sex"].map({"male": "남성", "female": "여성"})


def one_way(col, title):
    """칸 하나로 묶어서 인원수, 생존자수, 생존율을 보여준다."""
    g = df.groupby(col)["Survived"].agg(인원수="size", 생존자수="sum", 생존율="mean")
    g["생존율(%)"] = (g["생존율"] * 100).round(1)
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(g[["인원수", "생존자수", "생존율(%)"]])
    print()


def two_way(row, col, title):
    """칸 두 개로 묶어서 '생존율% (인원수명)' 형태의 표를 만든다."""
    g = df.groupby([row, col])["Survived"].agg(["mean", "size"])
    text = g.apply(lambda r: f"{r['mean'] * 100:.1f}% ({int(r['size'])}명)", axis=1)
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(text.unstack())
    print()


one_way("Sex", "1. 성별 생존율과 인원수")
one_way("Pclass", "2. 객실 등급별 생존율과 인원수")
two_way("Sex", "Pclass", "3. 성별 × 등급 생존율 (인원수)")
one_way("Embarked", "4. 탑승 항구별 생존율과 인원수")
two_way("Embarked", "Pclass", "5. 항구 × 등급 생존율 (인원수)")
