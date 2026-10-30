import sys, io, pathlib, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

# ルート定義(@app.post/get("/api/test-prompt"))が既にあるか確認
has_route = bool(re.search(r'@app\.(post|get)\("/api/test-prompt"\)', content))
print(f"route exists: {has_route}")
if has_route:
    print("既に存在するため終了")
    sys.exit(0)

OLD = '@app.get("/api/last-prompt")'
NEW = (
    '@app.post("/api/test-prompt")\n'
    'async def test_prompt_endpoint(req: SinglePanelRequest, request: Request):\n'
    '    """[TEST_PROMPT_MODE_V1] dry-run: プロンプト生成のみ・ComfyUI未投入"""\n'
    '    global _TEST_PROMPT_MODE\n'
    '    _cid = request.headers.get("X-Client-Id","qa_dry") or "qa_dry"\n'
    '    if not _gen_lock_acquire(_cid, "test-prompt"):\n'
    '        return JSONResponse({"ok": False, "error": "busy"}, status_code=409)\n'
    '    try:\n'
    '        _TEST_PROMPT_MODE = True\n'
    '        return await _generate_single_panel_locked(req)\n'
    '    finally:\n'
    '        _TEST_PROMPT_MODE = False\n'
    '        _gen_lock_release(_cid)\n'
    '\n'
    '\n'
    '@app.get("/api/last-prompt")'
)

if OLD not in content:
    print("❌ @app.get('/api/last-prompt') が見つからない")
    sys.exit(1)

content = content.replace(OLD, NEW, 1)
with open(API, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ /api/test-prompt エンドポイント追加完了")
