# -*- coding: utf-8 -*-
"""
[원고] 부천한의원 목디스크 이렇게 접근해야 빨리 낫습니다.

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (사용자 지정 제목, 후보 목록과는 별개).

사용법: python "run_8월2주_목디스크.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = r"C:\Users\SAMSUNG\Downloads\8월2주_A_목디스크_원고.md"
TITLE = "부천한의원 목디스크 이렇게 접근해야 빨리 낫습니다."

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("오늘은 목디스크 이야기를 해보려 합니다.", "stock_images/neck_01.jpg"),
    # 2. "목디스크, 어떤 상태인가요?" 섹션
    ("정작 원인인 목은 그대로 남게 됩니다.", "stock_images/neck_02.jpg"),
    # 3. "이런 증상이 있다면 목을 의심해 보세요" 섹션
    ("꽤 분명한 신호입니다.", "stock_images/neck_03.jpg"),
    # 4. "목디스크, 이렇게 접근합니다" 섹션
    ("저희가 보는 방향입니다.", "stock_images/neck_04.jpg"),
    # 5. 마무리 CTA 위
    ("그 신호를 미루지 마시길 권해드립니다.", "stock_images/neck_05.jpg"),
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
