---
name: preview-page
description: 특정 페이지를 PNG로 렌더링해서 시각 확인한다. args로 페이지 번호를 넘긴다
---

args 예시: `28` 또는 `28 40 58` (여러 페이지 동시 가능)

## 절차

1. args에서 페이지 번호를 파싱한다. 없으면 사용자에게 묻는다.

2. output.pdf가 존재하는지 확인한다. 없으면 `/generate-pdf`를 먼저 실행한다.

3. 지정된 페이지를 1.5배 해상도로 렌더링한다:
   ```python
   import fitz
   doc = fitz.open("output.pdf")
   mat = fitz.Matrix(1.5, 1.5)
   pages = [28, 40]  # args에서 받은 번호들
   for pg_num in pages:
       pg = pg_num - 1  # 0-indexed
       if 0 <= pg < len(doc):
           pix = doc[pg].get_pixmap(matrix=mat)
           path = f"/tmp/preview_{pg_num:03d}.png"
           pix.save(path)
           print(f"저장: {path}")
   ```

4. Read 도구로 렌더링된 이미지를 열어 시각 확인한다.

5. 원본 PDF(`클로드 세미나.pdf`)와 비교하려면 원본도 같은 방식으로 렌더링한다:
   ```python
   import fitz
   orig = fitz.open("클로드 세미나.pdf")
   mat = fitz.Matrix(1.5, 1.5)
   for pg_num in pages:
       pg = pg_num - 1
       pix = orig[pg].get_pixmap(matrix=mat)
       pix.save(f"/tmp/original_{pg_num:03d}.png")
   ```
