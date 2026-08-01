# test-github-actions

GitHub Actions を学ぶためのリポジトリです。TypeScript + Vite + Vitest で、**PR 作成時に自動でテストが実行される**構成になっています。Vercel へのデプロイも試せるよう、`index.html` を持つ静的サイトとして動きます。

## セットアップ

パッケージマネージャは pnpm を使用します。未インストールなら Corepack で有効化できます。

```bash
corepack enable pnpm
pnpm install
```

## コマンド

| コマンド              | 内容                                     |
| --------------------- | ---------------------------------------- |
| `pnpm run dev`        | 開発サーバーを起動（http://localhost:5173） |
| `pnpm test`           | テストを 1 回実行する                    |
| `pnpm run test:watch` | ファイル変更を監視してテスト実行         |
| `pnpm run typecheck`  | 型チェックのみ（出力なし）               |
| `pnpm run build`      | `dist/` に本番用の静的ファイルを出力     |
| `pnpm run preview`    | ビルド結果をローカルで配信して確認       |

## CI（GitHub Actions）

ワークフロー定義: [.github/workflows/test.yml](.github/workflows/test.yml)

### 実行タイミング

- `main` 宛ての PR が作成されたとき、および PR に push されたとき
- `main` に直接 push されたとき

### 実行内容

Node.js 20 / 22 のマトリクスで、以下を順に実行します。

1. `pnpm install --frozen-lockfile` — `pnpm-lock.yaml` どおりに依存をインストール
2. `pnpm run typecheck` — 型エラーがないか確認
3. `pnpm test` — Vitest でテスト実行
4. `pnpm run build` — 本番ビルドが通るか確認（Vercel と同じ工程）

pnpm のバージョンは `package.json` の `packageManager` フィールドで固定され、`pnpm/action-setup` がそれを読み取ります。

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

## デプロイ（Vercel）

`index.html` を入口とする Vite の静的サイトなので、Vercel はフレームワークプリセット「Vite」を自動検出します。設定ファイルは不要で、既定値は以下のとおりです。

| 項目             | 値                        |
| ---------------- | ------------------------- |
| Build Command    | `pnpm run build`          |
| Output Directory | `dist`                    |
| Install Command  | `pnpm install`            |

Vercel に GitHub リポジトリを連携すると、`main` への push が本番デプロイ、PR ごとに Preview デプロイが自動で作られます。

> **次の学習ステップ:** この自動デプロイを GitHub Actions 側から制御する方法（Vercel CLI + `VERCEL_TOKEN` を使い、CI のテストが通ってからデプロイする）に進むと、CI と CD のつながりが理解しやすくなります。

## ディレクトリ構成

```
.
├── .github/workflows/test.yml  # CI の定義
├── index.html                  # 画面の入口（Vite のエントリ）
├── src/
│   ├── main.ts                 # DOM と計算ロジックの接続
│   ├── style.css               # 画面のスタイル
│   ├── calculator.ts           # サンプル実装
│   └── calculator.test.ts      # サンプルテスト
├── pnpm-workspace.yaml         # pnpm の設定（ビルドスクリプト許可）
├── tsconfig.json
└── vite.config.ts              # Vite と Vitest 共通の設定
```
