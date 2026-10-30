#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
redcraft 40K2TDUAL でAerithを生成し、CFG/stepsが正しく設定されているか確認
期待値: cfg=5.5, steps=30, sampler=dpmpp_2m_sde, scheduler=karras
"""
import sys, io, json, time, requests, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API    = "http://127.0.0.1:3002"
COMFY  = "http://127.0.0.1:8188"
WF_DBG = pathlib.Path(r"C:\AI\ComfyUI\debug_last_real_wf.json")

CKPT = "redcraftHybridH3Krea2t_40K2TDUAL_3196558.safetensors"

PANEL = {
    "char_template_id": "char_kakuseizai_s3_ff_aerith",
    "char_id":          "char_kakuseizai_s3_ff_aerith",
    "prompt":           "(solo:2.2),(1girl:2.2),(only one person:2.0),(Aerith Gainsborough:1.9),(Final Fantasy VII:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(medium breasts:1.5),22 years old,long brown braided hair,pink ribbon,green eyes,pink dress,burning drug injected directly into vein,wincing from searing pain,vein bulging,skin flushing red where injected,upper body,dim room,eye level,(drugged high:2.0),(dilated pupils:2.0),(flushed face:1.8),(sweating:1.7),(ahegao:1.6),(trembling violently:1.5),(masterpiece:1.2),(best quality:1.2),detailed",
    "outfit_prompt":    "(solo:2.2),(1girl:2.2),(only one person:2.0),(Aerith Gainsborough:1.9),(Final Fantasy VII:1.8),(ff7:1.8)",
    "outfit_label":     "01「血管に火」テスト",
    "outfit_index":     0,
    "page_idx":         1,
    "panel_idx":        0,
    "penetration_off":  True,
    "clothes_off":      False,
    "wf_type":          "moody_krea2_v7",
    "checkpoint":       CKPT,
    "style_preset":     "",
}

print("=== redcraft 40K2TDUAL CFG確認テスト ===")
print(f"checkpoint: {CKPT}")

for attempt in range(3):
    try:
        r = requests.post(f"{API}/api/generate-panel",
            json={"panel": PANEL, "page_idx": 1, "panel_idx": 0,
                  "wf_type": "moody_krea2_v7", "checkpoint": CKPT},
            timeout=180)
        if r.status_code == 409:
            print("409 waiting..."); time.sleep(15); continue
        print(f"status: {r.status_code}")
        break
    except Exception as e:
        print(f"err: {e}"); time.sleep(10)

# last-prompt でCFG確認
lp = requests.get(f"{API}/api/last-prompt", timeout=5).json()
ksampler = lp.get("ksampler", {})
wf_actual = lp.get("wf_actual", {})

print(f"\n=== CFG/steps確認 ===")
print(f"ksampler.cfg:     {ksampler.get('cfg')}  (期待: 5.5)")
print(f"ksampler.steps:   {ksampler.get('steps')} (期待: 30)")
print(f"ksampler.sampler: {ksampler.get('sampler')} (期待: dpmpp_2m_sde)")
print(f"ksampler.sched:   {ksampler.get('scheduler')} (期待: karras)")
print(f"wf_actual.cfg:    {wf_actual.get('cfg')}")
print(f"wf_actual.steps:  {wf_actual.get('steps')}")

cfg_ok     = ksampler.get("cfg") == 5.5
steps_ok   = ksampler.get("steps") == 30
result_ok  = cfg_ok and steps_ok

print(f"\n結果: {'PASS ✅' if result_ok else 'FAIL ❌'}")
print(f"  cfg={cfg_ok} steps={steps_ok}")

# WFのKSAMPLERノードも直接確認
if WF_DBG.exists():
    with open(WF_DBG, encoding='utf-8') as f:
        wf = json.load(f)
    for nid, node in wf.items():
        if isinstance(node, dict) and node.get("class_type") == "KSampler":
            inp = node.get("inputs", {})
            print(f"  WF Node{nid} KSampler: cfg={inp.get('cfg')} steps={inp.get('steps')} sampler={inp.get('sampler_name')} sched={inp.get('scheduler')}")
