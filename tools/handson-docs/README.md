# tools/handson-docs

ハンズオンの手順書（静的 HTML）の生成スクリプト。

- `content.py` — 各セクションの内容。ここを編集する
- `generate.py` — HTML を生成する。`sections/branches.json` と照合して、存在しないブランチ名を使っていたらエラーにする

```bash
python3 tools/handson-docs/generate.py   # プロジェクトルートで実行
```

出力: `index.html`（目次）、`sections/NN-xxx/index.html`、`sections/assets/`。生成物は Git に入れている。

## 二重管理を避けるために

- `index.html` と `sections/NN-xxx/index.html` は**生成物**。ファイルの先頭に、その旨のコメントがある。直接編集しない
- 内容を直すときは `content.py` を編集して、`generate.py` を実行し、生成物も一緒にコミットする
- CI（`test.yml` の `Check generated handson docs`）が、再生成した結果とコミットした HTML が一致するか確認する。手で直した HTML や、再生成し忘れがあれば失敗する
