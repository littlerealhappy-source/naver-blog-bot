# -*- coding: utf-8 -*-
"""
[원고] 족저근막염 증상, 아침 첫발 디딜 때 발뒤꿈치가 찌릿하다면 | 부천 족저근막염 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (치료 섹션 체외충격파 문단의
체외충격파 글 URL) — 파서가 링크 카드로 변환한다.

[권장 사진] 3번은 사진이 두 장(체외충격파, 약침)이라 총 6장이다. 체외충격파
사진은 충격파 설명 문장 바로 뒤(그다음 "지난 글" 두 줄과 링크 카드가 온다),
약침 사진은 약침 문단 뒤에 둔다.

4번은 FAQ의 '집에서 할 수 있는 관리' 답변 뒤에 둬서 스트레칭 사진이 그
설명 바로 옆에 오게 했다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_10월5주_족저근막염.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월5주_A_족저근막염_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("구조적으로 짚어 치료합니다.", "stock_images/plantar_01.jpg",
     "아침 첫발에 발뒤꿈치 통증을 느끼는 족저근막염"),
    # 2. "족저근막염이란 무엇인가요?" 섹션
    ("근막이 뒤꿈치뼈에 붙는 자리부터 탈이 납니다.", "stock_images/plantar_02.jpg",
     "발의 아치를 잡아주는 족저근막 위치"),
    # 3-1. 치료 섹션의 체외충격파 설명 뒤 (링크 카드와는 두 줄 떨어져 있다)
    ("회복 반응을 깨우고 통증을 줄입니다.", "stock_images/plantar_03.jpg",
     "족저근막염 체외충격파 치료"),
    # 3-2. 치료 섹션의 약침 문단 뒤
    ("그 지점에 정확히 약침을 넣어 염증을 가라앉힙니다.", "stock_images/plantar_04.jpg",
     "초음파로 족저근막 두께를 확인하며 시행하는 약침"),
    # 4. FAQ '집에서 할 수 있는 관리는요?' 답변 뒤
    (
        "아침에 일어나기 전 발가락을 몸 쪽으로 젖혀 발바닥을 늘려주고, "
        "벽을 짚고 종아리를 충분히 늘려주세요. 집에서도 맨발보다 쿠션 있는 "
        "실내화가 좋습니다.",
        "stock_images/plantar_05.jpg",
        "족저근막염 발바닥·종아리 스트레칭",
    ),
    # 5. 마무리 (연락처 안내 바로 위)
    ("카톡편지로 정리해 보내드립니다.", "stock_images/plantar_06.jpg",
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
