# -*- coding: utf-8 -*-
"""
[원고] 나잇살이 안 빠지는 건 의지가 아니라 근육 문제입니다

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (후보 3개 중 2번 선택, "부천한의원|" 접두어 없음).

사용법: python "run_7월4주_다이어트.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/7월4주_B_다이어트_원고.md"
TITLE = "나잇살이 안 빠지는 건 의지가 아니라 근육 문제입니다"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래 - 다이어트 클리닉 배너
    ("오늘은 그 이야기를 해보려 합니다.", "stock_images/diet_01.jpg"),
    # 2. "나잇살이 안 빠지는 진짜 이유" 섹션
    ("많은 분들이 여기에 해당하십니다.", "stock_images/diet_02.jpg"),
    # 3. "한약 다이어트는 무엇이 다른가" 섹션
    ("이것이 한약 다이어트의 강점입니다.", "stock_images/diet_03.jpg"),
    # 4. "나에게 맞는 다이어트인지가 먼저입니다" 섹션 - 맥파진단/인바디
    ("접근을 다르게 합니다.", "stock_images/diet_04.jpg"),
    # 5. 마무리 CTA 위
    ("따져보실 때입니다.", "stock_images/diet_05.jpg"),
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
