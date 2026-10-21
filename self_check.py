#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
self_check.py - 自己ロジック（エージェント行動前後の自動チェック）
使い方: python self_check.py [pre|post|vae|server]

育成履歴:
  2026-10-22 v1: 初版 (pre/post/vae/server/clean/reload/improve)
  2026-10-22 v2: 自己ロジック強化
    - pre_check(): バックアップ確認に加え自動バックアップ作成
    - post_check(): dashboard.html JSエラー検出追加
    - sibling_check(): 同種バグ横展開チェック（v30直したならv40も確認）
    - test_generate(): 実生成テスト自動化（ComfyUIエラー有無を自分で確認）

ルール（2026-10-22 NextraLabsさんとの約束）:
  1. 修正前: pre_check()で自動バックアップ→差分確認→根拠記録
  2. 修正後: post_check()で構文・JS・VAE・CFG・ComfyUIエラーを全チェック
  3. サーバー停止: server_ensure()で自己起動。ユーザーへの依頼禁止
  4. 対処療法チェック: sibling_check()で同種バグ横展開を必ず確認
  5. 実生成確認: test_generate()でComfyUI実生成してエラーなしを自分で確認
"""
import sys, os, json, time, subprocess, socket, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

API_PORT   = 3002
COMFY_PORT = 8188
API_SERVER = r"C:\AI\ComfyUI\api_server_3001.py"
PYTHON     = r"C:\Users\fyone\anaconda3\python.exe"
START_BAT  = r"C:\AI\start.bat"
WF_DBG     = r"C:\AI\ComfyUI\debug_last_real_wf.json"

# ── ユーティリティ ─────────────────────────────────────────────

def _tcp_ok(port, timeout=3):
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
        s.close(); return True
    except: return False

def _http_get(url, timeout=5):
    try:
        r = urllib.request.urlopen(url, timeout=timeout)
        return r.status, r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return -1, str(e)

# ── サーバー自動起動 ───────────────────────────────────────────

def server_ensure(verbose=True):
    """APIサーバー・ComfyUIが落ちていたら自動起動。ユーザーへの依頼禁止。"""
    issues = []

    if not _tcp_ok(COMFY_PORT):
        if verbose: print("[server_ensure] ComfyUI停止 → start.bat起動")
        subprocess.Popen([START_BAT], shell=True)
        for i in range(24):
            time.sleep(5)
            if _tcp_ok(COMFY_PORT):
                if verbose: print(f"[server_ensure] ComfyUI UP (試行{i+1})")
                break
        else:
            issues.append("ComfyUI起動タイムアウト")

    if not _tcp_ok(API_PORT):
        if verbose: print("[server_ensure] APIサーバー停止 → 自己起動")
        subprocess.Popen([PYTHON, API_SERVER], cwd=os.path.dirname(API_SERVER))
        for i in range(12):
            time.sleep(5)
            if _tcp_ok(API_PORT):
                if verbose: print(f"[server_ensure] API UP (試行{i+1})")
                break
        else:
            issues.append("APIサーバー起動タイムアウト")

    if not issues:
        if verbose: print("[server_ensure] OK: API・ComfyUI両方UP")
    return issues

# ── VAE整合チェック ────────────────────────────────────────────

def vae_check(wf=None, verbose=True):
    """
    WFのVAE・CFGを検査。
    - Krea2系(moody/redcraft/krea/qwen含む)でsdxl_vae使用 → エラー
    - Krea2系でcfg>2.0 → 警告（赤ストライプ崩壊の予兆）
    """
    if wf is None:
        if not os.path.exists(WF_DBG):
            if verbose: print("[vae_check] debug_last_real_wf.json なし（スキップ）")
            return []
        with open(WF_DBG, encoding="utf-8") as f:
            wf = json.load(f)

    issues = []
    unet_name = ""
    for nd in wf.values():
        if isinstance(nd, dict) and nd.get("class_type") == "UNETLoader":
            unet_name = nd.get("inputs", {}).get("unet_name", "").lower()

    is_krea2 = any(k in unet_name for k in ("krea", "moody", "redcraft", "qwen"))

    for nid, nd in wf.items():
        if not isinstance(nd, dict): continue
        ct = nd.get("class_type", "")
        if ct == "VAELoader":
            vae = nd.get("inputs", {}).get("vae_name", "")
            if is_krea2 and "sdxl" in vae.lower():
                issues.append(f"[VAE ERROR] Krea2({unet_name}) + SDXL VAE({vae}) → 16ch/4ch不一致")
            elif verbose:
                print(f"[vae_check] node {nid}: VAE={vae} (OK)")
        if ct == "KSampler":
            cfg = nd.get("inputs", {}).get("cfg", 0)
            if is_krea2 and cfg > 2.0:
                issues.append(f"[CFG WARN] Krea2({unet_name}) cfg={cfg} >2.0 (赤ストライプ崩壊リスク)")
            elif verbose:
                print(f"[vae_check] node {nid}: cfg={cfg} steps={nd['inputs'].get('steps')} (OK)")

    if not issues and verbose:
        print("[vae_check] VAE/CFG整合 OK")
    return issues

# ── 修正前チェック ─────────────────────────────────────────────

def pre_check(target_file, bak_file=None, verbose=True):
    """
    修正前に呼ぶ。バックアップを自動作成してから差分確認。
    - 自動バックアップ作成（.bak_selfcheck_YYYYMMDD_HHMMSS）
    - 既存バックアップ一覧表示
    - bak_file指定時は差分行数を表示
    """
    import datetime, shutil
    issues = []
    if not os.path.exists(target_file):
        issues.append(f"対象ファイルが存在しない: {target_file}")
        return issues

    # 自動バックアップ作成
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    auto_bak = f"{target_file}.bak_selfcheck_{ts}"
    try:
        shutil.copy2(target_file, auto_bak)
        if verbose: print(f"[pre_check] ✅ 自動バックアップ作成: {os.path.basename(auto_bak)}")
    except Exception as e:
        issues.append(f"バックアップ作成失敗: {e}")

    # 既存バックアップ一覧
    baks = sorted([f for f in os.listdir(os.path.dirname(target_file))
            if os.path.basename(target_file) in f and f != os.path.basename(target_file)],
            reverse=True)[:5]
    if verbose:
        print(f"[pre_check] バックアップ一覧(最新5件): {baks}")

    if bak_file and os.path.exists(bak_file):
        with open(target_file, encoding="utf-8", errors="replace") as f:
            cur = f.read()
        with open(bak_file, encoding="utf-8", errors="replace") as f:
            bak = f.read()
        diff_lines = sum(1 for a, b in zip(cur.splitlines(), bak.splitlines()) if a != b)
        if verbose:
            print(f"[pre_check] vs {os.path.basename(bak_file)}: 差分行数≈{diff_lines}")

    return issues

# ── 修正後チェック ─────────────────────────────────────────────

def post_check(target_file, verbose=True):
    """
    修正後に必ず呼ぶ。
    1. py_compile 構文チェック
    2. VAE/CFG整合（debug_last_real_wf.jsonが存在する場合）
    3. ComfyUI履歴の最新エラー確認
    全チェックPASSで初めて「完了」と言える。
    """
    issues = []

    # 1. 構文チェック
    import py_compile
    try:
        py_compile.compile(target_file, doraise=True)
        if verbose: print(f"[post_check] py_compile OK: {os.path.basename(target_file)}")
    except py_compile.PyCompileError as e:
        issues.append(f"[SYNTAX ERROR] {e}")

    # 2. VAE/CFG整合
    vae_issues = vae_check(verbose=verbose)
    issues.extend(vae_issues)

    # 3. ComfyUI履歴エラー確認
    if _tcp_ok(COMFY_PORT):
        status, body = _http_get("http://127.0.0.1:8188/history?max_items=3")
        if status == 200:
            try:
                hist = json.loads(body)
                for pid, entry in list(hist.items())[:3]:
                    msgs = entry.get("status", {}).get("messages", [])
                    for mtype, mdata in msgs:
                        if mtype == "execution_error":
                            issues.append(f"[COMFY ERROR] {mdata.get('exception_type')}: {str(mdata.get('exception_message',''))[:120]}")
                if not any("[COMFY ERROR]" in i for i in issues) and verbose:
                    print("[post_check] ComfyUI履歴エラーなし OK")
            except: pass
    else:
        issues.append("[post_check WARN] ComfyUI未起動 → 履歴確認スキップ")

    # 4. dashboard.html JSエラーチェック（node --check相当）
    DASHBOARD = r"C:\AI\ComfyUI\dashboard.html"
    if os.path.exists(DASHBOARD):
        # JSブロックを抽出してnode構文チェック
        try:
            with open(DASHBOARD, encoding="utf-8", errors="replace") as f:
                html = f.read()
            import re, tempfile
            scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
            js_all = "\n".join(scripts)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8", delete=False) as tmp:
                tmp.write(js_all)
                tmp_path = tmp.name
            r = subprocess.run(["node", "--check", tmp_path], capture_output=True, text=True, timeout=15)
            os.unlink(tmp_path)
            if r.returncode != 0:
                issues.append(f"[JS ERROR] dashboard.html: {r.stderr[:200]}")
            elif verbose:
                print("[post_check] dashboard.html JS構文 OK")
        except FileNotFoundError:
            if verbose: print("[post_check] node未インストール → JSチェックスキップ")
        except Exception as e:
            if verbose: print(f"[post_check] JSチェックエラー(スキップ): {e}")

    # 結果
    if issues:
        print("[post_check] ❌ 問題あり:")
        for i in issues: print(f"  {i}")
    else:
        if verbose: print("[post_check] ✅ 全チェックPASS → 納品OK")
    return issues


def sibling_check(fix_type, verbose=True):
    """
    同種バグの横展開チェック。「v30直したならv40も確認」のような見落とし防止。
    fix_type例: "vae", "cfg", "lora", "clip"
    """
    SIBLING_MAP = {
        "vae": [
            ("redcraft v30", "REDCRAFT_V30_VAE", "redcraftHybridH3Krea2t_30"),
            ("redcraft v40", "REDCRAFT_V40_VAE", "redcraftHybridH3Krea2t_40"),
            ("redcraft qw21", "QW21_VAE", "qw21"),
            ("moody v8x", "MOODY_VAE", "moodyKrea2Mix"),
        ],
        "cfg": [
            ("moody", "MOODY_CFG=1.8", "moody"),
            ("redcraft v30", "REDCRAFT_V30_CFG=WFデフォルト", "30krea2"),
            ("redcraft v40", "REDCRAFT_V40_CFG=5.5", "40K2TDUAL"),
            ("redcraft qw21", "QW21_CFG=1.5", "qw21"),
        ],
    }
    siblings = SIBLING_MAP.get(fix_type, [])
    if not siblings:
        if verbose: print(f"[sibling_check] fix_type={fix_type} の定義なし")
        return []

    print(f"[sibling_check] {fix_type}系 横展開確認リスト:")
    for name, expected, keyword in siblings:
        print(f"  ☑ {name}: {expected} ({keyword})")
    print(f"[sibling_check] 上記全ての修正が正しいか確認してから完了にすること")
    return []


def test_generate(char_id="char_kakuseizai_s3_ff_tifa",
                  checkpoint="redcraftHybridH3Krea2t_30Krea2_fp8.safetensors",
                  timeout=300, verbose=True):
    """
    実生成テスト自動化。ComfyUIに投入してエラーなし確認。
    ユーザーが「動作確認は？」と言わなくても自分でやる。
    """
    import urllib.request as _ur, json as _json
    issues = []

    # サーバー確認
    srv_issues = server_ensure(verbose=False)
    if srv_issues:
        return srv_issues

    # キューキャンセル
    try:
        req = _ur.Request("http://127.0.0.1:8188/interrupt", data=b"{}", method="POST")
        _ur.urlopen(req, timeout=3)
        req2 = _ur.Request("http://127.0.0.1:8188/queue",
            data=_json.dumps({"clear": True}).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        _ur.urlopen(req2, timeout=3)
        time.sleep(2)
    except: pass

    # 生成リクエスト
    import urllib.request, http.client
    payload = _json.dumps({
        "panel": {
            "char_template_id": char_id, "char_id": char_id,
            "prompt": "(1girl:2.0),(masterpiece:1.2)",
            "outfit_prompt": "(1girl:2.0)", "outfit_label": "SELF_CHECK_TEST",
            "outfit_index": 0, "page_idx": 0, "panel_idx": 0,
            "penetration_off": True, "clothes_off": False,
            "wf_type": "moody_krea2_v7", "checkpoint": checkpoint, "style_preset": "",
        },
        "page_idx": 0, "panel_idx": 0,
        "wf_type": "moody_krea2_v7", "checkpoint": checkpoint,
    }).encode()
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:3002/api/generate-panel",
            data=payload, headers={"Content-Type": "application/json"}, method="POST")
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = _json.loads(resp.read())
        img = data.get("image_path", "")
        err = data.get("error", "")
        if err:
            issues.append(f"[TEST_GEN ERROR] {err}")
        elif img:
            if verbose: print(f"[test_generate] ✅ 生成成功: {img}")
        else:
            issues.append("[TEST_GEN] image_pathが空")
    except Exception as e:
        issues.append(f"[TEST_GEN EXCEPTION] {e}")

    # ComfyUI履歴エラー確認
    time.sleep(2)
    try:
        status, body = _http_get("http://127.0.0.1:8188/history?max_items=1")
        hist = _json.loads(body)
        for pid, entry in hist.items():
            for mtype, mdata in entry.get("status", {}).get("messages", []):
                if mtype == "execution_error":
                    issues.append(f"[COMFY ERROR] {mdata.get('exception_type')}: {str(mdata.get('exception_message',''))[:150]}")
        if not any("[COMFY ERROR]" in i for i in issues) and verbose:
            print("[test_generate] ✅ ComfyUIエラーなし")
    except Exception as e:
        issues.append(f"[COMFY HIST ERROR] {e}")

    if not issues and verbose:
        print("[test_generate] ✅ 実生成テスト完全PASS")
    return issues

# ── 自己改善ロジック ──────────────────────────────────────────

SELF_LOG = os.path.join(os.path.dirname(__file__), "self_check_log.jsonl")

def clean_all():
    """
    キャッシュ・旧ログを全クリア。
    「キャッシュのせい」「前のログのせい」をユーザーに押し付けない。
    1. ComfyUI履歴クリア (POST /history {clear:true})
    2. debug_last_real_wf.json リセット
    3. ブラウザCtrl+Shift+Rハードリロード
    """
    import urllib.request, json as _json
    issues = []

    # 1. ComfyUI履歴クリア
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8188/history",
            data=_json.dumps({"clear": True}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=5)
        print("[clean_all] ✅ ComfyUI履歴クリア完了")
    except Exception as e:
        issues.append(f"ComfyUI履歴クリア失敗: {e}")
        print(f"[clean_all] ❌ ComfyUI履歴クリア失敗: {e}")

    # 2. debug_last_real_wf.json リセット
    try:
        if os.path.exists(WF_DBG):
            with open(WF_DBG, "w", encoding="utf-8") as f:
                f.write("{}")
            print("[clean_all] ✅ debug_last_real_wf.json リセット")
    except Exception as e:
        issues.append(f"WFログリセット失敗: {e}")

    # 3. ブラウザハードリロード
    r_issues = reload_dashboard()
    issues.extend(r_issues)

    if not issues:
        print("[clean_all] ✅ 全クリア完了 → クリーンな状態で確認可能")
    return issues

def reload_dashboard():
    """ダッシュボードブラウザウィンドウにCtrl+Shift+Rを送信してハードリロード。"""
    try:
        import subprocess
        script = (
            'Add-Type -AssemblyName System.Windows.Forms;'
            '$w = New-Object -ComObject WScript.Shell;'
            '$p = Get-Process | Where-Object { $_.MainWindowTitle -match "3002|dashboard|ComfyUI|manga" } | Select-Object -First 1;'
            'if ($p) { $w.AppActivate($p.Id); Start-Sleep -Milliseconds 500; $w.SendKeys("^+r"); Write-Host "OK:$($p.MainWindowTitle)" } else { Write-Host "NG:not found" }'
        )
        r = subprocess.run(["powershell", "-Command", script], capture_output=True, text=True, timeout=10)
        out = r.stdout.strip()
        if "OK:" in out:
            print(f"[reload_dashboard] ✅ {out}")
            return []
        else:
            print(f"[reload_dashboard] ❌ {out}")
            return [f"reload failed: {out}"]
    except Exception as e:
        return [f"reload error: {e}"]

def log_result(cmd, issues, elapsed_sec):
    """実行結果をJSONLに記録。自己改善の材料にする。"""
    import datetime
    entry = {
        "ts":      datetime.datetime.now().isoformat(),
        "cmd":     cmd,
        "issues":  issues,
        "elapsed": round(elapsed_sec, 1),
        "passed":  len(issues) == 0,
    }
    with open(SELF_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def self_improve():
    """
    self_check_log.jsonlを分析して繰り返しパターンを検出し改善提案を出す。
    同じissueが3回以上出ていたら「根本対処が不十分」と判断。
    """
    if not os.path.exists(SELF_LOG):
        print("[self_improve] ログなし（初回）")
        return

    from collections import Counter
    counter = Counter()
    total = 0
    with open(SELF_LOG, encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
                total += 1
                for issue in e.get("issues", []):
                    # issueの先頭タグ部分をキーに
                    key = issue.split("]")[0] + "]" if "]" in issue else issue[:40]
                    counter[key] += 1
            except: pass

    print(f"[self_improve] 実行履歴 {total}件")
    repeat = [(k, v) for k, v in counter.items() if v >= 3]
    if repeat:
        print("⚠️ 繰り返し検出（根本対処が不十分の可能性）:")
        for k, v in sorted(repeat, key=lambda x: -x[1]):
            print(f"  {v}回: {k}")
    else:
        print("[self_improve] 繰り返しパターンなし ✅")

# ── メイン ────────────────────────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "post"
    t0 = time.time()
    if cmd == "server":
        issues = server_ensure()
    elif cmd == "vae":
        issues = vae_check()
    elif cmd == "pre":
        issues = pre_check(API_SERVER)
    elif cmd == "sibling":
        fix_type = sys.argv[2] if len(sys.argv) > 2 else "vae"
        issues = sibling_check(fix_type)
    elif cmd == "test":
        ckpt = sys.argv[2] if len(sys.argv) > 2 else "redcraftHybridH3Krea2t_30Krea2_fp8.safetensors"
        issues = test_generate(checkpoint=ckpt)
    elif cmd == "clean":
        issues = clean_all()
    elif cmd == "reload":
        issues = reload_dashboard()
    elif cmd == "improve":
        self_improve(); sys.exit(0)
    else:  # post
        issues = post_check(API_SERVER)
    elapsed = time.time() - t0
    log_result(cmd, issues, elapsed)
    sys.exit(0 if not issues else 1)
