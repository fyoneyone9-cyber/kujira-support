#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix: KREA2_KSAMPLERブロックが _is_qw21_ks=False 時にスキップされる問題
原因: _is_redcraft_ks等の定義とKSAMPLERループが全て `if _is_qw21_ks:` ブロック内に
      入っているため、QW21でないredcraft(40K2TDUAL等)はCFG/stepsが設定されない
修正: `if _is_qw21_ks: ... else:` の else 節にredcraft/moody用KSAMPLERループを追加
"""
import sys, io, pathlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
bak = API.parent / (API.name + ".bak_redcraft_ksampler_fix")
shutil.copy2(API, bak)
print(f"Backup: {bak.name}")

with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

# _is_qw21_ks=False経路で REDCRAFT_PENIS_GUARD_V1 の前に
# redcraft/moody用KSAMPLERを設定するelseブロックを挿入する
#
# 挿入ポイント: `if _is_qw21_ks:` ブロックの終わり
# "# [REDCRAFT_PENIS_GUARD_V1" の直前に else: ブロックを追加

OLD = '''        # [REDCRAFT_PENIS_GUARD_V1 2026-10-10] RedCraft/Amateur(moody_krea2_v7, qwen3vl CLIP)は'''

NEW = '''        else:
            # [KSAMPLER_NON_QW21_V1 2026-10-22] _is_qw21_ks=False経路(redcraft 40K2TDUAL等)の
            # CFG/steps設定。_is_qw21_ks=Trueブロック内にしか定義がなかったため未設定だった
            # Fix: 根本原因はインデントのスコープ外れ。else節で同等の判定・設定を実施する
            import os as _os_nq
            def _nq_f(_k, _d):
                try: return float(_os_nq.environ.get(_k, "") or _d)
                except: return _d
            def _nq_i(_k, _d):
                try: return int(float(_os_nq.environ.get(_k, "") or _d))
                except: return _d
            _nq_sampler = _os_nq.environ.get("MOODY_SAMPLER", "") or ""
            _nq_sched   = _os_nq.environ.get("MOODY_SCHED", "") or ""
            _nq_is_redcraft  = "redcraft" in (_ckpt_fc or "") or "amateur" in (_ckpt_fc or "")
            _nq_is_moody     = "moody" in (_ckpt_fc or "")
            _nq_rc_all       = (_ckpt_fc or "").lower()
            _nq_is_rc_v40    = "_40" in _nq_rc_all or "40k" in _nq_rc_all
            _nq_is_rc_v30    = ("_30" in _nq_rc_all or "30k" in _nq_rc_all or "fp8" in _nq_rc_all) and not _nq_is_rc_v40
            for _nid, _nd in wf.items():
                if not (isinstance(_nd, dict) and _nd.get("class_type") == "KSampler"):
                    continue
                if _nq_is_redcraft:
                    if _nq_is_rc_v40:
                        _nd["inputs"]["cfg"]          = _nq_f("REDCRAFT_V40_CFG", 5.5)
                        _nd["inputs"]["steps"]        = _nq_i("REDCRAFT_V40_STEPS", 30)
                        _nd["inputs"]["sampler_name"] = _nq_sampler or "dpmpp_2m_sde"
                        _nd["inputs"]["scheduler"]    = _nq_sched   or "karras"
                        print(f"[KSAMPLER_NON_QW21] RedCraft v40 cfg=5.5 steps=30", flush=True)
                    elif _nq_is_rc_v30:
                        _nd["inputs"]["cfg"]          = _nq_f("REDCRAFT_V30_CFG", 4.0)
                        _nd["inputs"]["steps"]        = _nq_i("REDCRAFT_V30_STEPS", 24)
                        _nd["inputs"]["sampler_name"] = _nq_sampler or "dpmpp_2m"
                        _nd["inputs"]["scheduler"]    = _nq_sched   or "karras"
                        print(f"[KSAMPLER_NON_QW21] RedCraft v30 cfg=4.0 steps=24", flush=True)
                    else:
                        _nd["inputs"]["cfg"]   = _nq_f("REDCRAFT_CFG", 3.6)
                        _nd["inputs"]["steps"] = _nq_i("REDCRAFT_STEPS", 16)
                        print(f"[KSAMPLER_NON_QW21] RedCraft fallback cfg=3.6 steps=16", flush=True)
                elif _nq_is_moody:
                    _nd["inputs"]["cfg"]   = _nq_f("MOODY_CFG", 1.8)
                    _nd["inputs"]["steps"] = _nq_i("MOODY_STEPS", 14)
                    print(f"[KSAMPLER_NON_QW21] Moody cfg=1.8 steps=14", flush=True)
                else:
                    _nd["inputs"]["cfg"]   = _nq_f("MOODY_CFG", 2.5)
                    _nd["inputs"]["steps"] = _nq_i("MOODY_STEPS", 14)
                    print(f"[KSAMPLER_NON_QW21] fallback cfg=2.5 steps=14", flush=True)

        # [REDCRAFT_PENIS_GUARD_V1 2026-10-10] RedCraft/Amateur(moody_krea2_v7, qwen3vl CLIP)は'''

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    with open(API, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ fix applied")
else:
    print("❌ target not found")
