#!/usr/bin/env python3
"""Skill の機械チェック（簡易版）。使い方: lint_skills.py <skills ディレクトリ> ...

ERROR: name とディレクトリ名の不一致 / name・description の欠落
WARN : SKILL.md が 500 行超 / 本文に !`...` / curl・wget・外部 URL / ~/.ssh など
NOTE : allowed-tools あり / scripts/ あり（人が目視で確認する）
機械チェックは補助。最終判断は人が行う。
"""
import re
import sys
from pathlib import Path

SUSPICIOUS = re.compile(r"curl |wget |https?://|~/\.ssh|\.env\b|base64 ")
EXEC_BLOCK = re.compile(r"!`[^`]+`")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    result: dict[str, str] = {}
    if match:
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "-")):
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
    return result


def lint(skill_dir: Path) -> list[str]:
    path = skill_dir / "SKILL.md"
    if not path.exists():
        return [f"ERROR {skill_dir}: SKILL.md がありません"]
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    out = []
    if meta.get("name") != skill_dir.name:
        out.append(f"ERROR {path}: name({meta.get('name')!r}) とディレクトリ名({skill_dir.name!r})が一致しません")
    if not meta.get("description"):
        out.append(f"ERROR {path}: description がありません")
    if len(text.splitlines()) > 500:
        out.append(f"WARN  {path}: 500 行を超えています")
    for number, line in enumerate(text.splitlines(), 1):
        if EXEC_BLOCK.search(line):
            out.append(f"WARN  {path}:{number}: 読み込み時にシェル実行される !`...` があります → {line.strip()}")
        elif SUSPICIOUS.search(line):
            out.append(f"WARN  {path}:{number}: ネットワーク・認証情報に関わる記述 → {line.strip()}")
    if "allowed-tools" in meta:
        out.append(f"NOTE  {path}: allowed-tools = {meta['allowed-tools']}（範囲が広すぎないか確認）")
    if (skill_dir / "scripts").is_dir():
        out.append(f"NOTE  {skill_dir}/scripts/ があります（中身を人が読む）")
    return out


def main(roots: list[str]) -> int:
    findings: list[str] = []
    for root in roots:
        for skill_dir in sorted(p for p in Path(root).iterdir() if p.is_dir()):
            findings += lint(skill_dir)
    print("\n".join(findings) if findings else "指摘なし")
    return 1 if any(f.startswith("ERROR") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) if len(sys.argv) > 1 else 2)
