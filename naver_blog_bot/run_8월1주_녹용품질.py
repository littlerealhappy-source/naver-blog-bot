# -*- coding: utf-8 -*-
"""
[원고] 녹용 파는 곳마다 등급이 다릅니다 (TV·네이버·약국·한의원 비교)

제목이 이미 확정되어 있고([제목] 섹션) 첫 줄(# ...)과도 동일해서
parse_manuscript가 읽은 제목을 그대로 쓴다.

사용법: python "run_8월1주_녹용품질.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = r"C:\Users\SAMSUNG\Downloads\8월1주_B_녹용품질_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("꼭 확인하셔야 할 이야기를 해드리겠습니다.", "stock_images/antler_01.jpg"),
    # 2. "소고기에 등급이 있듯" 섹션
    ("얼마나 들어갔느냐", "stock_images/antler_02.jpg"),
    # 3. "녹용과 녹각은 다릅니다" 섹션
    ("최고로 칩니다.", "stock_images/antler_03.jpg"),
    # 4. "저희가 러시아산 분골을 고집하는 이유" 섹션
    ("서류로 보여드립니다.", "stock_images/antler_04.jpg"),
    # 5. "눈으로 보여드리는 녹용" 섹션
    ("많은 분들이 믿고 찾아주십니다.", "stock_images/antler_05.jpg"),
    # 6. 마무리 CTA 위
    ("그 녹용의 등급과 부위 때문이었을 수 있습니다.", "stock_images/antler_06.jpg"),
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
