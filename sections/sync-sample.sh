#!/usr/bin/env bash
# _sample/ を、sample/ を持つ各セクションにコピーする。
#   ./sync-sample.sh          コピーして同期する
#   ./sync-sample.sh --check  コピーせず、ずれがあれば失敗する（CI 用）
# 新しいセクションで題材を使うときは、そのセクションに空の sample/ を作ってから実行する。
set -euo pipefail
cd "$(dirname "$0")"

mode="${1:-sync}"
status=0
for sample in */sample; do
  dir="${sample%/sample}"
  if [ "$mode" = "--check" ]; then
    if ! diff -r -x README.md _sample "$sample" > /dev/null; then
      echo "ずれています: $sample（./sync-sample.sh を実行してください）"
      status=1
    fi
  else
    rm -rf "$sample"
    cp -R _sample "$sample"
    rm -f "$sample/README.md"
  fi
done

if [ "$mode" = "--check" ]; then
  [ "$status" -eq 0 ] && echo "sample/ はすべて _sample/ と一致しています"
  exit "$status"
fi
echo "sample/ を同期しました"
