import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S3 jk_A のブロックを確認（outfits構造把握）
idx = content.find("char_kakuseizai_s3_jk_A")
next_id = content.find("{id:'char_", idx+10)
block = content[idx:next_id]
print("=== S3 jk_A ブロック（先頭600文字）===")
print(block[:600])
print()

# S2 aerith も確認
idx2 = content.find("char_kakuseizai_s2_aerith")
next_id2 = content.find("{id:'char_", idx2+10)
block2 = content[idx2:next_id2]
print("=== S2 aerith（先頭300文字）===")
print(block2[:300])
