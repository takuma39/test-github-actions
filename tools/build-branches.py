#!/usr/bin/env python3
"""セクション用のブランチを、main から生成・検証する。

ブランチ = main + `.claude/` の差し替え（+ `.mcp.json` など、branches.json の files）。
`.claude/` の中身は、branches.json の sources にあるディレクトリを順に重ねて作る。
main の `.claude/skills/pr-review` は、セクションのブランチには入れない。

使い方（プロジェクトルートで、main を最新にしてから）:
    python3 tools/build-branches.py            ブランチを作る（既にあれば、main から作り直す）
    python3 tools/build-branches.py --check    ブランチが、main と元データの内容と合っているか検証する

作るのはローカルのブランチだけ。push はしない（作り直したブランチを push するときは、強制 push が要る）。
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "sections/branches.json").read_text(encoding="utf-8"))
BASE = MANIFEST["base"]
BRANCHES = MANIFEST["branches"]


def git(*args, cwd=ROOT, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True)


def files_of(dir_: Path):
    """ディレクトリ配下の、ファイルの相対パス → 内容（バイト列）。後ろの sources が前を上書きする。"""
    return {p.relative_to(dir_).as_posix(): p.read_bytes() for p in sorted(dir_.rglob("*")) if p.is_file()}


def expected_files(branch):
    """ブランチに入るはずの、.claude/ と追加ファイルの、パス → 内容。"""
    out = {}
    for src in branch["sources"]:
        for rel, data in files_of(ROOT / src).items():
            out[f".claude/{rel}"] = data
    for src, dest in branch.get("files", {}).items():
        out[dest] = (ROOT / src).read_bytes()
    return out


def ensure_clean_base():
    if git("status", "--porcelain", "--untracked-files=no").stdout.strip():
        sys.exit("未コミットの変更があります。コミットするか戻してから実行してください。")
    if git("rev-parse", "--verify", BASE, check=False).returncode != 0:
        sys.exit(f"ベースのブランチ {BASE} が見つかりません。")
    current = git("branch", "--show-current").stdout.strip()
    if current != BASE:
        sys.exit(f"{BASE} ブランチで実行してください（元データを {BASE} の内容から読むため。いまは {current}）。")


def build():
    ensure_clean_base()
    tmp = Path(tempfile.mkdtemp(prefix="build-branches-"))
    try:
        for b in BRANCHES:
            wt = tmp / b["name"]
            git("worktree", "add", "-q", "-f", "-B", b["name"], str(wt), BASE)
            claude = wt / ".claude"
            shutil.rmtree(claude, ignore_errors=True)
            for rel, data in expected_files(b).items():
                dest = wt / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            git("add", "-A", cwd=wt)
            git("-c", "user.name=handson-build", "-c", "user.email=handson-build@example.invalid",
                "commit", "-q", "-m", f"build: {b['name']} 用の .claude/ を生成する\n\n"
                f"元データ: {', '.join(b['sources'])}", cwd=wt)
            git("worktree", "remove", "--force", str(wt))
            print(f"作成: {b['name']}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        git("worktree", "prune")
    print(f"\n{len(BRANCHES)} 本のブランチを作成しました（ローカルのみ。push はしていません）")


def check():
    problems = []
    for b in BRANCHES:
        name = b["name"]
        if git("rev-parse", "--verify", name, check=False).returncode != 0:
            problems.append(f"{name}: ブランチがありません")
            continue
        if git("merge-base", "--is-ancestor", BASE, name, check=False).returncode != 0:
            problems.append(f"{name}: {BASE} の最新を取り込んでいません（作り直してください）")
        want = expected_files(b)
        # 1) .claude/ と追加ファイルが、元データと一致しているか
        have = set(git("ls-tree", "-r", "--name-only", name, "--", ".claude").stdout.split())
        for rel in sorted(have | set(want)):
            if not rel.startswith(".claude/") and rel not in want:
                continue
            if rel not in want:
                problems.append(f"{name}: 元データにないファイル {rel}")
            elif rel not in have and rel.startswith(".claude/"):
                problems.append(f"{name}: ファイルがありません {rel}")
            else:
                got = subprocess.run(["git", "show", f"{name}:{rel}"], cwd=ROOT, capture_output=True).stdout
                if got != want[rel]:
                    problems.append(f"{name}: 内容が元データと違います {rel}")
        # 2) .claude/ と追加ファイル以外が、main と同じか
        allowed = {rel for rel in want}
        changed = git("diff", "--name-only", f"{BASE}...{name}").stdout.split()
        # main 側の .claude/ の削除も含めて、差分は .claude/ か追加ファイルだけのはず
        for rel in changed:
            if not rel.startswith(".claude/") and rel not in allowed:
                problems.append(f"{name}: .claude/ 以外が main と違います {rel}")
    if problems:
        print("\n".join(problems))
        print(f"\n問題 {len(problems)} 件")
        sys.exit(1)
    print(f"{len(BRANCHES)} 本すべて、main と元データに一致しています")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="作らずに、検証だけする")
    args = ap.parse_args()
    check() if args.check else build()
