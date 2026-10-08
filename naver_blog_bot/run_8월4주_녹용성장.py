# -*- coding: utf-8 -*-
"""
[원고] 또래보다 작은 우리 아이, '크겠지' 하고 기다려도 될까요

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보 3개 중 1번 선택).

내부 링크는 원고 본문에 직접 들어가 있다 ("성장은 녹용 하나로 되지
않습니다" 섹션의 녹용품질 글 URL) — 파서가 링크 카드로 변환하므로
여기서 따로 지정하지 않는다.

사용법: python "run_8월4주_녹용성장.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/8월4주_B_녹용성장_원고.md"
TITLE = "또래보다 작은 우리 아이, '크겠지' 하고 기다려도 될까요"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("해보려 합니다.", "stock_images/growth_01.jpg"),
    # 2. "키에는 '골든타임'이 있습니다" 섹션
    ("무엇보다 중요합니다.", "stock_images/growth_02.jpg"),
    # 3. "우리 아이, 지금 어디쯤 자라고 있을까요" 섹션
    ("찾아보시는 것이 좋습니다.", "stock_images/growth_03.jpg"),
    # 4. "성장에 녹용이 도움이 될까요" 섹션
    ("처방이 달라져야 합니다.", "stock_images/growth_04.jpg"),
    # 5. 마무리 CTA 위
    ("가장 중요한 일입니다.", "stock_images/growth_05.jpg"),
]


if __name__ == "__main__":
    _, blocks, tags = parse_manuscript(MANUSCRIPT)
    blocks = insert_images_at_anchors(blocks, IMAGE_ANCHORS)

    print(f"제목: {TITLE}")
    print(f"블록 수: {len(blocks)}, 태그: {tags}")

    publish_post(
        blog_id="littlerealhappy",
        title=TITLE,
        blocks=blocks,
        tags=tags,
        publish=False,  # 임시저장까지만. 검토 후 발행은 별도 결정.
        headless=False,
        debug=True,
    )
