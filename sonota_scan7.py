# -*- coding: utf-8 -*-
# 「その他」80体の実体特定:
# 1) idOverride形式（触手幼女/小学生/中学生/ナースの変種定義） 2) char_youjo_flat_等の乳サイズ系（日本語名ID）
# 3) エンタコール乳児
import re, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

# idOverride 全件
ov = re.findall(r'"idOverride":\s*"(char_[a-zA-Z0-9_]+)"', s)
print('idOverride count:', len(ov))
pref = collections.Counter('_'.join(x.split('_')[:3]) for x in ov)
for k, v in sorted(pref.items()):
    print('  OV', k, v)

# 日本語を含むid（char_youjo_flat_さくら 等）
jids = sorted(set(re.findall(r"id:\s*'(char_[a-zA-Z0-9_]*[^\x00-\x7F'][^']*)'", s)))
print('japanese-char ids:', len(jids))
pref2 = collections.Counter(re.match(r"(char_[a-z0-9_]+_)", x).group(1) for x in jids)
for k, v in sorted(pref2.items()):
    print('  JP', k, v)

# エンタコール乳児のid
for m in list(re.finditer(r'エンタコール', s)):
    i = m.start()
    back = s[max(0,i-400):i+50]
    ids = re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", back)
    if ids:
        print('ENTA near id:', ids[-1])
# 乳児系idの候補
for p in ['char_enta', 'char_tentacall', 'char_entacall', 'nyuuji']:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]*" + p.replace('char_','') + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(p, len(ids), ids[:12])
