import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# L8607付近のKSAMPLERブロックがどのifブロック内にあるか調べる
# L8600-8620のインデントを確認
for i in range(8595, 8625):
    l = lines[i]
    stripped = l.lstrip()
    indent = len(l) - len(stripped)
    print(f"L{i+1} [indent={indent}]: {l.rstrip()[:120]}")
