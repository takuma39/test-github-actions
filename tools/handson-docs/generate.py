#!/usr/bin/env python3
"""ハンズオンの手順書（静的 HTML）を生成する。

使い方（プロジェクトルートで）:
    python3 tools/handson-docs/generate.py

出力: index.html（目次）、sections/NN-xxx/index.html、sections/assets/{style.css,app.js}
手順書の内容は content.py にある。ブランチ名は sections/branches.json と照合する。
"""
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content import RESET_NOTE, SECTIONS, VERIFIED  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "sections"
esc = html.escape

GENERATED = "<!-- このファイルは tools/handson-docs/generate.py で生成している。直接編集せず、content.py を直して再生成する -->\n"

MANIFEST = json.loads((OUT / "branches.json").read_text(encoding="utf-8"))
KNOWN = {MANIFEST["base"]} | {b["name"] for b in MANIFEST["branches"]}

CSS = """:root{--bg:#fbfaf8;--fg:#1f1d1a;--muted:#6b665e;--line:#e4e0d8;--card:#ffffff;--accent:#c4552d;--accent-fg:#ffffff;--code-bg:#f3f0ea;--ok:#2f6f4f;--ok-bg:#e8f3ec;--warn-bg:#fdf1e7;--ask:#1d4f91;--sh:#444}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171614;--fg:#ece8e1;--muted:#a39d92;--line:#33302b;--card:#201e1b;--accent:#e8845f;--accent-fg:#1a1100;--code-bg:#2a2723;--ok:#7fcf9f;--ok-bg:#1f2e26;--warn-bg:#2f261d;--ask:#8db8f0;--sh:#c9c4ba}}
:root[data-theme="dark"]{--bg:#171614;--fg:#ece8e1;--muted:#a39d92;--line:#33302b;--card:#201e1b;--accent:#e8845f;--accent-fg:#1a1100;--code-bg:#2a2723;--ok:#7fcf9f;--ok-bg:#1f2e26;--warn-bg:#2f261d;--ask:#8db8f0;--sh:#c9c4ba}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 -apple-system,BlinkMacSystemFont,"Hiragino Sans","Yu Gothic UI",sans-serif}
.wrap{max-width:820px;margin:0 auto;padding:24px 16px 80px}
a{color:var(--accent)}
.crumb{font-size:14px;color:var(--muted)}
h1{font-size:28px;line-height:1.35;margin:8px 0 8px}
h2{font-size:20px;margin:40px 0 12px;padding-bottom:6px;border-bottom:2px solid var(--line)}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 16px}
.tag{font-size:13px;background:var(--code-bg);border:1px solid var(--line);border-radius:999px;padding:2px 12px;color:var(--muted)}
.goal{background:var(--warn-bg);border-left:4px solid var(--accent);padding:12px 16px;border-radius:6px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em;background:var(--code-bg);padding:1px 6px;border-radius:4px}
pre{background:var(--code-bg);border:1px solid var(--line);border-radius:8px;padding:12px 14px;overflow-x:auto;font-size:13.5px;line-height:1.6;margin:8px 0}
pre code{background:none;padding:0}
.cmd{display:flex;gap:8px;align-items:flex-start;margin:8px 0}
.cmd pre{flex:1;margin:0;white-space:pre-wrap;word-break:break-word}
.cmd .lab{font-size:12px;font-weight:700;letter-spacing:.04em;padding:2px 8px;border-radius:4px;margin-top:10px;white-space:nowrap}
.cmd.ask .lab{background:var(--ask);color:var(--bg)}
.cmd.sh .lab{background:var(--sh);color:var(--bg)}
button.copy{font:inherit;font-size:13px;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:4px 10px;cursor:pointer;margin-top:6px;white-space:nowrap}
button.copy:hover{border-color:var(--accent)}
ol.steps{list-style:none;counter-reset:s;padding:0;margin:0}
ol.steps>li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px 12px 52px;margin:14px 0;position:relative}
ol.steps>li::before{content:counter(s);position:absolute;left:14px;top:14px;width:28px;height:28px;border-radius:50%;background:var(--accent);color:var(--accent-fg);font-weight:700;text-align:center;line-height:28px}
.step-t{font-weight:700;margin:0 0 4px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.step-t label{font-weight:400;font-size:13px;color:var(--muted);cursor:pointer}
.do{margin:6px 0}
.expect{background:var(--ok-bg);border-left:4px solid var(--ok);padding:8px 12px;border-radius:6px;margin:8px 0;font-size:15px}
.expect b.k{color:var(--ok)}
.note{font-size:14px;color:var(--muted);margin:6px 0 0}
table{border-collapse:collapse;width:100%;font-size:14.5px;margin:10px 0;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
th{background:var(--code-bg)}
ul.pts{padding-left:22px}
ul.pts li{margin:6px 0}
.nav{display:flex;justify-content:space-between;gap:12px;margin-top:48px;flex-wrap:wrap}
.nav a{border:1px solid var(--line);background:var(--card);padding:8px 14px;border-radius:8px;text-decoration:none}
details{margin:8px 0}
summary{cursor:pointer;color:var(--muted)}
.rows{display:grid;gap:10px;margin-top:12px}
.row{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.row .head{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.row .n{color:var(--accent);font-weight:700}
.row .t{font-weight:700}
.row .g{font-size:13.5px;color:var(--muted);margin:2px 0 0}
.row .open{margin-left:auto;font-size:14px}
.row .cmd{margin:8px 0 0}
"""

