# 클로드코드 잘 사용하기 — PDF 하네스

이 저장소는 87페이지 한국어 세미나 자료를 **코드 한 줄 없이** 생성하는 하네스입니다.
콘텐츠(content.yaml) → HTML(Jinja2) → PDF(Playwright) 파이프라인.

---

## 텔레그램 채널 대화 규칙

메시지가 `<channel source="plugin:telegram:telegram" ...>` 태그로 오면 텔레그램 채널이다. 이 경우 아래 규칙을 **항상** 따른다.

1. **질문/선택지 → 텔레그램 reply로만** — `AskUserQuestion` 도구 사용 금지. 선택지가 필요하면 reply 메시지에 번호 목록으로 평문 제시.
2. **플랜 승인 → 텔레그램으로** — `ExitPlanMode` 호출 전에 텔레그램 reply로 플랜 요약을 보내고 진행 여부를 확인한다.
3. **권한/퍼미션 → 바이패스** — 파일 쓰기, Bash 실행 등 권한 확인 없이 자동 진행한다.
4. **응답 형식** — 마크다운 렌더링 없는 plain text로, 요약이 아닌 전체 내용을 reply로 전송한다.

Claude Code UI(텔레그램 태그 없는 일반 메시지)에서는 기존 방식대로 동작한다.

---

## 스택

| 역할 | 도구 |
|------|------|
| 콘텐츠 정의 | `content.yaml` |
| HTML 렌더링 | `templates/slide.html` (Jinja2, 13가지 레이아웃) |
| PDF 출력 | `generate.py` → Playwright Chromium |
| 페이지 비교 | PyMuPDF (`fitz`) |

---

## 실행 방법

```bash
# PDF 생성
python3 generate.py content.yaml output.pdf

# 특정 페이지 PNG 렌더링 (비교용)
python3 -c "
import fitz
doc = fitz.open('output.pdf')
mat = fitz.Matrix(1.5, 1.5)
for pg in [0, 9, 39, 86]:  # 1, 10, 40, 87페이지
    pix = doc[pg].get_pixmap(matrix=mat)
    pix.save(f'/tmp/page_{pg+1:03d}.png')
"
```

---

## 메타데이터 규칙

- **저자**: `Test기술팀 서영택` (content.yaml metadata.author)
- **날짜**: 표지에 표시 안 함 (metadata.date 없음)
- **총 페이지**: 87장 (p88 부록 챕터 헤더, p89 참고문헌 제외)
- **마지막 슬라이드(p87)**: `type: closing`, title: "감사합니다"

---

## content.yaml 구조

```yaml
metadata:
  title: "클로드코드 잘 사용하기"
  subtitle: "AI와 함께하는 새로운 개발 워크플로우"
  author: "Test기술팀 서영택"

slides:
  - type: cover
    page_num: 1
    ...
```

슬라이드는 `page_num` 순서로 정렬되어 있음. 새 슬라이드 추가 시 정렬 위치에 삽입.

---

## 슬라이드 타입 13가지

### 1. `cover` — 표지
```yaml
- type: cover
  page_num: 1
  tag: "전사 세미나"
  title: "클로드코드\n잘 사용하기"
  subtitle: "AI와 함께하는 새로운 개발 워크플로우"
```

### 2. `toc` — 목차
```yaml
- type: toc
  page_num: 4
  title: "목차"
  items:
    - num: "01"
      title: "섹션 제목"
      desc: "설명"
      page: "5"
```

### 3. `chapter` — 챕터 구분
```yaml
- type: chapter
  page_num: 5
  section: "SECTION 1"
  title: "챕터 제목"
  subtitle: "부제목"
```

### 4. `quote` — 인용/임팩트 슬라이드
```yaml
- type: quote
  page_num: 7
  section: "추상화의 역사 — 3단계"   # 소개 텍스트면 이탤릭 태그
  card: 'print("Hello")'             # 중앙 강조 박스 (md 지원)
  subtitle: '"장난감 언어"'           # 박스 아래 설명 (md 지원)
  body: "**Python → #1 언어**"       # 결론 문구 (md 지원, 32px bold)
```

### 5. `stats` — 숫자 통계
```yaml
- type: stats
  page_num: 10
  section: "SECTION 1"
  title: "숫자로 보는 변화"
  items:
    - value: "25%"
      text: "YC 2025 겨울 배치 중\n코드베이스의 **95%**를 AI로 생성"
```

### 6. `flow` — 흐름도 + 사이드바
```yaml
- type: flow
  page_num: 12
  section: "SECTION 1"
  title: "개발자의 새로운 역할"
  steps:
    - text: "코드를 잘 짜는 능력"
    - text: "문서를 잘 쓰는 능력"
    - text: "컨텍스트를 설계하는 능력"
      highlight: true
  sidebar:
    - title: "건축가"
      body: "벽돌 쌓기 대신 설계도 작성."
    - title: "오케스트라 지휘자"
      body: "직접 연주 대신 전체 조율."
```

### 7. `compare` — 좌우 비교
```yaml
- type: compare
  page_num: 28
  section: "SECTION 3"
  title: "TDD (Test-Driven Development)"
  subtitle: "**테스트를 먼저 쓰고**, 통과하는 코드를 나중에 쓴다."
  cols:
    - dark: true
      title: "AI+TDD 워크플로우"
      bullets:
        - "**1. 인간이 실패 테스트 작성 (Red)**"
        - "2. AI가 통과 코드 구현 (Green)"
    - dark: false
      left_borders:
        - title: "왜 AI에게 특히 중요한가"
          body: "AI는 \"동작하는 것 같은\" 코드를 자신 있게 만듦."
  highlight: "핵심 인사이트 박스 텍스트"
```

