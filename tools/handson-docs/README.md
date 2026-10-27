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

## Claude Code の版が変わったとき

手順書の一部（特に**セクション 12**）は、Claude Code の実装に依存した挙動を「確認結果」として書いている。公式に保証された仕様ではないので、版が上がると期待値がずれることがある。

- 確認した版は `content.py` の `VERIFIED` に書いてある（現在: Claude Code 2.1.87）
- `generate.py` は、手元の `claude --version` が `VERIFIED` と違うと、警告を出す（失敗にはしない）
- 警告が出たら、`section-12-permissions` ブランチで、手順書の次の手順を実際に試す
  - 手順 4: Bash の `cat sample/.env` が、`Read(./sample/.env)` の deny で拒否されるか
  - 手順 5: 変数を経由した `cat $env_file` が読めてしまうか
  - `find -delete` の手順（確認が出るか、allow に足すと削除できてしまうか）
- 結果が変わっていたら `content.py` の期待結果を直し、変わっていなければ `VERIFIED` の版だけを更新して、再生成する