JS = r"""(function(){
  function fallbackCopy(text){var t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(t)}
  document.addEventListener('click',function(e){
    var b=e.target.closest('button.copy'); if(!b) return;
    var text=b.parentNode.querySelector('pre code').textContent;
    var done=function(){var o=b.textContent;b.textContent='コピーしました';setTimeout(function(){b.textContent=o},1200)};
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(done,function(){fallbackCopy(text);done()})}
    else{fallbackCopy(text);done()}
  });
  var page=location.pathname;
  document.querySelectorAll('input[data-step]').forEach(function(c){
    var key='steps:'+page+':'+c.dataset.step;
    try{c.checked=localStorage.getItem(key)==='1'}catch(e){}
    c.addEventListener('change',function(){try{localStorage.setItem(key,c.checked?'1':'0')}catch(e){}});
  });
})();
"""


def cmd(kind, text):
    label = "Claude に入力" if kind == "ask" else "ターミナル"
    return (f'<div class="cmd {kind}"><span class="lab">{label}</span>'
            f'<pre><code>{esc(text)}</code></pre><button class="copy" type="button">コピー</button></div>')


def table(spec):
    head, rows = spec
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


def switch(branch):
    return f"git switch {branch}"


def page(i, s):
    prev_s = SECTIONS[i - 1] if i > 0 else None
    next_s = SECTIONS[i + 1] if i < len(SECTIONS) - 1 else None
    out = [GENERATED + f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s['id'][:2]} {esc(s['title'])} | Skills ハンズオン</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body><div class="wrap">
