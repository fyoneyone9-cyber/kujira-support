#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aerithタグ消滅の中間チェックポイントを api_server_3001.py に追加する
"""
import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_FILE = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')

with open(API_FILE, encoding='utf-8', errors='replace') as f:
    content = f.read()

# チェックポイントを追加する位置と識別子
# (ユニークな前後文字列, 挿入するコード)
CHECKPOINTS = [
    # L41698の直後
    (
        'wf["6"]["inputs"]["text"] = _bypass_pos\n\n            # === BYPASS2_WF6_SEX_FILTER ===',
        'wf["6"]["inputs"]["text"] = _bypass_pos\n            _dbg_aerith = "aerith" in _bypass_pos.lower() or "final fantasy" in _bypass_pos.lower(); print(f"[AERITH_CP_41698] bypass_pos has_aerith={_dbg_aerith}", flush=True)\n\n            # === BYPASS2_WF6_SEX_FILTER ===',
    ),
    # L43534の直後 (_pos_final代入後)
    (
        'wf["6"]["inputs"]["text"] = _pos_final\n\n\n            # ── clothes_off: 服タグ除去 + 裸タグ注入 ──',
        'wf["6"]["inputs"]["text"] = _pos_final\n            _dbg_aerith43 = "aerith" in _pos_final.lower() or "final fantasy" in _pos_final.lower(); print(f"[AERITH_CP_43534] pos_final has_aerith={_dbg_aerith43}", flush=True)\n\n\n            # ── clothes_off: 服タグ除去 + 裸タグ注入 ──',
    ),
]

modified = content
for old, new in CHECKPOINTS:
    if old in modified:
        modified = modified.replace(old, new, 1)
        print(f"✅ チェックポイント追加成功")
    else:
        print(f"❌ 対象文字列が見つかりません: {old[:60]!r}")

if modified != content:
    with open(API_FILE, 'w', encoding='utf-8') as f:
        f.write(modified)
    print("書き込み完了")
else:
    print("変更なし")
