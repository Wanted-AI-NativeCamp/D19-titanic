# Design System — TITANIC Simple Museum Editorial

- Version: 1.0
- Document: `design-simple.md`
- Project: TITANIC Ocean Archive
- Style: Simple Museum Editorial

## 1. 디자인 콘셉트

**1912년의 항해 기록을 현대적인 데이터로 다시 읽는 디지털 아카이브.**

실제 역사박물관이나 해양 기록관의 웹사이트처럼 진중하면서도 현대적이고 깔끔한 디자인을 지향한다.

과거의 분위기는 오래된 종이 질감이 아닌 역사 사진, 선박 이미지, 정제된 타이포그래피와 여백으로 표현한다.

### 핵심 키워드

- Minimal Museum
- Modern Editorial
- Monochrome
- Maritime Archive
- Clean Data Visualization

## 2. 컬러 시스템

| Token | HEX | 용도 |
|---|---|---|
| Deep Navy | `#071B2D` | Hero, 페이지 외곽 배경 |
| Navy Surface | `#102A40` | Hero 보조 영역 |
| White | `#FFFFFF` | 콘텐츠 카드 |
| Off White | `#F8F9FA` | 카드 내부 보조 영역 |
| Border Gray | `#E6E8EB` | 구분선, 테두리 |
| Mid Gray | `#A0A5AA` | 비활성 요소 |
| Text Gray | `#626870` | 보조 텍스트 |
| Charcoal | `#242424` | 차트 및 강조 |
| Black | `#111111` | 제목 및 본문 |

컬러는 네이비, 화이트, 블랙, 그레이로 제한한다. 베이지, 세피아, 금색, 화려한 그라데이션은 사용하지 않는다.

## 3. 공통 Hero

### 구성

- 모든 페이지에 동일한 타이타닉 선박 이미지 Asset 사용
- Deep Navy 배경
- 좌측 타이틀과 설명
- 우측 선박 이미지
- 하단 CTA 또는 탐색 태그

### 페이지별 표현

- Landing: 대형 TITANIC 타이틀
- Project: PROJECT OVERVIEW
- Methods: ANALYSIS PROCESS
- Analysis: FINAL ANALYSIS

Hero는 페이지마다 콘텐츠만 변경하고 이미지, 타이포그래피, 기본 배치와 분위기를 통일한다.

## 4. 타이포그래피

| 용도 | 권장 폰트 |
|---|---|
| TITANIC 타이틀 | Barlow Condensed |
| 영문 제목 | Inter |
| 한글 제목 및 본문 | Noto Sans KR |
| 데이터 및 숫자 | Inter |
| 코드 | JetBrains Mono |

### 크기

| 요소 | Desktop | Mobile |
|---|---|---|
| Hero Main | 96~120px | 48~64px |
| Page Title | 48px | 32px |
| Section Title | 32px | 26px |
| Card Title | 24px | 20px |
| Body | 16px | 15px |
| Caption | 13px | 12px |
| KPI | 40~56px | 32~40px |

넓은 여백과 명확한 글자 크기 차이로 정보 위계를 만든다.

## 5. 레이아웃

- Max Content Width: 1200px
- Desktop Side Padding: 48~64px
- Mobile Side Padding: 20~24px
- Desktop Grid: 12 Columns
- Mobile: Single Column 우선
- Section Spacing: 96~120px
- Component Gap: 16~24px

모든 페이지는 동일한 정렬 기준과 콘텐츠 너비를 사용한다.

## 6. 랜딩 페이지

### F1 Hero

- 대형 TITANIC 타이틀
- 선박 이미지
- 프로젝트 소개 문구
- 간결한 CTA

### F2 프로젝트 소개

- 역사 사진과 프로젝트 배경
- 여백 중심의 Editorial Layout
- 상세 페이지 이동 링크

### F3 분석 방법 소개

- 단계 번호와 제목
- 분석 과정 요약
- 정돈된 목록 또는 카드

### F4 종합 분석 프리뷰

- 주요 KPI
- 대표 차트
- 분석 결과 요약
- 전체 분석 이동 CTA

### F5 Footer

- Deep Navy 배경
- 프로젝트 정보
- 데이터 출처
- 사용 기술

랜딩은 스크롤에 따라 콘텐츠가 자연스럽게 연결되도록 구성한다.

## 7. 상세 페이지 공통 구조

**Dark Hero + Floating White Content Card**

Hero 아래의 어두운 배경을 유지하면서, 독립적인 화이트 콘텐츠 카드를 배치한다.

페이지 전체를 화이트 배경으로 전환하지 않는다.

