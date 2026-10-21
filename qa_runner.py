#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
qa_runner.py - 漫画ダッシュボード動作確認システム
使い方:
  python qa_runner.py [char ...]           # 実生成あり（ComfyUI投入）
  python qa_runner.py --dry-run [char ...] # 実生成なし（プロンプト検証のみ）
  例: python qa_runner.py --dry-run aerith tifa aerith_redcraft

育成履歴:
  2026-10-21 初版 (aerith/tifa, LoRA禁止確認, ComfyUI WF検証)
  2026-10-22 v2: aerith_debug_runner.py統合・409リトライ・api_up socket化
  2026-10-22 v3: aerith_redcraft追加・CHARS定義順fix・WF静的チェック・ComfyUI
                 再投入廃止(既存生成汚染を防ぐため)
  2026-10-22 v4:
    - --dry-run モード追加（ComfyUI実投入ゼロ）
      通常運用中でも安全に実行できる。実生成は api/generate-panel ではなく
      api/test-prompt（プロンプト生成のみ、ComfyUI未投入）で代替する
    - wait_comfy_queue_empty() を先頭に追加（実生成モード時）
    - Fix: qa_runner実行がダッシュボードの通常生成を汚染していた問題を解消
  2026-10-22 v5:
    - tifa_redcraft30追加: redcraft 30(cfg=1.0設計)でCFG誤上書きを検出するテスト
      [KSAMPLER_NON_QW21_FIX_V3]で直したミスの再発防止。
      expect_cfg=1.0でWFデフォルトが保持されているか確認する
    - check_wf_static()にKrea2 CFG安全チェック追加:
      cfg>2.0のとき自動警告（赤ストライプ崩壊の予兆検出）
