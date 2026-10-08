# -*- coding: utf-8 -*-
"""
[원고] 두통약을 달고 사는데 낫지 않는다면, 이것 때문입니다.

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보가 아닌 원장님이 직접 정한 제목).

내부 링크는 원고 본문에 직접 들어가 있다 ("한의원에서는 어떻게
접근하나요" 섹션의 목디스크 글 URL) — 파서가 링크 카드로 변환하므로
여기서 따로 지정하지 않는다.

사용법: python "run_9월2주_일자목두통.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월2주_A_일자목두통_원고.md"
TITLE = "두통약을 달고 사는데 낫지 않는다면, 이것 때문입니다."

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("일자목과 긴장성 두통 이야기를 해보려 합니다.", "stock_images/headache_01.jpg"),
    # 2. "그 시작에는 일자목이 있습니다" 섹션
    ("두통이 자꾸 되돌아오는 것입니다.", "stock_images/headache_02.jpg"),
    # 3. 원고가 지정한 "이런 분들이 특히" 섹션은 본문에 없어서,
    #    자세 이야기가 나오는 "자세만큼, 스트레스가 문제입니다" 섹션 끝에 둔다
    ("근본적인 개선이 이루어집니다.", "stock_images/headache_03.jpg"),
    # 4. "한의원에서는 어떻게 접근하나요" 섹션 (추나·침 설명 직후, 링크 카드와 떨어뜨림)
    ("함께 가라앉는 데 도움이 됩니다.", "stock_images/headache_04.jpg"),
    # 5. 마무리 CTA 위
    ("카톡편지로 정리해 보내드립니다.", "stock_images/headache_05.jpg"),
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
