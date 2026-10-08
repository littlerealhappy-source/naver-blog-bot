# -*- coding: utf-8 -*-
"""
[원고] 부천한의원, 공진단 구매를 고민중이라면 꼭 보셔야합니다.

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보가 아닌 원장님이 직접 정한 제목).

내부 링크는 원고 본문에 직접 들어가 있다 ("이왕 드실 거라면, 제대로 된
것을" 섹션의 공진단 글 URL) — 파서가 링크 카드로 변환하므로 여기서
따로 지정하지 않는다.

사용법: python "run_9월2주_공진단피로.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월2주_B_공진단피로_원고.md"
TITLE = "부천한의원, 공진단 구매를 고민중이라면 꼭 보셔야합니다."

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("그에 대한 한방 처방 이야기를 해보려 합니다.", "stock_images/fatigue_01.jpg"),
    # 2. "커피는 '적금을 깨는' 것과 같습니다" 섹션 (악순환 설명 직후).
    #    섹션 마지막 줄 "신호일 수 있습니다."는 도입부 강조 문구와 겹쳐 쓰지 않는다.
    ("피로의 골은 더 깊어집니다.", "stock_images/fatigue_02.jpg"),
    # 3. "공진단이 도움이 될 수 있습니다" 섹션
    ("복용하시는 것이 좋습니다.", "stock_images/fatigue_03.jpg"),
    # 4. "이왕 드실 거라면, 제대로 된 것을" 섹션 (재료 설명 직후, 링크 카드 앞)
    ("정품 사향만 사용합니다.", "stock_images/fatigue_04.jpg"),
    # 5. 마무리 CTA 위
    ("그에 맞는 처방을 안내해 드립니다.", "stock_images/fatigue_05.jpg"),
]


if __name__ == "__main__":
    _, blocks, tags = parse_manuscript(MANUSCRIPT)
    blocks = insert_images_at_anchors(blocks, IMAGE_ANCHORS)

    print(f"제목: {TITLE}")
    print(f"블록 수: {len(blocks)}, 태그: {tags}")

    publish_post(
        blog_id="littlerealhappy",
        title=TITLE,
        blocks=blocks,
        tags=tags,
        publish=False,  # 임시저장까지만. 검토 후 발행은 별도 결정.
        headless=False,
        debug=True,
    )
