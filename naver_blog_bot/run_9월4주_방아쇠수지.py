# -*- coding: utf-8 -*-
"""
[원고] 아침마다 손가락이 굽은채 '딸깍' 걸리며 펴진다면

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보가 아닌 원장님이 직접 정한 제목).

내부 링크는 원고 본문에 직접 들어가 있다 ("손저림과는 다릅니다" 섹션의
손저림 글 URL) — 파서가 링크 카드로 변환하므로 여기서 따로 지정하지
않는다.

이 원고는 [권장 사진]이 5장이 아니라 4장이다.

사용법: python "run_9월4주_방아쇠수지.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월4주_A_방아쇠수지_원고.md"
TITLE = "아침마다 손가락이 굽은채 '딸깍' 걸리며 펴진다면"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("치료의 출발이라고 생각합니다.", "stock_images/trigger_01.jpg"),
    # 2. "방아쇠수지, 어떤 상태인가요?" 섹션
    ("특히 아침에 증상이 심한 것이 특징입니다.", "stock_images/trigger_02.jpg"),
    # 3. "한의원에서는 어떻게 접근하나요" 섹션
    ("순환을 돕습니다.", "stock_images/trigger_03.jpg"),
    # 4. 마무리 CTA 위
    ("살펴보시길 권해드립니다.", "stock_images/trigger_04.jpg"),
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
