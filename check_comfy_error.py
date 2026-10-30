import sys, io, requests, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

COMFY = "http://127.0.0.1:8188"

# 直近のhistoryからエラーを確認
try:
    r = requests.get(f"{COMFY}/history", timeout=5)
    hist = r.json()
    print(f"history entries: {len(hist)}")
    for pid, entry in list(hist.items())[-3:]:
        status = entry.get("status", {})
        msgs = status.get("messages", [])
        print(f"\nprompt_id={pid[:16]}")
        print(f"  completed={status.get('completed')} status_str={status.get('status_str')}")
        for msg_type, msg_data in msgs[-5:]:
            print(f"  msg: {msg_type} = {str(msg_data)[:120]}")
        outputs = entry.get("outputs", {})
        for nid, out in outputs.items():
            if "images" in out:
                print(f"  output node{nid}: {len(out['images'])} images")
except Exception as e:
    print(f"history error: {e}")

# queue状態
try:
    r2 = requests.get(f"{COMFY}/queue", timeout=5)
    q = r2.json()
    print(f"\nqueue: running={len(q.get('queue_running',[]))} pending={len(q.get('queue_pending',[]))}")
except Exception as e:
    print(f"queue error: {e}")
