import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for wf_name in ["redcraft_solo_api.json", "moody_krea2_v7_api.json"]:
    p = pathlib.Path(r"C:\AI\ComfyUI\workflows") / wf_name
    if not p.exists():
        print(f"NOT FOUND: {wf_name}"); continue
    with open(p, encoding='utf-8-sig', errors='replace') as f:
        wf = json.load(f)
    print(f"\n=== {wf_name} ===")
    for nid, node in wf.items():
        if not isinstance(node, dict): continue
        ct = node.get("class_type", "")
        inp = node.get("inputs", {})
        if ct in ("UNETLoader", "CheckpointLoaderSimple", "CheckpointLoader"):
            print(f"  Node{nid} ({ct}): {inp}")
        if ct == "KSampler":
            print(f"  Node{nid} KSampler: cfg={inp.get('cfg')} steps={inp.get('steps')} sampler={inp.get('sampler_name')} sched={inp.get('scheduler')}")
