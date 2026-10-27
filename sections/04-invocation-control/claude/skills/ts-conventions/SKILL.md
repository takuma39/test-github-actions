---
name: ts-conventions
description: TypeScript ファイルを書く・直すときの規約。
paths:
  - "**/*.ts"
---

# TypeScript 規約

最初に「[ts-conventions 参照]」と1行だけ出力する。

- `any` を使わない。型が決まらないときは `unknown` で受けて絞り込む
- 関数の戻り値の型を明示する
- 例外メッセージは日本語で書く
