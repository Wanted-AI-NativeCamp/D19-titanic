import os

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("data/titanic_clean.csv")
os.makedirs("chart", exist_ok=True)

# 차트 제목 (아직 비워둠 - 고른 문장을 여기에 넣는다)
TITLES = {
    1: "",
    2: "",
    3: "",
    4: "",
}

CLASS_NAMES = {1: "1등석", 2: "2등석", 3: "3등석"}
df["등급"] = df["Pclass"].map(CLASS_NAMES)
df["성별"] = df["Sex"].map({"male": "남성", "female": "여성"})
ORDER = ["1등석", "2등석", "3등석"]


def save(fig, number, name, title):
    fig.update_layout(title_text=title, template="plotly_white", font=dict(size=14))
    path = f"chart/{number}_{name}.html"
    fig.write_html(path, include_plotlyjs="cdn")
    print("저장:", path)


# 1. 등급별 생존율 막대 (막대 위: 생존율과 인원수)
g = df.groupby("등급")["Survived"].agg(["mean", "sum", "size"]).reindex(ORDER)
fig1 = go.Figure(go.Bar(
    x=g.index,
    y=g["mean"] * 100,
    text=[f"{m * 100:.1f}%<br>({int(s)}/{int(n)}명)" for m, s, n in zip(g["mean"], g["sum"], g["size"])],
    textposition="outside",
    marker_color="#4C78A8",
))
fig1.update_layout(xaxis_title="객실 등급", yaxis_title="생존율 (%)",
                   yaxis=dict(range=[0, 80], ticksuffix="%"))
save(fig1, 1, "등급별_생존율", TITLES[1])

# 2. 성별 × 등급 생존율 묶음 막대
g2 = df.groupby(["성별", "등급"])["Survived"].agg(["mean", "size"]).reset_index()
fig2 = go.Figure()
for sex, color in [("남성", "#4C78A8"), ("여성", "#E45756")]:
    d = g2[g2["성별"] == sex].set_index("등급").reindex(ORDER)
    fig2.add_trace(go.Bar(
        name=sex,
        x=d.index,
        y=d["mean"] * 100,
        text=[f"{m * 100:.1f}%<br>({int(n)}명)" for m, n in zip(d["mean"], d["size"])],
        textposition="outside",
        marker_color=color,
    ))
fig2.update_layout(barmode="group", xaxis_title="객실 등급", yaxis_title="생존율 (%)",
                   yaxis=dict(range=[0, 115], ticksuffix="%"), legend_title_text="성별")
save(fig2, 2, "성별_등급별_생존율", TITLES[2])

# 3. 나이 분포 히스토그램: 위 = 원본(빈칸 제외), 아래 = 전체 중앙값으로 채운 버전
# (titanic_clean.csv의 Age는 호칭별로 채워져 있으므로, age_missing으로 원래 값만 골라 사용)
original = df.loc[df["age_missing"] == 0, "Age"]
overall_median = original.median()
filled = df["Age"].where(df["age_missing"] == 0, overall_median)

bins = dict(start=0, end=80, size=5)
fig3 = make_subplots(
    rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
    subplot_titles=(f"원본 (빈칸 제외, {len(original)}명)",
                    f"전체 중앙값({overall_median:g}세)으로 채움 ({len(filled)}명)"),
)
fig3.add_trace(go.Histogram(x=original, xbins=bins, marker_color="#4C78A8", showlegend=False), row=1, col=1)
fig3.add_trace(go.Histogram(x=filled, xbins=bins, marker_color="#F58518", showlegend=False), row=2, col=1)
fig3.update_xaxes(title_text="나이 (세)", row=2, col=1)
fig3.update_yaxes(title_text="인원수 (명)", range=[0, 300], row=1, col=1)
fig3.update_yaxes(title_text="인원수 (명)", range=[0, 300], row=2, col=1)
save(fig3, 3, "나이분포_원본vs중앙값", TITLES[3])

# 4. 등급별 운임 박스 차트
fig4 = go.Figure()
for cls, color in zip(ORDER, ["#4C78A8", "#F58518", "#54A24B"]):
    fig4.add_trace(go.Box(y=df.loc[df["등급"] == cls, "Fare"], name=cls,
                          marker_color=color, boxmean=False, showlegend=False))
fig4.update_layout(xaxis_title="객실 등급", yaxis_title="운임 (파운드)")
save(fig4, 4, "등급별_운임", TITLES[4])
