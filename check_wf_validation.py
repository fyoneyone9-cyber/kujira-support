import sys, io, json, pathlib, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# last-promptからWFを取得してComfyUIに検証リクエスト
API = "http://127.0.0.1:3002"
COMFY = "http://127.0.0.1:8188"

# debug_last_real_wf.jsonを確認
wf_file = pathlib.Path(r"C:\AI\ComfyUI\debug_last_real_wf.json")
if not wf_file.exists():
    print("debug_last_real_wf.json not found")
    # 他のデバッグWFを探す
    for f in pathlib.Path(r"C:\AI\ComfyUI").glob("debug_last*.json"):
        print(f"Found: {f.name} ({f.stat().st_size} bytes)")
    sys.exit(1)

with open(wf_file, encoding='utf-8') as f:
    wf = json.load(f)

print(f"WF nodes: {list(wf.keys())}")

# 各ノードのclass_typeとkey inputsを確認
for nid, node in wf.items():
    if not isinstance(node, dict): continue
    ct = node.get("class_type", "?")
    inputs = node.get("inputs", {})
    # LoRALoader系を探す
    if "Lora" in ct or "lora" in ct.lower():
        lora_name = inputs.get("lora_name", "?")
        print(f"  Node {nid} ({ct}): lora_name={lora_name!r}")
    # CLIPLoader
    if "CLIP" in ct:
        print(f"  Node {nid} ({ct}): {dict(list(inputs.items())[:3])}")

# ComfyUIに直接投げてエラー詳細を取得
print("\n=== ComfyUI validation ===")
try:
    payload = {"prompt": wf, "client_id": "debug_test"}
    r = requests.post(f"{COMFY}/prompt", json=payload, timeout=10)
    print(f"Status: {r.status_code}")
    resp = r.json()
    if "error" in resp:
        print(f"Error: {resp['error']}")
    if "node_errors" in resp:
        for nid, err in resp["node_errors"].items():
            print(f"Node {nid}: {err}")
    if r.status_code == 200:
        print("WF accepted by ComfyUI ✅")
except Exception as e:
    print(f"Request error: {e}")
