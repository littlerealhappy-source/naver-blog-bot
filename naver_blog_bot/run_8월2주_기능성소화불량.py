# -*- coding: utf-8 -*-
"""
[원고] 내시경은 정상인데 속이 계속 더부룩하다면 (기능성 소화불량·담적)

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보 3개 중 1번 선택).

이번 글은 소화기 클러스터의 첫 글이라 원고에 명시된 대로 내부 링크
없음.

사용법: python "run_8월2주_기능성소화불량.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/8월2주_B_기능성소화불량_원고.md"
TITLE = "내시경은 정상인데 속이 계속 더부룩하다면 (기능성 소화불량·담적)"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("기능성 소화불량 이야기를 해보려 합니다.", "stock_images/dyspepsia_01.jpg"),
    # 2. "기능성 소화 문제는 여러 얼굴로 나타납니다" 섹션
    ("여기에 해당하는 경우가 많습니다.", "stock_images/dyspepsia_02.jpg"),
    # 3. "소화 문제가 몸 전체로 번지기도 합니다" 섹션
    ("소화 기능부터 함께 살펴볼 필요가 있습니다.", "stock_images/dyspepsia_03.jpg"),
    # 4. "한의원에서는 어떻게 접근하나요" 섹션
    ("저희가 보는 방향입니다.", "stock_images/dyspepsia_04.jpg"),
    # 5. 마무리 CTA 위
    ("들여다보실 때입니다.", "stock_images/dyspepsia_05.jpg"),
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
