# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# QR keepリスト・trim対象・OUTFIT_PROTECT等を探す
keywords = ['outfit_protect', 'OUTFIT_PROTECT', 'leash', 'on all fours', 'four', 'dd:outfit', 'keep_outfit', 'pose_protect']
for kw in keywords:
    hits = [(i+1, l.rstrip()) for i, l in enumerate(lines) if kw in l]
    if hits:
        print(f'=== {kw} ===')
        for ln, txt in hits[:5]:
            print(f'  L{ln}: {txt[:120]}')