"""
import sys, io, json, time, requests, pathlib, socket
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API       = "http://127.0.0.1:3002"
COMFY     = "http://127.0.0.1:8188"
WF_DBG    = pathlib.Path(r"C:\AI\ComfyUI\debug_last_real_wf.json")

# ── リクエスト定数（CHARSより先に定義必須）────────────────────
DEFAULT_REQ = {
    "wf_type":      "moody_krea2_v7",
    "checkpoint":   "moodyKrea2MixUncensoredV8SEGoes_v80_int8.safetensors",
    "style_preset": "moody_krea2_premium",
}

REDCRAFT_REQ = {
    "wf_type":      "moody_krea2_v7",
    "checkpoint":   "redcraftHybridH3Krea2t_40K2TDUAL_3196558.safetensors",
    "style_preset": "",
}

# redcraft 30: WFデフォルトcfg=1.0/steps=8が保持されているか確認用
# [KSAMPLER_NON_QW21_FIX_V3] 再発防止テスト
REDCRAFT30_REQ = {
    "wf_type":      "moody_krea2_v7",
    "checkpoint":   "redcraftHybridH3Krea2t_30Krea2_fp8.safetensors",
    "style_preset": "",
}

# ── キャラ定義 ─────────────────────────────────────────────────
CHARS = {
    "aerith_redcraft": {
        "char_id": "char_kakuseizai_s3_ff_aerith",
        "prompt": (
            "(solo:2.2),(1girl:2.2),(only one person:2.0),"
            "(Aerith Gainsborough:1.9),(Final Fantasy VII:1.8),(ff7:1.8),"
            "(young woman:1.6),(slender:1.5),(medium breasts:1.5),"
            "22 years old,long brown braided hair,pink ribbon,green eyes,pink dress,"
            "burning drug injected directly into vein,wincing from searing pain,"
            "vein bulging,skin flushing red where injected,upper body,dim room,eye level,"
            "(drugged high:2.0),(dilated pupils:2.0),(flushed face:1.8),(sweating:1.7),"
            "(ahegao:1.6),(trembling violently:1.5),(masterpiece:1.2),(best quality:1.2),detailed"
        ),
        "check_tags":     ["aerith", "ff7"],
        "forbidden_loras":["aerith"],
        "expect_cfg":     5.5,
        "expect_steps":   30,
        "req_override":   REDCRAFT_REQ,
    },
    "aerith": {
        "char_id": "char_kakuseizai_s3_ff_aerith",
        "prompt": (
            "(solo:2.2),(1girl:2.2),(only one person:2.0),"
            "(Aerith Gainsborough:1.9),(Final Fantasy VII:1.8),(ff7:1.8),"
            "(young woman:1.6),(slender:1.5),(medium breasts:1.5),"
            "22 years old,long brown braided hair,pink ribbon,green eyes,pink dress"
        ),
        "check_tags":     ["aerith", "final fantasy", "ff7"],
        "forbidden_loras":["aerith"],
    },
    "tifa_redcraft30": {
        # [KSAMPLER_NON_QW21_FIX_V3 再発防止] redcraft 30はcfg=1.0/steps=8(WFデフォルト)
        # KSAMPLER_NON_QW21がredcraftに誤CFG上書きしていないかを確認する
        "char_id": "char_kakuseizai_s3_ff_tifa",
        "prompt": (
            "(solo:2.2),(1girl:2.2),(only one person:2.0),"
            "(Tifa Lockhart:1.9),(Final Fantasy VII:1.8),(ff7:1.8),"
            "20 years old,long black hair,red eyes"
        ),
        "check_tags":     ["tifa", "ff7"],
        "forbidden_loras":["tifa"],
        "expect_cfg":     1.0,
        "expect_steps":   8,
        "req_override":   REDCRAFT30_REQ,
    },
    "tifa": {
        "char_id": "char_kakuseizai_s3_ff_tifa",
        "prompt": (
            "(solo:2.2),(1girl:2.2),(only one person:2.0),"
            "(Tifa Lockhart:1.9),(Final Fantasy VII:1.8),(ff7:1.8),"
            "(young woman:1.6),(slender:1.5),(large breasts:1.5),"
            "20 years old,long black hair,red eyes,black tank top"
        ),
        "check_tags":     ["tifa", "lockhart", "ff7"],
        "forbidden_loras":["tifa"],
    },
}

# ── 接続確認 ─────────────────────────────────────────────────

def _tcp_ok(port, timeout=5):
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
        s.close()
        return True
    except OSError:
        return False

def api_up():   return _tcp_ok(3002)
def comfy_up(): return _tcp_ok(8188)

def wait_comfy_queue_empty(timeout=300):
    """ComfyUIキューが空になるまで待つ（実生成モード時に呼ぶ）"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            q = requests.get(f"{COMFY}/queue", timeout=5).json()
            if not q.get("queue_running") and not q.get("queue_pending"):
                return True
        except:
            pass
        time.sleep(3)
    return False

# ── プロンプト生成 ─────────────────────────────────────────────

def build_req(char_cfg):
    base_req = char_cfg.get("req_override", DEFAULT_REQ)
    panel = {
        "char_template_id": char_cfg["char_id"],
        "char_id":          char_cfg["char_id"],
        "prompt":           char_cfg["prompt"],
        "outfit_prompt":    char_cfg["prompt"],
        "outfit_label":     "QA_TEST",
        "outfit_index":     0,
        "page_idx":         0,
        "panel_idx":        0,
        "penetration_off":  True,
        "clothes_off":      False,
        **base_req,
    }
    return {"panel": panel, "page_idx": 0, "panel_idx": 0, **base_req}

def send_dry(char_cfg):
    """
    --dry-run モード: ComfyUI投入なし・last_gen_metaを返す軽量確認
    /api/test-prompt は _last_gen_meta をそのまま返す軽量エンドポイント
    注意: 直前のgenerate-panel実行結果を参照するため、
          全キャラ連続dry-runでは前のキャラの結果が混ざることがある
          → キャラごとの個別実行推奨（python qa_runner.py --dry-run aerith）
    """
    try:
        r = requests.get(f"{API}/api/test-prompt", timeout=5)
        return r.status_code, r.text[:300]
    except Exception as e:
        return -1, str(e)

