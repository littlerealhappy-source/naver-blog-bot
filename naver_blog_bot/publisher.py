"""
저장된 세션(naver_session.json)으로 네이버 블로그 글쓰기 페이지에 접속해
제목/본문(문단·소제목·구분선·사진·링크카드)/태그를 입력하고 발행(또는 임시저장
상태로 두기)까지 수행하는 스크립트.

실제 blog.naver.com/{id}/postwrite 화면을 inspect_editor.py, inspect_rich_features.py
로 분석해 확인한 구조 기준 (2026-07 시점):
- 에디터는 iframe이 아니라 최상위 페이지에 바로 렌더링됨
- 제목: .se-title-text .se-text-paragraph
- 본문 컴포넌트: .se-component.se-text .se-text-paragraph
- 사진 툴바 버튼: button[data-group="documentToolbar"][data-name="image"]
- 링크(=OG 미리보기 카드, 인라인 하이퍼링크 아님):
  button[data-group="documentToolbar"][data-name="oglink"] -> URL 입력
  (input.se-popup-oglink-input) -> 확인(button.se-popup-button-confirm)
- 글자색: 텍스트 선택 후 button[data-group="propertyToolbar"][data-name="font-color"]
  -> 팔레트에서 button.se-color-palette[data-color="#RRGGBB"] 클릭
- 소제목: 커서가 해당 줄에 있는 상태에서
  button.se-text-format-toolbar-button[data-name="text-format"] 클릭 후
  button[data-name="text-format"][data-value="sectionTitle"] 클릭
  (본문으로 되돌릴 땐 data-value="text")
- 구분선: button[data-group="documentToolbar"][data-name="horizontal-line"]
- 발행 버튼(1차): button[data-click-area="tpb.publish"] -> 설정 패널이 뜸
  - 태그 입력: input#tag-input (텍스트 입력 후 Enter로 태그 추가)
  - 최종 발행 확인: button[data-testid="seOnePublishBtn"]
- 저장(임시저장) 버튼: button[data-click-area="tpb.save"]
- 화면에 보이지 않는 동일 구조의 숨겨진 사본이 DOM에 존재하는 경우가 있어,
  텍스트/role 기반으로 요소를 찾을 땐 항상 :visible 로 필터링해야 함

콘텐츠는 블록 리스트로 표현한다 (자세한 형식은 make_paragraph_blocks 등 참고):
  {"type": "paragraph", "runs": [{"text": "..."}, {"text": "...", "color": "#ff0010"}]}
  {"type": "subheading", "text": "..."}
  {"type": "divider"}
  {"type": "image", "path": "..."}
  {"type": "link_card", "url": "..."}

주의: 네이버가 화면 구조를 바꾸면 이 셀렉터들도 깨질 수 있습니다.
오류 시 debug_output/error_screenshot.png 와 error_traceback.txt 를 보고 다시 보정하세요.
"""

import re
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, TimeoutError as PWTimeout

SESSION_FILE = "naver_session.json"
DEBUG_DIR = Path("debug_output")
DEFAULT_EMPHASIS_COLOR = "#ff0010"


def debug_dump(page: Page, tag: str, enabled: bool):
    if not enabled:
        return
    DEBUG_DIR.mkdir(exist_ok=True)
    page.screenshot(path=str(DEBUG_DIR / f"{tag}.png"), full_page=True)
    (DEBUG_DIR / f"{tag}.html").write_text(page.content(), encoding="utf-8")


def dismiss_continue_dialog(page: Page):
    """'작성 중인 글이 있습니다' 팝업이 뜨면 취소(새 글 시작).

    같은 구조의 숨겨진 사본이 DOM에 더 있을 수 있어 :visible 로 화면에
    실제로 보이는 버튼만 선택한다.
    """
    try:
        page.locator(".se-popup-button-cancel:visible").first.click(timeout=3000)
        print("이어서 작성 팝업을 감지해 취소를 눌렀습니다.")
        page.wait_for_timeout(500)
    except PWTimeout:
        print("이어서 작성 팝업이 감지되지 않았습니다 (없었거나 이미 닫혀있음).")


def dismiss_alert_popup(page: Page) -> str | None:
    """'파일 전송 오류' 등 확인 버튼만 있는 알림 팝업이 떠 있으면 닫는다.

    팝업 제목을 반환하고, 팝업이 없으면 None을 반환한다.
    """
    try:
        confirm_btn = page.locator(".se-popup-button-confirm:visible").first
        confirm_btn.wait_for(state="visible", timeout=800)
    except PWTimeout:
        return None
    try:
        title = page.locator(".se-popup-title:visible").first.inner_text(timeout=1000)
    except Exception:
        title = "(제목 확인 실패)"
    confirm_btn.click()
    page.wait_for_timeout(500)
    return title


