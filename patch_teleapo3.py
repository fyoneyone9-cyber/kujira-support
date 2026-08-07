import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 各セクションを抽出
def extract_section(content, start_marker, end_marker):
    start = content.find(start_marker)
    end = content.find(end_marker, start)
    if start == -1 or end == -1:
        print(f'ERROR: marker not found. start={start}, end={end}')
        return None, None, None
    return content[start:end], start, end

# セクション境界マーカー
NAVI_END    = '          {/* ── AI切り返しサジェスト (Gemini API) ── */}'
AI_START    = '          {/* ── AI切り返しサジェスト (Gemini API) ── */}'
AI_END      = '          {/* ── メモ欄 ── */}'
MEMO_START  = '          {/* ── メモ欄 ── */}'
MEMO_END    = '          {/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}'
SCRIPT_START = '          {/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}'
SCRIPT_END  = '\n        </div>\n      )}\n\n      {/* ─── TAB: 米山パターン ─── */}'

# 各セクションの内容を取得
ai_section = content[content.find(AI_START):content.find(AI_END)]
memo_section = content[content.find(MEMO_START):content.find(MEMO_END)]
script_section = content[content.find(SCRIPT_START):content.find(SCRIPT_END) + len(SCRIPT_END)]

print(f'AI section: {len(ai_section)} chars, starts at line {content[:content.find(AI_START)].count(chr(10))+1}')
print(f'Memo section: {len(memo_section)} chars, starts at line {content[:content.find(MEMO_START)].count(chr(10))+1}')
print(f'Script section: {len(script_section)} chars, starts at line {content[:content.find(SCRIPT_START)].count(chr(10))+1}')

# scriptセクションを切り取ってnaviの直後・aiサジェストの前に移動
# 現在の順番: ...NAVI_END + AI + MEMO + SCRIPT + </div>)}...
# 新しい順番: ...NAVI_END + SCRIPT(スクリプト+切り返し) + AI + MEMO + </div>)}...

# まずscript_sectionを元の場所から除去（MEMO_ENDからSCRIPT_ENDまで）
old_block = content[content.find(MEMO_END):content.find(SCRIPT_END) + len(SCRIPT_END)]
new_block = '\n        </div>\n      )}\n\n      {/* ─── TAB: 米山パターン ─── */}'

content_without_script = content.replace(old_block, new_block, 1)

# scriptのうちスクリプト+切り返しだけ（</div>)}を除いた部分）
script_only = content[content.find(SCRIPT_START):content.find(SCRIPT_END)]

# NAVI_ENDの直後に挿入
insert_point = NAVI_END
content_final = content_without_script.replace(
    insert_point,
    script_only + '\n\n          ' + insert_point.strip(),
    1
)

print(f'Final lines: {content_final.count(chr(10))}')

with open(FILE, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content_final)
print('Done')
