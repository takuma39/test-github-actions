#!/usr/bin/env bash
# _sample/ を、題材を使う各セクションの sample/ にコピーする
set -euo pipefail
cd "$(dirname "$0")"
for dir in 01-auto-invoke 02-slash-invoke 03-description 04-invocation-control 05-scripts 06-dynamic-fork 07-hooks 08-subagents; do
  rm -rf "$dir/sample"
  mkdir -p "$dir"
  cp -R _sample "$dir/sample"
  rm -f "$dir/sample/README.md"
done
echo "sample/ を同期しました"
