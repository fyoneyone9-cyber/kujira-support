import sys, json, copy
sys.path.insert(0,'C:/AI/ComfyUI')
sys.stdout.reconfigure(encoding='utf-8')
import quality_rules as qr
import importlib; importlib.reload(qr)

with open(r'C:\AI\ComfyUI\debug_last_real_wf.json', encoding='utf-8', errors='replace') as f:
    d = json.load(f)

pos_before = d['6']['inputs']['text']
wf = copy.deepcopy(d)
wf2, log = qr.apply_quality_rules(wf, wf_type='moody_krea2_v7', ckpt='redcraftHybridH3Krea2t_30Krea2_fp8')
pos_after = wf2['6']['inputs']['text']
tags_before = [t.strip() for t in pos_before.split(',') if t.strip()]
tags_after  = [t.strip() for t in pos_after.split(',') if t.strip()]

print(f'POS: {len(tags_before)} -> {len(tags_after)} tags')
print(f'CHARS: {len(pos_before)} -> {len(pos_after)} chars')
print()
print('--- remaining tags ---')
for t in tags_after:
    print(t)
