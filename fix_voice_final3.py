import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

ai_block_start = 562      # 0-indexed (line 563)
keyword_block_start = 631  # 0-indexed (line 633, 2行前がdiv開始)
yoneyama_block_start = 470 # 0-indexed (line 471)

# AIブロック抽出
ai_block_lines = lines[ai_block_start:keyword_block_start]
ai_block_text = ''.join(ai_block_lines)

# マイクボタン追加
old_btn = '              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}'
new_btn = (
    '              <button\n'
    '                onClick={isListening ? stopListening : startListening}\n'
    '                className={`px-4 py-4 rounded-xl text-xl transition-all flex-shrink-0 ${isListening ? \'bg-red-600 text-white animate-pulse\' : \'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600\'}`}\n'
    '                title={isListening ? \'\u505c\u6b62\' : \'\u30de\u30a4\u30af\u5165\u529b\'}>\n'
    '                {isListening ? \'\u23f9\ufe0f\' : \'\U0001f399\ufe0f\'}\n'
    '              </button>\n'
    '              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}'
)
ai_block_text = ai_block_text.replace(old_btn, new_btn, 1)

# 音声認識中メッセージ追加
old_err = '            {aiError && '
new_err = (
    '            {isListening && <div className="flex items-center gap-2 bg-red-950/40 border border-red-700/40 rounded-xl p-4 mb-4 text-base text-red-300 animate-pulse">'
    '\U0001f399\ufe0f \u97f3\u58f0\u8a8d\u8b58\u4e2d\u2026 \u76f8\u624b\u306e\u58f0\u3092\u805e\u304b\u305b\u3066\u304f\u3060\u3055\u3044'
    '</div>}\n'
    '            {aiError && '
)
ai_block_text = ai_block_text.replace(old_err, new_err, 1)

new_ai_block_lines = ai_block_text.splitlines(keepends=True)

# 新しい行リスト: AIブロックを元の場所から削除し、米山パターンの前に挿入
# 1. AIブロックを削除
lines_without_ai = lines[:ai_block_start] + lines[keyword_block_start:]

# 2. 米山パターンの位置調整（AIブロック削除でずれる）
ai_block_len = keyword_block_start - ai_block_start
new_yoneyama_pos = yoneyama_block_start  # AIブロックは米山パターンより後ろにあったのでずれなし

print(f"AI block length: {ai_block_len} lines")
print(f"Inserting before line {new_yoneyama_pos+1}: {lines_without_ai[new_yoneyama_pos][:60]}")

# 3. 米山パターンの前にAIブロックを挿入
final_lines = lines_without_ai[:new_yoneyama_pos] + ['\n'] + new_ai_block_lines + ['\n'] + lines_without_ai[new_yoneyama_pos:]

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)
print(f"Saved, total lines: {len(final_lines)}")

# 4. importにuseRefとuseEffectを追加
with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "import { useState, useCallback } from 'react'",
    "import { useState, useCallback, useRef } from 'react'"
)

# 音声認識state/refをaiPattern定義の後に追加
old_pattern = "  const [aiPattern, setAiPattern] = useState<string>('yoneyama')\n"
new_pattern = (
    "  const [aiPattern, setAiPattern] = useState<string>('yoneyama')\n\n"
    "  // \u97f3\u58f0\u8a8d\u8b58\n"
    "  const [isListening, setIsListening] = useState(false)\n"
    "  const recognitionRef = useRef<any>(null)\n\n"
    "  const startListening = useCallback(() => {\n"
    "    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition\n"
    "    if (!SR) { alert('\u3053\u306e\u30d6\u30e9\u30a6\u30b6\u306f\u97f3\u58f0\u8a8d\u8b58\u306b\u5bfe\u5fdc\u3057\u3066\u3044\u307e\u305b\u3093\uff08Chrome\u63a8\u5968\uff09'); return }\n"
    "    const recog = new SR()\n"
    "    recog.lang = 'ja-JP'\n"
    "    recog.continuous = false\n"
    "    recog.interimResults = true\n"
    "    recog.onstart = () => setIsListening(true)\n"
    "    recog.onresult = (e: any) => {\n"
    "      const transcript = Array.from(e.results).map((r: any) => r[0].transcript).join('')\n"
    "      setAiInput(transcript)\n"
    "      if (e.results[e.results.length - 1].isFinal) {\n"
    "        setIsListening(false)\n"
    "        fetchAiSuggestions(transcript, aiPattern)\n"
    "      }\n"
    "    }\n"
    "    recog.onerror = () => setIsListening(false)\n"
    "    recog.onend = () => setIsListening(false)\n"
    "    recognitionRef.current = recog\n"
    "    recog.start()\n"
    "  }, [aiPattern, fetchAiSuggestions])\n\n"
    "  const stopListening = useCallback(() => {\n"
    "    recognitionRef.current?.stop()\n"
    "    setIsListening(false)\n"
    "  }, [])\n"
)
content = content.replace(old_pattern, new_pattern, 1)

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("State/ref added, done!")
