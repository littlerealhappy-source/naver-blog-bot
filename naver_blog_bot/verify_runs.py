# -*- coding: utf-8 -*-
"""
run 스크립트 오프라인 검증. 네이버에 접속하지 않고 원고 파싱 결과만 확인한다.

사용법:
    python verify_runs.py                     모든 run_*.py 검사
    python verify_runs.py run_A.py run_B.py   지정한 스크립트만 검사 + 블록 상세 출력

결과는 debug_output/verify_report.txt 에 UTF-8로 저장한다.
"""

import importlib.util
import sys
from pathlib import Path

BOT = Path(__file__).parent
sys.path.insert(0, str(BOT))

from manuscript_parser import insert_images_at_anchors, parse_manuscript  # noqa: E402

REPORT = BOT / "debug_output" / "verify_report.txt"
LEAK_MARKERS = ["[제목", "[링크", "[해시태그]", "[권장 사진]", "[글의 목적]", "**", "==", "(https://", "> "]
SENTENCE_ENDS = (".", "?", "!", "다", "요")


def block_text(block: dict) -> str:
    if block.get("type") == "paragraph":
        return "".join(run.get("text", "") for run in block.get("runs", []))
    return block.get("text") or block.get("url") or block.get("path") or ""


def load_run_script(path: Path):
    spec = importlib.util.spec_from_file_location("run_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_script(path: Path, detail: bool, lines: list[str]) -> list[str]:
    problems: list[str] = []
    module = load_run_script(path)

    manuscript = BOT / module.MANUSCRIPT
    if not manuscript.exists():
        return [f"원고 없음: {module.MANUSCRIPT}"]

    title, blocks, tags = parse_manuscript(str(manuscript))
    title = getattr(module, "TITLE", None) or title
    anchors = getattr(module, "IMAGE_ANCHORS", [])
    body = "\n".join(block_text(b) for b in blocks)

    for anchor, image in anchors:
        count = body.count(anchor)
        if count != 1:
            problems.append(f"앵커 {count}회: {anchor!r}")
        if not (BOT / image).exists():
            problems.append(f"사진 없음: {image}")

    placed = insert_images_at_anchors(blocks, anchors) if anchors else blocks
    types = [b["type"] for b in placed]
    if types.count("image") != len(anchors):
        problems.append(f"사진 삽입 {types.count('image')}/{len(anchors)}")

    for i, block in enumerate(placed):
        if block["type"] != "image":
            continue
        neighbors = {placed[j]["type"] for j in (i - 1, i + 1) if 0 <= j < len(placed)}
        if "link_card" in neighbors:
            problems.append(f"사진과 링크 카드가 붙어 있음: {block['path']}")
        before = block_text(placed[i - 1]).rstrip() if i else ""
        if not before.rstrip("\"'”’").endswith(SENTENCE_ENDS):
            problems.append(f"문장 중간에 사진: {block['path']} 앞 {before!r}")

    problems.extend(f"본문에 표기 남음: {m!r}" for m in LEAK_MARKERS if m in body)

    summary = {t: types.count(t) for t in sorted(set(types))}
    lines.append(f"[{'OK' if not problems else 'WARN'}] {path.name}")
    lines.append(f"    제목: {title}")
    lines.append(f"    태그 {len(tags)}개, 블록 {summary}")
    lines.extend(f"    ! {p}" for p in problems)

    if detail:
        lines.append(f"    태그: {tags}")
        for a, image in anchors:
            lines.append(f"    앵커 {body.count(a)}회  {a!r} -> {image}")
        for i, block in enumerate(placed):
            kind = block["type"]
            if kind == "paragraph":
                if any(r.get("bold") or r.get("color") for r in block["runs"]):
                    lines.append(f"    {i}\tP*\t{block['runs']}")
            elif kind == "image":
                after = block_text(placed[i + 1]) if i + 1 < len(placed) else ""
                before = block_text(placed[i - 1]) if i else ""
                lines.append(f"    {i}\tIMAGE\t{block['path']}  앞 {before!r} / 뒤 {after!r}")
            else:
                lines.append(f"    {i}\t{kind.upper()}\t{block_text(block)!r}")
        lines.append("")

    return problems


def main(argv: list[str]) -> int:
    detail = len(argv) > 1
    paths = [BOT / name for name in argv[1:]] or sorted(BOT.glob("run_*.py"))

    lines: list[str] = []
    all_problems = 0
    for path in paths:
        try:
            all_problems += len(check_script(path, detail, lines))
        except Exception as exc:
            all_problems += 1
            lines.append(f"[FAIL] {path.name}: {exc!r}")

    lines.append("")
    lines.append(f"검사 {len(paths)}편, 문제 {all_problems}건")
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"checked={len(paths)} problems={all_problems} report={REPORT}")
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
