---
name: generate-pdf
description: PDF를 생성하고 주요 페이지를 렌더링해서 시각 확인한다
---

1. 프로젝트 루트에서 PDF를 생성한다:
   ```
   python3 generate.py content.yaml output.pdf
   ```

2. 생성 완료 후 페이지 수와 파일 크기를 확인한다:
   ```python
   import fitz
   doc = fitz.open("output.pdf")
   print(f"총 {len(doc)}페이지, {os.path.getsize('output.pdf')//1024}KB")
   ```

3. 커버(p1), 대표 콘텐츠(p10, p40), 마지막(p87) 페이지를 렌더링해서 Read 도구로 시각 확인한다:
   ```python
   import fitz
   doc = fitz.open("output.pdf")
   mat = fitz.Matrix(1.5, 1.5)
   for pg in [0, 9, 39, 86]:
       pix = doc[pg].get_pixmap(matrix=mat)
       pix.save(f"/tmp/preview_{pg+1:03d}.png")
   ```

4. 문제가 보이면 사용자에게 보고하고 수정 여부를 확인한다.
