# app — 電卓アプリ

ハンズオンのセクション 09（ブラウザ打鍵）と 10（CI）で使う、TypeScript + Vite + Vitest の小さな電卓アプリです。`index.html` を持つ静的サイトとして動くので、Vercel にもデプロイできます。

コマンドはリポジトリ直下で実行します（`package.json` が `app/` を向いています）。

## セットアップ

パッケージマネージャは pnpm です。未インストールなら Corepack で有効化できます。

```bash
corepack enable pnpm
pnpm install
```

## コマンド

| コマンド              | 内容                                       |
| --------------------- | ------------------------------------------ |
| `pnpm run dev`        | 開発サーバーを起動（http://localhost:5173） |
| `pnpm test`           | テストを 1 回実行する                      |
| `pnpm run test:watch` | ファイル変更を監視してテスト実行           |
| `pnpm run typecheck`  | 型チェックのみ（出力なし）                 |
| `pnpm run build`      | リポジトリ直下の `dist/` に本番用の静的ファイルを出力 |
| `pnpm run preview`    | ビルド結果をローカルで配信して確認         |

## CI

テストの CI（`.github/workflows/test.yml`）の内容は、ハンズオンの [セクション 10](../sections/10-ci-review/index.html) にまとめています。

## デプロイ（Vercel）

`app/` の Vite の静的サイトで、Vercel はフレームワークプリセット「Vite」を自動検出します。成果物は従来どおりリポジトリ直下の `dist/` に出る（`app/vite.config.ts` の `build.outDir`）ので、設定は次のままで動きます。

| 項目             | 値               |
| ---------------- | ---------------- |
| Build Command    | `pnpm run build` |
| Output Directory | `dist`           |
| Install Command  | `pnpm install`   |

Vercel に GitHub リポジトリを連携すると、`main` への push が本番デプロイ、PR ごとに Preview デプロイが自動で作られます。

> **次の学習ステップ:** この自動デプロイを GitHub Actions 側から制御する方法（Vercel CLI + `VERCEL_TOKEN` を使い、CI のテストが通ってからデプロイする）に進むと、CI と CD のつながりが理解しやすくなります。

## ディレクトリ構成

```
app/
├── index.html           画面の入口（Vite のエントリ）
├── src/
│   ├── main.ts          DOM と計算ロジックの接続
│   ├── style.css        画面のスタイル
│   ├── calculator.ts    サンプル実装
│   └── calculator.test.ts  サンプルテスト
├── tsconfig.json
└── vite.config.ts       Vite と Vitest 共通の設定
```
