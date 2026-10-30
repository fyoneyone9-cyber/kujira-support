import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# S1の全キャラIDを位置順で確認
target_ids = [
    'char_kakuseizai_jk_A', 'char_kakuseizai_jk_B', 'char_kakuseizai_jk_C',
    'char_kakuseizai_chuugaku_A', 'char_kakuseizai_chuugaku_B', 'char_kakuseizai_chuugaku_C',
    'char_kakuseizai_shougaku_A', 'char_kakuseizai_shougaku_B', 'char_kakuseizai_shougaku_C',
    'char_kakuseizai_youchien_A', 'char_kakuseizai_youchien_B', 'char_kakuseizai_youchien_C',
    'char_kakuseizai_tifa', 'char_kakuseizai_aerith',
]
positions = []
for cid in target_ids:
    idx = content.find(cid + "'")
    positions.append((idx, cid))

positions.sort()
print("S1キャラ位置順:")
for pos, cid in positions:
    print(f"  {pos}: {cid}")
