# -*- coding: utf-8 -*-
"""
마크다운 원고 파일을 파싱해 네이버 블로그에 입력하는 실행 스크립트.

사용법:
  1. MANUSCRIPT 경로를 원고 파일로 지정
  2. IMAGE_ANCHORS 에 (본문 문구, 이미지 경로) 지정 — 해당 문구가 있는
     블록 바로 뒤에 이미지가 들어간다. [권장 사진] 지시 기준으로 배치.
  3. python run_manuscript.py   (publish=False: 임시저장까지만)
"""

from manuscript_parser import parse_manuscript, insert_images_at_anchors
from publisher import publish_post

MANUSCRIPT = "manuscripts/7월2주_A_허리디스크_원고.md"

# [권장 사진] 지시 기준 배치 (자리표시 이미지 — 발행 전 실제 사진으로 교체)
IMAGE_ANCHORS = [
    # 1. 도입부 인용구 아래
    ("치료받고 나면 며칠은 괜찮은데", "stock_images/01_consult.jpg"),
    # 2. "정확히 어떤 상태인가요" 섹션 - 척추·디스크 모형
    ("수핵이 밀려나와 주변 신경을 자극하는", "stock_images/02_spine.jpg"),
    # 3. "움직임을 되돌리는 치료" 섹션 - 추나/약침 장면
    ("건강보험이 적용되어 부담도 줄었습니다", "stock_images/03_therapy.jpg"),
    # 4. "일상에서의 관리" 섹션 - 카톡편지 캡처
    ("치료의 완성이기 때문입니다", "stock_images/04_letter.jpg"),
    # 5. 마무리 CTA 위
    ("움직임을 치료하는 접근", "stock_images/05_clinic.jpg"),
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
