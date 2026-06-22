---
name: update-slide
description: 기존 슬라이드를 수정한다. args로 페이지 번호와 변경 내용을 넘긴다
---

args 예시: `40 "카드 3번 body 텍스트를 '메모리 관리' 로 변경"`

## 절차

1. args에서 페이지 번호와 변경 내용을 파싱한다.

2. content.yaml에서 `page_num: <번호>` 슬라이드를 찾는다.

3. 요청된 필드를 수정한다. 수정 전 원래 값을 확인하고 변경 사항을 명확히 설명한다.

4. md 필터 지원 필드 (`body`, `subtitle`, `title`, `bullets`, `lb.body`, `lb.title`)에서는 `**굵게**`, `\n` 사용 가능.

5. 수정 후 `/preview-page <번호>`로 결과를 시각 확인한다.

## 자주 쓰는 수정 패턴

- **텍스트 변경**: 해당 필드 값만 교체
- **카드 추가**: `cards` 리스트에 항목 추가 (6개 이상이면 3열 자동 전환)
- **highlight 추가**: 슬라이드 최하단에 강조 박스 (`highlight: "텍스트"`)
- **다크 카드 토글**: `dark: true/false`
- **섹션 배지 변경**: `section: "SECTION N"` 또는 소개 텍스트
