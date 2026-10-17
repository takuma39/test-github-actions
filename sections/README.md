# sections/ — Skills ハンズオン

手を動かして Claude Code の Skills・hooks・sub-agent・MCP を学ぶ教材。**`index.html` をブラウザで開く**と手順書が見られる（ビルド不要の静的 HTML）。

各セクションは自分専用の `.claude/` を持つ。使うときは、そのディレクトリで `claude` を起動する。

```bash
cd sections/01-auto-invoke && claude
```

| # | セクション | 内容 |
| --- | --- | --- |
| 00 | overview | 全体像、`/skills`、`/context` |
| 01 | auto-invoke | `/` なしで Skill が自動で呼ばれる |
| 02 | slash-invoke | `/名前` で手動で呼ぶ |
| 03 | description | description で起動率が変わる |
| 04 | invocation-control | 手動専用・背景知識・引数・paths |
| 05 | scripts | scripts で検査を自動化 |
| 06 | dynamic-fork | `` !`cmd` `` と `context: fork` |
| 07 | hooks | Skill（お願い）と hooks（強制）の違い |
| 08 | subagents | sub-agent と並行実行 |
| 09 | browser-e2e | Playwright MCP でブラウザ打鍵 |
| 10 | ci-review | GitHub Actions から Skill を呼ぶ |
| 11 | safety | Skill の監査 |

## 注意

- リポジトリ直下の `.claude/skills/pr-review` は CI 用。親ディレクトリの Skill は子でも読み込まれるため、**全セクションの `/skills` に見える**。
- 題材のコピー元は `_sample/`。変更したら `./sync-sample.sh` で各セクションの `sample/` に反映する（演習で書き換えたサンプルを元に戻すときにも使う）。
- 前提: Claude Code、Node.js 22 以上、pnpm、Python 3。
- 結果は LLM の判断で変わる。手順書の「期待する結果」は作成時に確認した例。