def get_saved_count(page: Page) -> int | None:
    """저장 버튼 옆의 임시저장 글 개수를 읽는다 (저장 성공 검증용)."""
    try:
        label = (
            page.locator('button[aria-label*="임시저장된 글"]').first.get_attribute(
                "aria-label", timeout=2000
            )
            or ""
        )
        m = re.search(r"(\d+)", label)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def dismiss_help_panel(page: Page):
    """우측에 뜨는 '도움말' 패널이 저장/발행 버튼을 가리는 걸 막기 위해 닫는다."""
    try:
        page.locator("button.se-help-panel-close-button:visible").first.click(timeout=3000)
        print("도움말 패널을 닫았습니다.")
    except PWTimeout:
        print("도움말 패널이 감지되지 않았습니다 (없었거나 이미 닫혀있음).")


def type_title(page: Page, title: str):
    title_area = page.locator(".se-title-text .se-text-paragraph").first
    title_area.click()
    page.keyboard.type(title, delay=50)


# ---------------------------------------------------------------------------
# 인라인 서식 (글자색)
# ---------------------------------------------------------------------------

def apply_font_color(page: Page, hex_color: str):
    """커서의 '펜' 색을 바꾼다. 선택 영역이 없어도 이후 타이핑에 적용된다."""
    page.locator(
        'button[data-group="propertyToolbar"][data-name="font-color"]:visible'
    ).first.click()
    page.locator(
        f'button.se-color-palette[data-color="{hex_color}"]:visible'
    ).first.click()


DEFAULT_TEXT_COLOR = "#000000"


TYPING_DELAY_MS = 25  # 키 입력 간격. 너무 빠르면 에디터/서버가 따라오지 못한다.
ACTION_PAUSE_MS = 900  # 툴바 클릭/단축키 등 동작 사이의 여유 시간.


def type_run(page: Page, run: dict):
    """타이핑 후 드래그로 선택해 서식을 입히는 방식은 타이핑이 에디터에
    완전히 반영되기 전에 선택 동작이 끼어드는 race condition으로 텍스트가
    사라지는 문제가 있었다. 그래서 서식(볼드/색)을 먼저 켠 상태로 타이핑하고,
    끝나면 다시 꺼서 다음 텍스트에 영향이 없도록 하는 방식으로 바꿨다.
    """
    text = run["text"]
    bold = run.get("bold")
    color = run.get("color")

    if bold:
        page.keyboard.press("Control+b")
        page.wait_for_timeout(ACTION_PAUSE_MS)
    if color:
        apply_font_color(page, color)
        page.wait_for_timeout(ACTION_PAUSE_MS)

    page.keyboard.type(text, delay=TYPING_DELAY_MS)
    page.wait_for_timeout(ACTION_PAUSE_MS)  # 타이핑이 에디터에 반영될 시간을 줌

    if bold:
        page.keyboard.press("Control+b")
        page.wait_for_timeout(ACTION_PAUSE_MS)
    if color:
        apply_font_color(page, DEFAULT_TEXT_COLOR)
        page.wait_for_timeout(ACTION_PAUSE_MS)


# ---------------------------------------------------------------------------
# 블록 단위 구성요소
# ---------------------------------------------------------------------------

def set_current_line_style(page: Page, value: str):
    """value: "text"(본문) 또는 "sectionTitle"(소제목)."""
    page.locator(
        'button.se-text-format-toolbar-button[data-name="text-format"]:visible'
    ).first.click()
    page.wait_for_timeout(ACTION_PAUSE_MS)
    page.locator(
        f'button[data-name="text-format"][data-value="{value}"]:visible'
    ).first.click()
    page.wait_for_timeout(ACTION_PAUSE_MS)


def type_subheading(page: Page, text: str):
    page.keyboard.type(text, delay=TYPING_DELAY_MS)
    set_current_line_style(page, "sectionTitle")
    page.keyboard.press("Enter")
    set_current_line_style(page, "text")  # 다음 줄은 다시 본문 스타일로


