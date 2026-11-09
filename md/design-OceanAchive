# Design System — TITANIC Ocean Archive

- **Version:** 1.0
- **Document:** design.md
- **Project:** TITANIC — Ocean Archive
- **Style:** Museum Editorial × Dark Maritime Archive
- **Scope:** Landing F1~F5 + Detail Pages

---

## 1. 디자인 콘셉트

### 1.1 디자인 정의

**1912년의 항해 기록을 현대적인 데이터 분석으로 다시 읽는 디지털 아카이브.**

실제 해양 박물관이나 역사 기록관에서 운영할 법한 진중하고 정제된 웹사이트를 지향한다.

랜딩에서는 타이타닉의 역사적 분위기와 스토리텔링을 강조하고, 상세 페이지에서는 분석 과정과 결과를 명료하게 전달한다.

### 1.2 핵심 디자인 방향

**Dark Archive Hero + White Editorial Content Card**

- Hero: 어두운 심해 네이비와 타이타닉 이미지
- Content: 화이트 카드 기반의 정돈된 정보 구조
- Typography: 역사적 분위기를 전달하는 영문 타이틀과 현대적인 본문
- Data: 흑백·그레이 중심의 명료한 차트
- Interaction: 절제된 전환과 선택 중심

### 1.3 디자인 키워드

- Ocean Archive
- Museum Editorial
- Maritime History
- Monochrome
- Minimal
- Historical Documentary
- Contemporary Data Visualization

### 1.4 지양할 디자인

- 게임형 탐사 UI
- 퀘스트 및 레벨 표현
- 오래된 종이 질감
- 베이지·세피아 배경
- 장식적인 빈티지 테두리
- 네온 및 과도한 발광 효과
- 복잡한 3D 애니메이션
- 과도한 아이콘과 장식

---

## 2. 컬러 시스템

### 2.1 기본 팔레트

| Token | HEX | 용도 |
|---|---|---|
| Deep Navy | `#071B2D` | Hero 및 바깥 배경 |
| Navy Surface | `#102A40` | 어두운 보조 영역 |
| White | `#FFFFFF` | 콘텐츠 카드 |
| Off White | `#F7F7F7` | 카드 내부 보조 영역 |
| Light Gray | `#E5E5E5` | 테두리 및 구분선 |
| Mid Gray | `#B5B5B5` | 비활성 요소 |
| Archive Gray | `#777777` | 보조 텍스트 |
| Charcoal | `#242424` | 강조 요소 및 주요 차트 |
| Archive Black | `#111111` | 본문 및 제목 |

### 2.2 컬러 사용 원칙

- Dark Hero는 Deep Navy를 기본으로 한다.
- 상세 콘텐츠는 White 카드로 표시한다.
- 카드 내부의 보조 영역은 Off White를 사용한다.
- 일반 본문은 Archive Black을 사용한다.
- 차트는 흑백과 그레이 계열을 중심으로 구성한다.
- Hero를 제외한 상세 콘텐츠에는 블루 계열 강조색을 사용하지 않는다.
- 베이지·세피아·금색 계열을 사용하지 않는다.
- 그라데이션과 Glow 효과는 기본적으로 사용하지 않는다.

### 2.3 CSS 토큰

```css
:root {
  --navy-900: #071B2D;
  --navy-800: #102A40;

  --white: #FFFFFF;
  --off-white: #F7F7F7;
  --gray-200: #E5E5E5;
  --gray-400: #B5B5B5;
  --gray-600: #777777;
  --charcoal: #242424;
  --black: #111111;

  --bg-hero: var(--navy-900);
  --bg-page: var(--navy-900);
  --bg-card: var(--white);
  --bg-card-secondary: var(--off-white);

  --text-on-dark: var(--white);
  --text-primary: var(--black);
  --text-secondary: #595959;

  --border-default: var(--gray-200);
}
```

---

## 3. 공통 Hero 디자인

### 3.1 기본 원칙

랜딩, 분석 방법 소개, 종합 분석 페이지는 동일한 타이타닉 선박 이미지를 사용한다.

페이지별로 이미지 자체를 변경하지 않고 제목, 설명, 태그 및 콘텐츠를 변경한다.

### 3.2 이미지 규칙

- 동일한 이미지 Asset을 재사용한다.
- 흑백 또는 저채도 타이타닉 선박 이미지를 사용한다.
- 짙은 네이비 배경과 자연스럽게 결합한다.
- 이미지의 주요 피사체가 잘리지 않도록 한다.
- 텍스트 가독성을 확보한다.
- 실제 역사 사진과 생성 이미지를 구분한다.
- 역사적 사실을 전달하는 자료에는 검증된 출처를 사용한다.

