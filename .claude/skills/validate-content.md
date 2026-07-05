---
name: validate-content
description: content.yaml 전체 구조를 검증한다. page_num 순서, 슬라이드 타입 유효성, 필수 필드 누락을 체크한다
---

## 절차

1. content.yaml을 읽어 파싱한다:
   ```python
   import yaml
   with open('content.yaml') as f:
       data = yaml.safe_load(f)
   slides = data['slides']
   ```

2. 다음 항목을 순서대로 체크한다:

   **① YAML 문법**: 파싱 성공 여부

   **② 슬라이드 수**: 총 슬라이드 수 출력 (현재 하네스 기준 87장)

   **③ page_num 연속성**: page_num이 오름차순인지, 중복은 없는지
   ```python
   nums = [s['page_num'] for s in slides]
   dups = [n for n in nums if nums.count(n) > 1]
   out_of_order = [(nums[i], nums[i+1]) for i in range(len(nums)-1) if nums[i] >= nums[i+1]]
   ```

   **④ 슬라이드 타입 유효성**: 허용 타입 13종만 사용됐는지
   ```python
   VALID_TYPES = {'cover','toc','chapter','quote','stats','flow','compare','cards3','table','list-rows','grid','content','closing'}
   invalid = [(s['page_num'], s['type']) for s in slides if s['type'] not in VALID_TYPES]
   ```

   **⑤ 필수 필드 누락**: 타입별로 최소한 title(또는 type 고유 필드) 존재 여부

   **⑥ closing 슬라이드**: 정확히 1개, p87에 위치하는지

3. 결과를 요약 출력한다:
   ```
   ✅ YAML 문법 정상
   📄 총 87슬라이드
   ✅ page_num 연속성 정상
   ✅ 슬라이드 타입 전부 유효
   ✅ closing 슬라이드 p87 확인
   ```
   문제가 있으면 해당 항목을 ❌로 표시하고 상세 내용을 출력한다.

4. 오류가 있으면 수정 여부를 사용자에게 확인한다.
