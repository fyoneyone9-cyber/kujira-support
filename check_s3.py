import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
print("s3_ff_tifa:", 'char_kakuseizai_s3_ff_tifa' in content)
print("s3_ff_aerith:", 'char_kakuseizai_s3_ff_aerith' in content)
print("s3_youchien:", 'char_kakuseizai_s3_youchien' in content)
print("s3_jk_C:", 'char_kakuseizai_s3_jk_C' in content)
print("s3_peach:", 'char_kakuseizai_s3_peach' in content)
print("s3_mitsuri:", 'char_kakuseizai_s3_mitsuri' in content)
# S3の末尾を探す
last_s3 = None
for m in re.finditer(r'char_kakuseizai_s3_[a-z_]+', content):
    last_s3 = m.group()
print("Last S3 char:", last_s3)
