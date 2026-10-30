import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LORA_DIR = pathlib.Path(r"C:\AI\ComfyUI\models\loras")
targets = [
    "aerith_illu.safetensors",
    "aerith_gainsborough_xl.safetensors",
    "aerith_gainsborough.safetensors",
    "tifa_lockhart_xl.safetensors",
    "Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors",
    "tifa_lockhart.safetensors",
]

print("=== LoRAファイル存在確認 ===")
for t in targets:
    p = LORA_DIR / t
    status = "✅ EXIST" if p.exists() else "❌ MISSING"
    print(f"{status}: {t}")

# 実在するLoRAの全リスト
print("\n=== 全LoRAファイル ===")
for f in sorted(LORA_DIR.iterdir()):
    if f.is_file():
        print(f"  {f.name} ({f.stat().st_size//1024}KB)")
