import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

OLD = '🔄 Hard Reload</button>'
NEW_BTNS = (
    '<button onclick="if(!confirm(\'APIサーバーをシャットダウンしますか？\'))return;'
    'fetch(\'/api/shutdown\',{method:\'POST\'}).then(()=>alert(\'シャットダウンしました\')).catch(e=>alert(\'エラー: \'+e))" '
    'title="APIサーバーをシャットダウン（ComfyUIは継続）" '
    'style="padding:4px 10px;font-size:11px;border-radius:6px;cursor:pointer;white-space:nowrap;font-weight:bold;'
    'border:1px solid #991b1b;background:#1c0505;color:#f87171">⏹ シャットダウン</button> '
    '<button onclick="if(!confirm(\'APIサーバーを再起動しますか？\'))return;'
    'fetch(\'/api/restart?force=1\',{method:\'POST\'}).then(r=>r.json()).then(d=>alert(\'再起動しました\')).catch(e=>alert(\'エラー: \'+e))" '
    'title="APIサーバーを強制再起動" '
    'style="padding:4px 10px;font-size:11px;border-radius:6px;cursor:pointer;white-space:nowrap;font-weight:bold;'
    'border:1px solid #92400e;background:#1c1000;color:#fbbf24">🔁 再起動</button> '
    '🔄 Hard Reload</button>'
)

if OLD not in content:
    print('ERROR: target string not found')
    sys.exit(1)

count = content.count(OLD)
print(f'Found {count} occurrence(s)')
content = content.replace(OLD, NEW_BTNS, 1)

# バージョン更新
import re as _re
m = _re.search(r'content="(\d{10})"', content)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'version: {old_ver} -> {new_ver}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
