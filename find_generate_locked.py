import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if '_generate_single_panel_locked' in l and 'async def' in l:
        print(f"L{i+1}: {l.rstrip()[:120]}")
    # ComfyUIへの実投入（queue_prompt/httpx/requests.post to 8188）のキー行も探す
    if '8188' in l and ('post' in l.lower() or 'queue' in l.lower()):
        print(f"L{i+1}: {l.rstrip()[:120]}")
