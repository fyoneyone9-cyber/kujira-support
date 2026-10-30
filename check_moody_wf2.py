import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

wf_files = list(pathlib.Path(r"C:\AI\ComfyUI\workflows").glob("*moody*krea2*"))
print(f"WF files found: {[f.name for f in wf_files]}")
for wf_path in wf_files:
    with open(wf_path, encoding='utf-8-sig', errors='replace') as f:
        wf = json.load(f)
    print(f"\n=== {wf_path.name} ===")
    for nid, node in wf.items():
        if not isinstance(node, dict): continue
        ct = node.get("class_type", "")
        if ct == "UNETLoader":
            unet = node.get("inputs", {}).get("unet_name", "?")
            print(f"  Node {nid} UNETLoader: unet_name={unet!r}")
