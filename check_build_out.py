import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\build_out.txt', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
errors = [l for l in lines if any(k in l for k in ['error','Error','failed','×','Type error'])]
print(''.join(errors[-30:]))
print('--- last 10 lines ---')
print(''.join(lines[-10:]))
