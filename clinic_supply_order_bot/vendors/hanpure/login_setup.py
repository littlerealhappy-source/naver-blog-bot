"""
최초 1회 실행용 스크립트.

이 스크립트는 아이디/비밀번호를 절대 입력하지 않습니다.
브라우저 창이 열리면 사용자가 직접 한퓨어몰에 로그인하세요.
로그인이 완료되면 세션(쿠키)을 hanpure_session.json 파일로 저장하고,
이후 order.py 는 이 파일을 재사용해 재로그인 없이 동작합니다.
"""

import traceback
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://hanpuremall.co.kr/shop2/?mode=login"
SESSION_FILE = "hanpure_session.json"
ERROR_LOG = "login_error.txt"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(LOGIN_URL)

        print("=" * 60)
        print("브라우저 창에서 직접 한퓨어몰 아이디로 로그인해주세요.")
        print("로그인 완료 후 이 터미널로 돌아와 Enter를 누르면")
        print(f"세션이 {SESSION_FILE} 로 저장됩니다.")
        print("=" * 60)
        input("로그인을 마쳤으면 Enter >> ")

        try:
            print(f"현재 페이지 주소: {page.url}")
            if "mode=login" in page.url:
                print("아직 로그인 페이지에 머물러 있는 것 같습니다.")
                print("완전히 로그인된 상태(마이페이지 등)에서 다시 실행해주세요.")
                return

            context.storage_state(path=SESSION_FILE)
            print(f"세션 저장 완료: {SESSION_FILE}")
        except Exception:
            with open(ERROR_LOG, "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
            print(f"오류가 발생했습니다. 자세한 내용은 {ERROR_LOG} 파일에 저장했습니다.")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
