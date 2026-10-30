"""
SDXL系WFファイルのCLIPLoaderをlongclip-L.ptに差し替える。
対象: CheckpointLoaderSimple を持つWFのうち、SDXL系（krea2/qwen/wan以外）
"""
import json, os, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WF_DIR = r'C:\AI\ComfyUI\workflows'
LONGCLIP = 'longclip-L.pt'

# SDXL系チェックポイントを使うWFかどうかの判定キーワード（除外=krea2/qwen/wan/gguf）
KREA2_KEYS = ['krea2', 'qwen', 'wan', 'gguf', 'redcraft', 'moody', 'darkbeast', 'redgpt', 'krea2edit']

changed = []
skipped = []

wf_files = [f for f in os.listdir(WF_DIR) if f.endswith('_api.json')]

for fname in sorted(wf_files):
    path = os.path.join(WF_DIR, fname)
    try:
        with open(path, encoding='utf-8') as f:
            wf = json.load(f)
    except Exception as e:
        print(f'SKIP(parse): {fname}: {e}')
        continue

    # CheckpointLoaderSimpleのckpt名を確認
    ckpt = ''
    for node in wf.values():
        if isinstance(node, dict) and node.get('class_type') == 'CheckpointLoaderSimple':
            ckpt = node.get('inputs', {}).get('ckpt_name', '').lower()
            break

    if not ckpt:
        skipped.append((fname, 'no ckpt'))
        continue

    # krea2系は対象外
    if any(k in ckpt for k in KREA2_KEYS):
        skipped.append((fname, f'krea2系: {ckpt[:40]}'))
        continue

    # CLIPSetLastLayer or DualCLIPLoader を探してLongCLIP化
    # 方針: CLIPTextEncodeに繋がるCLIPを提供するノードにLongCLIPLoaderを挿入
    # 最もシンプルな方法: CheckpointLoaderSimpleの直後にCLIPSetLastLayer(-1)があれば
    # それをLongCLIPLoaderに差し替え。なければ挿入。

    # まずDualCLIPLoader/CLIPLoaderが既にあるか確認
    has_clip_loader = any(
        isinstance(n, dict) and n.get('class_type') in ('CLIPLoader', 'DualCLIPLoader', 'LongCLIPLoader')
        for n in wf.values()
    )
    if has_clip_loader:
        skipped.append((fname, 'already has CLIPLoader'))
        continue

    # CheckpointLoaderSimpleノードIDを取得
    ckpt_node_id = None
    for nid, node in wf.items():
        if isinstance(node, dict) and node.get('class_type') == 'CheckpointLoaderSimple':
            ckpt_node_id = nid
            break

    if not ckpt_node_id:
        skipped.append((fname, 'ckpt node not found'))
        continue

    # CLIPTextEncodeノードを探してclip入力を確認
    clip_consumers = []
    for nid, node in wf.items():
        if isinstance(node, dict) and node.get('class_type') in ('CLIPTextEncode', 'CLIPTextEncodeSDXL'):
            clip_in = node.get('inputs', {}).get('clip')
            if isinstance(clip_in, list) and clip_in[0] == ckpt_node_id:
                clip_consumers.append((nid, node))

    if not clip_consumers:
        skipped.append((fname, 'no CLIPTextEncode linked to ckpt'))
        continue

    # バックアップ
    shutil.copy2(path, path + '.bak_longclip')

    # LongCLIPLoaderノードを追加
    new_id = str(max(int(k) for k in wf.keys() if k.isdigit()) + 1)
    wf[new_id] = {
        "class_type": "CLIPLoader",
        "inputs": {
            "clip_name": LONGCLIP,
            "type": "stable_diffusion"
        }
    }

    # CLIPTextEncodeのclip入力をLongCLIPLoaderに切り替え
    count = 0
    for nid, node in clip_consumers:
        node['inputs']['clip'] = [new_id, 0]
        count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)

    changed.append(f'{fname} (ckpt={ckpt[:40]}, {count} CLIPTextEncode updated)')
    print(f'OK: {fname}')

print(f'\n=== 変更済み {len(changed)}件 ===')
for c in changed: print(' ', c)
print(f'\n=== スキップ {len(skipped)}件 ===')
for s, r in skipped: print(f'  {s}: {r}')
