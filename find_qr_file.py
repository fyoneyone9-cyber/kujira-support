import os
for root, dirs, files in os.walk(r'C:\AI\ComfyUI'):
    for f in files:
        if f == 'quality_rules.py':
            print(os.path.join(root, f))
