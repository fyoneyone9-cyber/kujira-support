#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix: redcraft v40のVAEをqwen_image_vae.safetensors(16ch Krea2用)に修正
原因: L9227で "v40=sdxl_vae_fp16fix"(4ch)を設定していたが、
     40K2TDUALはKrea2アーキテクチャ(16ch latent)のためSDXL VAE(4ch)は不一致
     → RuntimeError: expected input to have 4 channels, but got 16 channels

コード品質メモ(次回の間違い防止):
  - REDCRAFT_V40_VAE コメントに "Krea2=16ch latent → qwen_image_vae必須" を明記
  - v30/v40判定はKrea2 vs SDXL判定とは独立。アーキテクチャを明示すること
"""
import sys, io, pathlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
bak = API.parent / (API.name + ".bak_redcraft_v40_vae")
shutil.copy2(API, bak)
print(f"Backup: {bak.name}")

with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

# v40=sdxl_vae_fp16fix → v40=qwen_image_vae に修正
# コメントも Krea2 16ch latent の旨を明記する
OLD = '''                elif _rc_is_v40_vae:
                    # v40: 内蔵VAE推奨だが外部ならsdxl fp16fix
                    _vae_target = __import__("os").environ.get("REDCRAFT_V40_VAE", "sdxl_vae_fp16fix.safetensors")'''

NEW = '''                elif _rc_is_v40_vae:
                    # v40(40K2TDUAL等): Krea2アーキテクチャ(16ch latent) → qwen_image_vae必須
                    # Fix: sdxl_vae_fp16fix(4ch)を設定していたが16ch不一致でVAEDecodeがクラッシュ
                    # [REDCRAFT_V40_VAE_FIX 2026-10-22] 4ch SDXL VAE → 16ch Krea2 VAE
                    _vae_target = __import__("os").environ.get("REDCRAFT_V40_VAE", "qwen_image_vae.safetensors")'''

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    with open(API, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ fix applied")
else:
    print("❌ target not found")
