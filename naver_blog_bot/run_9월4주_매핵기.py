# -*- coding: utf-8 -*-
"""
[원고] 목에 뭔가 걸린 것 같은데 내시경은 정상이라면, 매핵기

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보가 아닌 원장님이 직접 정한 제목).

내부 링크는 원고 본문에 직접 들어가 있다 ("역류성 식도염과 함께 오기도
합니다" 섹션의 기능성 소화불량 글 URL) — 파서가 링크 카드로 변환하므로
여기서 따로 지정하지 않는다.

도입부에 인용구 블록이 하나 있다.

사용법: python "run_9월4주_매핵기.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월4주_B_매핵기_원고.md"
TITLE = "목에 뭔가 걸린 것 같은데 내시경은 정상이라면, 매핵기"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("부르는 상태일 수 있습니다.", "stock_images/throat_01.jpg"),
    # 2. "매실 씨가 목에 걸린 듯한 느낌" 섹션
    ("검사에서 뚜렷한 이상이 없는 경우가 많습니다.", "stock_images/throat_02.jpg"),
    # 3. "검사가 정상인데 왜 걸린 느낌이 날까요" 섹션
    ("즉 '기울(氣鬱)'로 봅니다.", "stock_images/throat_03.jpg"),
    # 4. "한의원에서는 어떻게 접근하나요" 섹션
    ("자율신경의 균형을 돕습니다.", "stock_images/throat_04.jpg"),
    # 5. 마무리 CTA 위
    ("긴장과 기의 흐름부터 살펴보시길 권해드립니다.", "stock_images/throat_05.jpg"),
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
