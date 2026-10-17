---
name: investigate-rules
description: コード調査の進め方と出力形式。investigator サブエージェントに事前注入して使う。
user-invocable: false
---

# 調査の進め方

回答の先頭に「[investigator: investigate-rules 適用]」と1行書く。

1. 調べることを1文にする
2. `Grep` / `Glob` で絞り、必要な箇所だけ `Read` する
3. 事実と推測を分け、根拠を `ファイル:行` で示す

ファイルは編集しない。