def type_quote(page: Page, text: str):
    """인용구 입력.

    소제목과 달리 텍스트 스타일 토글이 아니라, 클릭하는 순간 '내용을
    입력하세요' / '출처 입력' 두 칸짜리 별도 블록(se-quotation)이 새로
    삽입되고 내용 입력란에 자동으로 포커스가 이동한다. 그래서 텍스트를
    먼저 쓰면 안 되고, 빈 줄에서 스타일을 먼저 적용해야 한다.
    """
    set_current_line_style(page, "quotation")
    page.wait_for_timeout(ACTION_PAUSE_MS)
    # 인용구 블록 삽입과 동시에 '내용을 입력하세요' 입력란에 포커스가 가 있다.
    page.keyboard.type(text, delay=TYPING_DELAY_MS)
    # 인용구 내용칸 안에서는 Escape/Enter가 블록을 못 벗어나고 내용칸 안에
    # 문단만 계속 쌓인다. type_quote 호출 시점엔 인용구가 항상 지금까지
    # 작성한 내용의 맨 끝이므로, 문서 맨 끝의 '본문 추가' 버튼을 눌러
    # 새 본문 문단으로 확실히 빠져나온다.
    page.locator("button.se-canvas-bottom-button:visible").first.click()
    page.wait_for_timeout(ACTION_PAUSE_MS)


def insert_divider(page: Page, style: str = "line1"):
    """구분선 삽입. style: "default"(짧은 선), "line1"(두 번째, 가장 긴 선) 등.

    툴바의 구분선 드롭다운 화살표를 눌러 스타일 목록을 연 뒤 원하는 스타일을
    직접 선택한다 (기본 버튼만 누르면 마지막 사용 스타일이 들어가서 예측 불가).
    """
    page.locator(
        'button[data-group="documentToolbar"][data-name="horizontal-line"]'
        '[aria-haspopup="true"]:visible'
    ).first.click()
    page.wait_for_timeout(ACTION_PAUSE_MS)
    page.locator(
        f'button[data-group="documentToolbar"][data-name="horizontal-line"]'
        f'[data-role="option"][data-value="{style}"]:visible'
    ).first.click()
    page.wait_for_timeout(ACTION_PAUSE_MS)


def insert_image(page: Page, image_path: str, retries: int = 3):
    """툴바의 사진 버튼을 클릭해 뜨는 OS 파일 선택창에 파일을 넣는다.

    '파일 전송 오류' 같은 일시적 오류 팝업이 뜨면 닫고 잠시 기다렸다 재시도한다.
    """
    for attempt in range(1, retries + 1):
        image_button = page.locator(
            'button[data-group="documentToolbar"][data-name="image"]:visible'
        ).first

        with page.expect_file_chooser() as fc_info:
            image_button.click()
        file_chooser = fc_info.value
        file_chooser.set_files(str(Path(image_path).resolve()))

        # 업로드 반영 대기 (썸네일이 본문에 삽입될 때까지)
        page.wait_for_timeout(4000)

        popup_title = dismiss_alert_popup(page)
        if popup_title is None:
            return
        print(f"이미지 업로드 중 팝업 감지({popup_title}) — {attempt}/{retries}회, 10초 후 재시도")
        page.wait_for_timeout(10000)

    raise RuntimeError(f"이미지 업로드가 {retries}회 연속 실패했습니다: {image_path}")


def insert_link_card(page: Page, url: str):
    page.locator(
        'button[data-group="documentToolbar"][data-name="oglink"]:visible'
    ).first.click()

    url_input = page.locator("input.se-popup-oglink-input:visible").first
    url_input.click()
    url_input.fill(url)
    page.wait_for_timeout(ACTION_PAUSE_MS)

    # URL 입력만으로는 확인 버튼이 활성화되지 않고,
    # 돋보기(검색) 버튼을 눌러 미리보기를 불러와야 한다.
    page.locator("button.se-popup-oglink-button:visible").first.click()

    # 미리보기 로딩이 끝나 확인 버튼이 활성화(disabled 해제)될 때까지 대기
    confirm_btn = page.locator(
        "button.se-popup-button-confirm:visible:not([disabled])"
    ).first
    confirm_btn.wait_for(state="visible", timeout=15000)
    confirm_btn.click()
    page.wait_for_timeout(1500)


# ---------------------------------------------------------------------------
# 블록 리스트 실행
# ---------------------------------------------------------------------------

