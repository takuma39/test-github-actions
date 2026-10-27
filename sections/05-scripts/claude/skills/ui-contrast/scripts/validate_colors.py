#!/usr/bin/env python3
"""文字色と背景色のコントラスト比を WCAG 2.x AA 基準で検証する（標準ライブラリのみ）。

使い方: validate_colors.py "<文字色HEX>" "<背景色HEX>" [--large]
終了コード: 0 = AA 合格 / 1 = 不合格 / 2 = 入力エラー
"""
import re
import sys


def parse_hex(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value.strip())
    if not match:
        raise ValueError(f"HEX として読めません: {value!r}（例: #1a1a1a / #fff）")
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    return int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)


def luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    lighter, darker = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def main(argv: list[str]) -> int:
    large = "--large" in argv
    args = [a for a in argv if a != "--large"]
    if len(args) != 2:
        print("使い方: validate_colors.py \"<文字色HEX>\" \"<背景色HEX>\" [--large]")
        return 2
    try:
        fg, bg = parse_hex(args[0]), parse_hex(args[1])
    except ValueError as error:
        print(f"入力エラー: {error}")
        return 2

    ratio = contrast(fg, bg)
    threshold = 3.0 if large else 4.5
    aaa = 4.5 if large else 7.0
    if ratio >= threshold:
        print(f"{ratio:.2f}:1 → AA PASS / AAA {'PASS' if ratio >= aaa else 'FAIL'}")
        return 0
    print(f"{ratio:.2f}:1 → FAIL（AA は {threshold}:1 以上が必要）")
    print("次の行動: 前景色を暗く（または背景色を明るく）して、もう一度検証してください")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
