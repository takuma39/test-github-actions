# test-github-actions

GitHub Actions を学ぶためのリポジトリです。TypeScript + Vitest で、**PR 作成時に自動でテストが実行される**構成になっています。

## セットアップ

```bash
npm install
```

## コマンド

| コマンド             | 内容                             |
| -------------------- | -------------------------------- |
| `npm test`           | テストを 1 回実行する            |
| `npm run test:watch` | ファイル変更を監視してテスト実行 |
| `npm run typecheck`  | 型チェックのみ（出力なし）       |
| `npm run build`      | `dist/` に JavaScript を出力     |

## CI（GitHub Actions）

ワークフロー定義: [.github/workflows/test.yml](.github/workflows/test.yml)

### 実行タイミング

- `main` 宛ての PR が作成されたとき、および PR に push されたとき
- `main` に直接 push されたとき

### 実行内容

Node.js 20 / 22 のマトリクスで、以下を順に実行します。

1. `npm ci` — `package-lock.json` どおりに依存をインストール
2. `npm run typecheck` — 型エラーがないか確認
3. `npm test` — Vitest でテスト実行

`concurrency` 設定により、同じ PR に連続で push した場合は古い実行が自動でキャンセルされます。

## 動作確認の手順

```bash
git checkout -b test-ci
# src/calculator.ts などを編集
git commit -am "テスト用の変更"
git push -u origin test-ci
```

GitHub 上で PR を作成すると、PR 画面の下部に「Test on Node 20.x / 22.x」のチェックが表示されます。

> **補足:** リポジトリの Settings → Branches でブランチ保護ルールを追加し、`Test` を必須チェックにすると、テストが通らない限りマージできなくなります。

## ディレクトリ構成

```
.
├── .github/workflows/test.yml  # CI の定義
├── src/
│   ├── calculator.ts           # サンプル実装
│   └── calculator.test.ts      # サンプルテスト
├── tsconfig.json
└── vitest.config.ts
```
