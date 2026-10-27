# sections/ — 手順書と、`.claude/` の元データ

ハンズオンの手順書（`NN-xxx/index.html`）と、各セクションの `.claude/` の**元データ**を置く。全体の説明は、プロジェクトルートの `README.md` を参照。

## 元データ（`claude/`）

各セクションの `NN-xxx/claude/` が、そのセクション用のブランチの `.claude/` になる。**`.claude` とドットを付けないのは、`main` や他のブランチで Skill として読み込まれないようにするため。**

| 元データ | 作られるブランチ |
| --- | --- |
| `01-auto-invoke/claude` | `section-01-auto-invoke`（02 も同じ） |
| `03-description/claude` | `section-03-description` |
| `04-invocation-control/claude` | `section-04-invocation-control` |
| `05-scripts/claude` | `section-05-scripts` |
| `06-dynamic-fork/claude` | `section-06-dynamic-fork` |
| `07-hooks/claude-skill-only` | `section-07a-skill-only` |
| `07-hooks/claude` | `section-07b-hooks` |
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
