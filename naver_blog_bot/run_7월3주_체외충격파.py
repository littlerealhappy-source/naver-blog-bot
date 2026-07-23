# -*- coding: utf-8 -*-
"""
[원고] 부천한의원| 밤에만 유독 아픈 어깨, 근육통이 아니라 '돌' 때문일 수 있습니다

사용법: python run_7월3주_체외충격파.py   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = r"C:\Users\SAMSUNG\Downloads\7월3주_A_체외충격파석회성건염_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 인용구 아래
    ("무리해서 근육이 뭉쳤나 보다", "stock_images/shoulder_01.jpg"),
    # 2. "어깨 힘줄에 '돌'이 생긴다는 것" 섹션 - 회전근개 구조 설명
    ("돌처럼 굳어지는 상태를 말합니다.", "stock_images/shoulder_02.jpg"),
    # 3. "오십견과 헷갈리기 쉽습니다" 섹션 - 감별진단
    ("남이 들어줘도 특정 각도에서 딱 멈춥니다.", "stock_images/shoulder_03.jpg"),
    # 4. "체외충격파, 굳어버린 조직을 깨우는 치료" 섹션 - 핵심 컷
    ("저희가 중심에 두는 것이 ", "stock_images/shoulder_04.jpg"),
    # 5. "여기에 두 가지를 더합니다" 섹션 - 초음파 유도 약침
    ("그 지점에 약침을 정확히 전달합니다.", "stock_images/shoulder_05.jpg"),
    # 6. 마무리 CTA 위
    ("진단하고 치료합니다.", "stock_images/shoulder_06.jpg"),
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
