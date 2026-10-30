import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = pathlib.Path(r"C:\AI\ComfyUI\workflows\redcraft_solo_api.json")
with open(p, encoding='utf-8-sig', errors='replace') as f:
    wf = json.load(f)
for nid, node in wf.items():
    if not isinstance(node, dict): continue
    ct = node.get("class_type", "")
    if "sampler" in ct.lower() or "ksampler" in ct.lower():
        print(f"Node{nid} class_type={ct!r}: {dict(list(node.get('inputs',{}).items())[:5])}")
