# -*- coding: utf-8 -*-
"""
[원고] 조금만 걸어도 다리에 힘이 안 들어간다면, 지금 바로 치료받아야 합니다

이번 원고는 제목이 이미 확정되어 있고([제목] 섹션), 첫 줄(# ...)과도
동일해서 parse_manuscript가 읽은 제목을 그대로 쓴다.

사용법: python "run_8월1주_척추관협착증.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/8월1주_A_척추관협착증_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("척추관협착증 이야기를 해보려 합니다.", "stock_images/stenosis_01.jpg"),
    # 2. "척추관협착증, 어떤 상태인가요?" 섹션
    ("다리로 가는 신호에 문제가 생기는 것입니다.", "stock_images/stenosis_02.jpg"),
    # 3. "허리디스크와는 무엇이 다를까요?" 섹션
    ("정확한 감별이 먼저입니다.", "stock_images/stenosis_03.jpg"),
    # 4. "협착증, 이렇게 접근합니다" 섹션
    ("저희가 보는 방향입니다.", "stock_images/stenosis_04.jpg"),
    # 5. 마무리 CTA 위
    ("그 신호를 미루지 마시길 권해드립니다.", "stock_images/stenosis_05.jpg"),
]


if __name__ == "__main__":
    title, blocks, tags = parse_manuscript(MANUSCRIPT)
    blocks = insert_images_at_anchors(blocks, IMAGE_ANCHORS)

    print(f"제목: {title}")
    print(f"블록 수: {len(blocks)}, 태그: {tags}")

    publish_post(
        blog_id="littlerealhappy",
        title=title,
        blocks=blocks,
        tags=tags,
        publish=False,  # 임시저장까지만. 검토 후 발행은 별도 결정.
        headless=False,
        debug=True,
    )
