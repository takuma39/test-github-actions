# sample — 題材（電卓）

ハンズオンの全セクションで共通して使う題材。**全ブランチで同じ内容**で、ブランチごとに違うのは `.claude/` だけ。

学習用に、次の不備を意図的に残している（レビューや調査で見つけてもらうため）。

- `average([])` が `NaN` を返す
- `percentOf(x, 0)` が `Infinity` を返す
- `parseNumber("abc")` が `NaN` を返す
- テストが `add` と `divide` の正常系しかない

セクション 12（permissions）の演習用に、ダミーのファイルも入れている。

- `.env` — 値は偽物（`dummy-token-12345`）。読み取りの拒否を試すためのもの
- `tmp.txt` — 削除の拒否を試すためのもの
- `notes.txt` — 編集の確認（ask）を試すためのもの

演習で書き換えたら、`git restore .` で元に戻す（新しく作ったファイルは `git clean -f sample` で消す）。
