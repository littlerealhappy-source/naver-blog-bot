# -*- coding: utf-8 -*-
"""
[원고] 손목건초염 증상, 엄지 쪽 손목이 시큰하고 아기 안기가 힘들다면 | 부천 손목통증 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (감별 섹션의 손목터널증후군 글
URL) — 파서가 링크 카드로 변환한다.

원고 메모대로 9월4주 방아쇠수지 글이 발행되면 "방아쇠수지" 문단 끝에 그
URL을 "(https://...)" 한 줄로 추가해도 된다(링크 2개). 아직 URL이 없어서
지금은 손목터널증후군 링크 하나만 들어간다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_10월4주_손목건초염.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월4주_A_손목건초염_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("구조적으로 짚어 치료합니다.", "stock_images/wrist_01.jpg",
     "아기를 안다가 엄지 쪽 손목이 아픈 손목건초염"),
    # 2. "손목건초염이란 무엇인가요?" 섹션
    ("더 붓는 악순환이 생깁니다.", "stock_images/wrist_02.jpg",
     "엄지 쪽 손목 터널을 지나는 두 힘줄 해부도"),
    # 3. "집에서 확인하는 방법이 있나요?" 섹션
    ("억지로 세게 꺾지는 마세요.", "stock_images/wrist_03.jpg",
     "엄지를 감싸 주먹 쥐고 손목을 꺾는 손목건초염 자가진단"),
    # 4. 치료 섹션 끝
    ("손목 주변의 순환을 돕습니다.", "stock_images/wrist_04.jpg",
     "초음파로 손목 힘줄과 건초를 확인하며 시행하는 약침"),
    # 5. 마무리 (연락처 안내 바로 위)
    ("카톡편지로 정리해 보내드립니다.", "stock_images/wrist_05.jpg",
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
