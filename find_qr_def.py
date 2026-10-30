import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules\quality_rules.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# apply_quality_rules 関数定義と weight_budget 処理を探す
for i, l in enumerate(lines):
    if 'def apply_quality_rules' in l or 'weight_budget' in l or 'priority_tags' in l or 'keep' in l.lower() and 'budget' in lines[max(0,i-3):i+1]:
        print(f'L{i+1}: {l.rstrip()}')
