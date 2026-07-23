# -*- coding: utf-8 -*-
"""
구분선 드롭다운의 실제 스타일 선택자, 그리고 인용구 적용 후 Enter를 눌렀을 때
실제로 무슨 일이 일어나는지 확인하기 위한 정찰용 스크립트.

각 단계마다 화면에서 직접 해당 동작을 수행한 뒤 터미널에서 Enter를
누르면, 그 시점의 스크린샷+HTML을 debug_output/dq_XX_*.png/html 로 남깁니다.
저장/발행은 하지 않습니다.

사용법: python inspect_divider_quote.py
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

        body_area = page.locator(".se-component.se-text .se-text-paragraph").first
        body_area.click()

        # --- 구분선 드롭다운 ---
        step(
            1,
            "상단 툴바의 '구분선' 아이콘 옆 화살표(또는 아이콘 자체)를 클릭해서\n"
            "구분선 스타일 목록(여러 종류의 선)이 펼쳐진 상태로 두세요.\n"
            "(아직 아무 스타일도 클릭하지 마세요!)",
        )
        debug_dump(page, "dq_01_divider_dropdown_open", True)

        step(
            2,
            "목록에서 '두 번째' 스타일(가장 긴 선)을 클릭해서 실제로 삽입하세요.",
        )
        debug_dump(page, "dq_02_divider_line1_applied", True)

        # --- 인용구 → Enter ---
        page.keyboard.type("인용구테스트문장", delay=20)
        debug_dump(page, "dq_03_before_quote_style", True)

        step(
            3,
            "방금 입력된 '인용구테스트문장' 줄에 커서를 두고,\n"
            "왼쪽 상단 스타일 드롭다운(본문/소제목/인용구)에서 '인용구'를 클릭하세요.",
        )
        debug_dump(page, "dq_04_quote_style_applied", True)

        step(
            4,
            "이제 그 줄 끝에서 Enter 키를 한 번 누르세요 (딱 한 번만).",
        )
        debug_dump(page, "dq_05_after_enter", True)

        step(
            5,
            "이어서 아무 문장이나 입력해보세요 (예: '다음문단테스트').\n"
            "입력한 텍스트가 인용구 스타일로 보이는지, 일반 본문으로 보이는지 확인.",
        )
        debug_dump(page, "dq_06_after_typing_next", True)

        print("\n모든 단계 완료. 브라우저를 닫습니다 (저장/발행 안 함).")
        browser.close()


if __name__ == "__main__":
    main()