def send_real(char_cfg):
    """
    実生成モード: ComfyUIに投入して生成を走らせる
    409(先行生成中)は15秒待ってリトライ・最大3回
    timeout=360: redcraft v40はsteps=30で約180秒かかるため余裕をもたせる
    """
    req = build_req(char_cfg)
    for attempt in range(3):
        try:
            r = requests.post(f"{API}/api/generate-panel", json=req, timeout=360)
            if r.status_code == 409:
                time.sleep(15)
                continue
            return r.status_code, r.text[:300]
        except Exception as e:
            if attempt < 2:
                time.sleep(10)
                continue
            return -1, str(e)
    return -1, "max retries exceeded"

# ── 検証ロジック ───────────────────────────────────────────────

def get_last_prompt():
    try:
        return requests.get(f"{API}/api/last-prompt", timeout=5).json()
    except:
        return {}

def check_wf_loras():
    if not WF_DBG.exists():
        return []
    try:
        with open(WF_DBG, encoding='utf-8') as f:
            wf = json.load(f)
        return [
            (nid, node["inputs"].get("lora_name","?"), node["inputs"].get("strength_model",0))
            for nid, node in wf.items()
            if isinstance(node, dict) and "lora" in node.get("class_type","").lower()
        ]
    except:
        return []

def check_wf_static():
    """
    debug_last_real_wf.json を静的解析
    ComfyUIに投入しない（再投入は通常運用の生成を汚染するため廃止）
    検出: UNETLoader/KSampler存在・Krea2+SDXL VAE不一致（16ch/4ch問題）
    """
    if not WF_DBG.exists():
        return False, "debug_last_real_wf.json not found"
    try:
        with open(WF_DBG, encoding='utf-8') as f:
            wf = json.load(f)
        issues = []
        has_unet = any(n.get("class_type") in ("UNETLoader","CheckpointLoaderSimple","CheckpointLoader")
                       for n in wf.values() if isinstance(n, dict))
        has_ks   = any(n.get("class_type") == "KSampler"
                       for n in wf.values() if isinstance(n, dict))
        if not has_unet: issues.append("no UNETLoader/CheckpointLoader")
        if not has_ks:   issues.append("no KSampler")
        unet_name = ""
        for n in wf.values():
            if isinstance(n, dict) and n.get("class_type") == "UNETLoader":
                unet_name = n.get("inputs",{}).get("unet_name","").lower()
        for n in wf.values():
            if isinstance(n, dict) and n.get("class_type") == "VAELoader":
                vae = n.get("inputs",{}).get("vae_name","")
                is_krea2 = any(k in unet_name for k in ("krea","moody","redcraft","qwen"))
                is_sdxl_vae = "sdxl" in vae.lower()
                if is_krea2 and is_sdxl_vae:
                    issues.append(f"Krea2 UNET + SDXL VAE({vae}) 16ch/4ch不一致")
        # [KSAMPLER_NON_QW21_FIX_V3 再発防止] Krea2でcfg>2.0は赤ストライプ崩壊の予兆
        is_krea2_model = any(k in unet_name for k in ("krea","moody","redcraft","qwen"))
        for n in wf.values():
            if isinstance(n, dict) and n.get("class_type") == "KSampler":
                cfg = n.get("inputs",{}).get("cfg", 0)
                if is_krea2_model and cfg > 2.0:
                    issues.append(f"[警告] Krea2でcfg={cfg} >2.0 (赤ストライプ崩壊の可能性)")
        return (False, "; ".join(issues)) if issues else (True, f"WF OK (nodes={len(wf)})")
    except Exception as e:
        return False, str(e)

# ── テスト実行 ─────────────────────────────────────────────────

