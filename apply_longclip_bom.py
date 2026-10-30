"""BOMありファイルへのLongCLIP適用"""
import json, os, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WF_DIR = r'C:\AI\ComfyUI\workflows'
LONGCLIP = 'longclip-L.pt'
KREA2_KEYS = ['krea2', 'qwen', 'wan', 'gguf', 'redcraft', 'moody', 'darkbeast', 'redgpt']

targets = ['moody_krea2_v7_api.json', 'pornmaster_klein_api.json', 'sdxlswreal_api.json']

for fname in targets:
    path = os.path.join(WF_DIR, fname)
    try:
        with open(path, encoding='utf-8-sig') as f:
            wf = json.load(f)
    except Exception as e:
        print(f'FAIL: {fname}: {e}'); continue

    ckpt = ''
    ckpt_node_id = None
    for nid, node in wf.items():
        if isinstance(node, dict) and node.get('class_type') == 'CheckpointLoaderSimple':
            ckpt = node.get('inputs', {}).get('ckpt_name', '').lower()
            ckpt_node_id = nid
            break

    if not ckpt_node_id:
        print(f'SKIP: {fname}: no ckpt'); continue
    if any(k in ckpt for k in KREA2_KEYS):
        print(f'SKIP: {fname}: krea2系 ({ckpt[:40]})'); continue

    has_clip_loader = any(
        isinstance(n, dict) and n.get('class_type') in ('CLIPLoader', 'DualCLIPLoader', 'LongCLIPLoader')
        for n in wf.values()
    )
    if has_clip_loader:
        print(f'SKIP: {fname}: already has CLIPLoader'); continue

    clip_consumers = [
        (nid, node) for nid, node in wf.items()
        if isinstance(node, dict) and node.get('class_type') in ('CLIPTextEncode', 'CLIPTextEncodeSDXL')
        and isinstance(node.get('inputs', {}).get('clip'), list)
        and node['inputs']['clip'][0] == ckpt_node_id
    ]
    if not clip_consumers:
        print(f'SKIP: {fname}: no CLIPTextEncode linked to ckpt'); continue

    shutil.copy2(path, path + '.bak_longclip')
    new_id = str(max(int(k) for k in wf.keys() if k.isdigit()) + 1)
    wf[new_id] = {"class_type": "CLIPLoader", "inputs": {"clip_name": LONGCLIP, "type": "stable_diffusion"}}
    for nid, node in clip_consumers:
        node['inputs']['clip'] = [new_id, 0]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)
    print(f'OK: {fname} ckpt={ckpt[:40]} {len(clip_consumers)}件更新')
