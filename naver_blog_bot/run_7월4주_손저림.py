# -*- coding: utf-8 -*-
"""
[원고] 손이 저릴때, 손목만 봐서는 낫지 않는 진짜 이유

원고 파일의 첫 줄(# ...)은 "(제목은 원장님이 확정 / 후보는 하단 참고)"라는
자리표시일 뿐이라 실제 제목은 아래 TITLE로 직접 지정한다 (사용자가 후보
중 문구를 다듬어 확정, "부천한의원|" 접두어는 붙이지 않기로 함).

사용법: python "run_7월4주_손저림.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = r"C:\Users\SAMSUNG\Downloads\7월4주_A_손저림_원고 (1).md"
TITLE = "손이 저릴때, 손목만 봐서는 낫지 않는 진짜 이유"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("오늘은 그 이야기를 해보려 합니다.", "stock_images/handnumb_01.jpg"),
    # 2. "손저림, 손목 문제일까 목 문제일까" 섹션
    ("정확히 확인하는 것이 안전합니다.", "stock_images/handnumb_02.jpg"),
    # 3. "목과 어깨를 함께 보는 치료" 섹션
    ("치료도 두 곳을 함께 다루었습니다.", "stock_images/handnumb_03.jpg"),
    # 4. "집에서 지켜주시면 좋은 것들" 섹션
    ("회복의 한 과정입니다.", "stock_images/handnumb_04.jpg"),
    # 5. 마무리 CTA 위
    ("한 번쯤 목까지 확인해 보시길 권해드립니다.", "stock_images/handnumb_05.jpg"),
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
