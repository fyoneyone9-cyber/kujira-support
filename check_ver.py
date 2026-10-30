import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
ver = re.search(r'content="(\d{10,})"', content)
print('Version:', ver.group(1) if ver else 'not found')
print('peach in file:', 'char_kakuseizai_peach' in content)
print('mitsuri in file:', 'char_kakuseizai_mitsuri' in content)
print('tifa S1 in file:', 'char_kakuseizai_tifa' in content)
print('aerith S1 in file:', 'char_kakuseizai_aerith' in content)
