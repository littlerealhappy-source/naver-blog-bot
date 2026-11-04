# -*- coding: utf-8 -*-
"""
[원고] 수험생 공진단, 수능 앞두고 체력과 집중력이 떨어졌다면 | 부천 총명공진단 한의원

첫 줄(# ...)이 실제 제목이라 그대로 쓴다.

내부 링크는 원고 본문에 직접 들어가 있다 ("공진단, 무엇을 보고 골라야
하나요?" 섹션의 공진단 사향 글 URL) — 파서가 링크 카드로 변환한다.

사진 설명칸은 IMAGE_ANCHORS의 세 번째 값으로 자동 입력된다(자리표시 사진
안에도 같은 문구가 적혀 있다).

사용법: python "run_11월1주_수험생총명공진단.py"   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/11월1주_B_수험생총명공진단_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 아래
    ("원내에서 직접 빚고 있습니다.", "stock_images/exam_01.jpg",
     "수능을 앞두고 지친 수험생"),
    # 2. "총명공진단이란 무엇인가요?" 섹션
    ("수험생과 머리를 많이 쓰는 분들을 위해 구성했습니다.", "stock_images/exam_02.jpg",
     "원내에서 직접 빚은 총명공진단"),
    # 3. "공진단, 무엇을 보고 골라야 하나요?" 섹션의 검사성적서 문장 뒤
    #    (링크 카드와는 한 줄 떨어져 있다)
    ("정품 사향의 검사성적서를 상담 때 직접 보여드립니다.", "stock_images/exam_03.jpg",
     "공진단 정품 사향 검사성적서"),
    # 4. 처방 섹션의 진찰 문단 뒤
    ("수험생의 기력과 긴장 상태를 확인합니다.", "stock_images/exam_04.jpg",
     "맥파진단기기로 수험생 컨디션 확인"),
    # 5. 마무리 (연락처 안내 바로 위, 선물 포장 문장 뒤)
    ("선물용 포장도 해드립니다.", "stock_images/exam_05.jpg",
     "선물 포장된 수험생 공진단"),
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
