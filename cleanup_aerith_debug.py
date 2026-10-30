#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
デバッグコードを削除して本番状態に戻す
削除対象:
  - [QR_AERITH_DEBUG] ブロック (L48666-48682)
  - [QR_AERITH_DEBUG2] ブロック (L56672-56692)
  - [AERITH_CP_38593] print
  - [AERITH_CP_38595] print
  - [AERITH_CP_BYPASS_ENTRY] print
  - [AERITH_CP_41698] print
  - [AERITH_CP_43534] print
  - [AERITH_CP_HT2] print
  - [REAL_BOOST_AERITH_CHECK] ブロック (L56703-56714)
保持:
  - [OP_REINJECT_GUARD_V1] (修正として恒久保持)
"""
import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_FILE = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')

with open(API_FILE, encoding='utf-8', errors='replace') as f:
    content = f.read()

import shutil
bak = API_FILE.parent / (API_FILE.name + ".bak_predebugclean")
shutil.copy2(API_FILE, bak)
print(f"Backup: {bak.name}")

original = content

# ---- 削除ブロック定義 (old_text -> new_text) ----
CLEANUPS = [
    # [AERITH_CP_38593] print と [AERITH_CP_38595] print
    (
        '        print(f"[AERITH_CP_38593] is_moody_zit={_is_moody_zit_wf} use_anime={_use_anime_wf_s} fp_has_aerith={\'aerith\' in full_positive.lower()}", flush=True)\n'
        '        if not _is_moody_zit_wf:\n'
        '\n'
        '            if "6" in wf: wf["6"]["inputs"]["text"]=full_positive\n'
        '            print(f"[AERITH_CP_38595] wf6_after_fp={\'aerith\' in (wf.get(\'6\') or {}).get(\'inputs\',{}).get(\'text\',\'\').lower()}", flush=True)',
        '        if not _is_moody_zit_wf:\n'
        '\n'
        '            if "6" in wf: wf["6"]["inputs"]["text"]=full_positive',
    ),
    # [AERITH_CP_BYPASS_ENTRY] print
    (
        '        _dbg_wf6_before_bypass = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '        print(f"[AERITH_CP_BYPASS_ENTRY] wf6_has_aerith={\'aerith\' in _dbg_wf6_before_bypass.lower()} len={len(_dbg_wf6_before_bypass)}", flush=True)\n'
        '\n'
        '        if "6" in wf:',
        '        if "6" in wf:',
    ),
    # [QR_AERITH_DEBUG] ブロック (first apply_quality_rules前後)
    (
        '            # [QR_AERITH_DEBUG] apply_quality_rules前後のAerithタグ確認\n'
        '            _qr_before_txt = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '            _qr_aerith_before = \'aerith\' in _qr_before_txt.lower() or \'final fantasy\' in _qr_before_txt.lower()\n'
        '            print(f"[QR_AERITH_BEFORE] aerith={_qr_aerith_before} prio_has_aerith={\'aerith\' in (_qr_prio or \'\').lower()}", flush=True)\n',
        '',
    ),
    (
        '            _qr_after_txt = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '            _qr_aerith_after = \'aerith\' in _qr_after_txt.lower() or \'final fantasy\' in _qr_after_txt.lower()\n'
        '            print(f"[QR_AERITH_AFTER] aerith={_qr_aerith_after}", flush=True)\n'
        '            if _qr_aerith_before and not _qr_aerith_after:\n'
        '                print(f"[QR_AERITH_LOST_IN_QR] prio={_qr_prio[:200]!r}", flush=True)\n'
        '                print(f"[QR_AERITH_LOST_BEFORE] {_qr_before_txt[:400]!r}", flush=True)\n'
        '                print(f"[QR_AERITH_LOST_AFTER] {_qr_after_txt[:400]!r}", flush=True)\n',
        '',
    ),
    # [QR_AERITH_DEBUG2] ブロック (second apply_quality_rules前後)
    (
        '            # [QR_AERITH_DEBUG2] アニメルートapply_quality_rules前後のAerithタグ確認\n'
        '            _qr2_before_txt = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '            _qr2_aerith_before = \'aerith\' in _qr2_before_txt.lower() or \'final fantasy\' in _qr2_before_txt.lower()\n'
        '            print(f"[QR_AERITH2_BEFORE] aerith={_qr2_aerith_before} prio_has_aerith={\'aerith\' in (_qr_prio or \'\').lower()}", flush=True)\n',
        '',
    ),
    (
        '            _qr2_after_txt = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '            _qr2_aerith_after = \'aerith\' in _qr2_after_txt.lower() or \'final fantasy\' in _qr2_after_txt.lower()\n'
        '            print(f"[QR_AERITH2_AFTER] aerith={_qr2_aerith_after}", flush=True)\n'
        '            if _qr2_aerith_before and not _qr2_aerith_after:\n'
        '                print(f"[QR_AERITH2_LOST] prio={(_qr_prio or \'\')[:200]!r}", flush=True)\n'
        '                print(f"[QR_AERITH2_LOST_AFTER] {_qr2_after_txt[:400]!r}", flush=True)\n',
        '',
    ),
    # [REAL_BOOST_AERITH_CHECK] ブロック
    (
        '                    _rb_before = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '                    wf, _rb_log = _pp.real_boost(wf, tag="real")\n'
        '                    _rb_after = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '                    _aerith_before = \'aerith\' in _rb_before.lower() or \'final fantasy\' in _rb_before.lower()\n'
        '                    _aerith_after = \'aerith\' in _rb_after.lower() or \'final fantasy\' in _rb_after.lower()\n'
        '                    print(f"[REAL_BOOST_AERITH_CHECK] before={_aerith_before} after={_aerith_after}", flush=True)\n'
        '                    if _aerith_before and not _aerith_after:\n'
        '                        print(f"[REAL_BOOST_AERITH_LOST] before={_rb_before[:200]!r}", flush=True)\n'
        '                        print(f"[REAL_BOOST_AERITH_LOST] after={_rb_after[:200]!r}", flush=True)\n',
        '                    wf, _rb_log = _pp.real_boost(wf, tag="real")\n',
    ),
    # [AERITH_CP_41698] print
    (
        '            wf["6"]["inputs"]["text"] = _bypass_pos\n'
        '            _dbg_aerith = "aerith" in _bypass_pos.lower() or "final fantasy" in _bypass_pos.lower(); print(f"[AERITH_CP_41698] bypass_pos has_aerith={_dbg_aerith}", flush=True)\n',
        '            wf["6"]["inputs"]["text"] = _bypass_pos\n',
    ),
    # [AERITH_CP_43534] print
    (
        '            wf["6"]["inputs"]["text"] = _pos_final\n'
        '            _dbg_aerith43 = "aerith" in _pos_final.lower() or "final fantasy" in _pos_final.lower(); print(f"[AERITH_CP_43534] pos_final has_aerith={_dbg_aerith43}", flush=True)\n',
        '            wf["6"]["inputs"]["text"] = _pos_final\n',
    ),
    # [AERITH_CP_HT2] print
    (
        '        # === WF6_SHOUGAKU_HEIGHT_FIX (waisnack_real) ===\n'
        '        _dbg_ht2_wf6 = (wf.get("6") or {}).get("inputs",{}).get("text","")\n'
        '        print(f"[AERITH_CP_HT2] wf6_has_aerith={\'aerith\' in _dbg_ht2_wf6.lower()} len={len(_dbg_ht2_wf6)}", flush=True)\n'
        '        if "6" in wf:',
        '        # === WF6_SHOUGAKU_HEIGHT_FIX (waisnack_real) ===\n'
        '        if "6" in wf:',
    ),
]

replaced = 0
for old, new in CLEANUPS:
    if old in content:
        content = content.replace(old, new, 1)
        replaced += 1
        print(f"  ✅ Removed debug block ({old[:50]!r}...)")
    else:
        print(f"  ⚠️  Not found: {old[:60]!r}")

print(f"\nTotal removed: {replaced}/{len(CLEANUPS)}")

if content != original:
    with open(API_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ api_server_3001.py saved")
else:
    print("No changes made")
