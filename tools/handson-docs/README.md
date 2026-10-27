# tools/handson-docs

ハンズオンの手順書（静的 HTML）の生成スクリプト。

- `content.py` — 各セクションの内容。ここを編集する
- `generate.py` — HTML を生成する。`sections/branches.json` と照合して、存在しないブランチ名を使っていたらエラーにする

```bash
python3 tools/handson-docs/generate.py   # プロジェクトルートで実行
```

出力: `index.html`（目次）、`sections/NN-xxx/index.html`、`sections/assets/`。生成物は Git に入れている。
