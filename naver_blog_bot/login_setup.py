"""
최초 1회 실행용 스크립트.

이 스크립트는 아이디/비밀번호를 절대 입력하지 않습니다.
브라우저 창이 열리면 사용자가 직접 네이버에 로그인하세요 (2단계 인증 포함).
로그인이 완료되면 세션(쿠키)을 naver_session.json 파일로 저장하고,
이후 publisher.py 는 이 파일을 재사용해 재로그인 없이 동작합니다.
"""

import traceback
from playwright.sync_api import sync_playwright

SESSION_FILE = "naver_session.json"
ERROR_LOG = "login_error.txt"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://nid.naver.com/nidlogin.login")

        print("=" * 60)
        print("브라우저 창에서 직접 네이버 아이디로 로그인해주세요.")
        print("(2단계 인증/캡차가 뜨면 화면 안내에 따라 직접 처리)")
        print("로그인 완료 후 이 터미널로 돌아와 Enter를 누르면")
        print(f"세션이 {SESSION_FILE} 로 저장됩니다.")
        print("=" * 60)
        input("로그인을 마쳤으면 Enter >> ")

        try:
            # 페이지 이동 없이 현재 컨텍스트의 쿠키만 확인 (이동 시 로그인 리다이렉트와
            # 충돌해 오류가 나는 문제를 피하기 위함)
            print(f"현재 페이지 주소: {page.url}")
            cookies = context.cookies()
            has_session_cookie = any(c["name"] == "NID_SES" for c in cookies)

            if not has_session_cookie:
                print("로그인 세션이 확인되지 않았습니다.")
                print("브라우저 창이 아직 로그인 화면/인증 화면에 머물러 있지 않은지 확인 후")
                print("완전히 로그인된 상태(네이버 메인이나 내 블로그 화면)에서 다시 실행해주세요.")
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
