import sys, io, os, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

lora_dirs = [
    r"C:\AI\ComfyUI\models\loras",
    r"C:\AI\ComfyUI\models\lora",
]

print("=== Aerith LoRA 検索 ===")
for d in lora_dirs:
    p = pathlib.Path(d)
    if not p.exists():
        print(f"DIR NOT FOUND: {d}")
        continue
    matches = list(p.rglob("*aerith*")) + list(p.rglob("*Aerith*"))
    if matches:
        for m in matches:
            print(f"FOUND: {m}")
    else:
        print(f"NOT FOUND in {d}")
        # 全LoRA一覧（先頭30件）
        all_loras = list(p.rglob("*.safetensors"))[:30]
        print(f"  Sample files ({len(all_loras)}):")
        for f in all_loras[:10]:
            print(f"    {f.name}")
