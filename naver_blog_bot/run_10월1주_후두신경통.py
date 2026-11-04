# -*- coding: utf-8 -*-
"""
[원고] 후두신경통 증상, 뒤통수가 찌릿하고 전기가 오는 것 같다면 | 부천 두통 한의원

이 원고부터는 첫 줄(# ...)이 자리표시가 아니라 실제 제목이라 그대로 쓴다.

원고는 "긴장성 두통과는 어떻게 다른가요" 섹션 끝에 9월2주 A(일자목·긴장성
두통) 글 링크를 넣으라고 했지만 그 글의 URL이 아직 없어서 링크 없이 발행한다.
URL이 생기면 원고 그 위치에 "(https://...)" 한 줄을 넣고 다시 돌리면 링크
카드가 들어간다.

사진 설명칸은 아직 자동으로 입력되지 않는다. 각 사진 주석의 설명 문구를
에디터에서 직접 넣는다(자리표시 사진 안에도 같은 문구가 적혀 있다).

사용법: python "run_10월1주_후두신경통.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월1주_A_후두신경통_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    #    설명: 뒤통수가 찌릿한 후두신경통으로 머리를 짚는 모습
    ("구조적으로 짚어 치료합니다.", "stock_images/occipital_01.jpg"),
    # 2. "후두신경통이란 무엇인가요?" 섹션
    #    설명: 뒷목 근육 사이를 지나 두피로 가는 대후두신경 위치
    ("신경이 쉽게 조여지게 됩니다.", "stock_images/occipital_02.jpg"),
    # 3. 치료 섹션
    #    설명: 초음파로 대후두신경 주변을 보며 시행하는 약침
    ("긴장된 몸과 마음을 이완시킵니다.", "stock_images/occipital_03.jpg"),
    # 4. 마무리 (연락처 안내 바로 위)
    #    설명: 부천시청역 365경희성심한의원 진료실
    ("카톡편지로 정리해 보내드립니다.", "stock_images/occipital_04.jpg"),
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
