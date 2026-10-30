# -*- coding: utf-8 -*-
import io, re
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
for i, l in enumerate(L, 1):
    if re.search(r"IntegRow|pms_linked|smartlock_linked|\u672a\u9023\u643a|\u8981\u5bfe\u5fdc", l):
        print("%5d| %s" % (i, l.rstrip()[:180]))
