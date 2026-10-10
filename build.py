"""Build the browser (PWA) version of 認定調査 特記事項メモ.

usage: python build.py <app body html>
The body file is the same page that is published on claude.ai; this script wraps it
in a full HTML document with the PWA manifest and service worker, and writes docs/.
"""
import pathlib, re, shutil, sys

here = pathlib.Path(__file__).resolve().parent
src = pathlib.Path(sys.argv[1])
docs = here / "docs"
docs.mkdir(exist_ok=True)

body = src.read_text(encoding="utf-8")
body = re.sub(r'^\s*<meta charset="utf-8">\s*', "", body)
title = re.search(r"<title>(.*?)</title>", body).group(1)
body = body.replace(f"<title>{title}</title>", "", 1)
shutil.copyfile(src, here / "src" / "app.html")

head = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="theme-color" content="#2A4A8A">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="特記事項メモ">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>
:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box;height:100%}}
body{{margin:0;font-size:14px}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
</head>
<body>
"""
tail = """
<script>
if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
</script>
</body>
</html>
"""
(docs / "index.html").write_text(head + body + tail, encoding="utf-8", newline="\n")
print("built", docs / "index.html")
