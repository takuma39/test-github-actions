// PostToolUse hook: 編集が成功するたびに、記録を追記する。
import { appendFileSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const input = JSON.parse(readFileSync(0, "utf8"));
const filePath = String(input.tool_input?.file_path ?? "");
const line = `${new Date().toISOString()} ${input.tool_name} ${filePath}\n`;

appendFileSync(join(dirname(fileURLToPath(import.meta.url)), "edit.log"), line);
