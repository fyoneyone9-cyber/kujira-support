import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 衣装・状況タグ（outfitで指定すべきもの）がbaseに入っていたら問題
BAD_KEYWORDS = [
    'torn', 'pushed aside', 'disheveled', 'ripped', 'lifted', 'pulled up',
    'pulled down', 'off shoulder', 'topless', 'naked', 'nude', 'exposed',
    'school uniform', 'walking', 'sitting', 'lying', 'crying', 'screaming',
    'day 0', 'day 1', 'number collar', 'mattress', 'bedroom', 'dark street',
    'bound', 'tied', 'restrained', 'blindfold', 'gag',
]

# 全char_rape_ を抽出
# push形式: window.CHAR_TEMPLATES.female.push({id: 'char_rape_...'
pattern = re.compile(r"window\.CHAR_TEMPLATES\.female\.push\(\{([^;]{0,3000}?)\}\);", re.DOTALL)

issues = []
ok = []

for m in pattern.finditer(content):
    block = m.group(1)
    id_m = re.search(r"id:\s*'(char_rape[^']+)'", block)
    if not id_m:
        continue
    cid = id_m.group(1)
    prompt_m = re.search(r"prompt:\s*'([^']{0,500})'", block)
    if not prompt_m:
        continue
    prompt = prompt_m.group(1).lower()
    
    bad_found = [k for k in BAD_KEYWORDS if k in prompt]
    if bad_found:
        issues.append((cid, bad_found, prompt_m.group(1)[:150]))
    else:
        ok.append(cid)

print(f'=== 問題あり: {len(issues)}体 ===')
for cid, bads, prompt in issues:
    print(f'\n[NG] {cid}')
    print(f'  NG keys: {bads}')
    print(f'  prompt: {prompt}')

print(f'\n=== 問題なし: {len(ok)}体 ===')
for c in ok:
    print(f'  [OK] {c}')
