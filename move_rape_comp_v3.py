"""
RAPE_COMP_V3_FINALブロックを PROMPT_ORDER_V1 の直前に移動する。
- wf['6']への注入タグを PROMPT_ORDER が compo バケットに分類→77tok内前方配置
- 末尾/先頭追加ロジック不要になるので追加先をシンプルに末尾のまま維持
"""
import sys, io, subprocess, tempfile, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# ── ブロック境界検出 ──
v3_start = v3_end = po_line = None
for i, l in enumerate(lines):
    if '# [RAPE_COMP_V3_FINAL 2026-10-21]' in l and v3_start is None:
        v3_start = i
    if v3_start and i > v3_start and '_payload_r = {"prompt": wf' in l and v3_end is None:
        v3_end = i  # _payload_r行は移動しない (境界マーカーとして使う)
    if '# ===== PROMPT_ORDER_V1' in l and po_line is None:
        po_line = i

assert v3_start and v3_end and po_line, f"検出失敗: v3={v3_start},{v3_end} po={po_line}"
assert po_line < v3_start, "PROMPT_ORDERが既にV3より後ろ"

print(f"V3ブロック: L{v3_start+1}~L{v3_end} ({v3_end - v3_start}行)")
print(f"PROMPT_ORDER: L{po_line+1}")

# V3ブロック = v3_start 〜 v3_end-1 (v3_end行 = _payload_r は残す)
v3_block = lines[v3_start:v3_end]

# V3ブロックを元の位置から削除
new_lines = lines[:v3_start] + lines[v3_end:]

# PROMPT_ORDER_V1の位置を再計算 (V3削除でずれた)
shift = v3_end - v3_start
new_po = po_line  # po_line < v3_start なのでずれない

# PROMPT_ORDER_V1行の直前にV3ブロックを挿入
new_lines = new_lines[:new_po] + v3_block + new_lines[new_po:]

print(f"挿入先: L{new_po+1} (PROMPT_ORDER直前)")

# 構文チェック
tmp = tempfile.mktemp(suffix='.py')
with open(tmp, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
result = subprocess.run(
    [r'C:\Users\fyone\anaconda3\python.exe', '-m', 'py_compile', tmp],
    capture_output=True, text=True
)
os.remove(tmp)
if result.returncode != 0:
    print('SYNTAX ERROR:', result.stderr[:300])
    sys.exit(1)
print('構文OK')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('書き込み完了')
