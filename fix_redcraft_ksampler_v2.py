#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix v2: KSAMPLER_NON_QW21のelse:ブロックのindentが間違っていた(8→4に修正)
"""
import sys, io, pathlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
bak = API.parent / (API.name + ".bak_ksampler_v2")
shutil.copy2(API, bak)
print(f"Backup: {bak.name}")

with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 間違ったindent=8のelse:ブロックを削除して、indent=4の正しい位置に挿入する
# 削除対象: indent=8 の else: ブロック（KSAMPLER_NON_QW21）
OLD_WRONG = '''        else:
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

        # [REDCRAFT_PENIS_GUARD_V1'''

# 正しいindent=4のelse:ブロック
NEW_CORRECT = '''    else:
        # [KSAMPLER_NON_QW21_V1 2026-10-22] _is_qw21_ks=False経路(redcraft 40K2TDUAL等)の
        # CFG/steps設定。_is_qw21_ks=Trueブロック内にしか定義がなかったため未設定だった
        # Fix v1でindent=8の誤挿入→v2でindent=4に修正
        import os as _os_nq
        def _nq_f(_k, _d):
            try: return float(_os_nq.environ.get(_k, "") or _d)
            except: return _d
        def _nq_i(_k, _d):
            try: return int(float(_os_nq.environ.get(_k, "") or _d))
            except: return _d
        _nq_sampler = _os_nq.environ.get("MOODY_SAMPLER", "") or ""
        _nq_sched   = _os_nq.environ.get("MOODY_SCHED", "") or ""
        _nq_is_redcraft = "redcraft" in (_ckpt_fc or "") or "amateur" in (_ckpt_fc or "")
        _nq_is_moody    = "moody" in (_ckpt_fc or "")
        _nq_rc_all      = (_ckpt_fc or "").lower()
        _nq_is_rc_v40   = "_40" in _nq_rc_all or "40k" in _nq_rc_all
        _nq_is_rc_v30   = ("_30" in _nq_rc_all or "30k" in _nq_rc_all or "fp8" in _nq_rc_all) and not _nq_is_rc_v40
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

        # [REDCRAFT_PENIS_GUARD_V1'''

if OLD_WRONG in content:
    content = content.replace(OLD_WRONG, NEW_CORRECT, 1)
    with open(API, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ fix v2 applied")
else:
    print("❌ target not found - checking partial...")
    # 部分確認
    if "KSAMPLER_NON_QW21_V1" in content:
        print("  NON_QW21ブロック自体は存在する")
    if "        else:" in content and "KSAMPLER_NON_QW21" in content:
        print("  indent=8のelse:が残っている可能性")
