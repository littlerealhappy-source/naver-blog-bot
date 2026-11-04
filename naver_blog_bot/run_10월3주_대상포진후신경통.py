# -*- coding: utf-8 -*-
"""
[원고] 대상포진 후 신경통, 물집은 나았는데 옷만 스쳐도 아프다면 | 부천 대상포진 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (치료 섹션 약침 문단의 약침 글
URL) — 파서가 링크 카드로 변환한다.

[권장 사진] 4번은 사진이 두 장(약침, 한약)이라 총 6장이다. 약침 사진은
약침 설명 문장 바로 뒤(그다음 "지난 글" 두 줄과 링크 카드가 온다), 한약
사진은 치료 섹션 끝에 둔다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_10월3주_대상포진후신경통.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월3주_A_대상포진후신경통_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("구조적으로 짚어 치료합니다.", "stock_images/shingles_01.jpg",
     "대상포진 후 신경통으로 옆구리를 짚는 모습"),
    # 2. "대상포진 후 신경통이란 무엇인가요?" 섹션
    ("잘못된 통증 신호를 보내게 됩니다.", "stock_images/shingles_02.jpg",
     "신경을 따라 띠 모양으로 나타나는 대상포진 후 신경통 부위"),
    # 3. "신경은 왜 이렇게 회복이 더딘가요?" 섹션
    ("통증이 오래 남는 큰 이유가 됩니다.", "stock_images/shingles_03.jpg",
     "신경 재생에 필요한 영양과 순환"),
    # 4-1. 치료 섹션의 약침 설명 뒤 (링크 카드와는 두 줄 떨어져 있다)
    ("남아 있는 염증을 가라앉히고 순환을 돕습니다.", "stock_images/shingles_04.jpg",
     "초음파로 신경 주변을 확인하며 시행하는 약침"),
    # 4-2. 치료 섹션 끝 (한약 문단 뒤)
    ("통증이 다시 심해지지 않도록 돕습니다.", "stock_images/shingles_05.jpg",
     "대상포진 후 신경통 한약"),
    # 5. 마무리 (연락처 안내 바로 위)
    ("카톡편지로 정리해 보내드립니다.", "stock_images/shingles_06.jpg",
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
