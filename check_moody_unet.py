import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = pathlib.Path(r"C:\AI\ComfyUI\models\unet")
if p.exists():
    for f in p.iterdir():
        if 'moody' in f.name.lower():
            print(f"FOUND: {f.name}")
    all_files = list(p.iterdir())
    print(f"Total unet files: {len(all_files)}")
else:
    print("unet dir not found")
    # checkpoints も確認
    for cp_dir in [r"C:\AI\ComfyUI\models\checkpoints", r"C:\AI\ComfyUI\models\Stable-diffusion"]:
        p2 = pathlib.Path(cp_dir)
        if p2.exists():
            for f in p2.iterdir():
                if 'moody' in f.name.lower():
                    print(f"CHECKPOINT: {f.name}")
