# -*- coding: utf-8 -*-
"""
클로드 대화에서 받는 표준 원고 형식(마크다운)을 publisher.py 블록으로 변환.

지원 문법:
  # 제목            -> 글 제목 (첫 번째 것만)
  ## 소제목         -> 구분선(긴 선) + 소제목
  ---              -> 무시 (소제목 앞 구분선은 자동 삽입)
  > 인용문          -> 인용구 스타일 문단
  **볼드**          -> 볼드
  {색}텍스트{색}     -> 강조색
  ==텍스트==        -> 강조색 (동일 처리)
  {링크=URL}텍스트{링크} -> 텍스트는 일반 텍스트로 남기고,
                        해당 문단 그룹이 끝난 뒤 링크 카드 삽입
  빈 줄             -> 문단 그룹 구분 (그룹 사이에만 빈 줄 여백)
  [해시태그] 섹션    -> #태그들 추출, 이후 본문 아님
  [권장 사진]/[글의 목적] -> 지시사항이므로 본문에서 제외
  [링크 걸 위치] 섹션 -> 줄 형식: - "앵커문구" (설명) → URL
                        해당 앵커문구가 있는 블록 바로 뒤에 링크 카드 삽입.
                        URL이 http(s)로 시작하지 않으면(아직 미확정 등)
                        명확한 오류로 알려준다.

원고 내 줄바꿈 호흡을 살리기 위해, 그룹 안의 각 줄은 빈 줄 없이 이어지고
그룹이 끝날 때만 빈 줄이 들어간다.
"""

import re
from pathlib import Path

DEFAULT_EMPHASIS_COLOR = "#ff0010"

_INLINE_PATTERN = re.compile(r"(\*\*(.+?)\*\*|\{색\}(.+?)\{색\}|==(.+?)==)", re.DOTALL)
_LINK_PATTERN = re.compile(r"\{링크=([^}]+)\}(.*?)\{링크\}", re.DOTALL)
_LINK_POSITION_PATTERN = re.compile(r'-\s*"([^"]+)"[^→]*→\s*(.+)$')


def parse_inline_block(text: str, emphasis_color: str) -> tuple[list[dict], list[str]]:
    """여러 줄(개행 포함)에 걸친 텍스트를 runs 리스트로 변환.

    **, {색}, == 마커가 줄바꿈을 넘어 다음 줄까지 이어지는 경우가 있어
    (예: "**석회성건염을 오래 방치한 어깨에서\\n회전근개 파열...이유**입니다.")
    한 줄씩 따로 파싱하지 않고 문단 그룹 전체를 한 번에 파싱한다. 개행 문자는
    run의 text 안에 그대로 남고, 호출부(split_runs_by_line)에서 줄 단위로
    다시 나눈다.
    """
    links: list[str] = []

    def link_repl(m):
        links.append(m.group(1))
        return m.group(2)

    text = _LINK_PATTERN.sub(link_repl, text)

    runs: list[dict] = []
    pos = 0
    for m in _INLINE_PATTERN.finditer(text):
        if m.start() > pos:
            runs.append({"text": text[pos:m.start()]})
        if m.group(2) is not None:  # **볼드**
            runs.append({"text": m.group(2), "bold": True})
        elif m.group(3) is not None:  # {색}...{색}
            runs.append({"text": m.group(3), "color": emphasis_color})
        else:  # ==...==
            runs.append({"text": m.group(4), "color": emphasis_color})
        pos = m.end()
    if pos < len(text):
        runs.append({"text": text[pos:]})
    if not runs:
        runs.append({"text": ""})
    return runs, links


def split_runs_by_line(runs: list[dict]) -> list[list[dict]]:
    """run의 text 안에 섞여 있는 개행을 기준으로 줄 단위 runs 리스트로 나눈다."""
    lines: list[list[dict]] = [[]]
    for run in runs:
        parts = run["text"].split("\n")
        for i, part in enumerate(parts):
            if i > 0:
                lines.append([])
            if part:
                new_run = dict(run)
                new_run["text"] = part
                lines[-1].append(new_run)
    return lines