<div class="crumb"><a href="../../index.html">Skills ハンズオン</a> / セクション {s['id'][:2]}</div>
<h1>{s['id'][:2]}　{s['title']}</h1>
<div class="meta"><span class="tag">資料 {s['pdf']}</span></div>
<div class="goal"><b>このセクションのゴール</b><br>{s['goal']}</div>
<h2>準備</h2>"""]

    if s.get("prepare"):
        out.append("<p>先に、プロジェクトルートで次を実行する（<code>pnpm dev</code> は別のターミナルで、起動したままにする）。</p>")
        for p in s["prepare"]:
            out.append(cmd(*p))

    branches = s["branches"]
    if s.get("same_branch_as"):
        out.append(f"<p>セクション {s['same_branch_as']} と<b>同じブランチ</b>（<code>{branches[0]}</code>）のまま続ける。切り替えは要らない。</p>")
    elif len(branches) == 1 and branches[0] == MANIFEST["base"]:
        out.append("<p>このセクションは <code>main</code> ブランチで進める。</p>")
        out.append(cmd("sh", switch(branches[0])))
    elif len(branches) == 1:
        out.append("<p>このセクションのブランチに切り替える。<code>.claude/</code> の中身が、このセクション用に入れ替わる。</p>")
        out.append(cmd("sh", switch(branches[0])))
    else:
        out.append("<p>このセクションは、次のブランチを順に切り替えて進める（手順の中で指示する）。最初は 1 つ目。</p>")
        for b in branches:
            out.append(cmd("sh", switch(b)))
    out.append(f'<p class="note">{RESET_NOTE}</p>')
    out.append(f"<details open><summary>このセクションの中身（<code>.claude/</code> など）</summary><pre><code>{esc(s['files'])}</code></pre></details>")

    out.append('<h2>やってみる</h2><ol class="steps">')
    for n, st in enumerate(s["steps"], 1):
        out.append(f"<li><p class=\"step-t\">{st['t']}<label><input type=\"checkbox\" data-step=\"{n}\"> 済み</label></p>")
        if st.get("do"):
            out.append(f"<p class=\"do\">{st['do']}</p>")
        for kind, text in st["items"]:
            out.append(cmd(kind, text))
        if st.get("expect"):
            out.append(f"<div class=\"expect\"><b class=\"k\">期待する結果</b>　{st['expect']}</div>")
        if st.get("note"):
            out.append(f"<p class=\"note\">{st['note']}</p>")
        out.append("</li>")
    out.append("</ol>")

    if s.get("table"):
        out.append("<h2>整理</h2>" + table(s["table"]))
    for title, code in s.get("snippets", []):
        out.append(f"<details><summary>{esc(title)}</summary><pre><code>{esc(code)}</code></pre></details>")
    out.append('<h2>ここがポイント</h2><ul class="pts">' + "".join(f"<li>{p}</li>" for p in s["points"]) + "</ul>")
    out.append('<h2>うまくいかないとき</h2><ul class="pts">' + "".join(f"<li>{p}</li>" for p in s["trouble"]) + "</ul>")
    out.append('<p class="note">LLM の判断で動くため、結果は毎回同じとは限らない。「期待する結果」はこの教材で確認した例。違う結果になっても、言い換えて何度か試す。</p>')

    nav = ['<div class="nav">']
    nav.append(f'<a href="../{prev_s["id"]}/index.html">← {prev_s["id"][:2]} {prev_s["title"]}</a>' if prev_s else '<a href="../../index.html">← 目次</a>')
    nav.append(f'<a href="../{next_s["id"]}/index.html">{next_s["id"][:2]} {next_s["title"]} →</a>' if next_s else '<a href="../../index.html">目次へ →</a>')
    nav.append("</div>")
    out.append("".join(nav))
    out.append('</div><script src="../assets/app.js"></script></body></html>')
    return "\n".join(out)


def index():
    rows = []
    for s in SECTIONS:
        cmds = "".join(
            f'<div class="cmd sh"><span class="lab">ターミナル</span><pre><code>{esc(switch(b))}</code></pre><button class="copy" type="button">コピー</button></div>'
            for b in s["branches"])
        if s.get("same_branch_as"):
            cmds = f'<p class="g">セクション {s["same_branch_as"]} と同じブランチのまま</p>'
        rows.append(
            f'<div class="row"><div class="head"><span class="n">{s["id"][:2]}</span><span class="t">{s["title"]}</span>'
            f'<a class="open" href="sections/{s["id"]}/index.html">手順書を開く →</a></div>'
            f'<p class="g">{s["goal"].split("。")[0]}。</p>{cmds}</div>')
    return GENERATED + f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Skills ハンズオン</title>
<link rel="stylesheet" href="sections/assets/style.css">
</head>
<body><div class="wrap">
<h1>Claude Code Skills ハンズオン</h1>
<p>Skills・hooks・sub-agent・MCP・権限設定を、手を動かしながら順に確かめる教材。<b>ブランチを切り替えて進める</b>。どのブランチも <code>.claude/</code> 以外は同じ内容で、切り替えると、そのセクション用の Skill や設定が使えるようになる。</p>
<div class="goal"><b>進め方</b><br>1. このリポジトリを clone し、プロジェクトルートで <code>pnpm install</code>（09 で使用）<br>2. プロジェクトルートでターミナルを開き、下の一覧から進めたいセクションの <code>git switch</code> をコピーして貼り付ける<br>3. Claude Code を<b>新しい会話</b>で開き（ターミナルなら <code>claude</code>）、「手順書を開く」の手順を、上から順に進める<br>4. 終わったら <code>git restore .</code> で変更を戻してから、次のセクションへ切り替える</div>
<h2>セクション一覧</h2>
<p class="note">コマンドは、プロジェクトルートで開いたターミナルで実行する。</p>
<div class="rows">{"".join(rows)}</div>
<h2>前提</h2>
<ul class="pts">
<li>Claude Code が使えること（ログイン済み）。この教材はターミナルの <code>claude</code> で動作を確認している。VS Code 拡張でも、切り替えたあとに新しい会話を開けば同じはずだが、未確認</li>
<li>Git、Node.js 22 以上、pnpm（09 の画面確認で使う）、Python 3（05・11）、Node.js（07 の hook）</li>
<li>00・10・11 は <code>main</code> ブランチで進める。<code>main</code> の <code>.claude/</code> には、CI 用の <code>pr-review</code> だけがある</li>
<li>題材は電卓（<code>sample/</code>）。学習用に、<b>わざと不備を入れている</b>（<code>average([])</code> が <code>NaN</code>、<code>percentOf(x, 0)</code> が <code>Infinity</code>、<code>parseNumber("abc")</code> が <code>NaN</code>、テストが正常系だけ。一覧は 01 にもある）</li>
</ul>
<h2>おすすめの順番</h2>
<p>最初に 00 → 01 → 02 → 03 で基本（自動と手動、description）をつかむ。そのあとは興味のあるものから。<b>07（hooks）→ 12（権限）</b>は続けて進めると、「お願い」「強制」「権限」の違いが分かりやすい。08（sub-agent）と 09（ブラウザ打鍵）は、01〜03 を終えてからがおすすめ。</p>
<p class="note">資料: 「Skills 入門」（社内共有用 PDF）。各ページの「資料 P○」は、その PDF のページ番号。</p>
</div><script src="sections/assets/app.js"></script></body></html>
"""


def warn_if_claude_version_changed():
    """手元の Claude Code の版が、手順書で「確認した版」と違えば、再確認を促す（失敗にはしない）。"""
    if not shutil.which("claude"):
        return
    try:
        out = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=15).stdout
    except (OSError, subprocess.SubprocessError):
        return
    verified = VERIFIED.split()[-1]
    if verified not in out:
        print(f"[注意] 手元の Claude Code は {out.strip() or '不明'} で、手順書は {VERIFIED} で確認した内容です。"
              "セクション 12 の手順 4・5（Read の deny と Bash）を再確認し、問題なければ content.py の VERIFIED を更新してください。",
              file=sys.stderr)


def main():
    unknown = sorted({b for s in SECTIONS for b in s["branches"]} - KNOWN)
    if unknown:
        sys.exit(f"sections/branches.json にないブランチ名: {unknown}")
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/style.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets/app.js").write_text(JS, encoding="utf-8")
    (ROOT / "index.html").write_text(index(), encoding="utf-8")
    for i, s in enumerate(SECTIONS):
        d = OUT / s["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(i, s), encoding="utf-8")
    print(f"generated {len(SECTIONS) + 1} pages")
    warn_if_claude_version_changed()


main()
