# -*- coding: utf-8 -*-
"""
[원고] 40대 다이어트, 덜 먹는데도 뱃살이 안 빠진다면 | 부천 다이어트 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (굶는 다이어트 섹션의 위고비 후
다이어트 글 URL) — 파서가 링크 카드로 변환한다.

[권장 사진] 3번은 사진이 두 장(인바디, 경희미보탕)이라 총 6장이다. 각각
인바디 문단 뒤, 경희미보탕 문단 뒤에 둔다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_10월4주_40대다이어트.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월4주_B_40대다이어트_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("함께 보는 다이어트를 진료하고 있습니다.", "stock_images/diet40_01.jpg",
     "40대 나잇살 뱃살로 고민하는 모습"),
    # 2. "굶는 다이어트가 40대에 더 위험한 이유는?" 섹션 (붉은 강조 문장 뒤,
    #    위고비 문단과 링크 카드보다 위)
    ("근육은 지키고 지방을 줄이는 것이어야 합니다.", "stock_images/diet40_02.jpg",
     "근육은 지키고 체지방을 줄이는 40대 다이어트"),
    # 3-1. 솔루션 섹션의 인바디 문단 뒤
    ("무엇을 줄이고 무엇을 지킬지 정합니다.", "stock_images/diet40_03.jpg",
     "인바디로 근육량과 체지방 확인"),
    # 3-2. 솔루션 섹션의 경희미보탕 문단 뒤
    ("1:1로 따로 짓는 맞춤 다이어트 한약입니다.", "stock_images/diet40_04.jpg",
     "1:1 맞춤 다이어트 한약 경희미보탕"),
    # 4. 다이어트 케어 문단 뒤 (솔루션 섹션 끝)
    ("부위별 관리를 마무리합니다.", "stock_images/diet40_05.jpg",
     "지방분해침 림프마사지 멀티부항 포톤치료 다이어트 케어"),
    # 5. 마무리 (연락처 안내 바로 위)
    ("카톡편지로 정리해 보내드립니다.", "stock_images/diet40_06.jpg",
     "부천시청역 365경희성심한의원 진료실"),
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
