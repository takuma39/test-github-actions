// PreToolUse hook: 保護対象のファイルへの書き込みを、Claude の意思に関係なくブロックする。
// 終了コード 2 + stderr のメッセージで、ツール呼び出しが拒否され、Claude に理由が渡される。
//
// 止められる範囲（教材としての限界も含めて把握しておく）
//   - Edit / Write / MultiEdit の file_path が保護対象に一致するもの
//   - Bash のコマンドに保護対象のパスと「書き込みらしい操作」が両方含まれるもの（簡易判定）
// 止められないもの
//   - 変数展開・スクリプト経由・別名リンクなど、コマンド文字列から読み取れない書き込み
//   - 本気で守るなら、権限設定（permissions の deny）やファイルの権限も併用する
import { readFileSync } from "node:fs";

// 相対パスで書かれた Bash コマンドにも一致するよう、先頭の / は付けない
const PROTECTED = ["sample/src/calculator.ts", ".claude/skills/"];
// sed -i / perl -i / tee / mv / cp / rm / リダイレクト（2>&1 などは除く）
const WRITE_LIKE = /\b(sed|perl)\s+-[a-zA-Z]*i|\b(tee|mv|cp|rm)\b|(?<![0-9&])>/;

const input = JSON.parse(readFileSync(0, "utf8"));
// Windows のパス区切りも同じ形で比較する
const normalize = (value) => String(value ?? "").replaceAll("\\", "/");

let target = "";
if (input.tool_name === "Bash") {
  const command = normalize(input.tool_input?.command);
  if (WRITE_LIKE.test(command)) target = command;
} else {
  target = normalize(input.tool_input?.file_path);
}

const hit = PROTECTED.find((pattern) => target.includes(pattern));
if (hit) {
  console.error(`[hook] 保護されています（${hit}）。編集せず、修正案を提示してください。`);
  process.exit(2);
}
