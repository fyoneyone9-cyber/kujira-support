import sys, io, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
r = requests.get("http://127.0.0.1:3002/api/last-prompt", timeout=5)
data = r.json()
# LoRA関連フィールドを全部表示
for k, v in data.items():
    if 'lora' in k.lower() or 'lora' in str(v).lower()[:50]:
        print(f"{k}: {str(v)[:300]}")
# WFのLoRAノードを確認
import pathlib, json
wf_file = pathlib.Path(r"C:\AI\ComfyUI\debug_last_real_wf.json")
if wf_file.exists():
    with open(wf_file, encoding='utf-8') as f:
        wf = json.load(f)
    print("\n=== WFのLoRAノード ===")
    for nid, node in wf.items():
        if not isinstance(node, dict): continue
        ct = node.get("class_type", "")
        if "lora" in ct.lower() or "Lora" in ct:
            inp = node.get("inputs", {})
            lname = inp.get("lora_name", "?")
            str_m = inp.get("strength_model", "?")
            print(f"  Node {nid} ({ct}): {lname!r} @ {str_m}")
