#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FFキャラ（Aerith/Tifa）へのLoRA自動注入を無効化する
- _CHAR_LORA_MAP の ff_aerith / ff_tifa エントリを削除
- _FF_CHAR_LORAS の tifa / aerith エントリを削除
- テキストプロンプトのみで描写
"""
import sys, io, pathlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
bak = API.parent / (API.name + ".bak_no_ff_lora")
shutil.copy2(API, bak)
print(f"Backup: {bak.name}")

with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

original = content
changes = 0

# 1) _FF_CHAR_LORAS の tifa / aerith / yuffie → 空辞書に（存在しないLoRAを参照しない）
OLD1 = '''            _FF_CHAR_LORAS = {

                "tifa":  ("tifa_lockhart_xl.safetensors", 0.7, 0.7),

                "aerith": ("aerith_gainsborough_xl.safetensors", 0.7, 0.7),

                "yuffie": ("yuffie_kisaragi_xl.safetensors", 0.6, 0.6),

            }'''
NEW1 = '''            _FF_CHAR_LORAS = {}  # [FF_LORA_DISABLED 2026-10-21] LoRA不使用・テキストプロンプトのみ'''
if OLD1 in content:
    content = content.replace(OLD1, NEW1, 1)
    changes += 1
    print("✅ _FF_CHAR_LORAS cleared")
else:
    print("⚠️  _FF_CHAR_LORAS not found as expected")

# 2) _CHAR_LORA_MAP の ff_aerith エントリを削除
OLD2 = (
    '                "ff_aerith":       ("aerith_illu.safetensors",          "defait", 0.8, "aerith_illu.safetensors", "defait", 0.8),  # [AERITH_REAL_LORA_FIX 2026-10-21] real時もaerith_illu使用\n'
)
NEW2 = '                # "ff_aerith": LoRA disabled [FF_LORA_DISABLED 2026-10-21]\n'
if OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    changes += 1
    print("✅ ff_aerith entry removed from _CHAR_LORA_MAP")
else:
    print("⚠️  ff_aerith entry not found")

# 3) _CHAR_LORA_MAP の ff_tifa / kaizou3_tifa / kaizou_tifa エントリを削除
OLD3 = (
    '                "ff_tifa":         ("Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors", "TifaFF7Remake", 0.85, "Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors", "TifaFF7Remake", 0.8),\n'
    '                "kaizou3_tifa":    ("Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors", "TifaFF7Remake", 0.85, "Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors", "TifaFF7Remake", 0.8),\n'
    '                "kaizou_tifa":     ("Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors", "TifaFF7Remake", 0.85, "Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors", "TifaFF7Remake", 0.8),\n'
)
NEW3 = '                # ff_tifa/kaizou3_tifa/kaizou_tifa: LoRA disabled [FF_LORA_DISABLED 2026-10-21]\n'
if OLD3 in content:
    content = content.replace(OLD3, NEW3, 1)
    changes += 1
    print("✅ ff_tifa/kaizou3_tifa/kaizou_tifa entries removed from _CHAR_LORA_MAP")
else:
    print("⚠️  ff_tifa entries not found")

print(f"\n変更件数: {changes}/3")

if content != original:
    with open(API, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ api_server_3001.py saved")
else:
    print("変更なし")
