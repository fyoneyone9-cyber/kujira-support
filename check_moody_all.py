import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

search_dirs = [
    r"C:\AI\ComfyUI\models\unet",
    r"C:\AI\ComfyUI\models\checkpoints",
    r"C:\AI\ComfyUI\models\Stable-diffusion",
    r"C:\AI\ComfyUI\models",
]

for d in search_dirs:
    p = pathlib.Path(d)
    if not p.exists():
        continue
    # 直下ファイルのmoody確認
    for f in p.iterdir():
        if f.is_file() and 'moody' in f.name.lower():
            print(f"FOUND: {f}")
    # サブディレクトリも
    for f in p.rglob("*moody*"):
        print(f"RGLOB: {f}")
print("Search complete")
