# -*- coding: utf-8 -*-
import io, re
s = io.open(r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx",
            encoding="utf-8").read()
for m in re.finditer(r"const (TABLET_PAT|PRINTER_PAT|KIOSK_PAT|SURFACE_PAT)[^\n]*", s):
    print(m.group(0)[:200])
# 端末種別っぽい定義も探す
for m in re.finditer(r"const \w*_PAT\s*=[^\n]*", s):
    t = m.group(0)
    if any(k in t for k in ["KIOSK", "Surface", "surface", "\u5353\u4e0a", "\u30bf\u30d6\u30ec"]):
        print("  ", t[:200])
