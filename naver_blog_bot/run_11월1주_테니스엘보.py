# -*- coding: utf-8 -*-
"""
[원고] 테니스엘보 증상, 컵만 들어도 팔꿈치 바깥쪽이 찌릿하다면 | 부천 팔꿈치 통증 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (증상 섹션 끝의 목디스크 글 URL) —
파서가 링크 카드로 변환한다.

[권장 사진] 4번은 사진이 두 장(체외충격파, 약침)이라 총 6장이다. 각각 해당
치료 문단 뒤에 둔다.

사진 설명칸은 아직 자동으로 입력되지 않는다. 각 사진 주석의 설명 문구를
에디터에서 직접 넣는다(자리표시 사진 안에도 같은 문구가 적혀 있다).

사용법: python "run_11월1주_테니스엘보.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/11월1주_A_테니스엘보_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    #    설명: 컵을 들 때 팔꿈치 바깥쪽이 아픈 테니스엘보
    ("구조적으로 짚어 치료합니다.", "stock_images/elbow_01.jpg"),
    # 2. "테니스엘보란 무엇인가요?" 섹션
    #    설명: 팔꿈치 바깥쪽에 붙는 손목 펴는 근육 힘줄 위치
    ("원인은 손과 손목을 쓰는 습관에 있는 경우가 대부분입니다.", "stock_images/elbow_02.jpg"),
    # 3. "골프엘보와는 어떻게 다른가요?" 섹션
    #    설명: 테니스엘보와 골프엘보 통증 위치 비교
    ("반복적인 부담이 쌓여 생깁니다.", "stock_images/elbow_03.jpg"),
    # 4-1. 치료 섹션의 체외충격파 문단 뒤
    #    설명: 테니스엘보 체외충격파 치료
    ("회복 반응을 깨우고 통증을 줄입니다.", "stock_images/elbow_04.jpg"),
    # 4-2. 치료 섹션의 약침 문단 뒤
    #    설명: 초음파로 힘줄 부착부를 확인하며 시행하는 약침
    ("그 지점에 정확히 약침을 넣어 염증을 가라앉힙니다.", "stock_images/elbow_05.jpg"),
    # 5. 마무리 (연락처 안내 바로 위)
    #    설명: 부천시청역 365경희성심한의원 진료실
    ("카톡편지로 정리해 보내드립니다.", "stock_images/elbow_06.jpg"),
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
