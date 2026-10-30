#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/api/test-prompt エンドポイントを api_server_3001.py に追加する
動作: generate-panel と同じリクエストを受け取り、プロンプト生成だけ行い
      ComfyUI投入をスキップして positive_prompt / ksampler / lora情報を返す
実装: _TEST_PROMPT_MODE グローバルフラグを立ててから generate-panel の内部関数を呼び、
      ComfyUI投入ポイント(L28897付近)でフラグを確認してスキップ
"""
import sys, io, pathlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
bak = API.parent / (API.name + '.bak_test_prompt')
shutil.copy2(API, bak)
print(f"Backup: {bak.name}")

with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

# ── Step1: グローバルフラグを _last_gen_meta 定義付近に追加 ──
# 既に追加済みでないか確認
if '_TEST_PROMPT_MODE' in content:
    print("⚠ _TEST_PROMPT_MODE 既に存在 → Step1スキップ")
else:
    OLD_FLAG = '_last_gen_meta = {}'
    NEW_FLAG = ('_last_gen_meta = {}\n'
                '# [TEST_PROMPT_MODE_V1] /api/test-prompt時にComfyUI投入をスキップするフラグ\n'
                '_TEST_PROMPT_MODE = False')
    if OLD_FLAG in content:
        content = content.replace(OLD_FLAG, NEW_FLAG, 1)
        print("✅ Step1: _TEST_PROMPT_MODE フラグ追加")
    else:
        print("❌ Step1: _last_gen_meta = {} が見つからない")
        sys.exit(1)

# ── Step2: ComfyUI投入ポイントにフラグチェックを挿入 ──
# _post() 定義の直前でフラグチェック → Trueなら投入スキップ
if 'TEST_PROMPT_SKIP' in content:
    print("⚠ TEST_PROMPT_SKIP 既に存在 → Step2スキップ")
else:
    OLD_POST = (
        '            def _post():\n'
        '                try:\n'
        '                    r = _req4.post("http://127.0.0.1:8188/prompt"'
    )
    NEW_POST = (
        '            # [TEST_PROMPT_MODE_V1] dry-run時はComfyUI投入をスキップ\n'
        '            if _TEST_PROMPT_MODE:\n'
        '                print("[TEST_PROMPT_SKIP] ComfyUI投入スキップ", flush=True)\n'
        '                return JSONResponse({"ok": True, "dry_run": True,\n'
        '                    "positive_prompt": wf.get("6",{}).get("inputs",{}).get("text",""),\n'
        '                    "ksampler": {k: wf.get("7",{}).get("inputs",{}).get(k)\n'
        '                                for k in ["cfg","steps","sampler_name","scheduler"]},\n'
        '                    "loras": []})\n'
        '            def _post():\n'
        '                try:\n'
        '                    r = _req4.post("http://127.0.0.1:8188/prompt"'
    )
    if OLD_POST in content:
        content = content.replace(OLD_POST, NEW_POST, 1)
        print("✅ Step2: TEST_PROMPT_SKIP 挿入")
    else:
        print("❌ Step2: _post()定義が見つからない")
        sys.exit(1)

# ── Step3: /api/test-prompt エンドポイントを /api/last-prompt の直前に追加 ──
if '/api/test-prompt' in content:
    print("⚠ /api/test-prompt 既に存在 → Step3スキップ")
else:
    OLD_ENDPOINT = '@app.get("/api/last-prompt")'
    NEW_ENDPOINT = '''@app.post("/api/test-prompt")
async def test_prompt_endpoint(req: SinglePanelRequest, request: Request):
    """
    [TEST_PROMPT_MODE_V1] dry-run用: プロンプト生成のみ・ComfyUI未投入
    qa_runner.py --dry-run から使用。generate-panelと同じリクエストを受けて
    positive_prompt / ksampler / lora情報を返す
    """
    global _TEST_PROMPT_MODE
    _cid = request.headers.get("X-Client-Id","qa_dry") or "qa_dry"
    if not _gen_lock_acquire(_cid, "test-prompt"):
        return JSONResponse({"ok": False, "error": "busy"}, status_code=409)
    try:
        _TEST_PROMPT_MODE = True
        resp = await _generate_single_panel_locked(req)
        return resp
    finally:
        _TEST_PROMPT_MODE = False
        _gen_lock_release(_cid)


@app.get("/api/last-prompt")'''
    if OLD_ENDPOINT in content:
        content = content.replace(OLD_ENDPOINT, NEW_ENDPOINT, 1)
        print("✅ Step3: /api/test-prompt エンドポイント追加")
    else:
        print("❌ Step3: @app.get('/api/last-prompt') が見つからない")
        sys.exit(1)

with open(API, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 書き込み完了")
