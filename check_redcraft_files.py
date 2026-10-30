import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = pathlib.Path(r"C:\AI\ComfyUI\models\unet")
for f in sorted(p.iterdir()):
    if 'redcraft' in f.name.lower():
        print(f"UNET: {f.name}")
p2 = pathlib.Path(r"C:\AI\ComfyUI\models\checkpoints")
for f in sorted(p2.iterdir()):
    if 'redcraft' in f.name.lower():
        print(f"CKPT: {f.name}")
