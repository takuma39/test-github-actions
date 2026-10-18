# app — 電卓アプリ

ハンズオンのセクション 09（ブラウザ打鍵）と 10（CI）で使う、TypeScript + Vite + Vitest の小さな電卓アプリです。`index.html` を持つ静的サイトです。

コマンドはプロジェクトルートで実行します（`package.json` が `app/` を向いています）。

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
| `pnpm run build`      | `app/dist/` に本番用の静的ファイルを出力   |
| `pnpm run preview`    | ビルド結果をローカルで配信して確認         |

## CI

テストの CI（`.github/workflows/test.yml`）の内容は、ハンズオンの [セクション 10](../sections/10-ci-review/index.html) にまとめています。

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
