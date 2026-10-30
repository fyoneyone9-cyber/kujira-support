import sys
sys.stdout.reconfigure(encoding='utf-8')

for path in [r'C:\AI\ComfyUI\dashboard.html', r'C:\AI\ComfyUI\outfit_sets.json']:
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            content = f.read()
        idx = content.lower().find('biglust')
        if idx != -1:
            print(f"=== {path} idx={idx} ===")
            print(content[max(0,idx-100):idx+200])
    except Exception as e:
        print(f"{path}: {e}")
