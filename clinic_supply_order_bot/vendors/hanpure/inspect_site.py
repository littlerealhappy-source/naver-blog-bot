"""
한퓨어몰의 검색/상품/장바구니/주문서 화면 실제 DOM 구조를 확인하기 위한 정찰용 스크립트.

order.py의 셀렉터를 추측이 아니라 실제 화면을 보고 채워 넣기 위해 사용한다.
자동으로 검색/클릭을 시도하지 않고, 각 단계에서 사용자가 직접 브라우저를
조작한 뒤 Enter를 누르면 그 시점의 화면을 debug_output/에 저장한다.

사용법:
    1) login_setup.py 를 먼저 실행해 hanpure_session.json 을 만들어 두세요.
    2) python inspect_site.py 실행
    3) 안내에 따라 상품 검색 -> 상품 상세 -> 장바구니 담기 -> 주문서 작성 화면까지
       직접 이동하면서 각 단계마다 Enter를 눌러주세요.
    4) 결제 버튼을 누르기 직전 화면까지만 진행하고, 실제 결제는 누르지 마세요.
    5) debug_output/ 폴더에 생성된 파일들을 그대로 두면 Claude가 읽고
       order.py의 셀렉터를 채웁니다.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_FILE = "hanpure_session.json"
HOME_URL = "https://hanpuremall.co.kr/"
OUT_DIR = Path("debug_output")

STAGES = [
    ("01_home", "홈 화면에서 상품을 검색해 검색 결과 목록까지 이동하세요."),
    ("02_search_result", "검색 결과에서 원하는 상품의 상세 페이지로 들어가세요."),
    ("03_product_detail", "상품을 장바구니에 담으세요."),
    ("04_cart", "장바구니에서 주문서 작성(배송지 등) 화면으로 이동하세요."),
    ("05_order_form", "결제 버튼을 누르기 '직전' 화면까지만 이동하세요. (누르지 마세요!)"),
]


def snapshot(page, name: str):
    page.screenshot(path=str(OUT_DIR / f"{name}.png"), full_page=True)
    (OUT_DIR / f"{name}.html").write_text(page.content(), encoding="utf-8")
    print(f"  -> {name}.png / {name}.html 저장, 현재 URL: {page.url}")


def main():
    if not Path(SESSION_FILE).exists():
        print(f"{SESSION_FILE} 이 없습니다. login_setup.py 를 먼저 실행하세요.")
        return

    OUT_DIR.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()
        page.goto(HOME_URL)
        page.wait_for_load_state("networkidle")

        print("=" * 60)
        print("각 단계 안내에 따라 브라우저를 직접 조작한 뒤 Enter를 누르세요.")
        print("절대 실제 결제 버튼은 누르지 마세요.")
        print("=" * 60)

        for name, instruction in STAGES:
            print(f"\n[{name}] {instruction}")
            input("이동/조작을 마쳤으면 Enter >> ")
            snapshot(page, name)

        print(f"\n모든 단계 저장 완료. {OUT_DIR}/ 폴더를 그대로 두세요.")
        input("확인했으면 Enter를 눌러 브라우저를 닫습니다 >> ")
        browser.close()


if __name__ == "__main__":
    main()
