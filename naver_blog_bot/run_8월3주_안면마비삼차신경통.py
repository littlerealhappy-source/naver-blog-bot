# -*- coding: utf-8 -*-
"""
[원고] 삼차신경통과 안면마비, 얼굴 문제라고 다 같지 않습니다

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보 3개 중 3번 선택).

원고에 명시된 대로 이번 글은 연결할 기존 안면마비 글이 없어 내부 링크
없음 (다음 회차에 상호 링크 예정).

사용법: python "run_8월3주_안면마비삼차신경통.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/8월3주_A_안면마비삼차신경통_원고.md"
TITLE = "삼차신경통과 안면마비, 얼굴 문제라고 다 같지 않습니다"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("오늘은 그 이야기를 해보려 합니다.", "stock_images/facial_01.jpg"),
    # 2. "얼굴에는 서로 다른 두 신경이 있습니다" 섹션
    ("전혀 다른 증상이 나타나는 것입니다.", "stock_images/facial_02.jpg"),
    # 3. "삼차신경통" / "안면마비" 섹션
    ("먼저 의심해 볼 수 있습니다.", "stock_images/facial_03.jpg"),
    # 4. "한의원에서는 어떻게 접근하나요" 섹션
    ("통합적인 접근이 중요합니다.", "stock_images/facial_04.jpg"),
    # 5. 마무리 CTA 위
    ("미루지 마시길 권해드립니다.", "stock_images/facial_05.jpg"),
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
