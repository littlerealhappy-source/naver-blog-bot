# -*- coding: utf-8 -*-
"""
[원고] 미세먼지와 비염, 한의사가 직접 연구해봤습니다

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보 3개 중 3번 선택).

원고에 명시된 대로 이번 글은 호흡기 클러스터의 첫 글(논문 근거 허브)이라
연결할 기존 호흡기 글이 없어 내부 링크 없음 (향후 천식·기침·COPD 등
호흡기 글과 상호 링크 예정).

사용법: python "run_8월3주_비염미세먼지.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/8월3주_B_비염미세먼지_원고.md"
TITLE = "미세먼지와 비염, 한의사가 직접 연구해봤습니다"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("직접 연구 논문을 발표한 바 있습니다.", "stock_images/rhinitis_01.jpg"),
    # 2. "미세먼지가 코와 기관지를 괴롭히는 방식" 섹션
    ("나타나게 되는 것입니다.", "stock_images/rhinitis_02.jpg"),
    # 3. "'개자'라는 약재에 주목한 이유" 섹션
    ("도움이 될 가능성을 제시했습니다.", "stock_images/rhinitis_03.jpg"),
    # 4. "호흡기, 이렇게 접근합니다" 섹션
    ("저희가 보는 방향입니다.", "stock_images/rhinitis_04.jpg"),
    # 5. 마무리 CTA 위
    ("카톡편지로 보내드립니다.", "stock_images/rhinitis_05.jpg"),
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
