---
name: review-rules
description: コードレビューの観点と出力形式。reviewer サブエージェントに事前注入して使う。
user-invocable: false
---

# レビュー観点

回答の先頭に「[reviewer: review-rules 適用]」と1行書く。

1. 正しさ — 0 除算、空配列、`NaN`、例外の握りつぶし
2. テスト — 異常系が検証されているか
3. 型 — `any`、不必要な `as`

出力は表（重要度 High / Medium / Low、場所 `ファイル:行`、指摘）。修正はしない。
