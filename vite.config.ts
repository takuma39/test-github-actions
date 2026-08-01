// vitest/config の defineConfig は Vite の設定に test フィールドを足したもの。
// これ 1 ファイルで `vite build` と `vitest` の両方の設定を兼ねる。
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/**/*.test.ts"],
    reporters: process.env.GITHUB_ACTIONS ? ["default", "github-actions"] : ["default"],
  },
});
