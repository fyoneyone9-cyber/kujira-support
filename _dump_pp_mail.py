# -*- coding: utf-8 -*-
import io, csv, glob, os, json

p = [x for x in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
     if "\u5c0e\u5165\u652f\u63f4" in os.path.basename(x)][0]
print("FILE:", os.path.basename(p))
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))
io.open(r"C:\GensparkClaw\kujira-support\_ppmail.json", "w", encoding="utf-8").write(
    json.dumps(rows, ensure_ascii=False, indent=1))
print("rows:", len(rows))
