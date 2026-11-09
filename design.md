# Titanic Dashboard 디자인 시스템

`index_final.html`의 현재 디자인을 다른 곳에서도 그대로 쓸 수 있게 정리한 문서예요.
색은 CSS 변수(토큰)만 쓰고, 라이트/다크는 변수 값만 바꿔서 전환해요.

---

## 1. 원칙

1. **인디고 하나로 강조한다.** 강조는 인디고, "주의/가장 낮음"만 오렌지.
2. **채움색과 글자색을 나눈다.** 밝은 인디고·오렌지는 막대·배지 배경에만 쓰고, 글자는 `*-text` 토큰을 쓴다.
3. **카드 안의 카드.** 바깥 카드(`--surface`) 안에 지표 카드(`--wash-top`)를 넣어 깊이를 만든다. 테두리 대신 부드러운 그림자.
4. **색은 변수로만.** 컴포넌트에 hex를 직접 쓰지 않는다. (예외: 아래 "알려진 예외")
5. **둥글게.** 막대·배지·버튼은 끝이 둥근 형태(pill), 카드는 큰 라운드.

---

## 2. 색상 토큰

### 채움 (두 모드 공통)

| 토큰 | 값 | 용도 |
|---|---|---|
| `--indigo` | `#8c9eff` | 메인 강조: 막대, 강조 배지(`.hl`) 배경, 범례 점, 포커스 링 |
| `--alert` | `#ff8a5c` | "가장 낮음" 막대 |

### 글자

| 토큰 | 라이트 | 다크 | 용도 |
|---|---|---|---|
| `--indigo-text` | `#3f51b5` | `#8c9eff` | 배지·아이콘 칩 글자 |
| `--alert-text` | `#b93c0a` | `#ff8a5c` | 경고 수치, 경고 배지 글자 |
| `--ink` | `#10233a` | `#e8eaf6` | 본문·제목·수치 |
| `--ink-muted` | `#4b5b6b` | `#a4abc8` | 보조 글자, 라벨 |
| `--on-indigo` | `#ffffff` | `#0f1226` | 인디고 채움 위 글자 (`.hl`) |

### 면·보조

| 토큰 | 라이트 | 다크 | 용도 |
|---|---|---|---|
| `--surface` | `#ffffff` | `#171b33` | 바깥 카드, 패널, 버튼 배경 |
| `--wash-top` | `#eff1fb` | `#1d2240` | 지표 카드(`.k`), 배경 그라데이션 위 |
| `--wash-bottom` | `#fbfcff` | `#0f1226` | 배경 그라데이션 아래 |
| `--indigo-soft` | `#e8eaf6` | `#252b55` | 막대 트랙, 배지·아이콘 칩 배경 |
| `--indigo-mid` | `#7e8fe8` | `#5c6bc0` | 보조 막대(`.cb.lo`), 버튼 호버 테두리, 범례 링 |
| `--alert-soft` | `#fdece3` | `#3a2219` | 경고 배지 배경 |
| `--hairline` | `#d5d9ec` | `#2f3556` | 버튼 테두리 |
| `--shadow` | `0 8px 32px rgba(140,158,255,.18)` | `0 8px 32px rgba(0,0,0,.40)` | 카드 그림자 |
| `--glow` | `rgba(140,158,255,.14)` | `rgba(140,158,255,.12)` | 배경 왼쪽 위 은은한 빛 |

### 막대 농도 규칙
차트 행은 위에서 아래로 갈수록 연해진다: 맨 위 `--indigo` 100% → 맨 아래 40%.
`color-mix(in srgb, var(--indigo) N%, var(--indigo-soft))`로 만들고, 가장 낮은 행만 `--alert`.

---

## 3. 타이포그래피

