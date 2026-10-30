import sys, re
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'C:\AI\ComfyUI\dashboard.html'
with open(html_path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# S5キャラの char_prompt: → prompt: に置換
# 対象: char_kaizo_nichijou5_ を含むオブジェクト内の char_prompt フィールド
count = 0
def fix_char_prompt(m):
    global count
    count += 1
    return m.group().replace('char_prompt:', 'prompt:')

# S5ブロック全体を対象に置換
# nichijou5のpushブロック内のみ
pattern = re.compile(
    r"(window\.CHAR_TEMPLATES\.female\.push\(\{[^}]*char_kaizo_nichijou5_[^}]*\}\);)",
    re.DOTALL
)

def fix_block(m):
    block = m.group(1)
    fixed = block.replace('char_prompt:', 'prompt:')
    if fixed != block:
        global count
        count += 1
    return fixed

new_content = pattern.sub(fix_block, content)

if new_content == content:
    print("変更なし - パターンが見つからない可能性。手動確認が必要")
    # もっと単純な置換を試す
    # [S5 chars added] ブロックを探す
    idx = content.find('// [S5 chars added]')
    if idx >= 0:
        # S5ブロックの終わり（次の </script>）まで
        end = content.find('</script>', idx)
        s5_block = content[idx:end]
        fixed_block = s5_block.replace('  char_prompt:', '  prompt:')
        if fixed_block != s5_block:
            new_content = content[:idx] + fixed_block + content[end:]
            print(f"手動置換成功: {s5_block.count('char_prompt:')} 箇所を修正")
        else:
            print("S5ブロック内にchar_promptが見つからない")
    else:
        print("[S5 chars added] マーカーが見つからない")
else:
    print(f"修正完了: {count} ブロック")

# バージョン更新
ver_m = re.search(r'content="(\d+)"', new_content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    new_content = new_content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"version: {old_ver} → {new_ver}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

# 確認
with open(html_path, encoding='utf-8', errors='replace') as f:
    c2 = f.read()
m = re.search(r'id:\s*[\'"]char_kaizo_nichijou5_tifa[\'"][^\}]{0,300}', c2)
if m:
    print("\n=== 修正後 S5 tifa ===")
    print(m.group()[:300])
