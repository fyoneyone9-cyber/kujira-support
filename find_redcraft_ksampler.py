import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# KSAMPLER block の redcraft 判定部分を探す
print("=== KSAMPLER redcraft 判定 ===")
for i, l in enumerate(lines):
    if 'KREA2_KSAMPLER' in l or ('redcraft' in l.lower() and ('cfg' in l.lower() or 'steps' in l.lower())):
        print(f"L{i+1}: {l.rstrip()[:160]}")

print("\n=== cfg_steps_trace への書き込み ===")
for i, l in enumerate(lines):
    if 'cfg_steps_trace' in l and ('append' in l or 'redcraft' in l.lower()):
        print(f"L{i+1}: {l.rstrip()[:160]}")
