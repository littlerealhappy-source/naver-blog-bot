# -*- coding: utf-8 -*-
"""
[원고] 수족냉증 원인, 겨울만 되면 손발이 얼음장 같다면 | 부천 수족냉증 한의원

이 원고부터는 첫 줄(# ...)이 자리표시가 아니라 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (치료 섹션 한약 문단의 녹용품질
글 URL) — 파서가 링크 카드로 변환한다.

[권장 사진] 3번은 사진이 두 장(맥파진단기기, 녹용)이라 총 5장이다.
진단 문단 뒤에 맥파 사진, 녹용 문장 뒤에 녹용 사진을 두어 각각 해당
내용 옆에 오게 했다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_10월1주_수족냉증.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월1주_B_수족냉증_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("어떻게 나누어 보는지 정리해 드리겠습니다.", "stock_images/coldhands_01.jpg",
     "수족냉증으로 차가운 손을 감싸 쥔 모습"),
    # 2. "한의학에서는 수족냉증을 어떻게 나누나요?" 섹션
    ("어떤 유형인지 먼저 구분하는 것이 중요합니다.", "stock_images/coldhands_02.jpg",
     "양허·혈허·기체로 나눈 수족냉증 유형"),
    # 3-1. 치료 섹션의 진단 문단 뒤
    ("순환이 막혀 있는지를 확인합니다.", "stock_images/coldhands_03.jpg",
     "수족냉증 유형 확인을 위한 맥파진단기기 측정"),
    # 3-2. 치료 섹션의 녹용 문장 뒤 (뒤이어 "지난 글" 한 줄과 링크 카드가 온다)
    ("도움이 되는 경우가 많습니다.", "stock_images/coldhands_04.jpg",
     "러시아산 녹용 분골"),
    # 4. 마무리 (연락처 안내 바로 위)
    ("카톡편지로 정리해 보내드립니다.", "stock_images/coldhands_05.jpg",
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
