import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 挿入されたティファの前後を確認
tifa_idx = content.rfind("char_kakuseizai_tifa'")
print("Before tifa (200 chars):")
print(repr(content[tifa_idx-200:tifa_idx]))
print()
print("After tifa block start:")
print(repr(content[tifa_idx:tifa_idx+200]))
print()
# ティファの後にエアリスがあるか
aerith_after = content.find("char_kakuseizai_aerith'", tifa_idx)
print(f"Aerith after tifa at: {aerith_after}")
print(repr(content[aerith_after-10:aerith_after+100]))
