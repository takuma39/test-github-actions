# Claude Code Skills ハンズオン

Claude Code の **Skills・hooks・sub-agent・MCP** を、手を動かしながら順に確かめる教材です。セクションごとに専用の `.claude/` があり、そのディレクトリで `claude` を起動すると、そのセクション用の Skill が使えます。

## はじめかた

1. このリポジトリを clone する
2. プロジェクトルートの [index.html](index.html) をブラウザで開く（ビルド不要の静的 HTML）
3. プロジェクトルートでターミナルを開き、進めたいセクションの `cd` をコピーして貼り付ける（例: `cd sections/01-auto-invoke`）
4. `claude` を起動し、「手順書を開く」の手順を上から順に進める

初めての人は、00 → 01 → 02 → 03 の順がおすすめです。

## 前提

- Claude Code が使えること（ログイン済み）
- Node.js 22 以上、pnpm（09 の画面確認で使う）、Python 3（05・11）
- 09 だけ、プロジェクトルートで `pnpm install` が必要

## セクション

| # | セクション | 学ぶこと |
| --- | --- | --- |
| 00 | [overview](sections/00-overview/index.html) | 全体像、`/skills`、`/context` |
| 01 | [auto-invoke](sections/01-auto-invoke/index.html) | `/` なしで Skill が自動で呼ばれる |
| 02 | [slash-invoke](sections/02-slash-invoke/index.html) | `/名前` で手動で呼ぶ |
| 03 | [description](sections/03-description/index.html) | description で起動率が変わる |
| 04 | [invocation-control](sections/04-invocation-control/index.html) | 手動専用・背景知識・引数・paths |
| 05 | [scripts](sections/05-scripts/index.html) | scripts で検査を自動化 |
| 06 | [dynamic-fork](sections/06-dynamic-fork/index.html) | `` !`cmd` `` と `context: fork` |
| 07 | [hooks](sections/07-hooks/index.html) | Skill（お願い）と hooks（強制）の違い |
| 08 | [subagents](sections/08-subagents/index.html) | sub-agent と並行実行 |
| 09 | [browser-e2e](sections/09-browser-e2e/index.html) | Playwright MCP でブラウザ打鍵 |
| 10 | [ci-review](sections/10-ci-review/index.html) | GitHub Actions から Skill を呼ぶ |
| 11 | [safety](sections/11-safety/index.html) | Skill の監査 |

## ディレクトリ構成

```
.
├── index.html            ハンズオンの目次（各セクションへのリンクと cd パスのコピー）
├── sections/             教材。セクションごとに手順書と専用の .claude/ がある
├── app/                  09・10 で使う電卓アプリ（Vite + Vitest）。詳細は app/README.md
├── .claude/skills/       CI 用の pr-review（全セクションに継承される）
└── .github/workflows/    CI（テスト、Claude によるレビュー）
```

## 注意

- プロジェクトルートの `.claude/skills/pr-review` は CI 用です。親ディレクトリの Skill は子でも読み込まれるため、**全セクションの `/skills` に見えます**。
- 題材には、レビュー用に**わざと不備を入れて**います（`average([])` が `NaN`、`percentOf(x, 0)` が `Infinity`、`parseNumber("abc")` が `NaN`、テストが正常系だけ）。
- 結果は LLM の判断で変わります。手順書の「期待する結果」は作成時に確認した例です。違う結果になっても、言い換えて何度か試してください。
