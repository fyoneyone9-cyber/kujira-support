# -*- coding: utf-8 -*-
"""実際にHTTPで配信されている内容を確認する（キャッシュ混入の切り分け）。"""
import urllib.request, io, os, glob

def get(u):
    req = urllib.request.Request(u, headers={"Cache-Control": "no-cache"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8")

for label, u in [
    ("API(dialog)", "http://localhost:3001/api/delivery/gas-source?f=dialog"),
    ("静的(dialog)", "http://localhost:3001/docs/hearing-gas-dialog.html"),
]:
    try:
        t = get(u)
    except Exception as e:
        print("%-14s ERR %s" % (label, e))
        continue
    print("=== %s (%d bytes) ===" % (label, len(t.encode())))
    for k, v in [
        ("フロントチェックイン", "\u30d5\u30ed\u30f3\u30c8\u30c1\u30a7\u30c3\u30af\u30a4\u30f3"),
        ("frontci", "frontci"),
        ("固定チェックボックス", "chk_pms"),
        ("PMS名入力欄", 'id="pms"'),
        ("getSheetNames", "getSheetNames"),
        ("getVersion", "getVersion"),
    ]:
        print("   %-22s %s" % (k, v in t))
    print()

# ディスク上に古いコピーが残っていないか
print("=== public/docs の中身 ===")
for p in sorted(glob.glob(r"C:\GensparkClaw\kujira-support\public\docs\*")):
    print("   %8d  %s" % (os.path.getsize(p), os.path.basename(p)))