def type_content_blocks(page: Page, blocks: list[dict]):
    body_area = page.locator(".se-component.se-text .se-text-paragraph").first
    body_area.click()

    for block in blocks:
        # 이미지 업로드 실패 알림 등이 비동기로 늦게 뜨는 경우가 있어,
        # 블록을 처리하기 전마다 떠 있는 팝업을 청소한다.
        popup_title = dismiss_alert_popup(page)
        if popup_title:
            print(f"블록 처리 전 팝업을 닫았습니다: {popup_title}")

        btype = block["type"]
        if btype == "paragraph":
            for run in block["runs"]:
                type_run(page, run)
            page.keyboard.press("Enter")
            # 문단 사이에 빈 줄을 넣어 여백을 준다 (blank_after: false로 끌 수 있음)
            if block.get("blank_after", True):
                page.keyboard.press("Enter")
            page.wait_for_timeout(300)  # 문단 사이 잠깐 숨 고르기
        elif btype == "subheading":
            type_subheading(page, block["text"])
        elif btype == "quote":
            type_quote(page, block["text"])
            if block.get("blank_after", True):
                page.keyboard.press("Enter")
        elif btype == "divider":
            insert_divider(page)
        elif btype == "image":
            insert_image(page, block["path"])
            page.keyboard.press("Enter")
        elif btype == "link_card":
            insert_link_card(page, block["url"])
        else:
            raise ValueError(f"알 수 없는 블록 타입: {btype}")


def make_paragraph_blocks(paragraphs: list[str], image_paths: list[str]) -> list[dict]:
    """예전 방식(문단 문자열 리스트 + 이미지 경로 리스트)을 블록으로 변환."""
    blocks = []
    img_idx = 0
    for para in paragraphs:
        blocks.append({"type": "paragraph", "runs": [{"text": para}]})
        if img_idx < len(image_paths):
            blocks.append({"type": "image", "path": image_paths[img_idx]})
            img_idx += 1
    while img_idx < len(image_paths):
        blocks.append({"type": "image", "path": image_paths[img_idx]})
        img_idx += 1
    return blocks


# ---------------------------------------------------------------------------
# 태그 / 발행 / 저장
# ---------------------------------------------------------------------------

def set_tags(page: Page, tags: list[str]):
    if not tags:
        return
    tag_input = page.locator("input#tag-input:visible").first
    for tag in tags:
        tag_input.click()
        tag_input.type(tag, delay=TYPING_DELAY_MS)
        page.keyboard.press("Enter")


def click_publish(page: Page, tags: list[str], debug: bool):
    page.locator('button[data-click-area="tpb.publish"]:visible').first.click()
    final_btn = page.locator('button[data-testid="seOnePublishBtn"]:visible').first
    final_btn.wait_for(state="visible", timeout=10000)

    set_tags(page, tags)
    debug_dump(page, "05_publish_panel_ready", debug)

    final_btn.click()


def click_save(page: Page, retries: int = 3):
    """저장 버튼을 누르고, 임시저장 개수가 늘었는지로 성공을 검증한다.

    오류 팝업이 뜨면 닫고 잠시 기다렸다 재시도한다.
    """
    for attempt in range(1, retries + 1):
        popup_title = dismiss_alert_popup(page)
        if popup_title:
            print(f"저장 전에 떠 있던 팝업을 닫았습니다: {popup_title}")

        before = get_saved_count(page)
        page.locator('button[data-click-area="tpb.save"]:visible').first.click()
        page.wait_for_timeout(2500)

        popup_title = dismiss_alert_popup(page)
        if popup_title:
            print(f"저장 중 팝업 감지({popup_title}) — {attempt}/{retries}회, 5초 후 재시도")
            page.wait_for_timeout(5000)
            continue

        after = get_saved_count(page)
        if before is not None and after is not None:
            if after > before:
                print(f"저장 확인됨 (임시저장 {before}개 -> {after}개)")
                return
            print(f"저장 개수가 늘지 않음({before} -> {after}) — {attempt}/{retries}회, 재시도")
            page.wait_for_timeout(3000)
            continue

        # 개수를 읽지 못한 경우: 팝업이 없었다면 성공으로 간주
        print("저장 완료 (임시저장 개수는 확인 불가).")
        return

    raise RuntimeError(f"저장이 {retries}회 연속 실패했습니다.")


def open_editor_with_relogin(page: Page, context, blog_id: str, headless: bool):
    """글쓰기 페이지로 이동한다. 저장된 세션이 만료되어 로그인 페이지로
    돌려보내지면, (headless가 아닐 경우) 그 자리에서 사용자가 직접
    로그인하도록 기다렸다가 세션을 새로 저장하고 이어서 진행한다.
    login_setup.py를 따로 실행하고 전체를 재실행하지 않아도 되게 하기 위함.
    """
    url = f"https://blog.naver.com/{blog_id}/postwrite"
    page.goto(url)
    try:
        page.locator(".se-title-text").first.wait_for(state="visible", timeout=30000)
        return
    except PWTimeout:
        if "nid.naver.com" not in page.url:
            raise

    if headless:
        raise RuntimeError(
            "저장된 로그인 세션이 만료되었습니다. headless=True 라서 이 자리에서\n"
            "로그인을 받을 수 없으니, headless=False 로 한 번 실행해 재로그인하세요."
        )

    print("=" * 60)
    print("저장된 로그인 세션이 만료되어 네이버가 로그인 페이지로 돌려보냈습니다.")
    print("지금 뜬 브라우저 창에서 직접 로그인해주세요 (2단계 인증 포함).")
    print("로그인 완료 후 이 터미널로 돌아와 Enter를 누르면 세션을 새로")
    print("저장하고 이어서 자동으로 진행합니다.")
    print("=" * 60)
    input("로그인을 마쳤으면 Enter >> ")

    cookies = context.cookies()
    if not any(c["name"] == "NID_SES" for c in cookies):
        raise RuntimeError("로그인이 확인되지 않았습니다. 완전히 로그인한 뒤 다시 실행하세요.")

    context.storage_state(path=SESSION_FILE)
    print(f"세션을 새로 저장했습니다: {SESSION_FILE}")

    page.goto(url)
    page.locator(".se-title-text").first.wait_for(state="visible", timeout=30000)


