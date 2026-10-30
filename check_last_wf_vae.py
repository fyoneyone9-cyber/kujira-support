import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
wf_file = pathlib.Path(r"C:\AI\ComfyUI\debug_last_real_wf.json")
with open(wf_file, encoding='utf-8') as f:
    wf = json.load(f)
print("=== debug_last_real_wf.json VAE/Decode関連ノード ===")
for nid, node in wf.items():
    if not isinstance(node, dict): continue
    ct = node.get("class_type","")
    if any(k in ct for k in ("VAE","Decode","Loader")):
        print(f"Node{nid} ({ct}): {node.get('inputs',{})}")
