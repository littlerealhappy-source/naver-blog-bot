"""
네이버 블로그 글쓰기 에디터의 실제 DOM 구조를 확인하기 위한 정찰용 스크립트.

브라우저 자동화 도구가 naver.com에 직접 접근하지 못하는 환경(정책 제한)에서
selector를 보정하기 위해, 사용자가 로컬에서 이 스크립트를 실행하고
결과 파일을 남기면 Claude가 그 파일을 읽어서 publisher.py의 selector를 고칩니다.

사용법:
    1) login_setup.py 를 먼저 실행해 naver_session.json 을 만들어 두세요.
    2) 아래 BLOG_ID 를 본인 블로그 ID로 바꾸세요.
    3) python inspect_editor.py 실행
    4) 브라우저 창에서 글쓰기 화면이 정상적으로 뜨는지 확인하고,
       (팝업이 있으면 직접 닫고) 터미널에서 Enter를 누르세요.
    5) inspect_output/ 폴더에 생성된 파일들을 그대로 두면 Claude가 읽습니다.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_FILE = "naver_session.json"
BLOG_ID = "littlerealhappy"
OUT_DIR = Path("inspect_output")


def main():
    if not Path(SESSION_FILE).exists():
        print(f"{SESSION_FILE} 이 없습니다. login_setup.py 를 먼저 실행하세요.")
        return

    OUT_DIR.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        page.goto(f"https://blog.naver.com/{BLOG_ID}/postwrite")
        page.wait_for_load_state("networkidle")

        print("=" * 60)
        print("글쓰기 화면이 떴는지 확인하세요.")
        print("'이어서 작성하시겠습니까?' 같은 팝업이 있으면 직접 닫아주세요.")
        print("준비되면 이 터미널로 돌아와 Enter >> ")
        print("=" * 60)
        input()

        page.screenshot(path=str(OUT_DIR / "full_page.png"), full_page=True)
        (OUT_DIR / "top_level.html").write_text(page.content(), encoding="utf-8")

        # mainFrame 안, 그리고 그 안의 se-iframe(있다면) 순서로 HTML 덤프
        try:
            main_frame_el = page.wait_for_selector("iframe#mainFrame", timeout=10000)
            main_frame = main_frame_el.content_frame()
            (OUT_DIR / "main_frame.html").write_text(main_frame.content(), encoding="utf-8")
            print("main_frame.html 저장 완료")

            se_iframe_el = main_frame.query_selector("iframe.se-iframe")
            if se_iframe_el:
                se_frame = se_iframe_el.content_frame()
                (OUT_DIR / "se_iframe.html").write_text(se_frame.content(), encoding="utf-8")
                print("se_iframe.html 저장 완료")
            else:
                print("se-iframe을 못 찾음 (mainFrame 안에 바로 에디터가 있을 수도 있음)")
        except Exception as e:
            print(f"프레임 탐색 중 오류: {e}")
            print("top_level.html 과 full_page.png 만으로 구조를 파악합니다.")

        print(f"\n결과가 {OUT_DIR}/ 에 저장되었습니다. 이 폴더를 그대로 두세요.")
        input("확인했으면 Enter를 눌러 브라우저를 닫습니다 >> ")
        browser.close()


if __name__ == "__main__":
    main()
