import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    html = f.read()
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
# script 17 (最大) の問題箇所付近を確認
s = scripts[17]
# peach/mitsuri 近辺
for cid in ['char_kakuseizai_peach', 'char_kakuseizai_mitsuri',
            'char_kakuseizai_s2_peach', 'char_kakuseizai_s2_mitsuri',
            'char_kakuseizai_s3_peach', 'char_kakuseizai_s3_mitsuri']:
    idx = s.find(f"id:'{cid}'")
    if idx >= 0:
        print(f"{cid}: push={'female.push(' in s[idx-60:idx]}, before={s[idx-30:idx]!r}")
    else:
        print(f"{cid}: NOT IN SCRIPT17")
