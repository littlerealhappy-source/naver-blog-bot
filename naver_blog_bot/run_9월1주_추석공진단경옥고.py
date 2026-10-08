# -*- coding: utf-8 -*-
"""
[원고] 추석 선물로 공진단과 경옥고, 무엇이 좋을까요

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보 3개 중 1번 선택).

내부 링크는 원고 본문에 직접 들어가 있다 ("저희 공진단은 이렇게
만듭니다" 섹션의 공진단 글 URL) — 파서가 링크 카드로 변환하므로
여기서 따로 지정하지 않는다.

사용법: python "run_9월1주_추석공진단경옥고.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월1주_C_추석공진단경옥고_원고.md"
TITLE = "추석 선물로 공진단과 경옥고, 무엇이 좋을까요"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("정리해 드리겠습니다.", "stock_images/chuseok_01.jpg"),
    # 2. "공진단, '황제의 명약'이라 불린 이유" 섹션
    ("쓰여 온 처방입니다.", "stock_images/chuseok_02.jpg"),
    # 3. "경옥고, 오래도록 사랑받아 온 보약" 섹션
    ("어르신 보양식으로 특히 사랑받아 왔습니다.", "stock_images/chuseok_03.jpg"),
    # 4. "저희 공진단은 이렇게 만듭니다" 섹션 (재료 설명 직후, 링크 카드 앞)
    ("저희 눈으로 확인한 공진단만 나갑니다.", "stock_images/chuseok_04.jpg"),
    # 5. "올 추석, 마음을 담은 선물" 섹션
    ("마음을 담을 수 있는 보약입니다.", "stock_images/chuseok_05.jpg"),
    # 6. 마무리
    ("성심을 다해 살펴보겠습니다.", "stock_images/chuseok_06.jpg"),
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