### 3.3 Hero 레이아웃

**Desktop**

- 좌측: 영문 레이블, 타이틀, 설명
- 우측: 타이타닉 이미지
- 하단: CTA 또는 페이지별 탐색 태그
- 넓은 여백과 명확한 정렬 유지

**Mobile**

- 타이틀 크기 축소
- 이미지 비율 조정
- 텍스트 가독성을 우선한 이미지 배치
- 탐색 태그는 가로 스크롤 또는 줄바꿈 허용

### 3.4 페이지별 Hero

**Landing Hero**
- TITANIC 대형 타이틀
- SURVIVAL ANALYSIS
- 프로젝트 소개 문구
- 주요 CTA

**Analysis Process Hero**
- ANALYSIS PROCESS 레이블
- 분석 방법 소개 타이틀
- 분석 과정 설명
- 8개 분석 단계 태그 (실습 8단계)

**Final Analysis Hero**
- FINAL ANALYSIS 레이블
- 종합 분석 타이틀
- 분석 결과 소개
- 5개 분석 항목 태그

---

## 4. 상세 콘텐츠 카드

### 4.1 공통 구조

분석 방법 소개 및 종합 분석 페이지는 전체 화이트 배경으로 전환하지 않는다.

**Dark Hero 및 Navy Background 위에 독립적인 White Content Card를 배치한다.**

### 4.2 카드 디자인

| 속성 | 기준 |
|---|---|
| Background | `#FFFFFF` |
| Border | `1px solid #E5E5E5` |
| Radius | 12~16px |
| Padding Desktop | 32~40px |
| Padding Mobile | 20~24px |
| Shadow | 매우 약하게 |
| Text | `#111111` |
| Secondary Area | `#F7F7F7` |

### 4.3 카드 배치

- Hero 하단과 콘텐츠 카드 사이에 자연스러운 연결을 만든다.
- 콘텐츠 카드는 어두운 배경 위에 독립적으로 배치한다.
- 카드 주변에 충분한 여백을 확보한다.
- 선택된 태그에 따라 카드 내부 콘텐츠만 변경한다.
- 카드 높이는 콘텐츠에 따라 자연스럽게 조절한다.
- 지나치게 많은 중첩 카드를 만들지 않는다.

### 4.4 카드 내부 정보 위계

1. 섹션 번호 및 레이블
2. 콘텐츠 제목
3. 간단한 설명
4. 주요 데이터 또는 활동
5. 코드·차트·표
6. 결과 해석
7. 보조 내비게이션

---

## 5. 타이포그래피

### 5.1 폰트

| 용도 | 폰트 |
|---|---|
| TITANIC 메인 타이틀 | Playfair Display |
| 영문 제목 | Playfair Display |
| 한글 제목 및 본문 | Noto Sans KR |
| 영문 UI 및 숫자 | Inter |
| 코드 | JetBrains Mono |

### 5.2 크기

| 구분 | Desktop | Mobile |
|---|---|---|
| Hero Title | 88~112px | 48~64px |
| Page Title | 48px | 32px |
| Section Title | 32px | 26px |
| Card Title | 24px | 20px |
| Body Large | 18px | 16px |
| Body | 16px | 15px |
| Caption | 13px | 12px |
| KPI | 40~56px | 32~40px |

### 5.3 사용 규칙

- Hero에서는 영문 타이포그래피를 강조한다.
- 상세 콘텐츠는 한글 가독성을 우선한다.
- 긴 본문은 줄간격 1.6~1.8을 사용한다.
- 섹션 레이블은 작은 대문자와 넓은 자간으로 표현한다.
- KPI 숫자는 Tabular Numbers를 적용한다.
- 지나친 Bold 및 장식적인 텍스트 사용을 피한다.

---

## 6. 태그 및 탭 컴포넌트

### 6.1 공통 원칙

분석 방법과 종합 분석 페이지는 동일한 탐색 태그 컴포넌트를 사용한다.

### 6.2 기본 스타일

**Inactive**
- Transparent Background
- White Text
- 1px White Border (낮은 불투명도)
- Radius: 999px

**Active**
- White Background
- Deep Navy Text
- Radius: 999px

**Hover**
- 테두리 및 배경 명도 변화
- 과도한 Glow 금지

### 6.3 분석 방법 태그

