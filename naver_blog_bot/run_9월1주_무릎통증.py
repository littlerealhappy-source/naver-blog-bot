# -*- coding: utf-8 -*-
"""
[원고] 계단 내려갈 때 무릎이 시큰하다면, 이유는 3가지입니다.

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보가 아닌 원장님이 직접 정한 제목).

원고에 명시된 대로 이번 글은 무릎 클러스터의 첫 글이라 연결할 기존
무릎 글이 없어 내부 링크 없음.

사용법: python "run_9월1주_무릎통증.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월1주_A_무릎통증_원고.md"
TITLE = "계단 내려갈 때 무릎이 시큰하다면, 이유는 3가지입니다."

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("무릎 통증 이야기를 해보려 합니다.", "stock_images/knee_01.jpg"),
    # 2. "무릎은 왜 아플까요" 섹션
    ("균형 문제인 경우가 많습니다.", "stock_images/knee_02.jpg"),
    # 3. "나이에 따라 원인이 다릅니다" 섹션
    ("정확히 확인하는 것이 먼저입니다.", "stock_images/knee_03.jpg"),
    # 4. "한의원에서는 어떻게 접근하나요" 섹션
    ("저희가 보는 방향입니다.", "stock_images/knee_04.jpg"),
    # 5. 마무리 CTA 위
    ("카톡편지로 정리해 보내드립니다.", "stock_images/knee_05.jpg"),
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
