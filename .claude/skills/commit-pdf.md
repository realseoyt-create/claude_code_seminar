---
name: commit-pdf
description: content.yaml과 output.pdf의 변경 사항을 기반으로 커밋 메시지를 자동 생성하고 커밋한다
---

## 절차

1. 변경된 파일을 확인한다:
   ```bash
   git diff --name-only
   git diff --staged --name-only
   ```

2. content.yaml이 변경됐으면 어떤 page_num이 수정됐는지 파악한다:
   ```bash
   git diff content.yaml | grep '^[+-]  page_num:' | head -20
   ```

3. 변경 내용을 기반으로 커밋 메시지를 자동 생성한다:
   - content.yaml만 변경: `Update slides: p{번호들}`
   - output.pdf만 변경: `Regenerate output.pdf`
   - 둘 다 변경: `Update slides p{번호들} and regenerate PDF`
   - 새 슬라이드 추가: `Add slide p{번호}: {제목}`

4. 커밋 전 사용자에게 메시지를 확인받는다:
   ```
   커밋 메시지: "Update slides: p28, p40 and regenerate PDF"
   진행할까요?
   ```

5. 확인 후 스테이징 및 커밋:
   ```bash
   git add content.yaml output.pdf
   git commit -m "..."
   ```

6. 커밋 완료 후 해시를 출력한다. 푸시 여부는 사용자에게 묻는다.

## 주의

- 민감 파일(.env 등)은 절대 포함하지 않는다
- output.pdf가 최신 상태인지 확인한다 (content.yaml 수정 후 PDF 재생성 여부)
- 재생성 안 됐으면 `/generate-pdf` 먼저 실행 권유
