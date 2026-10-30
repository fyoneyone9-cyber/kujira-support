#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
aerith_debug_runner.py
エアリス生成リクエストを実際のAPIサーバー(port 3002)に投げて
_location_debug.log から Aerith タグの消滅ポイントを特定する。
ComfyUIには接続しない（ダミーモードで実行）。
"""
import sys, io, json, time, os, requests, pathlib, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API = "http://127.0.0.1:3002"
LOG = pathlib.Path(r"C:\AI\ComfyUI\_location_debug.log")

OUTFIT_VALUE = (
    "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),"
    "(Aerith Gainsborough:1.9),(Final Fantasy VII:1.8),(ff7:1.8),"
    "(young woman:1.6),(slender:1.5),(medium breasts:1.5),"
    "22 years old,long brown braided hair,pink ribbon,green eyes,pink dress,"
    "forced to snort white powder, head yanked back, powder forced up nostrils,"
    "eyes watering, coughing violently, resisting hands pinned,"
    "upper body,dim room,eye level,"
    "(drugged high:2.0),(dilated pupils:2.0),(flushed face:1.8),(sweating:1.7),"
    "(heavy breathing:1.6),(euphoric:1.8),(ahegao:1.6),(rolling eyes:1.5),"
    "(drooling excessively:1.7),(trembling violently:1.5),"
    "(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed"
)

PANEL = {
    "char_template_id": "char_kakuseizai_s3_ff_aerith",
    "char_id": "char_kakuseizai_s3_ff_aerith",
    "prompt": OUTFIT_VALUE,
    "outfit_prompt": OUTFIT_VALUE,
    "outfit_label": "00「禁断の粉」",
    "outfit_index": 0,
    "page_idx": 0,
    "panel_idx": 0,
    "style_preset": "moody_krea2_premium",
    "wf_type": "moody_krea2_v7",
    "checkpoint": "moodyKrea2MixUncensoredV8SEGoes_v80_int8.safetensors",
    "penetration_off": True,
    "clothes_off": False,
}

# ログの末尾マーカーを記録
def log_tail_marker():
    if LOG.exists():
        with open(LOG, encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        return len(lines)
    return 0

# 末尾以降の新規ログを取得
def get_new_log(since_line):
    if not LOG.exists():
        return []
    with open(LOG, encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    return lines[since_line:]

# Aerithタグの消滅ポイントを特定
def analyze_log(lines):
    print("\n" + "="*60)
    print("=== Aerith タグ追跡結果 ===")
    print("="*60)
    checkpoints = []
    for i, line in enumerate(lines):
        line = line.rstrip()
        # チェックポイント系
        if any(k in line for k in [
            'FULL_POS_FULL', 'FULL_POS_CHECK', 'CP_BEFORE_USDU',
            'FINAL_SEND_WF6_FULL', 'CHECKPOINT_4', 'REAL_BOOST_AERITH',
            'POSE_PRESET', 'REAL_BOOST:', 'PAIPAN_SYNC',
            'dbg_outfit_injected', 'outfit_reinject_str',
        ]):
            has_aerith = 'aerith' in line.lower() or 'final fantasy' in line.lower() or 'ff7' in line.lower()
            marker = "✅" if has_aerith else "❌"
            print(f"{marker} L{i+1}: {line[:150]}")
            checkpoints.append((i, has_aerith, line[:100]))
    
    # 消滅ポイント特定
    print("\n--- 消滅ポイント分析 ---")
    last_true = None
    first_false = None
    for i, has, line in checkpoints:
        if has:
            last_true = (i, line)
        elif last_true is not None and first_false is None:
            first_false = (i, line)
    
    if last_true and first_false:
        print(f"最後にAerithあり: L{last_true[0]+1} {last_true[1][:80]}")
        print(f"最初にAerithなし: L{first_false[0]+1} {first_false[1][:80]}")
        print(f"\n→ この間でAerithタグが消えています")
    elif last_true and not first_false:
        print("Aerithタグは全チェックポイントで保持されています")
    else:
        print("チェックポイントが取得できませんでした")
    
    return checkpoints

# メイン
def main():
    print("=== エアリス動作確認システム ===")
    print(f"API: {API}")
    print(f"LOG: {LOG}")
    
    # APIサーバー確認
    try:
        r = requests.get(f"{API}/api/health", timeout=3)
        print(f"APIサーバー: UP (status={r.status_code})")
    except Exception as e:
        try:
            r = requests.get(f"{API}/api/version", timeout=3)
            print(f"APIサーバー: UP (version endpoint)")
        except Exception as e2:
            print(f"APIサーバーに接続できません: {e2}")
            print("先に start.bat でAPIサーバーを起動してください")
            return

    # ログのマーカー位置
    marker = log_tail_marker()
    print(f"ログマーカー: {marker}行目から追跡開始")
    
    # 既存生成をクリア（force restart不要）
    print("\ngenerate-panel APIに送信中...")
    
    try:
        r = requests.post(
            f"{API}/api/generate-panel",
            json={
                "panel": PANEL,
                "page_idx": 0,
                "panel_idx": 0,
                "wf_type": "moody_krea2_v7",
                "checkpoint": "moodyKrea2MixUncensoredV8SEGoes_v80_int8.safetensors",
            },
            timeout=120
        )
        print(f"レスポンス: status={r.status_code}")
        if r.status_code == 200:
            resp = r.json()
            print(f"positive_prompt先頭: {resp.get('positive_prompt','')[:200]}")
            has_aerith = 'aerith' in str(resp.get('positive_prompt','')).lower()
            print(f"Aerithタグ in positive_prompt: {'✅' if has_aerith else '❌'}")
        elif r.status_code == 409:
            print("409: 他の生成中。10秒待って再試行...")
            time.sleep(10)
            r = requests.post(
                f"{API}/api/generate-panel",
                json={
                    "panel": PANEL,
                    "page_idx": 0,
                    "panel_idx": 0,
                    "wf_type": "moody_krea2_v7",
                    "checkpoint": "moodyKrea2MixUncensoredV8SEGoes_v80_int8.safetensors",
                },
                timeout=120
            )
            print(f"再試行レスポンス: {r.status_code}")
        else:
            print(f"エラーレスポンス: {r.text[:300]}")
    except Exception as e:
        print(f"リクエストエラー: {e}")
    
    # last-prompt から確認
    print("\n--- /api/last-prompt から確認 ---")
    try:
        r = requests.get(f"{API}/api/last-prompt", timeout=5)
        lp = r.json()
        pos = lp.get('positive_prompt', '')
        has_aerith = 'aerith' in pos.lower() or 'final fantasy' in pos.lower()
        print(f"positive_prompt Aerith: {'✅ あり' if has_aerith else '❌ なし'}")
        print(f"positive_prompt先頭300: {pos[:300]}")
        
        # debug情報
        for k in ['dbg_outfit_injected', 'dbg_real_boost', 'dbg_pose_preset', 'dbg_qr']:
            if k in lp:
                print(f"{k}: {str(lp[k])[:200]}")
    except Exception as e:
        print(f"last-promptエラー: {e}")
    
    # ログ分析
    print("\n--- _location_debug.log 新規エントリ分析 ---")
    time.sleep(1)
    new_lines = get_new_log(marker)
    print(f"新規ログ行数: {len(new_lines)}")
    
    if new_lines:
        analyze_log(new_lines)
    else:
        print("新規ログなし（ログファイルが更新されていません）")
    
    print("\n=== 完了 ===")

if __name__ == '__main__':
    main()
