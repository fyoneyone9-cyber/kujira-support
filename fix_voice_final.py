import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# AIブロック: 563行目付近から始まる（0-indexed: 562）
# キーワード検索ブロック: 633行目（0-indexed: 632）
# まず行番号を正確に特定
ai_div_start = None
keyword_div_start = None
nav_end_line = None  # 切り返しナビの終わり（米山パターン開始の前）

for i, l in enumerate(lines):
    if '{/* AI\u5207\u308a\u8fd4\u3057 */' in l:
        ai_div_start = i
    if '\u30ad\u30fc\u30ef\u30fc\u30c9\u3067\u5207\u308a\u8fd4\u3057' in l:
        keyword_div_start = i - 2  # div開始は2行前
    if '\u7c73\u5c71\u30d1\u30bf\u30fc\u30f3\u2014\u30c8\u30fc\u30af\u30b9\u30af\u30ea\u30d7\u30c8' in l:
        nav_end_line = i - 2  # 米山パターンブロック開始の前

print(f"AI block starts at: {ai_div_start+1 if ai_div_start else 'NOT FOUND'}")
print(f"Keyword block starts at: {keyword_div_start+1 if keyword_div_start else 'NOT FOUND'}")
print(f"Nav end (before yoneyama): {nav_end_line+1 if nav_end_line else 'NOT FOUND'}")

if ai_div_start and keyword_div_start and nav_end_line:
    # AIブロックの終わり = キーワードブロックの1行前
    # AIブロックを取り出す
    # AIブロック開始: ai_div_startの2行前（空行+コメント）
    ai_block_start = ai_div_start  # {/* AI切り返し */}行
    ai_block_end = keyword_div_start  # キーワードdiv開始

    ai_block_lines = lines[ai_block_start:ai_block_end]
    print(f"AI block: lines {ai_block_start+1}-{ai_block_end}")
    print(f"AI block preview: {ai_block_lines[0][:60]}")

    # マイクボタンを追加したAIブロックを作成
    ai_block_text = ''.join(ai_block_lines)

    # マイクボタンをinputとAI提案ボタンの間に追加
    old_btn = '              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}'
    new_btn = '''              <button
                onClick={isListening ? stopListening : startListening}
                className={`px-4 py-4 rounded-xl text-xl transition-all flex-shrink-0 ${isListening ? 'bg-red-600 text-white animate-pulse' : 'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600'}`}
                title={isListening ? '停止' : 'マイク入力'}>
                {isListening ? '\u23f9\ufe0f' : '\U0001f399\ufe0f'}
              </button>
              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}'''
    ai_block_text = ai_block_text.replace(old_btn, new_btn, 1)

    # 認識中メッセージ追加
    old_err = '            {aiError && '
    new_err = '            {isListening && <div className="flex items-center gap-2 bg-red-950/40 border border-red-700/40 rounded-xl p-4 mb-4 text-base text-red-300 animate-pulse">\U0001f399\ufe0f \u97f3\u58f0\u8a8d\u8b58\u4e2d... \u76f8\u624b\u306e\u58f0\u3092\u805e\u304b\u305b\u3066\u304f\u3060\u3055\u3044</div>}\n            {aiError && '
    ai_block_text = ai_block_text.replace(old_err, new_err, 1)

    new_ai_lines = ai_block_text.splitlines(keepends=True)

    # 元のAIブロックを削除し、新しいブロックを切り返しナビの直後に挿入
    # 新しい行リストを構築
    new_lines = (
        lines[:ai_block_start] +       # AIブロック前
        lines[ai_block_end:]            # AIブロック削除（キーワード以降）
    )

    # nav_end_lineは削除後にずれるので調整
    shift = ai_block_end - ai_block_start
    nav_insert = nav_end_line - shift  # 削除分だけずれる

    # 挿入位置を確認
    print(f"Inserting AI block at new line: {nav_insert+1}")
    print(f"Line at insert: {new_lines[nav_insert][:60] if nav_insert < len(new_lines) else 'OUT OF RANGE'}")

    # 挿入
    final_lines = new_lines[:nav_insert] + ['\n'] + new_ai_lines + new_lines[nav_insert:]

    with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    print(f"Saved, total lines: {len(final_lines)}")
