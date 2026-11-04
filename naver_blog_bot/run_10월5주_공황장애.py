# -*- coding: utf-8 -*-
"""
[원고] 공황장애 증상, 갑자기 심장이 뛰고 숨이 막힌다면 | 부천 공황장애 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

원고는 "왜 아무 이유 없이 발작이 오나요" 섹션 끝에 9월4주 B(매핵기) 또는
9월3주 B(번아웃) 글 링크를 넣으라고 했지만 URL이 아직 없어서 링크 없이
발행한다. URL이 생기면 원고 그 위치에 "(https://...)" 한 줄을 넣고 다시
돌리면 링크 카드가 들어간다. 그 자리를 비워두려고 2번 사진은 섹션 끝이
아니라 바로 앞 문단 뒤에 둔다.

[권장 사진] 3번은 사진이 두 장(추나, 천추메가약침)이라 총 5장이다. 각각
해당 치료 문단 뒤에 둔다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_10월5주_공황장애.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월5주_B_공황장애_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("긴장이 쌓인 몸의 구조를 함께 살펴 치료합니다.", "stock_images/panic_01.jpg",
     "갑자기 가슴이 두근거리고 숨이 막히는 공황발작"),
    # 2. "왜 아무 이유 없이 발작이 오나요?" 섹션의 자율신경 설명 뒤
    #    (섹션 끝은 링크 카드 자리라 사진과 붙지 않게 비워둔다)
    ("작은 자극에도 경보가 쉽게 울리게 됩니다.", "stock_images/panic_02.jpg",
     "자율신경 균형이 무너진 공황장애"),
    # 3-1. 치료 섹션의 추나 문단 뒤
    ("부드럽게 풀어 몸이 진정할 수 있는 바탕을 만듭니다.", "stock_images/panic_03.jpg",
     "상부경추와 두개천골 추나 치료"),
    # 3-2. 치료 섹션의 천추메가약침 문단 뒤
    ("지친 몸의 기운을 채웁니다.", "stock_images/panic_04.jpg",
     "천추메가약침"),
    # 4. 마무리 (연락처 안내 바로 위)
    ("카톡편지로 정리해 보내드립니다.", "stock_images/panic_05.jpg",
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