def parse_manuscript(path: str, emphasis_color: str = DEFAULT_EMPHASIS_COLOR):
    """원고 파일을 (제목, 블록 리스트, 태그 리스트)로 변환."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    title: str | None = None
    blocks: list[dict] = []
    tags: list[str] = []
    link_positions: list[tuple[str, str]] = []  # (앵커 문구, URL)

    group: list[str] = []  # 현재 문단 그룹의 원본 줄들
    pending_links: list[str] = []
    meta_section: str | None = None  # [해시태그] 등 메타 섹션 진입 여부

    def flush_group():
        nonlocal group, pending_links
        if group:
            full_text = "\n".join(group)
            runs, links = parse_inline_block(full_text, emphasis_color)
            pending_links.extend(links)
            line_runs_list = split_runs_by_line(runs)
            for i, line_runs in enumerate(line_runs_list):
                if not line_runs:
                    line_runs = [{"text": ""}]
                blocks.append(
                    {
                        "type": "paragraph",
                        "runs": line_runs,
                        # 그룹 마지막 줄 뒤에만 빈 줄 여백을 넣는다
                        "blank_after": i == len(line_runs_list) - 1,
                    }
                )
            group = []
        for url in pending_links:
            blocks.append({"type": "link_card", "url": url})
        pending_links = []

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        # 메타 섹션 처리. "[링크 걸 위치] (2곳만)"처럼 대괄호 뒤에 부가
        # 설명이 붙는 경우가 있어, 줄 전체가 아니라 첫 "[...]" 부분만
        # 섹션 이름으로 삼는다.
        section_match = re.match(r"^(\[[^\]]+\])", stripped)
        if section_match:
            flush_group()
            meta_section = section_match.group(1)
            continue
        if meta_section == "[해시태그]":
            if stripped:
                tags.extend(t.lstrip("#") for t in stripped.split() if t.startswith("#"))
            continue
        if meta_section == "[링크 걸 위치]":
            m = _LINK_POSITION_PATTERN.match(stripped)
            if m:
                link_positions.append((m.group(1), m.group(2).strip()))
            continue
        if meta_section in ("[권장 사진]", "[글의 목적]", "[제목 후보 — 원장님이 확정]"):
            continue  # 지시사항 — 본문에 넣지 않음

        if not stripped:
            flush_group()
            continue

        if stripped.startswith("# ") and title is None:
            title = stripped[2:].strip()
            continue

        if stripped.startswith("## "):
            flush_group()
            blocks.append({"type": "divider"})
            blocks.append({"type": "subheading", "text": stripped[3:].strip()})
            continue

        if stripped == "---":
            continue  # 소제목 앞 구분선은 자동으로 넣으므로 무시

        if stripped.startswith("> "):
            flush_group()
            quote_text = stripped[2:].strip()
            blocks.append({"type": "quote", "text": quote_text})
            continue

        group.append(stripped)

    flush_group()

    if title is None:
        raise ValueError("원고에서 제목(# ...)을 찾지 못했습니다.")

    if link_positions:
        for anchor, url in link_positions:
            if not url.startswith(("http://", "https://")):
                raise ValueError(
                    f"[링크 걸 위치] \"{anchor}\" 항목의 URL이 아직 확정되지 않았습니다: {url}\n"
                    "실제 URL로 채운 뒤 다시 실행하세요."
                )
        blocks = _insert_after_anchors(blocks, link_positions, lambda url: {"type": "link_card", "url": url})

    return title, blocks, tags


def _block_text(b: dict) -> str:
    if b["type"] == "paragraph":
        return "".join(r["text"] for r in b["runs"])
    if b["type"] in ("quote", "subheading"):
        return b["text"]
    return ""


def _insert_after_anchors(blocks: list[dict], anchors: list[tuple[str, str]], make_block):
    """anchors: (본문 일부 문자열, make_block에 넘길 값). 해당 문자열이 포함된
    블록 바로 뒤에 make_block(value)로 만든 블록을 삽입한 새 리스트를 반환."""
    result = list(blocks)
    for snippet, value in anchors:
        for i, b in enumerate(result):
            if snippet in _block_text(b):
                result.insert(i + 1, make_block(value))
                break
        else:
            raise ValueError(f"앵커 문구를 본문에서 찾지 못했습니다: {snippet}")
    return result


def insert_images_at_anchors(blocks: list[dict], anchors: list[tuple[str, str]]):
    """anchors: (본문 일부 문자열, 이미지 경로). 해당 문자열이 포함된
    블록 바로 뒤에 이미지 블록을 삽입한 새 리스트를 반환."""
    return _insert_after_anchors(blocks, anchors, lambda path: {"type": "image", "path": path})
