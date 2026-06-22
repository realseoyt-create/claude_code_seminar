---
name: add-slide
description: content.yaml에 새 슬라이드를 추가한다. args로 페이지 번호, 타입, 제목을 넘긴다
---

args 예시: `42 grid "CLAUDE.md 작성 원칙"`

## 절차

1. **args 파싱**: 페이지 번호 / 슬라이드 타입 / 제목 순서로 받는다. 누락된 항목은 사용자에게 묻는다.

2. **타입별 YAML 템플릿 확인**: CLAUDE.md의 "슬라이드 타입 13가지" 섹션에서 해당 타입의 형식을 정확히 따른다.

3. **content.yaml 열기**: 지정된 `page_num`에 해당하는 위치에 삽입한다.
   - 앞뒤 슬라이드의 `page_num`을 확인해 번호 순서를 맞춘다.
   - 기존 page_num과 겹치면 사용자에게 확인 후 진행한다.

4. **섹션 배지**: 해당 페이지 범위에 맞는 섹션을 CLAUDE.md "섹션 구성" 표에서 선택한다.

5. **md 필터 적용 가능 필드**: body, subtitle, title, bullets 항목에서 `**굵게**`, `\n` 사용 가능함을 염두에 둔다.

6. 추가 후 `/generate-pdf`를 실행해 렌더링을 확인한다.

## 주의

- `cards` 6개 이상인 grid → 3열 그리드 자동 적용됨
- `type: closing`은 p87에만 하나 존재해야 함
- `type: chapter`에는 subtitle 필드가 필요함
