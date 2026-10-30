# -*- coding: utf-8 -*-
import io, csv, glob, os, json

p = [x for x in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
     if "PayPay" in os.path.basename(x)][0]
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))
out = {"rows": []}
for i, r in enumerate(rows):
    out["rows"].append({"i": i + 1, "cells": {str(j): c for j, c in enumerate(r) if c.strip()}})
io.open(r"C:\GensparkClaw\kujira-support\_paypay.json", "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=1))
print("WROTE rows=%d" % len(rows))
