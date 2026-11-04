# -*- coding: utf-8 -*-
"""
[원고] 부모님 보약 고르는 법, 기운 없고 입맛 떨어지신 부모님께 | 부천 녹용 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (녹용 섹션의 녹용품질 글 URL) —
파서가 링크 카드로 변환한다.

사진 설명칸은 아직 자동으로 입력되지 않는다. 각 사진 주석의 설명 문구를
에디터에서 직접 넣는다(자리표시 사진 안에도 같은 문구가 적혀 있다).

사용법: python "run_10월3주_부모님보약.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월3주_B_부모님보약_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    #    설명: 부모님 보약을 상담하는 자녀와 어르신
    ("보약을 많이 지어왔습니다.", "stock_images/parents_01.jpg"),
    # 2. "부모님 몸, 왜 채워드려야 할까요?" 섹션 (붉은 강조 문장 뒤)
    #    설명: 원기와 면역력을 채우는 부모님 보약
    ("다시 세워드리는 것이 핵심입니다.", "stock_images/parents_02.jpg"),
    # 3. 녹용 섹션 (분골·상대 문장 뒤, 링크 카드와는 한 줄 떨어져 있다)
    #    설명: 러시아산 녹용 분골과 상대 부위
    ("원내에서 직접 탕전합니다.", "stock_images/parents_03.jpg"),
    # 4. "어떻게 지어드리나요?" 섹션의 진찰 문단 뒤
    #    설명: 맥파진단기기로 어르신 혈관 상태 확인
    ("지금 드시는 약도 꼼꼼히 여쭤봅니다.", "stock_images/parents_04.jpg"),
    # 5. 마무리 (연락처 안내 바로 위). "카톡편지로 정리해 보내드립니다." 다음
    #    줄까지 한 문단이라, 문단이 끊기지 않게 마지막 줄 뒤에 둔다.
    #    설명: 부천시청역 365경희성심한의원 진료실
    ("멀리 계신 자녀분께도 함께 전해드릴 수 있습니다.", "stock_images/parents_05.jpg"),
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
