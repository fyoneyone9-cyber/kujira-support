# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

checks = ['popupAlerts', 'popupDismissed', 'setPopupAlerts', 'AlertPopup', 'slide-in', 'animate']
for chk in checks:
    found = [(i+1, l.rstrip()) for i, l in enumerate(lines) if chk in l]
    print(f'[{chk}] {len(found)} hits')
    for ln, txt in found[:3]:
        print(f'  L{ln}: {txt[:100]}')
