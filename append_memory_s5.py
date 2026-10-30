import sys
sys.stdout.reconfigure(encoding='utf-8')

mem_path = r'C:\Users\fyone\AppData\Roaming\Genspark Claw\users\ab54bf68-d5d4-409b-83d4-8b036308c046\workspace\memory\2026-10-23.md'

append_text = """
---

## ミス恒久対策: char_prompt フィールド名誤り（2026-10-23）

### ミス内容
- S5キャラ追加スクリプト(`add_s5_chars.py`)で `char_prompt:` フィールドを使った
- サーバーは `prompt:` しか読まない → キャラ情報が全無視 → outfit_promptだけがchar_promptになる
- 同じミスをS4でもやったのに再発した（学習できていなかった）

### 恒久対策（コードで実装済み）
| 対策 | 実装場所 |
|---|---|
| `add_char.py` に `char_prompt` キー検出→即ValueError | `C:\\GensparkClaw\\kujira-support\\add_char.py` `obj_to_js()` |
| 追加後検証スクリプト `verify_char_prompt.py` | `C:\\GensparkClaw\\kujira-support\\verify_char_prompt.py` |

### ルール（次回以降必須）
- **キャラ追加後は必ず `python verify_char_prompt.py <prefix>` を実行してからブラウザリロード**
- dashboard.htmlのJSオブジェクトフィールド名は必ずS4の既存キャラ定義と照合してから書く
- 新しいキャラ追加スクリプトを作るときは `add_char.py` の `obj_to_js()` を流用する（ガード済み）

### 正しいフィールド構造（S4を参照）
```
window.CHAR_TEMPLATES.female.push({
  id: 'char_xxx_yyy',
  label: '表示名',
  age: 'jk',
  prompt: 'キャラ特徴,...',   ← ★ここが prompt: （char_prompt: は絶対NG）
  outfits_ref: 'S0256',
});
```
"""

with open(mem_path, 'a', encoding='utf-8') as f:
    f.write(append_text)
print("追記完了")
