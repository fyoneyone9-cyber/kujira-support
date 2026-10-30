#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re, shutil, datetime
sys.stdout.reconfigure(encoding="utf-8")

DASHBOARD = r"C:\AI\ComfyUI\dashboard.html"

SCRIPT_CLOSE = "</script>"
SCRIPT_OPEN = "<script>"
CHAR_INIT = "window.CHAR_TEMPLATES = window.CHAR_TEMPLATES || { female: [], male: [] };"

def auto_fix(verbose=True, error_line=None):
    if not os.path.exists(DASHBOARD):
        if verbose: print("[auto_fix] dashboard.html not found")
        return False, []

    with open(DASHBOARD, encoding="utf-8", errors="replace") as f:
        html = f.read()

    fixed = []

    # === ルール1: push()終端残骸 ===
    lines = html.split("\n")
    new_lines = []
    n_fixed = 0
    trailing_re = re.compile(r'(\]|\})(,\s*\w+\s*:\s*\[\])+\s*\}\s*;')
    for line in lines:
        if "CHAR_TEMPLATES" in line and ("||" in line or "= {" in line):
            new_lines.append(line)
            continue
        new_line, n = trailing_re.subn("});", line)
        n_fixed += n
        new_lines.append(new_line)
    if n_fixed > 0:
        html = "\n".join(new_lines)
        fixed.append("push()終端残骸 x" + str(n_fixed))
        if verbose: print("[auto_fix] 修正: push()終端残骸 (" + str(n_fixed) + "箇所)")

    # === ルール2: </script>欠落 ===
    # CHAR_TEMPLATESの初期化の直前にCHAR_INITが来るのに</script>がない
    bad = "}\n\n\n" + CHAR_INIT
    good = "}\n\n" + SCRIPT_CLOSE + "\n" + SCRIPT_OPEN + "\n" + CHAR_INIT
    if bad in html:
        html = html.replace(bad, good)
        cnt = html.count(bad)  # 残数
        fixed.append("</script>欠落(3改行)")
        if verbose: print("[auto_fix] 修正: </script>欠落(3改行)")
    bad2 = "}\n\n" + CHAR_INIT
    # ただし直前に</script>がすでにある場合は除外
    bad2_real = SCRIPT_OPEN + "\n" + CHAR_INIT  # 正常パターンはこう来ない → bad2だけ確認
    if bad2 in html and SCRIPT_CLOSE + "\n" + SCRIPT_OPEN + "\n" + CHAR_INIT not in html:
        html = html.replace(bad2, "}\n\n" + SCRIPT_CLOSE + "\n" + SCRIPT_OPEN + "\n" + CHAR_INIT, 1)
        fixed.append("</script>欠落(2改行)")
        if verbose: print("[auto_fix] 修正: </script>欠落(2改行)")


    # === ルール3: outfits] 欠落 ===
    _b3 = chr(34)+chr(125)+chr(125)+chr(41)+chr(59)+chr(10)
    _g3 = chr(34)+chr(125)+chr(93)+chr(41)+chr(59)+chr(10)
    n3 = html.count(_b3)
    if n3 > 0:
        html = html.replace(_b3, _g3)
        fixed.append("outfits] 欠落 x"+str(n3))
        if verbose: print("[auto_fix] 修正: outfits] 欠落 ("+str(n3)+"箇所)")

    # === ルール4: outfits末尾 ダブルクォート二重 ===
    _b4a = chr(34)+chr(34)+chr(93)+chr(41)+chr(59)  # ""]);
    _g4a = chr(34)+chr(93)+chr(41)+chr(59)           # "]);
    n4 = html.count(_b4a)
    if n4 > 0:
        html = html.replace(_b4a, _g4a)
        fixed.append("outfits末尾二重クォート x"+str(n4))
        if verbose: print("[auto_fix] 修正: outfits末尾DQ重複 ("+str(n4)+"箇所)")

    # === 保存 ===
    if fixed:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(DASHBOARD, DASHBOARD + ".bak_autofix_" + ts)
        ver_m = re.search(r'content="(\d{10,})"', html)
        if ver_m:
            nv = str(int(ver_m.group(1)) + 1)
            html = html.replace('content="' + ver_m.group(1) + '"', 'content="' + nv + '"', 1)
            if verbose: print("[auto_fix] version -> " + nv)
        with open(DASHBOARD, "w", encoding="utf-8") as f:
            f.write(html)
        if verbose: print("[auto_fix] 保存完了 (" + str(len(fixed)) + "件修正)")
    else:
        if verbose: print("[auto_fix] 問題なし")

    return bool(fixed), fixed

if __name__ == "__main__":
    changed, results = auto_fix(verbose=True)
    sys.exit(0 if not results else 1)
