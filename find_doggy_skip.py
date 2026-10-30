import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'pose=doggy' in l or ('doggy' in l and 'pose_preset' in l) or ('pose_preset' in l and 'doggy' in l.lower()):
        print(f'{i}: {l}', end='')
        for j in range(i, min(len(lines), i+5)):
            print(f'  {j+1}: {lines[j]}', end='')
        print()
        break
