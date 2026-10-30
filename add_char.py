"""
add_char.py — dashboard.html キャラ安全追加スクリプト
=======================================================

使い方:
  1. このファイルの CHARS_TO_ADD リストにキャラ定義を書く
  2. python add_char.py を実行
  3. node --check が自動で走り、エラーがあれば追加されない

フォーマット:
  全キャラ push() 形式（2026-10-21統一済み）
  配列形式 }, { は使わない

outfits_ref 参照先:
  S0093 = ロヒプノール標準
  S0163 = ピンサロ標準
  S0210 = 覚醒剤アへ顔
  S0250 = 洗脳改造娘S3
  (outfit_sets.json で確認)
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')

DASHBOARD = r'C:\AI\ComfyUI\dashboard.html'

# ===== ここにキャラを定義する =====
# 例:
# CHARS_TO_ADD = [
#   {
#     'id': 'char_xxx_yyy_A',
#     'label': '表示名',
#     'gender': 'female',
#     'age': 'jk',           # youchien / shougaku / chuugaku / jk / adult
#     'prompt': '...',
#     'neg': '...',
#     'patterns_ref': 'S0093',
#     'outfits_ref': 'S0000',
#   },
# ]
CHARS_TO_ADD = [
    # ここに追加するキャラを書く
]
# ===================================

def obj_to_js(d):
    """Pythondict → JSオブジェクト文字列"""
    # [CHAR_PROMPT_FIELD_GUARD_V1] 誤ったフィールド名を即エラー
    if 'char_prompt' in d:
        raise ValueError(f"❌ WRONG FIELD 'char_prompt' in {d.get('id','?')} → 正しくは 'prompt'")
    if 'prompt' not in d:
        raise ValueError(f"❌ MISSING FIELD 'prompt' in {d.get('id','?')} → promptフィールドが必須")
    lines = ['window.CHAR_TEMPLATES.female.push({']
    for k, v in d.items():
        if isinstance(v, str):
            # シングルクォートをエスケープ
            escaped = v.replace("'", "\\'")
            lines.append(f"  {k}: '{escaped}',")
        elif isinstance(v, list):
            lines.append(f"  {k}: {v!r},")
        else:
            lines.append(f"  {k}: {v!r},")
    # 末尾カンマを除去
    lines[-1] = lines[-1].rstrip(',')
    lines.append('});')
    return '\n'.join(lines)

def validate_js(snippet):
    """node --check でJS構文検証"""
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(snippet); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=10)
    os.unlink(tmp.name)
    return r.returncode == 0, r.stderr.decode('utf-8', errors='replace')

def run():
    if not CHARS_TO_ADD:
        print("CHARS_TO_ADD が空です。追加するキャラを定義してください。")
        return

    with open(DASHBOARD, encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 挿入位置: block22の最後の </script> の直前
    # (最後の window.CHAR_TEMPLATES.female.push の後)
    scripts_iter = list(re.finditer(r'(<script(?:\s[^>]*)?>)(.+?)(</script>)',
                                     content, re.DOTALL | re.IGNORECASE))
    sc22 = scripts_iter[22]
    insert_pos = sc22.end(2)  # </script> の直前

    # JS断片を生成
    snippets = []
    for char in CHARS_TO_ADD:
        js = obj_to_js(char)
        ok, err = validate_js(js)
        if not ok:
            print(f"[ERROR] {char.get('id','?')} のJS構文エラー:")
            print(err)
            print("追加を中止しました。")
            return
        snippets.append(js)
        print(f"[OK] {char.get('id','?')} 検証完了")

    # バックアップ
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bak = DASHBOARD.replace('.html', f'_backup_addchar_{ts}.html')
    shutil.copy2(DASHBOARD, bak)
    print(f"Backup: {bak}")

    # 挿入
    insert_text = '\n\n' + '\n\n'.join(snippets) + '\n\n'
    content = content[:insert_pos] + insert_text + content[insert_pos:]

    # バージョン更新
    ver_m = re.search(r'content="(\d{10,})"', content)
    if ver_m:
        old_ver = ver_m.group(1)
        new_ver = str(int(old_ver) + 1)
        content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
        print(f"Version: {old_ver} -> {new_ver}")

    # 全体検証
    print("全ブロック検証中...")
    scripts_check = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
    all_ok = True
    for i, sc in enumerate(scripts_check):
        sc2 = sc.strip()
        if not sc2 or len(sc2) < 20: continue
        ok, err = validate_js(sc2)
        if not ok:
            print(f"[FAIL] block{i}: {err[:200]}")
            all_ok = False

    if not all_ok:
        print("検証失敗。保存しませんでした。バックアップを確認してください。")
        return

    with open(DASHBOARD, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"完了! {len(CHARS_TO_ADD)}キャラ追加 → {DASHBOARD}")
    print("次のステップ: ブラウザで Ctrl+Shift+R")

if __name__ == '__main__':
    run()
