---
name: summarize-changes
description: 未コミットの変更を要約する。「変更を要約して」「今の差分を説明して」と言われたときに使う。
allowed-tools: Bash(git diff *)
---

# 変更の要約

最初に「[summarize-changes 起動]」と1行だけ出力する。

## 変更ファイルの一覧

!`git diff HEAD --stat -- .`

## 依頼

上の一覧を2〜3行で要約する。
リスクがありそうなファイルだけ、`git diff HEAD -- <パス>` で中身を読む。
一覧が空なら「未コミットの変更はありません」と答えて終了する。
