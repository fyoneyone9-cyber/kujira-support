#!/usr/bin/env python
# -*- coding: utf-8 -*-
# qa_runner.pyのどのステップで出力が消えるか特定する
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print('step1: after TextIOWrapper', flush=True)
import json, time, requests, pathlib, uuid, socket
print('step2: after imports', flush=True)
socket.setdefaulttimeout(10)
print('step3: after setdefaulttimeout', flush=True)

API   = "http://127.0.0.1:3002"
COMFY = "http://127.0.0.1:8188"
print('step4: after constants', flush=True)

# api_up相当
try:
    s = socket.create_connection(("127.0.0.1", 3002), timeout=8)
    s.close()
    print('step5: api_up OK', flush=True)
except Exception as e:
    print(f'step5: api_up FAIL {e}', flush=True)

# comfy_up相当
try:
    s = socket.create_connection(("127.0.0.1", 8188), timeout=8)
    s.close()
    print('step6: comfy_up OK', flush=True)
except Exception as e:
    print(f'step6: comfy_up FAIL {e}', flush=True)

print('ALL DONE', flush=True)
