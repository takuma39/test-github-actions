// vitest/config の defineConfig は Vite の設定に test フィールドを足したもの。
// これ 1 ファイルで `vite build` と `vitest` の両方の設定を兼ねる。
import { defineConfig } from "vitest/config";

export default defineConfig({
  build: {
    // app/ をルートにしても、成果物は従来どおりリポジトリ直下の dist/ に出す。
    // Vercel の Output Directory（dist）を変えずに済む。
    outDir: "../dist",
    emptyOutDir: true,
  },
  test: {
    include: ["src/**/*.test.ts"],
    reporters: process.env.GITHUB_ACTIONS ? ["default", "github-actions"] : ["default"],
  },
});
