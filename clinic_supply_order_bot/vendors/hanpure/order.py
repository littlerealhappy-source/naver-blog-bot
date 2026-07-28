"""
한퓨어몰 주문 자동화.

3개 서브커맨드로 나뉜다:
  - search   : 상품명으로 검색해 후보(이름/가격/URL)를 출력한다.
  - prepare  : 상품을 장바구니에 담고 주문서(배송지 등)까지 작성한 뒤,
               결제 버튼을 누르기 '직전' 화면에서 멈추고 주문 요약
               스크린샷과 총액을 남긴다. 절대 결제를 완료하지 않는다.
  - confirm  : (사람이 확인한 뒤) 결제 버튼을 눌러 주문을 완료한다.

TODO: 이 파일은 골격만 잡혀 있고 실제 셀렉터는 비어 있다.
inspect_site.py 를 실행해 debug_output/ 에 저장된 실제 화면 구조를 보고
아래 TODO 표시된 부분을 채워야 동작한다.

사용 예:
    python order.py search --query "녹용정"
    python order.py prepare --product-url "https://hanpuremall.co.kr/..." --qty 10
    python order.py confirm
"""

import argparse
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PWTimeout, sync_playwright

SESSION_FILE = "hanpure_session.json"
HOME_URL = "https://hanpuremall.co.kr/"
DEBUG_DIR = Path("debug_output")


def debug_dump(page: Page, tag: str):
    DEBUG_DIR.mkdir(exist_ok=True)
    page.screenshot(path=str(DEBUG_DIR / f"{tag}.png"), full_page=True)
    (DEBUG_DIR / f"{tag}.html").write_text(page.content(), encoding="utf-8")


def require_session() -> None:
    if not Path(SESSION_FILE).exists():
        raise FileNotFoundError(
            f"{SESSION_FILE} 이 없습니다. 먼저 login_setup.py 를 실행해 세션을 저장하세요."
        )


def check_logged_in(page: Page):
    """로그인 세션 만료 여부 확인. 만료 시 재로그인 안내와 함께 예외를 던진다."""
    if "mode=login" in page.url:
        raise RuntimeError(
            "저장된 로그인 세션이 만료되어 한퓨어몰이 로그인 페이지로 돌려보냈습니다.\n"
            "login_setup.py 를 다시 실행해서 세션을 새로 저장한 뒤 재시도하세요."
        )


def cmd_search(args):
    require_session()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        try:
            context = browser.new_context(storage_state=SESSION_FILE)
            page = context.new_page()
            page.goto(HOME_URL)
            page.wait_for_load_state("networkidle")
            check_logged_in(page)

            debug_dump(page, "search_00_home")

            # TODO: inspect_site.py 로 확인한 검색창 셀렉터로 교체
            # 예: page.fill("#search_word", args.query); page.click("#search_button")
            # TODO: 검색 결과 목록에서 (이름, 가격, 상품 URL) 리스트를 뽑아 출력
            # for item in results:
            #     print(f"{item['name']} | {item['price']} | {item['url']}")
            raise NotImplementedError(
                "검색 셀렉터가 아직 채워지지 않았습니다. "
                "debug_output/02_search_result.html 을 참고해 cmd_search를 구현하세요."
            )
        finally:
            browser.close()


def cmd_prepare(args):
    require_session()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        try:
            context = browser.new_context(storage_state=SESSION_FILE)
            page = context.new_page()
            page.goto(args.product_url)
            page.wait_for_load_state("networkidle")
            check_logged_in(page)

            debug_dump(page, "prepare_00_product")

            # TODO: 수량 입력(args.qty) 후 장바구니 담기
            # TODO: 장바구니 -> 주문서 작성 화면 이동
            # TODO: 배송지 등 필수 항목 확인 (이미 저장된 기본 배송지가 있다고 가정)
            # TODO: 결제 버튼을 누르기 '직전' 화면에서 멈추고, 총액을 파싱해서 출력
            raise NotImplementedError(
                "장바구니/주문서 셀렉터가 아직 채워지지 않았습니다. "
                "debug_output/03_product_detail.html ~ 05_order_form.html 을 참고해 "
                "cmd_prepare를 구현하세요. 결제 버튼은 절대 클릭하지 마세요."
            )
        finally:
            browser.close()


def cmd_confirm(args):
    require_session()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        try:
            context = browser.new_context(storage_state=SESSION_FILE)
            page = context.new_page()
            page.goto(HOME_URL)
            page.wait_for_load_state("networkidle")
            check_logged_in(page)

            # TODO: 서버에 남아있는 장바구니/주문서로 이동해 결제 버튼 클릭
            # TODO: 결제 완료 화면 확인 후 성공/실패 출력
            raise NotImplementedError(
                "결제 확정 셀렉터가 아직 채워지지 않았습니다. cmd_confirm을 구현하세요."
            )
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description="한퓨어몰 주문 자동화")
    parser.add_argument(
        "--headless", action="store_true", help="브라우저 창을 띄우지 않고 실행"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="상품 검색")
    p_search.add_argument("--query", required=True)
    p_search.set_defaults(func=cmd_search)

    p_prepare = sub.add_parser("prepare", help="장바구니 담기 ~ 주문서 작성 (결제 직전 정지)")
    p_prepare.add_argument("--product-url", required=True)
    p_prepare.add_argument("--qty", type=int, required=True)
    p_prepare.set_defaults(func=cmd_prepare)

    p_confirm = sub.add_parser("confirm", help="결제 확정")
    p_confirm.set_defaults(func=cmd_confirm)

    args = parser.parse_args()

    try:
        args.func(args)
    except (FileNotFoundError, RuntimeError, NotImplementedError, PWTimeout) as e:
        print(f"오류: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
