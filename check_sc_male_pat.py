import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# _SC_MALE_PAT の定義を取得
for i, l in enumerate(lines, 1):
    if '_SC_MALE_PAT' in l and 'compile' in l and 56000 < i < 56140:
        print(f'{i}: {l[:200]}')
        break

# テスト
test = '(penetration:1.8),(double penetration:1.8),(cum inside:1.7),(oral sex:1.7)'
# _SC_MALE_PATのパターンをここには書けないので、キーワードだけ確認
for kw in ['penetration', 'cum inside', 'double penetration', 'oral sex', 'insertion']:
    print(f'  "{kw}" in test_lower: {kw in test.lower()}')