폰트는 두 가지예요.
- 본문 `--font`: **Pretendard Variable** (jsDelivr CDN) → Pretendard → Noto Sans KR → 시스템 폰트
- 로고 `--font-logo`: **Bebas Neue** (Google Fonts) → Impact → Arial Narrow. 굵기가 400 하나뿐이고 대문자 전용이라, 로고 글자는 `TITANIC`처럼 대문자로 쓴다.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
```

| 역할 | 크기 / 줄 높이 | 굵기 |
|---|---|---|
| 제목 `h1` | `clamp(28px, 4.4vw, 44px)` / 1.3, 자간 -.02em | 800 |
| 큰 수치 `.n` | 44px / 1.1, 숫자 고정폭(`tabular-nums`) | 800 |
| 차트 제목 `h2` | 18px | 800 |
| 로고 `TITANIC` (Bebas Neue) | 28px / 1, 자간 .02em | 400 |
| 결론 제목 `.row b` | 17px / 24px | 800 |
| 부제 `.sub` | 16px / 24px | 400 |
| 결론 본문 `.row` | 15px / 22px | 500 |
| 차트 행 이름·값 | 15px | 이름 700, 값 800 |
| 카드 라벨 `.k .l` | 14px | 700 |
| 비교 막대 줄, 보조값 | 13px | 400~800 |
| 배지, 범례, 푸터 | 12px | 배지 700 |

굵기는 400/500/700/800만 쓴다. 한글은 `word-break: keep-all`. 로고는 Bebas Neue에 굵기가 없어서 `font-weight: 400`으로 고정한다.

---

## 4. 모양과 간격

| 항목 | 값 |
|---|---|
| 바깥 카드·패널 라운드 | 28px |
| 지표 카드 라운드 | 20px |
| 아이콘 칩 라운드 | 10px |
| 비교 막대 (높이 14px) | 라운드 7px |
| 차트 막대 (높이 22px) | 라운드 11px |
| 배지·강조 | 999px (pill) |
| 테마 버튼 | 28px 원형 |
| 최대 폭 | 1120px, 좌우 여백 16px |
| 섹션 간격 | 16px |
| 바깥 카드 안쪽 | 14px, 안쪽 요소 간격 12px |
| 지표 카드 안쪽 | 22px 28px |
| 차트 패널 안쪽 | 24px 32px 18px (모바일 20px 16px 14px) |

반응형 기준: **760px 이하**에서 3열 카드는 1열, 차트 행은 이름·값·태그 한 줄 + 막대 아래 줄.

---

## 5. 컴포넌트

| 컴포넌트 | 클래스 | 구성 |
|---|---|---|
| 지표 카드 묶음 | `.c3` > `.k` + `.cc` | 바깥 카드 안에 지표 카드(`.k`)와 결론(`.cc`) |
| 큰 수치 | `.k .l`, `.k .n` | 라벨 14px + 수치 44px |
| 비교 막대 | `.cr` > 이름 + `.ct`(트랙) > `.cb`(채움) + `.cv` | `.cb.lo`는 보조(`--indigo-mid`) |
| 단일 막대 | `.ct.all` > `.cb` | 전체 비율. 둥근 끝, 너비 = 실제 비율 |
| 범례 | `.lg` > `span` > `i` + 글자 | 10px 원형 점 |
| 결론 줄 | `.row` > `i`(번호 칩) + `b`(제목) + `em`(본문) | |
| 강조 배지 (제목 안) | `.hl` | 인디고 채움, 패딩 `1px .4em`, pill |
| 상태 배지 | `.pill`, `.pill.warn` | 12px, 인디고 소프트 / 오렌지 소프트 |
| 막대 차트 행 | `.hr` > `.hn` + `.tr` > `.br` + `.hv` + `.tg` | `.br.low`, `.hv.low`는 오렌지 |
| 테마 버튼 | `.tbtn` | 원형 아이콘 버튼, 달/해 SVG, `aria-label` + `title` |

---

## 6. 라이트 / 다크 모드

`<html data-theme="light|dark">`로 전환한다. 다크 블록은 **바뀌는 값만** 적는다 (`--indigo`, `--alert` 채움색은 공통).

- 첫 방문: OS의 `prefers-color-scheme`을 따른다.
- 선택은 `localStorage('theme')`에 저장 (접근 불가해도 오류 없이 동작).
- 깜빡임 방지: `<head>`의 인라인 스크립트가 화면이 그려지기 전에 `data-theme`을 정한다.
- 버튼에는 **눌렀을 때 바뀔 모드**의 아이콘을 보여준다: 라이트일 땐 달, 다크일 땐 해.

```html
<script>
  (function () {
    var t; try { t = localStorage.getItem('theme'); } catch (e) {}
    if (t !== 'dark' && t !== 'light') t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', t);
  })();
</script>
```

---

## 7. 가져다 쓰는 법

1. 위 폰트 링크와 테마 스크립트를 `<head>`에 넣는다.
2. 아래 토큰 블록을 `<style>` 맨 위에 붙인다.
3. 컴포넌트에는 색을 직접 쓰지 말고 `var(--…)`만 쓴다.

```css
:root{
  --indigo:#8c9eff; --alert:#ff8a5c;
  --indigo-text:#3f51b5; --alert-text:#b93c0a;
  --indigo-soft:#e8eaf6; --indigo-mid:#7e8fe8; --alert-soft:#fdece3;
  --ink:#10233a; --ink-muted:#4b5b6b; --hairline:#d5d9ec;
  --surface:#ffffff; --wash-top:#eff1fb; --wash-bottom:#fbfcff;
  --shadow:0 8px 32px rgba(140,158,255,.18);
  --on-indigo:#ffffff; --glow:rgba(140,158,255,.14);
  --font:"Pretendard Variable",Pretendard,"Noto Sans KR",system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  --font-logo:"Bebas Neue",Impact,"Arial Narrow",sans-serif;
  color-scheme:light;
}
:root[data-theme="dark"]{
  --indigo-text:#8c9eff; --alert-text:#ff8a5c;
  --indigo-soft:#252b55; --indigo-mid:#5c6bc0; --alert-soft:#3a2219;
  --ink:#e8eaf6; --ink-muted:#a4abc8; --hairline:#2f3556;
  --surface:#171b33; --wash-top:#1d2240; --wash-bottom:#0f1226;
  --shadow:0 8px 32px rgba(0,0,0,.40);
  --on-indigo:#0f1226; --glow:rgba(140,158,255,.12);
  color-scheme:dark;
}
```

---

## 8. 알려진 예외와 주의

- **라이트 모드 `.hl` (흰 글자 on `#8c9eff`)**: 대비 약 2.5:1로 낮다. 의도한 디자인이라 유지하지만, 접근성이 중요한 곳에서는 글자를 `--on-indigo:#0f1226`으로 쓰거나 배경을 더 진하게 한다.
- **라이트 모드 트랙**: `--indigo-soft`(`#e8eaf6`)와 카드 배경(`--wash-top`)의 밝기 차이가 작아, 비어 있는 부분은 은은하게만 보인다.
- **인라인 색**: 막대 농도(JS의 `color-mix`)와 범례 점(HTML `style`)은 CSS 밖에 있다. 색 체계를 바꿀 때 함께 확인한다.
- **원본 스크립트**: 이 문서는 `index_final.html` 기준이다. `t7_dashboard.py`의 `TEMPLATE`에는 아직 반영되지 않았고, 스크립트를 다시 실행하면 `index_final.html`이 덮어써진다.
