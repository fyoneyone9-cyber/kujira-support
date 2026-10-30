"""
[CHAR_PROMPT_FIELD_GUARD_V1]
キャラ追加後の必須検証スクリプト。
char_prompt: フィールドがあれば即エラー（正しいフィールド名は prompt:）
使い方: python verify_char_prompt.py [char_id_prefix]
例:   python verify_char_prompt.py char_kaizo_nichijou5
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'C:\AI\ComfyUI\dashboard.html'
prefix = sys.argv[1] if len(sys.argv) > 1 else None

with open(html_path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 全キャラのpush()ブロックを抽出
blocks = re.findall(
    r"window\.CHAR_TEMPLATES\.female\.push\(\{(.+?)\}\);",
    content, re.DOTALL
)

errors = []
warnings = []
checked = 0

for block in blocks:
    id_m = re.search(r"id:\s*['\"]([^'\"]+)['\"]", block)
    if not id_m:
        continue
    char_id = id_m.group(1)
    if prefix and not char_id.startswith(prefix):
        continue
    checked += 1

    # ❌ char_prompt: はNG（サーバーが読まないフィールド名）
    if re.search(r'\bchar_prompt\s*:', block):
        errors.append(f"❌ WRONG FIELD: {char_id} → 'char_prompt:' を 'prompt:' に修正せよ")

    # ✅ prompt: があるか確認
    if not re.search(r'\bprompt\s*:', block):
        errors.append(f"❌ MISSING FIELD: {char_id} → 'prompt:' フィールドがない")

    # outfits_ref があるか
    if not re.search(r'\boutfits_ref\s*:', block):
        warnings.append(f"⚠️  NO outfits_ref: {char_id}")

    # promptが空でないか
    pm = re.search(r"\bprompt\s*:\s*['\"]([^'\"]{0,30})", block)
    if pm and len(pm.group(1).strip()) < 5:
        errors.append(f"❌ EMPTY PROMPT: {char_id} → promptが短すぎる ({repr(pm.group(1))})")

print(f"検証対象: {checked} 体")
if errors:
    print("\n".join(errors))
    sys.exit(1)
elif warnings:
    print("\n".join(warnings))
    print("✅ エラーなし（警告あり）")
else:
    print("✅ 全件OK")
