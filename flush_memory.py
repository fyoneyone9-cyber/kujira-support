import sys, os
sys.stdout.reconfigure(encoding="utf-8")

path = r"C:\Users\fyone\AppData\Roaming\Genspark Claw\users\ab54bf68-d5d4-409b-83d4-8b036308c046\workspace\memory\2026-10-22.md"

with open(path, encoding="utf-8") as f:
    existing = f.read()

if "07:50" in existing:
    print("既に追記済み")
    sys.exit(0)

addition = """

---

## 2026-10-22 07:50 メモリフラッシュ追記

### char_prompt_lock バグ修正（確定・api_server_3001.py L24446）
- 根本原因: panel.get("char_prompt") or panel.get("base_prompt") がダッシュボードの送る prompt キーを見ていなかった
- 症状: outfit_reinject_strがあるシーンでchar_prompt_lockが空 → _char_anchor="" → Tifa/Aerithのキャラ名がpositiveに未反映
- 修正: panel.get("prompt") をフォールバックに追加（3番目）
- 確認: python self_check.py logcheck → positiveにTifa Lockhartが入っているか確認

### 恒久対策実装（2026-10-22 07:36〜07:45）
- ログ見ずに推測回答 → self_check.py logcheck: 最終プロンプト・CHAR_PROMPT_MISSING・diagnosticsを1発確認
- char_prompt_lock空でも気づかない → CHAR_PROMPT_GUARD_V1: api_server L24489後、空なら_char_prompt_guard.logに記録
- LOGボタンに出ない → _diagnose_prompt診断ルール9: CHAR_PROMPT_MISSINGを自動検出
- pre/post前に前回エラー見落とし → agent_sanity_check(): pre/post実行時に毎回強制チェック
- 動作確認が口約束 → self_check.py post 全PASS必須。PASSなし=納品禁止
- キャラoutfits重複追加 → auto_fix_dashboard.py ルール1〜4: 構文破壊を自動検知修正
- MEMORY.mdにミス恒久対策ログセクション追加済み

### char_kaizo_nichijou3_aerith outfits重複バグ（修正済み）
- 症状: S3エアリスがUIに出ない
- 根本: push定義内にoutfitsフィールドが2つ存在(30シーン x2) → ブラウザがオブジェクト末尾を認識できず
- 修正: バックアップから復元 → ブラケットカウントで正確な1つ目outfits末尾を特定 → 2つ目outfitsを切除 → });で正しく閉じる
- 確認: post_check PASS・outfits数=1・label数=30
- version: 1792442807

### 口約束をコードで強制する原則（確定ルール）
- ミス発生 → ログで根本原因特定 → コードで自動検知/防止 → MEMORY.mdに記録 → SOUL.mdも更新
- 反省文・口約束は不要。コードだけが恒久対策
"""

with open(path, "a", encoding="utf-8") as f:
    f.write(addition)
print("追記OK")
