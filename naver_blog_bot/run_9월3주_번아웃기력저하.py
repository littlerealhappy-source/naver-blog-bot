# -*- coding: utf-8 -*-
"""
[원고] 몸도 마음도 방전된 것 같다면 (번아웃과 기력저하)

원고 파일의 첫 줄(# ...)은 자리표시일 뿐이라 실제 제목은 TITLE로 직접
지정한다 (제목 후보 3개 중 2번 선택).

원고는 "녹용(분골·상대)이나 공진단" 문장 뒤에 공진단·피로 글(9월2주 B)
링크를 넣으라고 했지만 그 글의 URL이 아직 없어서 링크 없이 발행한다.
해당 글을 발행한 뒤 URL을 원고에 넣고 다시 돌리면 링크 카드가 들어간다.

이 원고는 [권장 사진]이 5장이 아니라 4장이고, 도입부에 인용구 블록이
하나 있다.

사용법: python "run_9월3주_번아웃기력저하.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/9월3주_B_번아웃기력저하_원고.md"
TITLE = "몸도 마음도 방전된 것 같다면 (번아웃과 기력저하)"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("이야기해 보려 합니다.", "stock_images/burnout_01.jpg"),
    # 2. "왜 쉬어도 회복이 안 될까요" 섹션
    ("월요일이 여전히 무거운 것입니다.", "stock_images/burnout_02.jpg"),
    # 3. "번아웃 회복, 이렇게 돕습니다" 섹션
    ("자율신경의 균형을 돕습니다.", "stock_images/burnout_03.jpg"),
    # 4. 마무리 CTA 위
    ("카톡편지로 정리해 보내드립니다.", "stock_images/burnout_04.jpg"),
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
