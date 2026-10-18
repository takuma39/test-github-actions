// PreToolUse hook: 保護対象のファイルへの Edit / Write を、Claude の意思に関係なくブロックする。
// 終了コード 2 + stderr のメッセージで、ツール呼び出しが拒否され、Claude に理由が渡される。
import { readFileSync } from "node:fs";

const PROTECTED = ["/sample/src/calculator.ts", "/.claude/skills/"];

const input = JSON.parse(readFileSync(0, "utf8"));
const filePath = String(input.tool_input?.file_path ?? "");

const hit = PROTECTED.find((pattern) => filePath.includes(pattern));
if (hit) {
  console.error(`[hook] ${filePath} は保護されています（${hit}）。編集せず、修正案を提示してください。`);
  process.exit(2);
}
