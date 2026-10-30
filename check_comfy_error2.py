import sys, io, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
COMFY = "http://127.0.0.1:8188"
r = requests.get(f"{COMFY}/history", timeout=5)
hist = r.json()
for pid, entry in list(hist.items())[-3:]:
    for msg_type, msg_data in entry.get("status",{}).get("messages",[]):
        if msg_type == "execution_error":
            print(f"prompt_id={pid[:16]}")
            print(f"  node_id={msg_data.get('node_id')} node_type={msg_data.get('node_type')}")
            print(f"  exception_type={msg_data.get('exception_type')}")
            print(f"  exception_message={msg_data.get('exception_message')}")
            print(f"  traceback tail={msg_data.get('traceback',[''])[-1] if msg_data.get('traceback') else ''}")
            print()
