# _sample

セクション共通の題材（電卓）。**これはコピー元**で、`sections/sync-sample.sh` が各セクションの `sample/` にコピーする。
編集するときはここを直してから `./sync-sample.sh` を実行する。

学習用に、次の不備を意図的に残している。レビューや調査で見つけるための題材。

- `average([])` が `NaN` を返す
- `percentOf(x, 0)` が `Infinity` を返す
- `parseNumber("abc")` が `NaN` を返す
- テストが `add` と `divide` の正常系しかない
