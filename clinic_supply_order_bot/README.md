# 한의원 물품 주문 자동화 (clinic_supply_order_bot)

텔레그램으로 "OO 필요해" 라고 말하면, 과거 주문 기록(`order_memory.json`)을 참고해
같은 상품을 같은 수량으로 재주문하도록 돕는 자동화. `naver_blog_bot`과 같은 패턴
(Playwright + 로그인 세션 저장)을 거래처별로 반복 적용한다.

## 안전 원칙

- **실제 결제 버튼은 자동으로 누르지 않는다.** 각 거래처 스크립트는 장바구니
  담기~주문서 작성까지만 자동화하고, 결제 직전 화면에서 멈춘 뒤 주문 요약
  (품목/수량/총액) 스크린샷을 남긴다. 사용자가 채팅으로 최종 확인한 뒤에만
  `confirm` 단계를 실행해 결제를 완료한다.
- 품목/수량 기억은 `order_memory.json`에 사람이 읽을 수 있는 형태로 저장한다.

## 현재 구현 범위

거래처 5곳(쿠팡, 한퓨어, 케이엠몰, 메디스트림, 자생한방병원 성남원외탕전실) 중
**한퓨어(한퓨어몰)를 먼저 파일럿으로 구현**해 전체 흐름을 검증한다. 나머지는
`vendors/hanpure/`와 같은 구조로 추가해나간다.

## 사용 순서 (한퓨어 예시)

1. 최초 1회, 로그인 세션 저장 (아이디/비번은 브라우저 창에서 직접 입력)
   ```
   python vendors/hanpure/login_setup.py
   ```
   `vendors/hanpure/hanpure_session.json`이 생성된다. **이 파일은 로그인 세션
   쿠키를 담고 있으므로 절대 깃허브 등에 올리지 마세요.**

2. 사이트 구조 조사 (셀렉터가 아직 안 채워져 있을 때 1회성으로 실행)
   ```
   python vendors/hanpure/inspect_site.py
   ```
   검색/상품/장바구니/주문서/결제 페이지의 DOM을 `debug_output/`에 남긴다.
   이 결과를 보고 `order.py`의 셀렉터를 채운다.

3. 상품 검색
   ```
   python vendors/hanpure/order.py search --query "녹용정"
   ```

4. 장바구니~주문서 작성 (결제 직전에서 정지)
   ```
   python vendors/hanpure/order.py prepare --product-url <URL> --qty 10
   ```

5. 최종 결제 (사용자가 확인한 뒤에만)
   ```
   python vendors/hanpure/order.py confirm
   ```

## 알아둘 점

- 세션이 만료되면 `login_setup.py`를 다시 실행해야 한다.
- 각 사이트의 실제 셀렉터는 사이트 업데이트로 언제든 바뀔 수 있다. 오류가 나면
  `debug_output/`의 스크린샷/HTML을 확인하고 `order.py`의 셀렉터를 보정한다.
- 캡차/2단계 인증은 자동으로 우회하지 않는다. `login_setup.py`는 항상
  `headless=False`로 열어 사용자가 직접 처리한다.

## 다음 단계 (미구현)

- 한퓨어 파일럿 검증 후 쿠팡, 케이엠몰, 메디스트림, 자생한방병원 성남원외탕전실
  순서로 `vendors/` 확장
- `order_memory.json`을 참고해 재주문 여부를 판단하는 흐름은 스크립트가 아니라
  Claude가 대화 중에 직접 수행 (README 상단 "안전 원칙" 참고)
