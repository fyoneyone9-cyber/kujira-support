import sys, io, pathlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
API = pathlib.Path(r'C:\AI\ComfyUI\api_server_3001.py')
shutil.copy2(API, API.parent / (API.name + '.bak_test_prompt3'))
with open(API, encoding='utf-8', errors='replace') as f:
    content = f.read()

# POST(SinglePanelRequest必須) → GET(引数なし)に変更
OLD = '@app.post("/api/test-prompt")\nasync def test_prompt_endpoint(req: SinglePanelRequest, request: Request):'
NEW = '@app.get("/api/test-prompt")\nasync def test_prompt_endpoint():'

OLD2 = (
    '    import json as _tp_json\n'
    '    try:\n'
    '        _tp_meta = dict(_last_gen_meta)\n'
    '        return JSONResponse({"ok": True, "dry_run": True, **_tp_meta})\n'
    '    except Exception as _tp_e:\n'
    '        return JSONResponse({"ok": False, "error": str(_tp_e)}, status_code=500)\n'
)
NEW2 = (
    '    try:\n'
    '        _tp_meta = dict(_last_gen_meta)\n'
    '        return JSONResponse({"ok": True, "dry_run": True, **_tp_meta})\n'
    '    except Exception as _tp_e:\n'
    '        return JSONResponse({"ok": False, "error": str(_tp_e)}, status_code=500)\n'
)

ok = True
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print("✅ POST→GET変更")
else:
    print("❌ エンドポイント定義が見つからない"); ok = False

if ok and OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    print("✅ import json削除")
else:
    print("⚠ import json行なし（スキップ）")

if ok:
    with open(API, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 書き込み完了")
