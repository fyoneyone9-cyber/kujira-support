# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

checks = ['popupAlerts', 'popupDismissed', 'setPopupAlerts', 'AlertPopup', '{AlertPopup}', 'animate-in', 'slide-in']
for chk in checks:
    found = [(i+1, l.rstrip()) for i, l in enumerate(lines) if chk in l]
    print(f'[{chk}] {len(found)} hits')
    for ln, txt in found[:2]:
        print(f'  L{ln}: {txt[:120]}')
