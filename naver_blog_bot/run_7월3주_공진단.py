# -*- coding: utf-8 -*-
"""
[원고] 공진단 먹고 효과 못 보셨다면, 0.1g을 확인 안 하셨기 때문입니다

주의(원고의 [글의 목적] 메모): "지난 글" 링크(녹용 관련)는 2주차 B글이
아직 없어서 1주차 A글 URL로 임시 기재되어 있습니다. 2주차 B글 발행 후
아래 IMAGE 아님 LINK URL을 실제 주소로 교체해야 합니다.

사용법: python run_7월3주_공진단.py   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/7월3주_B_공진단사향함량_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 인용구 아래
    ("비싼 돈 주고 먹었는데", "stock_images/gongjindan_01.jpg"),
    # 2. "황제의 명약" 섹션 - 원재료 사진
    ("'황제의 명약'이라는 별칭이 붙었습니다.", "stock_images/gongjindan_02.jpg"),
    # 3. "동의보감이 정한 기준" 섹션 - 계량 장면 (핵심 증거 사진)
    ("이 처방의 최소 기준선인 셈입니다.", "stock_images/gongjindan_03.jpg"),
    # 4. "저희 공진단은 기준치보다 높습니다" 섹션 - 조제 장면
    ("저희 눈으로 확인한 공진단만 나갑니다.", "stock_images/gongjindan_04.jpg"),
    # 5. 마무리 CTA 위
    ("그 공진단의 내용물 때문이었을 수 있습니다.", "stock_images/gongjindan_05.jpg"),
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
