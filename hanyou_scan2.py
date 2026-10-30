# -*- coding: utf-8 -*-
# 汎用カテゴリ（男性/職業・役割）の実ID数を確認（GDパターンから）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# male系
male_pats = ['char_salaryman', 'char_sarari', 'char_yankee', 'char_male_yankee', 'char_sensei', 'char_ikemen', 'char_oji', 'char_kimoi', 'char_incubus', 'char_male_student', 'char_male_college', 'char_shonen', 'char_tuxedo_mask', 'char_male_']
# job系
job_pats = ['char_jk_', 'char_jd_', 'char_ol_', 'char_teacher_', 'char_nurse_', 'char_maid_', 'char_idol_', 'char_policewoman_', 'char_swimcoach_', 'char_office_lady']
print('=== male ===')
tot = set()
for p in male_pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    if ids:
        print(p, len(ids), ids[:8])
        tot.update(ids)
print('male total unique:', len(tot))
print('=== job ===')
tot2 = set()
for p in job_pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    if ids:
        print(p, len(ids), ids[:8])
        tot2.update(ids)
print('job total unique:', len(tot2))
