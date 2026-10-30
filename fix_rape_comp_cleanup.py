"""
RAPE_COMP V2/V2_R を削除し V3_FINAL だけ残す。
また汎用構図（非レイプ）も V3_FINAL 直前に移動する。
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# --- 1) RAPE_COMP_V2 ブロック(L8885付近)を元の汎用のみに戻す ---
# if not _rc3_skip and not _rc3_has_angle and _rc3_is_rape: ... (大きいif)
# この部分を削除して、元の elif not _rc3_skip and not _rc3_has_angle: ブロックだけ残す

# V2ブロックの開始マーカー
V2_START = '                if not _rc3_skip and not _rc3_has_angle and _rc3_is_rape:'
V2_END_MARKER = '                elif not _rc3_skip and not _rc3_has_angle:'

idx_v2 = content.find(V2_START)
idx_elif = content.find(V2_END_MARKER)

if idx_v2 != -1 and idx_elif != -1 and idx_elif > idx_v2:
    # V2_STARTからV2_END_MARKERの直前まで削除
    # V2_END_MARKERを if not _rc3_skip and not _rc3_has_angle: に変更
    removed_block = content[idx_v2:idx_elif]
    new_elif = '                if not _rc3_skip and not _rc3_has_angle:'
    content = content[:idx_v2] + new_elif + '\n' + content[idx_elif + len(V2_END_MARKER):]
    print(f'V2ブロック削除OK: {len(removed_block)}文字')
else:
    print(f'ERROR: V2ブロック検索失敗 v2={idx_v2} elif={idx_elif}')

# --- 2) _rc3_is_rape 定義行を削除 ---
# これはもう参照されないので
RAPE_DEF_BLOCK = '''
                # [RAPE_COMP_V1 2026-10-21] レイプ/強制系専用構図プール
                # 性行為シーンはrc3_skipで既に除外済み → ここは非性行為強制シーン専用
                # 追跡・拘束・脱衣・事後など全フェーズに対応した構図を用意
                _rc3_is_rape = any(k in _rc3_lo for k in ['''
idx_rape_def = content.find('                _rc3_is_rape = any(k in _rc3_lo for k in [')
if idx_rape_def != -1:
    # この行から ): _rc3_phase = 'drag' まで（大きいブロック）は既に削除済みのはず
    # _rc3_is_rape 定義だけ残っているなら削除
    end_idx = content.find('\n', content.find('])', idx_rape_def)) + 1
    print(f'_rc3_is_rape定義位置: {idx_rape_def}')
else:
    print('_rc3_is_rape定義: 既に削除済み or 見つからず')

# --- 3) RAPE_COMP_V2_RELOCATED ブロックを削除 ---
V2R_START = '\n        # [RAPE_COMP_V2_RELOCATED 2026-10-21]'
V2R_END = '\n        except Exception as _rc2_e:\n            print(f\'[RAPE_COMP_V2_R] err: {_rc2_e}\', flush=True)\n'
idx_v2r = content.find(V2R_START)
idx_v2r_end = content.find(V2R_END, idx_v2r) if idx_v2r != -1 else -1
if idx_v2r != -1 and idx_v2r_end != -1:
    removed = content[idx_v2r : idx_v2r_end + len(V2R_END)]
    content = content[:idx_v2r] + '\n' + content[idx_v2r_end + len(V2R_END):]
    print(f'V2_R削除OK: {len(removed)}文字')
else:
    print(f'V2_R削除: 見つからず v2r={idx_v2r} end={idx_v2r_end}')

# 構文チェック
import tempfile, os, subprocess
tmp = tempfile.mktemp(suffix='.py')
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
result = subprocess.run([r'C:\Users\fyone\anaconda3\python.exe', '-m', 'py_compile', tmp], capture_output=True, text=True)
os.remove(tmp)
if result.returncode != 0:
    print('SYNTAX ERROR:', result.stderr[:200])
    sys.exit(1)
print('構文OK')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('書き込み完了')
