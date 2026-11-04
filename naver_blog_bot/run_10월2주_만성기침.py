# -*- coding: utf-8 -*-
"""
[원고] 기침이 3주 넘게 안 멈춘다면, 감기 뒤 오래가는 기침의 원인 | 부천 기침 한의원

이 원고부터는 첫 줄(# ...)이 자리표시가 아니라 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (후비루 문단의 비염 글 URL) —
파서가 링크 카드로 변환한다.

[권장 사진] 3번은 사진이 두 장(개자 약재, 논문 표지)이라 총 6장이다.
원고에 적힌 순서대로, 개자 추출물 결과 문단 뒤에 약재 사진, "들여다본
연구입니다." 뒤에 논문 표지를 둔다.

사진 설명칸은 아직 자동으로 입력되지 않는다. 각 사진 주석의 설명 문구를
에디터에서 직접 넣는다(자리표시 사진 안에도 같은 문구가 적혀 있다).

사용법: python "run_10월2주_만성기침.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월2주_B_만성기침_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    #    설명: 감기 뒤 기침이 오래가 콜록거리는 모습
    ("오래가는 기침 이야기를 해드리겠습니다.", "stock_images/cough_01.jpg"),
    # 2. "오래가는 기침, 언제부터 문제인가요?" 섹션
    #    설명: 급성·아급성·만성 기침 구분
    ("한 번쯤 원인을 살펴보는 것이 좋습니다.", "stock_images/cough_02.jpg"),
    # 3-1. 미세먼지 섹션의 개자 추출물 결과 문단 뒤
    #    설명: 개자 약재
    ("농도에 따라 줄이는 결과를 확인했습니다.", "stock_images/cough_03.jpg"),
    # 3-2. 미세먼지 섹션 끝
    #    설명: 대표원장 개자 미세먼지 기관지 연구 논문 표지
    ("들여다본 연구입니다.", "stock_images/cough_04.jpg"),
    # 4. 치료 섹션의 진단 문단 뒤
    #    설명: 기침 원인 확인을 위한 맥파진단기기 측정
    ("몸의 상태를 함께 확인합니다.", "stock_images/cough_05.jpg"),
    # 5. 마무리 (연락처 안내 바로 위)
    #    설명: 부천시청역 365경희성심한의원 진료실
    ("카톡편지로 정리해 보내드립니다.", "stock_images/cough_06.jpg"),
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
