import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = pathlib.Path(r"C:\AI\ComfyUI\workflows\redcraft_solo_api.json")
with open(p, encoding='utf-8-sig') as f:
    wf = json.load(f)
print(f"=== redcraft_solo_api.json nodes ===")
for nid, node in wf.items():
    if not isinstance(node, dict): continue
    ct = node.get("class_type","")
    if any(k in ct for k in ("VAE","Decode","Encode","Loader")):
        print(f"Node{nid} ({ct}): {node.get('inputs',{})}")

# VAEディレクトリ確認
vae_dir = pathlib.Path(r"C:\AI\ComfyUI\models\vae")
print(f"\n=== VAEファイル ===")
for f in sorted(vae_dir.iterdir()):
    if f.is_file():
        print(f"  {f.name}")
