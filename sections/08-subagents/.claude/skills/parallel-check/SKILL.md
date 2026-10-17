---
name: parallel-check
description: 指定ファイルのレビューと調査を、2つのサブエージェントで並行して行う。
argument-hint: "[ファイルパス]"
disable-model-invocation: true
---

# 並行チェック

最初に「[parallel-check 起動]」と1行だけ出力する。

対象は `$ARGUMENTS` のファイル。次の2つのサブエージェントを、**同じターンで同時に**起動する（順番に待たない）。

1. `reviewer` — 対象ファイルをレビューする
2. `investigator` — 対象ファイルの各関数が、どこから呼ばれているか、テストが存在するかを調べる

2つの結果が揃ったら、次の形式で1枚にまとめる。

```markdown
## 並行チェック結果
### レビュー（reviewer）
<表>
### 調査（investigator）
<呼び出し元とテストの状況>
### 総合所見
<優先して直すべき点を3つ以内>
```
