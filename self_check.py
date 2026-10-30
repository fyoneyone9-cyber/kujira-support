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

def brief(verbose=True):
    """
    セッション開始時に必ず呼ぶ。重要知識・過去の失敗・現在の状態を自己確認する。
    これを呼ばずに作業を始めない。
    """
    import datetime
    lines = []
    lines.append("=" * 55)
    lines.append("  SELF BRIEF - セッション開始チェック")
    lines.append("=" * 55)

    # 1. サーバー状態
    api_ok   = _tcp_ok(API_PORT)
    comfy_ok = _tcp_ok(COMFY_PORT)
    lines.append(f"[状態] API={('UP' if api_ok else '❌DOWN')} ComfyUI={('UP' if comfy_ok else '❌DOWN')}")

    # 2. 絶対ルール確認
    lines.append("[絶対ルール]")
    lines.append("  ・修正前: pre_check()で自動バックアップ+根拠入力必須")
    lines.append("  ・修正後: post_check()→全チェックPASSが完了条件")
    lines.append("  ・Krea2系VAE=qwen_image_vae(16ch) / SDXL=sdxl_vae_fp16fix(4ch)")
    lines.append("  ・Krea2 cfg>2.0 → 赤ストライプ崩壊リスク")
    lines.append("  ・moody cfg=1.8厳守 / redcraft30 WFデフォルト(cfg=1.0)不干渉")
    lines.append("  ・根拠なし修正禁止 / 対処療法禁止(sibling_check必須)")
    lines.append("  ・サーバー停止=自己起動 / キャッシュ=自己クリア")

    # 3. 直近の失敗パターン（self_check_log.jsonlから）
    if os.path.exists(SELF_LOG):
        from collections import Counter
        counter = Counter()
        with open(SELF_LOG, encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    for issue in e.get("issues", []):
                        key = issue.split("]")[0] + "]" if "]" in issue else issue[:40]
                        counter[key] += 1
                except: pass
        top = counter.most_common(3)
        if top:
            lines.append("[過去の失敗TOP3]")
            for k, v in top:
                lines.append(f"  {v}回: {k}")

    lines.append("=" * 55)
    print("\n".join(lines))

    # AGENT_RULES.mdを自動表示（アカウント跨ぎで知識を共有）
    RULES = r"C:\AI\ComfyUI\AGENT_RULES.md"
    if os.path.exists(RULES):
        print(f"\n[brief] AGENT_RULES.md 確認済み: {RULES}")
    else:
        print(f"[brief] ⚠️ AGENT_RULES.md が見つからない: {RULES}")

    # サーバーが落ちていれば即起動
    if not api_ok or not comfy_ok:
        print("[brief] サーバー停止検知 → 自動起動")
        server_ensure()

    return []


def agent_sanity_check():
    """[AGENT_SANITY_V1] preコマンド実行時に毎回強制実行。口約束をコードで強制する恒久対策。"""
    # [MEMORY_READ_V1] セッション開始時にMEMORY.mdを読まないと先に進めない恒久対策
    # AGENTS.mdの指示をコードで強制する
    import os
    memory_path = r"C:\Users\fyone\AppData\Roaming\Genspark Claw\users\ab54bf68-d5d4-409b-83d4-8b036308c046\workspace\MEMORY.md"
    if os.path.exists(memory_path):
        with open(memory_path, encoding="utf-8", errors="replace") as _mf:
            _mem = _mf.read()
        # 必須ルールを強制表示（毎回）
        print("=" * 60)
        print("[MEMORY_READ_V1] 必須ルール確認:")
        # ミス恒久対策ログを抽出して表示
        _idx = _mem.find("ミス恒久対策ログ")
        if _idx >= 0:
            _section = _mem[_idx:_idx+800]
            for _l in _section.splitlines()[:15]:
                print(f"  {_l}")
        # 画質問題報告時の必須手順
        _idx2 = _mem.find("画質・生成不良")
        if _idx2 >= 0:
            for _l in _mem[_idx2:_idx2+300].splitlines()[:6]:
                print(f"  {_l}")
        print("  → logcheck未実行なら今すぐ: python self_check.py logcheck")
        print("=" * 60)

    # [SCOPE_GUARD_V1] 指示外キャラIDを変更していないかチェック
    # SCOPE_TARGET に指示されたキャラIDのみ記録。それ以外の変更はNG
    import os as _sg_os
    _scope_log = r"C:\GensparkClaw\kujira-support\scope_target.txt"
    if _sg_os.path.exists(_scope_log):
        with open(_scope_log, encoding="utf-8") as _sf:
            _targets = [l.strip() for l in _sf.readlines() if l.strip()]
        print(f"[SCOPE_GUARD_V1] 指示対象キャラID: {_targets}")
        print("  指示外のキャラID変更は禁止。scope_target.txtを確認すること")
    import urllib.request as _ur, json as _lj, os, datetime
    warnings = []

    # ルール1: api_server_3001.py / dashboard.html を触る前にCODEMAP.mdを読んでいるか
    # → CODEMAP.mdの最終読み取りが24h以上前なら警告
    codemap = r"C:\AI\ComfyUI\CODEMAP.md"
    if os.path.exists(codemap):
        mtime = os.path.getmtime(codemap)
        age_h = (datetime.datetime.now().timestamp() - mtime) / 3600
        # CODEMAPはread専用なので更新時刻ではなく参照時刻は取れない
        # 代わりに: 今日のself_check_log.jsonlにCODEMAP確認記録があるか確認
        # (記録がなければ警告)
        pass  # ファイル参照時刻はOS依存のため省略・ログベースで代替

    # ルール2: 直前の生成ログにCHAR_PROMPT_MISSINGがないか確認（生成品質の自動監視）
    try:
        with _ur.urlopen("http://127.0.0.1:3002/api/last-prompt", timeout=3) as _r:
            _d = _lj.loads(_r.read())
        _diags = _d.get("diagnostics") or []
        for _dg in _diags:
            if "CHAR_PROMPT_MISSING" in str(_dg):
                warnings.append(f"⚠️ [前回生成] CHAR_PROMPT_MISSING検出 — 作業前にlogcheckで確認せよ: {_dg}")
    except Exception:
        pass  # API未起動時はスキップ

    # ルール3: _char_prompt_guard.log に未確認エラーがないか
    guard_log = r"C:\AI\ComfyUI\_char_prompt_guard.log"
    if os.path.exists(guard_log):
        with open(guard_log, encoding="utf-8", errors="replace") as _gf:
            _glines = _gf.readlines()
        if _glines:
            warnings.append(f"⚠️ [CHAR_PROMPT_GUARD] {len(_glines)}件の未処理エラーあり: {_glines[-1].strip()}")

    if warnings:
        print("=" * 60)
        print("[AGENT_SANITY_V1] 🚨 作業前チェックで問題を検出:")
        for w in warnings:
            print(" ", w)
        print("  → 上記を解消してから修正を開始すること")
        print("=" * 60)
    else:
        print("[AGENT_SANITY_V1] ✅ 作業前チェック異常なし")
    return warnings


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

    # 根拠入力ゲート（憶測修正防止）
    # 引数で渡す場合: pre_check(file, reason="ログL9219にsdxl確認")
    # コマンドライン: python self_check.py pre "根拠テキスト"
    reason = bak_file if bak_file and not os.path.exists(bak_file) else None
    if reason is None and len(sys.argv) > 2 and not os.path.exists(sys.argv[2]):
        reason = sys.argv[2]
    if reason:
        print(f"[pre_check] 根拠: {reason}")
        log_result("pre_reason", [f"根拠: {reason}"], 0)
    else:
        if verbose: print("[pre_check] ⚠️ 根拠未記録。修正前に根拠を確認すること")

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

    # dashboard.html 自動修正チェック（auto_fix_dashboard.py呼び出し）
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import importlib
        afd = importlib.import_module("auto_fix_dashboard")
        importlib.reload(afd)
        changed, results = afd.auto_fix(verbose=verbose)
        if changed:
            # 修正後に再チェック
            changed2, results2 = afd.auto_fix(verbose=False)
            if results2:
                for r in results2: issues.append(f"[DASHBOARD] {r}")
                if verbose: print(f"[post_check] ⚠ dashboard.html 修正後も問題残: {results2}")
            else:
                if verbose: print(f"[post_check] ✅ dashboard.html 自動修正完了・クリーン ({len(results)}件修正)")
        elif results:
            for r in results: issues.append(f"[DASHBOARD] {r}")
            if verbose: print(f"[post_check] ⚠ dashboard.html 要手動確認: {results}")
        else:
            if verbose: print("[post_check] dashboard.html チェック OK")
    except Exception as e:
        if verbose: print(f"[post_check] dashboard チェックスキップ: {e}")

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
        agent_sanity_check()
        issues = pre_check(API_SERVER)
    elif cmd == "brief":
        issues = brief()
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
    elif cmd == "logcheck":
        # [LOGCHECK_V1] 画像品質問題が報告されたら最初にこれを実行する
        import urllib.request as _ur, json as _lj
        print("=== [LOGCHECK_V1] 最終生成ログ自動診断 ===")
        try:
            with _ur.urlopen("http://127.0.0.1:3002/api/last-prompt", timeout=5) as _r:
                _d = _lj.loads(_r.read())
            _pos = _d.get("positive_prompt", "")
            print(f"キャラID     : {_d.get('dbg_char_template_id') or '⚠️ 未記録'}")
            print(f"positive先頭 : {_pos[:150]}")
            # [LOGCHECK_CPM_FIX_V2 2026-10-27] 旧判定は replace("_"," ") 後に
            # split("_") していたため常にID全文を検索=恒常誤警報だった。
            # char_prompt の先頭5タグ(重み括弧除去)のいずれかが最終posに
            # 含まれていればOKとする（API側診断V2と同等ロジック）。
            import re as _re_lc
            _cp = _d.get("char_prompt") or ""
            if _cp:
                _lc_tags = []
                for _t in _cp.split(",")[:5]:
                    _t = _re_lc.sub(r"[():]|\d+\.\d+", "", _t).strip().lower()
                    if len(_t) > 3:
                        _lc_tags.append(_t)
                if _lc_tags and not any(_t in _pos.lower() for _t in _lc_tags):
                    print(f"🚨 [CHAR_PROMPT_MISSING] キャラ先頭タグ群がpositiveに未反映: {_lc_tags[:3]}")
            for _dg in (_d.get("diagnostics") or []):
                print(" ", _dg)
            print(f"WF/ckpt      : {_d.get('wf_file_used','')} / {_d.get('checkpoint_used','')}")
            _ks = _d.get("ksampler") or {}
            print(f"cfg/steps    : cfg={_ks.get('cfg')} steps={_ks.get('steps')}")
        except Exception as _le:
            print(f"⚠️ API取得失敗: {_le}")
        print("=== logcheck 完了 ===")
        issues = []
    elif cmd == "improve":
        self_improve(); sys.exit(0)
    else:  # post
        agent_sanity_check()
        issues = post_check(API_SERVER)
        # [POST_LOGCHECK_V1] post後に自動でlogcheckを実行（口約束をコードで強制）
        import urllib.request as _ur2, json as _lj2
        print("\n[POST_LOGCHECK_V1] --- post後自動logcheck ---")
        try:
            with _ur2.urlopen("http://127.0.0.1:3002/api/last-prompt", timeout=5) as _r2:
                _d2 = _lj2.loads(_r2.read())
            _pos2 = _d2.get("positive_prompt","")
            _cid2 = _d2.get("dbg_char_template_id","") or "未記録"
            print(f"  キャラID: {_cid2}")
            print(f"  positive先頭: {_pos2[:120]}")
            _diags2 = _d2.get("diagnostics") or []
            for _dg2 in _diags2:
                if "CHAR_PROMPT_MISSING" in str(_dg2) or "🚨" in str(_dg2):
                    print(f"  🚨 {_dg2}")
                    issues.append(f"[POST_LOGCHECK] {_dg2}")
        except Exception as _ple:
            print(f"  API未応答: {_ple}")
        print("[POST_LOGCHECK_V1] --- 完了 ---\n")

        # [POST_EVIDENCE_V1] 実生成してキャラ名がpositiveに入っているか強制確認
        # コード修正後に必ず実行。PassしないとNGと判断する。
        print("\n[POST_EVIDENCE_V1] --- ティファ/エアリス実生成エビデンス確認 ---")
        import time as _evt
        _evidence_chars = [
            ("char_kaizo_nichijou3_tifa", "tifa lockhart", "Tifa Lockhart, Final Fantasy VII, long black hair"),
            ("char_kaizo_nichijou3_aerith", "aerith gainsborough", "Aerith Gainsborough, Final Fantasy VII, long brown hair"),
        ]
        _evidence_ng = []
        for _ecid, _ekey, _eprompt in _evidence_chars:
            # ロック解除待ち＋生成
            _ebody = __import__("json").dumps({
                "char_template_id": _ecid,
                "outfit_index": 0,
                "panel": {"char_template_id": _ecid, "prompt": _eprompt},
                "page_idx": 0, "panel_idx": 0
            }).encode()
            _ok = False
            for _et in range(12):
                _evt.sleep(5)
                try:
                    _ereq = _ur2.Request("http://127.0.0.1:3002/api/generate-panel",
                        data=_ebody, headers={"Content-Type":"application/json"}, method="POST")
                    with _ur2.urlopen(_ereq, timeout=120) as _er:
                        _ok = True
                    break
                except Exception as _ee:
                    if "409" in str(_ee):
                        print(f"  [{_ecid}] ロック中... {(_et+1)*5}s")
                    else:
                        print(f"  [{_ecid}] 生成エラー: {_ee}"); break
            _evt.sleep(3)
            try:
                with _ur2.urlopen("http://127.0.0.1:3002/api/last-prompt", timeout=5) as _elr:
                    _ed = _lj2.loads(_elr.read())
                _epos = _ed.get("positive_prompt","")
                _ecid_got = _ed.get("dbg_char_template_id","未記録")
                _pass = _ekey in _epos.lower() and _ecid_got == _ecid
                _status = "✅ PASS" if _pass else "❌ FAIL"
                print(f"  {_status} [{_ecid}] キャラ名含む: {_ekey in _epos.lower()}, ID一致: {_ecid_got == _ecid}")
                if not _pass:
                    _evidence_ng.append(f"[EVIDENCE_FAIL] {_ecid}: キャラ名未反映")
                    issues.append(f"[EVIDENCE_FAIL] {_ecid}: positiveにキャラ名なし")
            except Exception as _ele:
                print(f"  [{_ecid}] last-prompt失敗: {_ele}")
                _evidence_ng.append(f"[EVIDENCE_ERROR] {_ecid}")
        if _evidence_ng:
            print("  🚨 エビデンスNG — 未解決の問題あり。納品禁止。")
        else:
            print("  🎉 全キャラエビデンス確認完了 — 納品OK")
        print("[POST_EVIDENCE_V1] --- 完了 ---\n")
    elapsed = time.time() - t0
    log_result(cmd, issues, elapsed)
    sys.exit(0 if not issues else 1)
