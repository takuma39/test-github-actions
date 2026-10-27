# Claude Code Skills ハンズオン

Claude Code の **Skills・hooks・sub-agent・MCP・権限設定**を、手を動かしながら順に確かめる教材です。**ブランチを切り替えて進めます。** どのブランチも `.claude/` 以外は同じ内容で、切り替えると、そのセクション用の Skill や設定が使えるようになります。

## はじめかた

1. このリポジトリを clone し、プロジェクトルートで `pnpm install`（09 で使う）
2. プロジェクトルートの [index.html](index.html) をブラウザで開く（ビルド不要の静的 HTML）
3. プロジェクトルートでターミナルを開き、進めたいセクションの `git switch` をコピーして貼り付ける（例: `git switch section-01-auto-invoke`）
4. Claude Code を**新しい会話**で開く（ターミナルなら `claude`）。「手順書を開く」の手順を、上から順に進める
5. 終わったら `git restore .` で変更を戻してから、次のセクションへ切り替える

初めての人は、00 → 01 → 02 → 03 の順がおすすめです。

## 前提

- Claude Code が使えること（ログイン済み）。動作確認はターミナルの `claude` で行っています。VS Code 拡張でも、切り替えたあとに新しい会話を開けば同じはずですが、未確認です
- Git、Node.js 22 以上、pnpm（09）、Python 3（05・11）
- 09 だけ、プロジェクトルートで `pnpm install` が必要

## セクションとブランチ

| # | セクション | ブランチ | 学ぶこと |
| --- | --- | --- | --- |
| 00 | [overview](sections/00-overview/index.html) | `main` | 全体像、`/skills`、`/context` |
| 01 | [auto-invoke](sections/01-auto-invoke/index.html) | `section-01-auto-invoke` | `/` なしで Skill が自動で呼ばれる |
| 02 | [slash-invoke](sections/02-slash-invoke/index.html) | 01 と同じ | `/名前` で手動で呼ぶ |
| 03 | [description](sections/03-description/index.html) | `section-03-description` | description で起動率が変わる |
| 04 | [invocation-control](sections/04-invocation-control/index.html) | `section-04-invocation-control` | 手動専用・背景知識・引数・paths |
| 05 | [scripts](sections/05-scripts/index.html) | `section-05-scripts` | scripts で検査を自動化 |
| 06 | [dynamic-fork](sections/06-dynamic-fork/index.html) | `section-06-dynamic-fork` | `` !`cmd` `` と `context: fork` |
| 07 | [hooks](sections/07-hooks/index.html) | `section-07a-skill-only` → `section-07b-hooks` | Skill（お願い）と hooks（強制）の違い |
| 08 | [subagents](sections/08-subagents/index.html) | `section-08-subagents` | sub-agent と並行実行 |
| 09 | [browser-e2e](sections/09-browser-e2e/index.html) | `section-09-browser-e2e` | Playwright MCP でブラウザ打鍵 |
| 10 | [ci-review](sections/10-ci-review/index.html) | `main` | GitHub Actions から Skill を呼ぶ |
| 11 | [safety](sections/11-safety/index.html) | `main` | Skill の監査 |
| 12 | [permissions](sections/12-permissions/index.html) | `section-12-permissions` | `settings.json` の `env` と権限 |

## ディレクトリ構成（`main`）

```
.
├── index.html            ハンズオンの目次（各セクションへのリンクと git switch のコピー）
├── sample/               全セクション共通の題材（電卓）。わざと不備を入れている
├── sections/             手順書と、各セクションの .claude/ の元データ（claude/、ドットなし）
│   └── branches.json     ブランチ名と、元データの対応表
├── app/                  09・10 で使う電卓アプリ（Vite + Vitest）。詳細は app/README.md
├── tools/handson-docs/   手順書（HTML）の生成スクリプト
├── .claude/skills/       CI 用の pr-review（main にだけある）
└── .github/workflows/    CI（テスト、Claude によるレビュー）
```

## 注意

- 題材には、レビュー用に**わざと不備を入れて**います（`average([])` が `NaN`、`percentOf(x, 0)` が `Infinity`、`parseNumber("abc")` が `NaN`、テストが正常系だけ）。
- 結果は LLM の判断で変わります。手順書の「期待する結果」は作成時に確認した例です。違う結果になっても、言い換えて何度か試してください。
- 個人設定（`~/.claude/settings.json`）も有効です。権限の設定によっては、期待する結果と違う動きになることがあります（セクション 12）。