def publish_post(
    title: str,
    blog_id: str,
    blocks: list[dict] | None = None,
    paragraphs: list[str] | None = None,
    image_paths: list[str] | None = None,
    tags: list[str] | None = None,
    publish: bool = False,
    headless: bool = False,
    debug: bool = True,
):
    """blocks 를 직접 넘기거나, 예전 방식대로 paragraphs+image_paths 를 넘겨도 된다."""
    if not Path(SESSION_FILE).exists():
        raise FileNotFoundError(
            f"{SESSION_FILE} 이 없습니다. 먼저 login_setup.py 를 실행해 세션을 저장하세요."
        )

    if blocks is None:
        blocks = make_paragraph_blocks(paragraphs or [], image_paths or [])

    image_blocks = [b["path"] for b in blocks if b["type"] == "image"]
    missing = [p for p in image_blocks if not Path(p).exists()]
    if missing:
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {missing}")

    tags = tags or []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=SESSION_FILE)
        # 링크 팝업이 클립보드를 읽으려 할 때 크롬 권한 창이 떠서 자동화가
        # 막히는 것을 방지하기 위해 클립보드 권한을 미리 허용해 둔다.
        context.grant_permissions(
            ["clipboard-read", "clipboard-write"], origin="https://blog.naver.com"
        )
        page = context.new_page()

        open_editor_with_relogin(page, context, blog_id, headless)

        try:
            debug_dump(page, "01_initial", debug)
            dismiss_continue_dialog(page)
            debug_dump(page, "02_after_continue_dialog", debug)

            type_title(page, title)
            type_content_blocks(page, blocks)
            debug_dump(page, "03_after_typing", debug)

            dismiss_help_panel(page)
            debug_dump(page, "04_after_help_dismiss", debug)

            if publish:
                print("발행을 시도합니다.")
                click_publish(page, tags, debug)
                page.wait_for_timeout(3000)
                debug_dump(page, "06_after_publish", debug)
                print("발행 완료.")
            else:
                print("저장 버튼을 클릭합니다 (발행은 하지 않음).")
                click_save(page)
                print("저장 완료.")
        except Exception as e:
            DEBUG_DIR.mkdir(exist_ok=True)
            page.screenshot(path=str(DEBUG_DIR / "error_screenshot.png"), full_page=True)
            (DEBUG_DIR / "error_traceback.txt").write_text(traceback.format_exc(), encoding="utf-8")
            print(f"오류 발생: {e}")
            print(f"디버깅용 파일 저장: {DEBUG_DIR}/error_screenshot.png, {DEBUG_DIR}/error_traceback.txt")
            raise
        finally:
            if not headless:
                page.wait_for_timeout(3000)
            browser.close()


if __name__ == "__main__":
    publish_post(
        blog_id="littlerealhappy",
        title="테스트 제목입니다",
        blocks=[
            {"type": "paragraph", "runs": [{"text": "이것은 첫 번째 문단입니다."}]},
            {"type": "image", "path": "test_images/test1.jpg"},
            {"type": "divider"},
            {"type": "subheading", "text": "소제목 예시"},
            {
                "type": "paragraph",
                "runs": [
                    {"text": "이 문장 중 "},
                    {"text": "강조된 부분", "color": DEFAULT_EMPHASIS_COLOR},
                    {"text": "이 있습니다."},
                ],
            },
            {
                "type": "paragraph",
                "runs": [{"text": "아래는 링크 카드 테스트입니다."}],
            },
            {"type": "link_card", "url": "https://blog.naver.com/littlerealhappy/224341878179"},
        ],
        tags=["테스트태그1", "테스트태그2"],
        publish=False,
        headless=False,
        debug=True,
    )
