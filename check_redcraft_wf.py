import sys, io, json, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

wf_dir = r'C:\AI\ComfyUI'
# redcraft_solo_api.json を探す
for root, dirs, files in os.walk(wf_dir):
    for f in files:
        if 'redcraft_solo' in f.lower() and f.endswith('.json'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            print(f'=== {path} ===')
            # width/height を全ノードから探す
            for node_id, node in data.items():
                inp = node.get('inputs', {})
                w = inp.get('width')
                h = inp.get('height')
                if w or h:
                    print(f'  node {node_id} ({node.get("class_type","")}): {w}x{h}')
            print()
