"""
/api/test-prompt を軽量エンドポイントに差し替え
generate-panelを呼ぶ重い実装→last_gen_metaを返すだけの軽量版に変更
dry-runの正確なプロンプト確認はqa_runner側でgenerate-panel→キャンセルの順で行う
"""
import sys, io, pathlib, re, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
shutil.copy2(API, API.parent / (API.name + '.bak_test_prompt2'))

with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 既存の重いtest-promptエンドポイントを軽量版に差し替え
OLD = (
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
)
NEW = (
    '@app.post("/api/test-prompt")\n'
    'async def test_prompt_endpoint(req: SinglePanelRequest, request: Request):\n'
    '    """\n'
    '    [TEST_PROMPT_MODE_V2] dry-run用軽量エンドポイント\n'
    '    generate-panelを呼ばず _last_gen_meta をそのまま返す\n'
    '    qa_runner --dry-run は generate-panel(実生成) → このエンドポイントで確認の順に変更\n'
    '    注意: generate-panelで生成が走った後のlast_gen_metaを返すため\n'
    '          qa_runnerはgenerate-panel完了後にこのエンドポイントを呼ぶこと\n'
    '    """\n'
    '    import json as _tp_json\n'
    '    try:\n'
    '        _tp_meta = dict(_last_gen_meta)\n'
    '        return JSONResponse({"ok": True, "dry_run": True, **_tp_meta})\n'
    '    except Exception as _tp_e:\n'
    '        return JSONResponse({"ok": False, "error": str(_tp_e)}, status_code=500)\n'
)

if OLD not in content:
    print("❌ 既存test-promptエンドポイントが見つからない")
    # 現在のtest-prompt定義を表示
    for i,l in enumerate(content.split('\n')):
        if 'test-prompt' in l or 'test_prompt' in l:
            print(f"  L{i+1}: {l[:100]}")
    sys.exit(1)

content = content.replace(OLD, NEW, 1)
with open(API, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ /api/test-prompt 軽量版に差し替え完了")
