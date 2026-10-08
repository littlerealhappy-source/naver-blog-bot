# -*- coding: utf-8 -*-
"""
[원고] 외출할 때마다 배가 아프고 화장실부터 찾게 된다면?

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보가 아닌 원장님이 직접 정한 제목).

내부 링크는 원고 본문에 직접 들어가 있다 ("검사엔 이상 없는데 왜
이럴까요" 섹션의 기능성 소화불량 글 URL) — 파서가 링크 카드로
변환하므로 여기서 따로 지정하지 않는다.

사용법: python "run_9월1주_과민성대장.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월1주_B_과민성대장_원고.md"
TITLE = "외출할 때마다 배가 아프고 화장실부터 찾게 된다면?"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("이 불편한 증상 이야기를 해보려 합니다.", "stock_images/ibs_01.jpg"),
    # 2. "검사엔 이상 없는데 왜 이럴까요" 섹션 (장 기능 설명 직후, 링크 카드 앞)
    ("증상이 나타나는 것입니다.", "stock_images/ibs_02.jpg"),
    # 3. "스트레스를 받으면 왜 배가 아플까요" 섹션
    ("잘 풀리지 않는 경우가 많습니다.", "stock_images/ibs_03.jpg"),
    # 4. "한의원에서는 어떻게 접근하나요" 섹션
    ("저희가 보는 방향입니다.", "stock_images/ibs_04.jpg"),
    # 5. 마무리 CTA 위
    ("고려해 보시길 권해드립니다.", "stock_images/ibs_05.jpg"),
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