- 01 데이터 살펴보기
- 02 결측치 찾기
- 03 왜 비었을까
- 04 결측 처리
- 05 처리 방법 실험
- 06 그룹별 생존율
- 07 시각화
- 08 대시보드

실습한 8단계를 그대로 쓴다. 실습하지 않은 `인사이트 도출` 단계는 두지 않는다 (PRD 참조).

### 6.4 종합 분석 태그

- 전체 요약
- 성별 분석
- 등급 분석
- 복합 분석
- 탑승 항구 분석

### 6.5 동작 규칙

- 선택된 태그는 한 개만 유지한다.
- 태그 선택 시 아래 콘텐츠 카드의 내용이 변경된다.
- 페이지 전체 새로고침 없이 전환한다.
- 키보드로 태그 선택이 가능해야 한다.
- 활성 태그는 시각적·의미적으로 구분한다.
- 모바일에서 태그가 잘리지 않도록 한다.
- 콘텐츠 전환 시 불필요한 스크롤 점프를 방지한다.

---

## 7. 분석 방법 콘텐츠 디자인

### 7.1 콘텐츠 구조

하나의 큰 White Card 내부에 다음 내용을 배치한다.

- 단계 번호
- 단계 제목
- 분석 목적
- 주요 활동
- 사용 도구
- 코드 예시
- 결과 표
- 해석
- 이전·다음 버튼

### 7.2 코드 영역

- Background: `#F7F7F7`
- Font: JetBrains Mono
- Text: `#242424`
- Radius: 6~8px
- Padding: 20~24px
- 복사 버튼 제공 가능
- 긴 코드는 가로 스크롤 지원

### 7.3 결과 표

- White Background
- Thin Gray Border
- 명확한 헤더
- 숫자 오른쪽 정렬
- 불필요한 컬러 강조 금지

### 7.4 해석 영역

- Off White 배경
- 제목과 설명 중심
- 핵심 발견을 간결하게 표시
- 과도한 아이콘과 강조 효과 제외

---

## 8. 종합 분석 콘텐츠 디자인

### 8.1 콘텐츠 구조

선택한 분석 항목의 White Dashboard Card 내부에 다음을 배치한다.

1. 분석 제목
2. 핵심 KPI
3. 주요 차트
4. 데이터 표 또는 비교 지표
5. 주요 인사이트

### 8.2 KPI 디자인

- White 또는 Off White 배경
- 큰 숫자 중심
- 단위 명확히 표시
- 보조 설명 최소화
- 과도한 아이콘 사용 금지

### 8.3 차트 디자인

- Black / Gray 중심
- White Background
- 축과 구분선 최소화
- 실제 수치 표시
- 표본 수 함께 제공
- 툴팁으로 상세 데이터 확인

### 8.4 차트 명암

| 역할 | 색상 |
|---|---|
| Primary Data | `#242424` |
| Secondary Data | `#777777` |
| Comparison Data | `#B5B5B5` |
| Background Bar | `#E5E5E5` |

동일한 의미의 데이터는 모든 차트에서 동일한 명암으로 표현한다.

### 8.5 데이터 해석

- 차트 하단에 핵심 인사이트 제공
- 실제 데이터 기반 해석만 사용
- 집단 간 비교 기준 명시
- 인과관계 단정 금지
- 수치와 텍스트의 일치 여부 검증

---

## 9. 랜딩 페이지 카드

### 9.1 Archive 카드

랜딩의 F2~F4는 Dark Archive 스타일을 유지한다.

### 9.2 스타일

- Navy Background
- White Text
- Thin White Border
- 역사 사진 또는 선박 도면
- 단계 번호
- 섹션 제목
- 간단한 설명
- Arrow CTA

### 9.3 인터랙션

- Hover 시 테두리 명도 변화
- CTA 클릭 시 상세 페이지 이동
- 과도한 확대 및 발광 효과 금지
- 이미지와 텍스트의 대비 유지

---

## 10. 버튼 및 공통 UI

### Primary Button — Dark Background

- White Background
- Navy Text
- Radius: 999px
- Hover: Light Gray

### Secondary Button — Dark Background

- Transparent Background
- White Text
- Thin White Border
- Radius: 999px

### Primary Button — White Card

- Background: `#111111`
- Text: `#FFFFFF`
- Radius: 4~6px

### Text Link

- Underline 또는 Arrow
- Hover 시 명도 변화
- 장식적 아이콘 최소화

---

## 11. 레이아웃 및 간격

