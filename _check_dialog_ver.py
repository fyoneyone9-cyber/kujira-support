# -*- coding: utf-8 -*-
"""配信中の dialog が最新版か確認する。"""
import io

d = io.open(r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html",
            encoding="utf-8").read()
checks = [
    ("タブを動的読込(getSheetNames)", "getSheetNames" in d),
    ("バージョン表示(getVersion)", "getVersion" in d),
    ("自動判定(suggestSheets)", "suggestSheets" in d),
    ("--- 以下は古い版の痕跡。全部 False が正 ---", None),
    ("PMS名の入力欄", 'id="pms"' in d),
    ("カードキーのメーカー欄", "cardkeyMaker" in d),
    ("固定チェックボックス chk_pms", "chk_pms" in d),
    ("フロントチェックイン", "frontci" in d or "\u30d5\u30ed\u30f3\u30c8" in d),
]
for label, v in checks:
    if v is None:
        print(label)
    else:
        print("  %-34s %s" % (label, v))
print("\nファイルサイズ: %d bytes" % len(d.encode("utf-8")))
