# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V3] サイドバーの日付/時刻をマウント後に描画する。
SSR時とブラウザ時で分が変わり React #418 になっていた（全ページで発生）。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\components\Sidebar.tsx"
bak = P + ".bak_clock2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
L = io.open(P, encoding="utf-8").read().split("\n")

# now の宣言を探す
decl = None
for i, l in enumerate(L):
    if re.search(r"const \[now, setNow\] = useState", l):
        decl = i
        print("now decl L%d| %s" % (i + 1, l.strip()[:120]))
        break
assert decl is not None, "now declaration not found"

# 初期値を null にする
L[decl] = ("  // [HYDRATION_FIX_V3 2026-10-29] SSRとブラウザで現在時刻が異なり\n"
           "  //   日付/時刻の表示が食い違って React #418 になっていた(全ページ)。\n"
           "  //   マウント後にだけ時刻を持たせる。\n"
           "  const [now, setNow] = useState<Date | null>(null)")

# dateStr / timeStr を null 安全に
for i, l in enumerate(L):
    if l.strip().startswith("const dateStr ="):
        L[i] = "  const dateStr = now ? `${now.getMonth() + 1}/${now.getDate()}（${JP_DAYS[now.getDay()]}）` : ''"
        print("dateStr patched L%d" % (i + 1))
    elif l.strip().startswith("const timeStr ="):
        L[i] = ("  const timeStr = now ? `${String(now.getHours()).padStart(2, '0')}:"
                "${String(now.getMinutes()).padStart(2, '0')}` : ''")
        print("timeStr patched L%d" % (i + 1))

io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("patched OK")
