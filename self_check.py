#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
self_check.py - 自己ロジック（エージェント行動前後の自動チェック）
使い方: python self_check.py [pre|post|vae|server]

育成履歴:
  2026-10-22 v1: 初版
    - pre_check(): 修正前に必ず呼ぶ（バックアップ比較・根拠確認）
    - post_check(): 修正後に必ず呼ぶ（py_compile・VAE整合・CFG安全・ComfyUIエラー）
    - server_ensure(): APIサーバー/ComfyUI自動起動（ユーザーに手間取らせない）
    - vae_check(): debug_last_real_wf.jsonのVAE/CFG整合確認

ルール（2026-10-22 NextraLabsさんとの約束）:
  1. 修正前: pre_check()で根拠確認・バックアップ差分確認
  2. 修正後: post_check()で構文・VAE・CFG・ComfyUIエラーを全チェック
  3. サーバー停止: server_ensure()で自己起動。ユーザーへの依頼禁止
  4. 対処療法チェック: 「同じ種類のバグが他にないか」を必ず確認してから完了
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
    修正前に呼ぶ。
    - バックアップ存在確認
    - bak_fileが指定されていれば差分の有無を確認
    """
    issues = []
    if not os.path.exists(target_file):
        issues.append(f"対象ファイルが存在しない: {target_file}")
        return issues

    # バックアップ一覧
    baks = [f for f in os.listdir(os.path.dirname(target_file))
            if os.path.basename(target_file) in f and f != os.path.basename(target_file)]
    if not baks:
        issues.append(f"[pre_check WARN] バックアップが見当たらない: {os.path.dirname(target_file)}")
    elif verbose:
        print(f"[pre_check] バックアップ {len(baks)}件 確認OK: {baks[:3]}")

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

    # 結果
    if issues:
        print("[post_check] ❌ 問題あり:")
        for i in issues: print(f"  {i}")
    else:
        if verbose: print("[post_check] ✅ 全チェックPASS → 納品OK")
    return issues

# ── 自己改善ロジック ──────────────────────────────────────────

SELF_LOG = os.path.join(os.path.dirname(__file__), "self_check_log.jsonl")

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
    elif cmd == "improve":
        self_improve(); sys.exit(0)
    else:  # post
        issues = post_check(API_SERVER)
    elapsed = time.time() - t0
    log_result(cmd, issues, elapsed)
    sys.exit(0 if not issues else 1)