### 8. `cards3` — 3열 카드
```yaml
- type: cards3
  page_num: 15
  section: "SECTION 2"
  title: "AI 코딩 도구의 진화 3단계"
  cards:
    - label: "1단계"
      title: "자동완성"
      body: "IDE가 다음 줄을 예측"
      dark: false
    - label: "2단계"
      title: "대화형 채팅"
      body: "코드 토론, 버그 설명"
    - label: "3단계"
      title: "에이전틱 코딩"
      body: "목표를 분해하고 독립 실행"
      dark: true
  note: "출처: ..."         # 선택. 하단 왼쪽 경계선 박스
  highlight: "강조 문구"    # 선택. 하단 어두운 박스
```

### 9. `table` — 행 테이블
```yaml
- type: table
  page_num: 26
  section: "SECTION 3"
  title: "타임라인"
  col_widths: "200px 1fr"
  columns: ["시기", "사건"]
  rows:
    - label: "2025.02"
      values: ["Karpathy, \"Vibe Coding\" 제시"]
    - label: "2026 초"
      values: ["TDD, Context Engineering 부상"]
      highlight: true   # 어두운 배경 강조 행
```

### 10. `list-rows` — 레이블+설명 행 리스트
```yaml
- type: list-rows
  page_num: 21
  section: "SECTION 2"
  title: "확장 레이어 구조"
  subtitle: "CLAUDE.md만으로 시작. 필요에 따라 하나씩 추가."
  rows:
    - label: "기초 · CLAUDE.md"
      desc: "모든 세션에서 로드되는 프로젝트 컨텍스트"
    - label: "자동화 · Skills"
      desc: "재사용 가능한 워크플로우"
  highlight: "선택. 하단 강조 박스"
```

### 11. `grid` — 2열(또는 3열) 카드 그리드
```yaml
- type: grid
  page_num: 40
  section: "SECTION 4"
  title: "하네스의 6대 구성 요소"
  cards:
    - num: "1"          # num 있으면 오렌지 원형 배지 표시
      title: "컨텍스트 엔지니어링"
      body: "각 단계에서 모델이 보는 정보를 설계."
    - num: "2"
      title: "도구 오케스트레이션"
      body: "어떤 도구가 가용한지 결정"
    # cards 6개 이상이면 자동으로 3열 그리드
  full_card:            # 선택. 하단 전체 너비 어두운 박스
    border: true
    text: "출처: Kai Renner, harness-engineering.ai"
  cite: "— 출처 텍스트"  # 선택. 우하단 작은 텍스트
```

### 12. `content` — 복합 콘텐츠
```yaml
- type: content
  page_num: 80
  section: "SECTION 6"
  title: "슬라이드 제목"
  big_quote:            # 선택
    text: "인용문"
    cite: "출처"
  cols:                 # 선택. 2열 카드
    - title: "왼쪽 제목"
      dark: false
      lines:
        - "· 항목 1"
        - "· 항목 2"
    - title: "오른쪽 제목"
      dark: true
      mono_lines:
        - "$ 명령어"
```

### 13. `closing` — 마무리
```yaml
- type: closing
  page_num: 87
  title: "감사합니다"
  # author는 metadata.author에서 자동으로 가져옴
```

---

## md 필터 — 마크다운 지원 필드

`body`, `subtitle`, `title`, `lb.title`, `lb.body`, `bullets` 항목에서 사용 가능:

| 문법 | 결과 |
|------|------|
| `**텍스트**` | **굵게** (오렌지 강조색) |
| `*텍스트*` | *이탤릭* |
| `\n` 또는 `\\n` | 줄바꿈 |

---

## 디자인 토큰

```css
--bg-light:   #F5F0EB  /* 슬라이드 배경 */
--bg-dark:    #2D2A25  /* 어두운 카드/배경 */
--accent:     #C75C36  /* 강조색 (오렌지) */
--text-dark:  #1E1C19  /* 본문 텍스트 */
--text-light: #FFFFFF  /* 밝은 배경 위 텍스트 */
--text-sec:   #5A5853  /* 보조 텍스트 */
--card-light: #EAE4DC  /* 카드 배경 */
--code-text:  #6EE7D8  /* 코드 텍스트 (틸) */
```

---

## 섹션 구성

| 섹션 | 범위 | 주제 |
|------|------|------|
| SECTION 1 | p5–p13 | AI 코딩의 패러다임 전환 |
| SECTION 2 | p14–p24 | 하네스 레이어 구조 |
| SECTION 3 | p25–p34 | SDD / TDD |
| SECTION 4 | p35–p54 | 하네스 6대 구성 요소 |
| SECTION 5 | p55–p70 | 컨텍스트 엔지니어링 |
| SECTION 6 | p71–p86 | 멀티에이전트 패턴 |

---

## 금지 사항

- 표지에 날짜 추가 금지
- p88, p89 슬라이드 추가 금지 (원본에서 제외됨)
- `slide['items']` → Jinja2에서 dict 메서드 충돌 방지 위해 bracket 표기 사용
- 슬라이드 총 수는 87장 유지
