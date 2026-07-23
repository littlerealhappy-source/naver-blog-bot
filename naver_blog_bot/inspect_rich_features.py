"""
링크 삽입, 강조색, 소제목 스타일, 구분선, 태그 입력란의 실제 UI 구조를
확인하기 위한 정찰용 스크립트.

각 단계마다 화면에서 직접 해당 동작을 수행한 뒤 터미널에서 Enter를
누르면, 그 시점의 스크린샷+HTML을 debug_output/rich_XX_*.png/html 로
남깁니다. 실제로 저장/발행은 하지 않습니다 (마지막에 그냥 브라우저를 닫음).

사용법: python inspect_rich_features.py
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

from publisher import (
    SESSION_FILE,
    debug_dump,
    dismiss_continue_dialog,
    dismiss_help_panel,
)

BLOG_ID = "littlerealhappy"


def step(n, instruction):
    print("\n" + "=" * 60)
    print(f"[{n}단계] {instruction}")
    input(">> 완료했으면 Enter >> ")


def main():
    if not Path(SESSION_FILE).exists():
        print(f"{SESSION_FILE} 이 없습니다. login_setup.py 를 먼저 실행하세요.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        page.goto(f"https://blog.naver.com/{BLOG_ID}/postwrite")
        page.locator(".se-title-text").first.wait_for(state="visible", timeout=30000)

        dismiss_continue_dialog(page)
        dismiss_help_panel(page)

        # 작업할 문장을 미리 입력해둠
        body_area = page.locator(".se-component.se-text .se-text-paragraph").first
        body_area.click()
        page.keyboard.type("테스트 링크용 문장입니다", delay=15)
        debug_dump(page, "rich_00_initial_text", True)

        step(
            1,
            "방금 입력된 문장을 마우스로 드래그해서 전체 선택한 다음,\n"
            "상단 툴바의 '링크' 아이콘을 클릭하세요.\n"
            "링크 입력창(URL 입력 팝업)이 뜬 상태로 두세요.",
        )
        debug_dump(page, "rich_01_link_dialog_open", True)

        step(
            2,
            "그 입력창에 https://naver.com 을 입력하고 확인(또는 Enter)을 눌러\n"
            "링크를 적용하세요.",
        )
        debug_dump(page, "rich_02_link_applied", True)

        step(
            3,
            "이번엔 새 줄에 아무 문장이나 입력한 후 드래그로 전체 선택하고,\n"
            "글자색/강조색 버튼을 눌러 색상 팔레트가 뜬 상태로 두세요.",
        )
        debug_dump(page, "rich_03_color_palette_open", True)

        step(
            4,
            "팔레트에서 원하는 색상을 하나 클릭해 적용하세요.",
        )
        debug_dump(page, "rich_04_color_applied", True)

        step(
            5,
            "새 줄에 '소제목 테스트' 라고 입력한 후, 커서가 그 줄에 있는 상태에서\n"
            "왼쪽 상단의 스타일 드롭다운(보통 '본문'이라고 쓰여있는 곳)을 클릭해\n"
            "목록이 펼쳐진 상태로 두세요.",
        )
        debug_dump(page, "rich_05_style_dropdown_open", True)

        step(
            6,
            "목록에서 소제목에 해당하는 스타일을 클릭해 적용하세요.",
        )
        debug_dump(page, "rich_06_subheading_applied", True)

        step(
            7,
            "새 줄에서 상단 툴바의 '구분선' 아이콘을 클릭하세요.\n"
            "스타일 메뉴가 뜨면 아무거나 하나 선택해서 실제로 삽입까지 해주세요.",
        )
        debug_dump(page, "rich_07_divider_applied", True)

        step(
            8,
            "마지막으로 태그를 입력할 수 있는 곳을 찾아 '테스트태그' 라고 입력해보세요.\n"
            "화면에 안 보이면 아래로 스크롤해서 찾아보세요.\n"
            "(주의: 발행 버튼을 눌러 설정 패널에서 찾아야 한다면 괜찮지만,\n"
            "최종 '발행' 확인 버튼은 누르지 마세요!)",
        )
        debug_dump(page, "rich_08_tag_input", True)

        print("\n모든 단계 완료. 브라우저를 닫습니다 (저장/발행 안 함).")
        browser.close()


if __name__ == "__main__":
    main()
