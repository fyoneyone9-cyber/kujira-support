import sys
path = r'C:\Users\fyone\AppData\Roaming\Genspark Claw\users\ab54bf68-d5d4-409b-83d4-8b036308c046\workspace\memory\2026-10-23.md'
append_text = """
## api_server_3001.py バグ修正（2026-10-23夜）

### 修正9: NIPPLE_LACTATION_SEX_V1
- **症状**: 「乳首吸われ」「強制授乳」シーンで `sex=none` → `bare breasts:1.5` がネガに入って胸が隠れる
- **根本原因**: `_W_FORE`（前戯キーワードリスト）に `nipple sucking`/`forced lactation` が未登録
- **修正**: `_W_FORE` に追加 → `sex=foreplay` → `bare breasts` ネガが入らなくなる
- **行番号**: L54044付近（`_W_FORE = (...)` の末尾）

### 修正10: KAIZOU_PENET_OVERRIDE_V1 精度改善
- **症状**: 「膣内異物挿入」シーンで `insertion` 単体ヒット → `male_scene=True` → ふたなり化
- **根本原因**: `KAIZOU_PENET_OVERRIDE_V1` が `_is_penet_real`（`insertion`単体でTrue）を使っていた
- **修正**: ペニス確実キーワードのみの `_is_penet_penis` リストを新設して差し替え
  - 除外: `insertion`単体（異物挿入の可能性）
  - 含む: `penetration`/`penis in vagina`/`vaginal sex`/`anal sex`/`rape`/`forced sex`/`fellatio`等
- **行番号**: L31773付近（KAIZOU_PENET_OVERRIDE_V1ブロック）
- **ログ**: `[KAIZOU_PENET_OVERRIDE_V1] 異物挿入のみ(ペニスなし) → male_scene=False維持`

### 修正11: KREA2_ORAL_PENET_DUO_V1
- **症状**: 「グループ奉仕（oral+penetration）」シーンで `has_duo=False` → solo強制 → 1人しか出ない
- **根本原因**: `KREA2_MULTIMALE_DUO_V1` は `oral sex`/`blowjob` 文字列を探すが、outfitに `oral`単体しかない場合スキップ
- **修正**: `_krea_oral_penet_combo`追加（`oral`+`penetration`同時存在で `has_duo=True`強制）
  + `group service`/`group sex`/`gang rape` 等のキーワードも `_krea_multimale` に追加
- **行番号**: L9635付近（KREA2_MULTIMALE_DUO_V1ブロック）

### 現在のAPIサーバー状態
- **オフライン**（`C:\AI\start.bat` 未起動）
- 修正1〜11がすべて `api_server_3001.py` に書き込み済み・py_compile OK
- start.bat起動後にVF連続生成で動作確認が必要

### 重要な学習
- `_W_FORE` vs `_W_PENET` vs `_W_NUDE`: SEX_STATE_V1の3段階判定。foreplayに入れると `sex=foreplay`、nudeに入れると `sex=nude`（penis=noneだが全裸OK）
- `KAIZOU_PENET_OVERRIDE_V1`の `insertion`除外: 今後「膣内/肛門以外の体腔への異物挿入」シーンは `insertion` だけ使い、ペニスが要るなら `penetration` を明示する
- Redcraft系（redcraftHybridH3Krea2t）はmoody/krea2同系列。cfg=1.5、steps=10、euler_ancestral、beta
"""

with open(path, 'a', encoding='utf-8') as f:
    f.write(append_text)
print("done")
