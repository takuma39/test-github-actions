# sections/ — 手順書と、`.claude/` の元データ

ハンズオンの手順書（`NN-xxx/index.html`）と、各セクションの `.claude/` の**元データ**を置く。全体の説明は、プロジェクトルートの `README.md` を参照。

## 元データ（`claude/`）

各セクションの `NN-xxx/claude/` が、そのセクション用のブランチの `.claude/` になる。複数の元データを重ねて作るブランチもある（`branches.json` の `sources` に、重ねる順に並べる）。**`.claude` とドットを付けないのは、`main` や他のブランチで Skill として読み込まれないようにするため。**

| 元データ | 作られるブランチ |
| --- | --- |
| `01-auto-invoke/claude` | `section-01-auto-invoke`（02 も同じ） |
| `03-description/claude` | `section-03-description` |
| `04-invocation-control/claude` | `section-04-invocation-control` |
| `05-scripts/claude` | `section-05-scripts` |
| `06-dynamic-fork/claude` | `section-06-dynamic-fork` |
| `07-hooks/claude-common` | `section-07a-skill-only` |
| `07-hooks/claude-common` + `07-hooks/claude-hooks` | `section-07b-hooks` |
| `08-subagents/claude` | `section-08-subagents` |
| `09-browser-e2e/claude` + `mcp.json`（→ `.mcp.json`） | `section-09-browser-e2e` |
| `12-permissions/claude` | `section-12-permissions` |

対応表は `branches.json`。00・10・11 は `main` で進めるので、ブランチはない。

## 手順書の更新

手順書は `tools/handson-docs/` のスクリプトで生成している。内容を直すときは `content.py` を編集して、プロジェクトルートで次を実行する。

```bash
python3 tools/handson-docs/generate.py
```

手順書に載せるコード（07 の hooks など）は、元データのファイルから読み込むので、手で写さなくてよい。

## ブランチの作り方・検証

セクション用のブランチは、`main` と元データ（`claude/`）から、スクリプトで作る。**ブランチを手で編集しない。** 直したいときは `main` の元データを直し、PR でマージしてから、ブランチを作り直す。

```bash
git switch main && git pull          # main を最新にする
python3 tools/build-branches.py      # ブランチを作る（既にあれば、main から作り直す。ローカルのみ）
python3 tools/build-branches.py --check   # main と元データに一致しているか検証する
```

- ブランチは、`main` に 1 コミット足した形になる（`.claude/` の差し替えと、09 の `.mcp.json`）。`main` の `.claude/skills/pr-review` は、セクションのブランチには入らない
- `--check` は、次の 3 つを見る。元データと内容が違う、`.claude/` と追加ファイル以外が `main` と違う、`main` の最新を取り込んでいない
- 作り直したブランチを GitHub に push するときは、強制 push が必要になる（ブランチは生成物なので問題ない）。受講者は `git pull` ではなく、`git fetch` のあと `git switch` し直す
