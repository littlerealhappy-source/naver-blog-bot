# -*- coding: utf-8 -*-
"""
[원고] 좌골신경통 증상, 엉덩이에서 다리 뒤로 찌릿하게 뻗친다면 | 부천 좌골신경통 한의원

이 원고부터는 첫 줄(# ...)이 자리표시가 아니라 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 (치료 섹션 끝의 허리디스크 글
URL) — 파서가 링크 카드로 변환한다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_10월2주_좌골신경통.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/10월2주_A_좌골신경통_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("그 위치에 따라 치료가 완전히 달라지기 때문입니다.", "stock_images/sciatica_01.jpg",
     "엉덩이에서 다리로 뻗치는 좌골신경통으로 허리를 짚는 모습"),
    # 2. "좌골신경통이란 무엇인가요?" 섹션
    ("증상의 이름에 가깝습니다.", "stock_images/sciatica_02.jpg",
     "허리에서 엉덩이를 지나 다리로 내려가는 좌골신경 경로"),
    # 3. 원인 섹션 (이상근증후군 설명 뒤)
    ("이 경우를 의심해 볼 수 있습니다.", "stock_images/sciatica_03.jpg",
     "이상근 아래를 지나는 좌골신경 해부도"),
    # 4. 치료 섹션 (치료 목록 끝, 링크 카드 앞 문단보다 위)
    ("순환을 돕습니다.", "stock_images/sciatica_04.jpg",
     "초음파로 좌골신경 주변을 확인하며 시행하는 약침"),
    # 5. 마무리 (연락처 안내 바로 위)
    ("카톡편지로 정리해 보내드립니다.", "stock_images/sciatica_05.jpg",
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