| 항목 | 기준 |
|---|---|
| Max Content Width | 1440px |
| Standard Content Width | 1200px |
| Desktop Side Padding | 48~64px |
| Tablet Side Padding | 32px |
| Mobile Side Padding | 20~24px |
| Desktop Grid | 12 Columns |
| Mobile Grid | 4 Columns |
| Section Spacing | 96~144px |
| Card Gap | 16~24px |

### 원칙

- 콘텐츠의 좌우 정렬선을 일관되게 유지한다.
- 카드 사이에 충분한 간격을 확보한다.
- 상세 콘텐츠는 지나치게 좁게 만들지 않는다.
- 표와 차트는 가독성에 맞춰 유연하게 배치한다.
- Mobile에서는 단일 컬럼을 우선한다.

---

## 12. 인터랙션 및 애니메이션

### 허용

| 요소 | 동작 | 시간 |
|---|---|---|
| Section Reveal | Subtle Fade | 200~300ms |
| Button Hover | Color Transition | 150~200ms |
| Tab Switch | Content Change | 150~200ms |
| Card Hover | Border Change | 150ms |
| Tooltip | Immediate Display | 0~100ms |

### 금지

- 강한 Glow
- 게임형 진행 애니메이션
- 움직이는 기포
- 과도한 Parallax
- 불필요한 3D 효과
- 반복적인 자동 모션
- 강제 스크롤

### 접근성

- `prefers-reduced-motion` 지원
- 키보드 탐색 지원
- 명확한 Focus 스타일
- 본문 명도 대비 4.5:1 이상
- 색상에만 의존하지 않는 상태 표현
- 차트의 텍스트 대체 정보 제공

---

## 13. 페이지별 디자인 적용

### Landing Page

- Dark Navy 배경
- 타이타닉 이미지 중심
- Archive 카드 스타일
- 스크롤형 스토리텔링
- F1~F5 연결

### Project Overview

- 공통 Hero 스타일 적용
- 역사적 기록과 설명 중심
- 콘텐츠 가독성 우선
- White Editorial Card 사용 가능

### Analysis Process

- 공통 Dark Hero
- 동일한 타이타닉 이미지
- 8개 단계 태그 (실습 8단계)
- 단일 White Content Card
- 코드·표·해석 표시

### Final Analysis

- 공통 Dark Hero
- 동일한 타이타닉 이미지
- 5개 분석 항목 태그
- White Dashboard Card
- KPI·차트·인사이트 표시

### Footer

- Deep Navy 또는 Charcoal
- White Text
- 데이터 출처 및 프로젝트 정보
- 장식 최소화

---

## 14. 반응형 및 접근성

### Desktop

- Hero의 텍스트와 이미지 좌우 배치
- 카드 내부 2열 구성 가능
- 차트 2열 배치 가능

### Tablet

- Hero 구성 조정
- 콘텐츠 카드 간격 축소
- 복잡한 그리드는 1~2열로 변경

### Mobile

- Hero 타이틀 축소
- 태그 가로 스크롤 허용
- White Card 단일 컬럼
- 차트 세로 배치
- 터치 영역 최소 44px 권장
- 가로 스크롤 표 별도 처리

---

## 15. 디자인 검수 체크리스트

- [ ] 공통 Hero 이미지가 동일한가?
- [ ] Hero의 색상과 타이포그래피가 일관적인가?
- [ ] 상세 콘텐츠가 독립적인 White Card로 표시되는가?
- [ ] 분석 방법 및 종합 분석의 태그 스타일이 동일한가?
- [ ] 선택한 태그의 활성 상태가 명확한가?
- [ ] 카드 내부 정보 위계가 명확한가?
- [ ] 차트의 숫자와 표본 수가 읽기 쉬운가?
- [ ] 베이지·세피아·게임형 UI가 제거되었는가?
- [ ] 반응형 레이아웃이 정상적인가?
- [ ] 키보드 및 접근성 검수가 완료되었는가?

---

## 16. 최종 디자인 원칙

**Ocean Archive는 역사적 분위기를 전달하는 Dark Hero와 현대적인 데이터 분석을 위한 White Editorial Card가 결합된 디지털 박물관이다.**

랜딩은 몰입감 있는 스토리텔링을 제공하고, 상세 페이지는 분석 과정과 결과를 명확하게 전달한다.

전체 경험은 진중하고 정제되어야 하며, 불필요한 장식보다 콘텐츠의 신뢰성, 정보의 위계, 사용자 탐색 편의성을 우선한다.
