# -*- coding: utf-8 -*-
"""
[원고] 사고 당일엔 멀쩡했는데, 며칠 뒤부터 아픈 이유

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보 3개 중 1번 선택).

원고에 명시된 대로 이번 글은 교통사고 클러스터의 첫 글이라 연결할 기존
교통사고 글이 없어 내부 링크 없음.

사용법: python "run_8월4주_교통사고후유증.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/8월4주_A_교통사고후유증_원고.md"
TITLE = "사고 당일엔 멀쩡했는데, 며칠 뒤부터 아픈 이유"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("교통사고 후유증 이야기를 해보려 합니다.", "stock_images/accident_01.jpg"),
    # 2. "왜 사고 다음 날부터 아플까요" 섹션
    ("오래 지속되는 통증을 남깁니다.", "stock_images/accident_02.jpg"),
    # 3. "한의원에서는 어떻게 접근하나요" 섹션
    ("저희가 보는 방향입니다.", "stock_images/accident_03.jpg"),
    # 4. "자동차보험으로 치료받으실 수 있습니다" 섹션
    ("편하게 문의 주세요.", "stock_images/accident_04.jpg"),
    # 5. 마무리 CTA 위
    ("카톡편지로 정리해 보내드립니다.", "stock_images/accident_05.jpg"),
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
