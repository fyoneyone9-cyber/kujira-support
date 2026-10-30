# -*- coding: utf-8 -*-
# job 33体の内訳を完全確定（teacher/maid/ol/jd/policewoman/swimcoach/office_lady含む）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
pats = ['char_jk_', 'char_jd_', 'char_ol_', 'char_teacher_', 'char_nurse_', 'char_maid_', 'char_idol_', 'char_policewoman_', 'char_swimcoach_', 'char_office_lady']
tot = set()
for p in pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    for x in ids:
        tot.add(x)
    if ids:
        print(p, len(ids))
        for x in ids:
            print('   ', x)
print('total:', len(tot))
