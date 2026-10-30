import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# L11359の global _last_gen_meta を try ブロックから取り出して関数先頭に移動
# まず関数定義を探す (L11359より前のdef)
target_line = 11359 - 1  # 0-indexed

# 該当のglobal行を削除
assert 'global _last_gen_meta' in lines[target_line], repr(lines[target_line])

# 含む関数の def を探す
func_start = None
for i in range(target_line, -1, -1):
    if lines[i].strip().startswith('def ') and not lines[i].startswith(' '):
        func_start = i
        break
    if lines[i].startswith('def ') or (lines[i].startswith('    def ') and i < target_line):
        # インデントを確認
        pass

# 最も近い def を探す（インデントレベル問わず）
for i in range(target_line, -1, -1):
    if re.match(r'^(def |    def |\tasync def )', lines[i]):
        func_start = i
        break

print(f"Function found at L{func_start+1}: {lines[func_start].rstrip()[:80]}")
print(f"Global decl at L{target_line+1}: {lines[target_line].rstrip()}")

# 関数の最初の実行文の前（docstring/pass/既存global後）にglobal宣言を挿入
# 戦略: try行を見つけてそのglobal行だけ削除し、関数先頭に追加する
# 簡単に: global宣言を try の外・関数直下に移動

# 現在のglobal行を削除
del lines[target_line]  # "        global _last_gen_meta\n" を削除

# 関数定義の次の行（インデント合わせて）に global を挿入
insert_pos = func_start + 1
# コメント・docstringを飛ばす
while insert_pos < len(lines):
    stripped = lines[insert_pos].strip()
    if stripped.startswith('#') or stripped.startswith('"""') or stripped == '':
        insert_pos += 1
    else:
        break

# インデントを関数本体に合わせる（4スペース）
lines.insert(insert_pos, '    global _last_gen_meta\n')
print(f"Inserted global at L{insert_pos+1}")

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