### 카드 스타일

| 요소 | 기준 |
|---|---|
| Background | `#FFFFFF` |
| Radius | 12px |
| Border | `1px solid #E6E8EB` |
| Padding Desktop | 32~40px |
| Padding Mobile | 20~24px |
| Shadow | 매우 약하게 |
| Inner Surface | `#F8F9FA` |

카드의 중첩을 최소화하고, 큰 콘텐츠 카드 내부에서 구분선과 여백으로 정보를 나눈다.

## 8. 분석 단계 및 항목 태그

분석 방법과 종합 분석에 동일한 태그 컴포넌트를 사용한다.

### 기본 상태

- Transparent Background
- White Text
- Thin White Border
- Pill Radius: 999px

### 선택 상태

- White Background
- Deep Navy Text
- Pill Radius: 999px

### 동작

- 한 번에 하나의 태그만 활성화
- 선택 시 아래 콘텐츠 카드만 전환
- 전체 페이지 새로고침 없음
- 선택 상태를 명확하게 표시
- 모바일에서는 가로 스크롤 허용

## 9. 분석 방법 콘텐츠 카드

### 정보 구조

1. 단계 번호와 제목
2. 분석 목적
3. 실제 수행 내용
4. 실습 코드
5. 분석 결과
6. 결과 해석
7. 이전·다음 단계

### 코드 스타일

- Background: `#F8F9FA`
- Font: JetBrains Mono
- Radius: 6px
- Padding: 20px
- 긴 코드는 가로 스크롤 허용

표와 코드, 설명은 과도한 카드 중첩 없이 구분선과 여백으로 분리한다.

## 10. 종합 분석 콘텐츠 카드

### 정보 구조

1. 분석 제목
2. 주요 KPI
3. 차트
4. 비교 데이터
5. 핵심 인사이트

### 차트 스타일

- White Background
- Black / Gray 데이터 색상
- 최소한의 축과 구분선
- 명확한 데이터 레이블
- 차트 아래 간결한 해석

### 차트 색상

| 역할 | HEX |
|---|---|
| Primary | `#242424` |
| Secondary | `#777777` |
| Comparison | `#B5B5B5` |
| Background | `#E6E8EB` |

동일한 의미의 데이터는 일관된 명암으로 표현한다.

## 11. 버튼 및 링크

### Dark Hero Button

- Primary: White Background + Navy Text
- Secondary: Transparent + White Border
- Radius: 999px

### White Content Button

- Primary: Black Background + White Text
- Secondary: White Background + Gray Border
- Radius: 4~6px

### Text Link

- 기본적으로 텍스트와 작은 화살표 조합
- Hover 시 밑줄 또는 명도 변화
- 장식적인 아이콘 최소화

## 12. 인터랙션

| 요소 | 동작 |
|---|---|
| 버튼 Hover | 150~200ms 색상 전환 |
| 태그 선택 | 선택 상태 변경 및 콘텐츠 전환 |
| 카드 Hover | 약한 테두리 변화 |
| 차트 Hover | 수치 Tooltip 표시 |
| 스크롤 | 절제된 Fade In |

### 제외

- 게임형 애니메이션
- 강한 Glow
- 움직이는 기포
- 과도한 Parallax
- 3D 회전
- 빈티지 종이 효과

`prefers-reduced-motion`을 지원하고 키보드 탐색 및 Focus 상태를 제공한다.

## 13. 반응형

### Desktop

- Hero 이미지와 텍스트 좌우 배치
- 콘텐츠 카드 최대 너비 유지
- 차트 2열 배치 가능

### Tablet

- 그리드와 간격 축소
- 카드 및 이미지 비율 조정

### Mobile

- Hero 타이틀 크기 축소
- 콘텐츠 카드 단일 컬럼
- 태그 가로 스크롤
- 차트 세로 배치
- 터치 영역 최소 44px 권장

## 14. 디자인 적용 원칙

1. 기존 분석 데이터와 기능을 유지한다.
2. 공통 Hero 이미지를 재사용한다.
3. 분석 방법과 종합 분석은 동일한 태그·카드 스타일을 사용한다.
4. 기존 대시보드의 시각 디자인을 재사용하지 않는다.
5. 모든 화면에서 타이포그래피, 여백, 컬러를 일관되게 적용한다.
6. 불필요한 장식과 복잡한 인터랙션을 추가하지 않는다.

**최종 목표:** 역사적 분위기를 유지하면서도 현대적인 박물관 웹사이트처럼 간결하고 정제된 데이터 아카이브를 구현한다.
