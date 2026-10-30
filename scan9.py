# 目的: 対象ジャンルの日本語名（キャラlabel）と、キャラpromptの雰囲気を確認
import re, json
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
targets = ['aigan','breedfac','groom','hyoui','jinshin','jitsufu','kinshin','kyoushi','lolidoll','lolifairy','lolifuzoku','lolify','lolihypapp','lolipreg','lolisucc','miko','rinjin','shouni','shuukyou','suimin','tsugakuro','yousha']
out = []
for g in targets:
    m = re.search(r"id:\s*['\"]char_" + g + r"_s1_[^'\"]+['\"]\s*,\s*label:\s*['\"]([^'\"]+)", s)
    m2 = re.search(r"id:\s*['\"]char_" + g + r"_s2_[^'\"]+['\"]\s*,\s*label:\s*['\"]([^'\"]+)", s)
    out.append(f"{g}: s1={m.group(1) if m else None} s2={m2.group(1) if m2 else None}")
open(r'C:\GensparkClaw\kujira-support\_s9.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
