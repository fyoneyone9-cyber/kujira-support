# -*- coding: utf-8 -*-
import io
p = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
L = io.open(p, encoding="utf-8").read().split("\n")
for i in range(84, 172):
    print("%4d| %s" % (i, L[i - 1].rstrip()[:140]))