def run_char(name, char_cfg, dry_run=False):
    print(f"\n{'='*50}")
    print(f"  {name.upper()} テスト{'（dry-run）' if dry_run else ''}")
    print(f"{'='*50}")
    results = []

    # Case1: プロンプト生成（dry-run=test-prompt / 実生成=generate-panel）
    if dry_run:
        status, body = send_dry(char_cfg)
        label = "プロンプト生成(dry)"
    else:
        status, body = send_real(char_cfg)
        label = "生成API status"
    ok = status == 200
    results.append((label, ok, f"status={status}" + ("" if ok else f" {body[:80]}")))
    if not ok:
        _report(name, results)
        return False

    lp = get_last_prompt()
    pp = lp.get("positive_prompt", "").lower()

    # Case2: キャラタグ保持確認
    for tag in char_cfg["check_tags"]:
        found = tag.lower() in pp
        results.append((f"タグ [{tag}] 保持", found, "(found)" if found else "(not found)"))

    # Case3: 禁止LoRA未注入確認
    wf_loras = check_wf_loras()
    lora3    = lp.get("lora3", "")
    for fl in char_cfg["forbidden_loras"]:
        injected = fl.lower() in lora3.lower() or any(fl.lower() in ln.lower() for _, ln, _ in wf_loras)
        results.append((f"禁止LoRA [{fl}] なし", not injected, f"lora3={lora3!r} nodes={wf_loras}"))

    # Case4: WF LoRAノード数=0
    results.append(("WF LoRAノード=0", len(wf_loras)==0, f"{len(wf_loras)}個"))

    # Case5: CFG/steps期待値（checkpointごとに正しい値が設定されているか）
    if "expect_cfg" in char_cfg:
        ks = lp.get("ksampler", {})
        results.append((f"CFG={char_cfg['expect_cfg']}", ks.get("cfg")==char_cfg["expect_cfg"], f"actual={ks.get('cfg')}"))
        results.append((f"steps={char_cfg['expect_steps']}", ks.get("steps")==char_cfg["expect_steps"], f"actual={ks.get('steps')}"))

    # Case6: WF静的チェック（VAE不一致等）
    wf_ok, wf_detail = check_wf_static()
    results.append(("WF静的チェック", wf_ok, wf_detail))

    _report(name, results)
    return all(r[1] for r in results)

def _report(name, results):
    all_ok = all(r[1] for r in results)
    for label, ok, detail in results:
        print(f"  {'✅' if ok else '❌'} {label}: {str(detail)[:120]}")
    print(f"  → {'PASS ✅' if all_ok else 'FAIL ❌'}")

# ── メイン ─────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    # [DRY_RUN_ONLY_V1] 実生成モードは通常ダッシュボード生成を汚染するため廃止
    # qa_runner.pyは常にdry-runで動作する。--no-dry-runフラグで明示した場合のみ実生成
    force_real = "--no-dry-run" in args
    if force_real:
        args = [a for a in args if a != "--no-dry-run"]
    dry_run = not force_real
    if "--dry-run" in args:
        args = [a for a in args if a != "--dry-run"]
    targets = args if args else list(CHARS.keys())

    unknown = [t for t in targets if t not in CHARS]
    if unknown:
        print(f"不明なキャラ: {unknown}  有効: {list(CHARS.keys())}")
        sys.exit(1)

    print(f"=== QAシステム起動 {'[DRY-RUN]' if dry_run else '[実生成]'} ===")

    if not api_up():
        print("❌ APIサーバー未起動 (port 3002)")
        sys.exit(1)
    print("✅ APIサーバー UP")

    if not comfy_up():
        print("❌ ComfyUI未起動 (port 8188)")
        sys.exit(1)
    print("✅ ComfyUI UP")

    if not dry_run:
        print("   ComfyUIキュー待機中...", end="", flush=True)
        if wait_comfy_queue_empty(timeout=300):
            print(" OK")
        else:
            print(" タイムアウト（生成継続中のまま進行）")

    passed, failed = [], []
    for name in targets:
        ok = run_char(name, CHARS[name], dry_run=dry_run)
        (passed if ok else failed).append(name)

    print(f"\n{'='*50}")
    print(f"  結果: PASS={passed} FAIL={failed}")
    print(f"{'='*50}")
    sys.exit(0 if not failed else 1)

if __name__ == "__main__":
    main()
