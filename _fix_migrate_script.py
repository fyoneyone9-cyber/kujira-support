# -*- coding: utf-8 -*-
"""移行対象をボタン語彙の完全一致だけに絞る。
p400_status には CSV由来の自由記述(日付/送り状番号/「済 2024/04予定」等)が入っており、
それを dashboard_todos に移すと今後CSVで更新されなくなる副作用が出るため。"""
import io

p = r"C:\GensparkClaw\kujira-support\_migrate_manual_status.js"
s = io.open(p, encoding="utf-8").read()

old = ("      // CSV\u5217\u306b\u5024\u304c\u3042\u308a\u3001todos\u5074\u306b\u307e\u3060\u7121\u3044"
       "\u5834\u5408\u3060\u3051\u79fb\u884c\u3059\u308b(\u65e2\u5b58\u306etodos\u5024\u3092\u58ca\u3055\u306a\u3044)\n"
       "      if (v && v !== '--' && v !== '-' && !todos[todoKey]) add[todoKey] = v;")
assert s.count(old) == 1, "anchor1"
new = ("      // \u3010\u91cd\u8981\u3011\u30dc\u30bf\u30f3\u8a9e\u5f59\u306b\u5b8c\u5168\u4e00\u81f4\u3059\u308b"
       "\u5024\u3060\u3051\u3092\u79fb\u884c\u3059\u308b\u3002\n"
       "      //   p400_status \u306b\u306f CSV\u7531\u6765\u306e\u81ea\u7531\u8a18\u8ff0"
       "(\u65e5\u4ed8/\u9001\u308a\u72b6\u756a\u53f7/\u300c\u6e08 2024/04\u4e88\u5b9a\u300d\u7b49)\u3082\n"
       "      //   \u5165\u3063\u3066\u304a\u308a\u3001\u305d\u308c\u307e\u3067 todos \u306b\u79fb\u3059\u3068"
       "\u4eca\u5f8cCSV\u3067\u66f4\u65b0\u3055\u308c\u306a\u304f\u306a\u308b\u526f\u4f5c\u7528\u304c\u51fa\u308b\u3002\n"
       "      //   \u624b\u52d5\u30dc\u30bf\u30f3\u3067\u5165\u308a\u3046\u308b\u5024\u3060\u3051\u3092"
       "\u300c\u624b\u52d5\u5024\u300d\u3068\u307f\u306a\u3059\u3002\n"
       "      if (v && BTN_VOCAB.includes(v) && !todos[todoKey]) add[todoKey] = v;")
s = s.replace(old, new, 1)

old2 = "const MAP = ["
assert s.count(old2) == 1, "anchor2"
new2 = ("// UI\u306e\u30dc\u30bf\u30f3\u304c\u51fa\u3057\u3046\u308b\u5024(EQUIP_STATUSES + PayCube\u5c02\u7528)\u3002"
        "\u3053\u308c\u4ee5\u5916\u306fCSV\u7531\u6765\u3068\u307f\u306a\u3059\u3002\n"
        "const BTN_VOCAB = ['\u672a\u767a\u6ce8', '\u767a\u6ce8\u6e08\u307f', '\u5165\u8377\u5c65\u6b74', "
        "'\u767a\u9001\u6e08\u307f', '\u7d0d\u54c1\u5b8c\u4e86', '\u8a2d\u5b9a\u5b8c\u4e86', "
        "'\u793e\u9577\u627f\u8a8d\u5f85\u3061']\n\nconst MAP = [")
s = s.replace(old2, new2, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("migrate script fixed")
