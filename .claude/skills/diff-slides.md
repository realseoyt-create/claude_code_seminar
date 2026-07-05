---
name: diff-slides
description: 원본 PDF(클로드 세미나.pdf)와 생성 PDF(output.pdf)를 페이지별로 픽셀 비교해서 차이나는 페이지 목록을 출력한다
---

args 예시: (없음 — 전체 비교) 또는 `28 40` (특정 페이지만)

## 절차

1. 두 PDF가 존재하는지 확인한다:
   ```python
   import os
   assert os.path.exists('output.pdf'), 'output.pdf 없음 — /generate-pdf 먼저 실행'
   assert os.path.exists('클로드 세미나.pdf'), '원본 PDF 없음'
   ```

2. args가 있으면 해당 페이지만, 없으면 전체 페이지를 비교한다:
   ```python
   import fitz
   orig = fitz.open('클로드 세미나.pdf')
   gen  = fitz.open('output.pdf')
   mat  = fitz.Matrix(1.0, 1.0)

   pages_to_check = [27, 39]  # args에서 파싱 (0-indexed), 없으면 range(min(len(orig), len(gen)))
   diffs = []
   for pg in pages_to_check:
       p1 = orig[pg].get_pixmap(matrix=mat)
       p2 = gen[pg].get_pixmap(matrix=mat)
       # 픽셀 단순 비교
       diff_ratio = sum(a != b for a, b in zip(p1.samples, p2.samples)) / len(p1.samples)
       if diff_ratio > 0.01:  # 1% 이상 차이
           diffs.append((pg+1, f'{diff_ratio*100:.1f}%'))
   ```

3. 결과를 출력한다:
   ```
   비교 완료: 87페이지 중 3페이지 차이
   ⚠️  p12 — 차이율 4.3%
   ⚠️  p28 — 차이율 2.1%
   ⚠️  p55 — 차이율 8.7%
   ```
   차이 없으면: `✅ 전체 페이지 일치`

4. 차이나는 페이지가 있으면 `/preview-page`로 해당 페이지를 렌더링해서 시각 확인한다.
