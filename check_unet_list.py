import sys, io, requests, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

COMFY = "http://127.0.0.1:8188"

# ComfyUIのオブジェクト情報からUNETLoaderの入力スキーマを取得
try:
    r = requests.get(f"{COMFY}/object_info/UNETLoader", timeout=5)
    info = r.json()
    inputs = info.get("UNETLoader", {}).get("input", {}).get("required", {})
    unet_list = inputs.get("unet_name", [None])[0]
    if isinstance(unet_list, list):
        print(f"UNETLoader unet_name options ({len(unet_list)}):")
        for name in unet_list:
            print(f"  {name}")
    else:
        print(f"unet_name type: {type(unet_list)}")
        print(json.dumps(inputs, ensure_ascii=False)[:500])
except Exception as e:
    print(f"Error: {e}")
