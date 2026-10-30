#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, io, json, time, requests, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API = "http://127.0.0.1:3002"

PANEL = {
    "char_template_id": "char_kakuseizai_s3_ff_tifa",
    "char_id": "char_kakuseizai_s3_ff_tifa",
    "prompt": "(solo:2.2),(1girl:2.2),(only one person:2.0),(Tifa Lockhart:1.9),(Final Fantasy VII:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(large breasts:1.5),20 years old,long black hair,red eyes,black tank top,black mini skirt,red gloves,red boots,upper body",
    "outfit_prompt": "(solo:2.2),(1girl:2.2),(only one person:2.0),(Tifa Lockhart:1.9),(Final Fantasy VII:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(large breasts:1.5),20 years old,long black hair,red eyes,black tank top",
    "outfit_label": "00「基本衣装」",
    "outfit_index": 0,
    "page_idx": 0,
    "panel_idx": 0,
    "style_preset": "moody_krea2_premium",
    "wf_type": "moody_krea2_v7",
    "checkpoint": "moodyKrea2MixUncensoredV8SEGoes_v80_int8.safetensors",
    "penetration_off": True,
    "clothes_off": False,
}

print("=== ティファ動作確認 ===")
try:
    r = requests.post(f"{API}/api/generate-panel",
        json={"panel": PANEL, "page_idx": 0, "panel_idx": 0,
              "wf_type": "moody_krea2_v7",
              "checkpoint": "moodyKrea2MixUncensoredV8SEGoes_v80_int8.safetensors"},
        timeout=120)
    print(f"status: {r.status_code}")
    if r.status_code != 200:
        print(f"エラー: {r.text[:300]}")
    else:
        print("✅ 生成成功")
except Exception as e:
    print(f"リクエストエラー: {e}")

# last-prompt確認
r2 = requests.get(f"{API}/api/last-prompt", timeout=5)
data = r2.json()
pp = data.get("positive_prompt", "")
has_tifa = "tifa" in pp.lower() or "lockhart" in pp.lower() or "ff7" in pp.lower()
print(f"\nTifaタグ in positive_prompt: {'✅' if has_tifa else '❌'}")
print(f"positive_prompt先頭300: {pp[:300]}")
print(f"lora3: {data.get('lora3','')!r}")
print(f"lora3_matched_key: {data.get('dbg_lora3_matched_key','')!r}")
print(f"lora_nodes: {data.get('lora_nodes','?')}")
