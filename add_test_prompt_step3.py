import sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

OLD = '@app.get("/api/last-prompt")'
NEW = '''@app.post("/api/test-prompt")
async def test_prompt_endpoint(req: SinglePanelRequest, request: Request):
    """
    [TEST_PROMPT_MODE_V1] dry-run用: プロンプト生成のみ・ComfyUI未投入
    qa_runner.py --dry-run から使用。
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

if OLD not in content:
    print("❌ '@app.get(\"/api/last-prompt\")' が見つからない")
    sys.exit(1)
if '/api/test-prompt' in content:
    print("⚠ /api/test-prompt 既に存在する箇所を確認:")
    for i,l in enumerate(content.split('\n')):
        if 'test-prompt' in l:
            print(f"  L{i+1}: {l[:100]}")
    sys.exit(0)

content = content.replace(OLD, NEW, 1)
with open(API, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ /api/test-prompt 追加完了")
