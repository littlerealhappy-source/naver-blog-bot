# -*- coding: utf-8 -*-
"""
[원고] 등이 결리고 아픈 자리가 돌아다닌다면, 파스로는 안 됩니다.

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보가 아닌 원장님이 직접 정한 제목).

원고에 명시된 대로 이번 글은 등·견갑골 클러스터의 첫 글이라 연결할
기존 글이 없어 내부 링크 없음.

이 원고는 [권장 사진]이 5장이 아니라 4장이다.

사용법: python "run_9월3주_등견갑골통증.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월3주_A_등견갑골통증_원고.md"
TITLE = "등이 결리고 아픈 자리가 돌아다닌다면, 파스로는 안 됩니다."

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("구조적으로 짚어 치료합니다.", "stock_images/back_01.jpg"),
    # 2. "통증이 '돌아다니는' 이유" 섹션
    ("돌아가며 비명을 지르는 셈입니다.", "stock_images/back_02.jpg"),
    # 3. "등 담결림, 이렇게 치료합니다" 섹션
    ("저희가 보는 목표입니다.", "stock_images/back_03.jpg"),
    # 4. 마무리 CTA 위
    ("카톡편지로 정리해 보내드립니다.", "stock_images/back_04.jpg"),
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
