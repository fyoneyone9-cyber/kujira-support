import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. useRefをimportに追加
content = content.replace(
    "import { useState, useCallback } from 'react'",
    "import { useState, useCallback, useRef, useEffect } from 'react'"
)

# 2. 音声認識の状態変数をaiPattern状態の後に追加
content = content.replace(
    "  const [aiPattern, setAiPattern] = useState<string>('yoneyama')",
    """  const [aiPattern, setAiPattern] = useState<string>('yoneyama')

  // 音声認識
  const [isListening, setIsListening] = useState(false)
  const recognitionRef = useRef<any>(null)

  const startListening = useCallback(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SpeechRecognition) { alert('このブラウザは音声認識に対応していません（Chrome推奨）'); return }
    const recog = new SpeechRecognition()
    recog.lang = 'ja-JP'
    recog.continuous = false
    recog.interimResults = true
    recog.onstart = () => setIsListening(true)
    recog.onresult = (e: any) => {
      const transcript = Array.from(e.results).map((r: any) => r[0].transcript).join('')
      setAiInput(transcript)
      if (e.results[e.results.length - 1].isFinal) {
        setIsListening(false)
        fetchAiSuggestions(transcript, aiPattern)
      }
    }
    recog.onerror = () => setIsListening(false)
    recog.onend = () => setIsListening(false)
    recognitionRef.current = recog
    recog.start()
  }, [aiPattern, fetchAiSuggestions])

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop()
    setIsListening(false)
  }, [])"""
)

# 3. AI切り返しブロックを切り取って切り返しナビの直後に移動
# まずAIブロックを特定して取得
ai_start_marker = "\n          {/* AI切り返し */}"
ai_end_marker = "\n          </div>\n\n          {/* キーワードで切り返しを検索 */}"

ai_start = content.find(ai_start_marker)
ai_end = content.find(ai_end_marker)
if ai_start < 0 or ai_end < 0:
    print("ERROR: AI block markers not found")
    print("ai_start:", ai_start, "ai_end:", ai_end)
else:
    ai_block = content[ai_start:ai_end]
    print("AI block found, length:", len(ai_block))

    # AIブロックを元の場所から削除
    content = content[:ai_start] + content[ai_end:]

    # マイクボタンをAIブロックのinputに追加（既存のinputの後に追加）
    old_mic = '''              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}'''
    new_mic = '''              <button
                onClick={isListening ? stopListening : startListening}
                className={`px-4 py-4 rounded-xl text-xl font-bold transition-all flex-shrink-0 ${isListening ? 'bg-red-600 hover:bg-red-500 text-white animate-pulse' : 'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600'}`}
                title={isListening ? '音声認識停止' : 'マイクで入力'}>
                {isListening ? '⏹️' : '🎙️'}
              </button>
              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}'''
    ai_block = ai_block.replace(old_mic, new_mic)

    # 音声認識中のメッセージをerrorメッセージの前に追加
    old_err = "            {aiError && "
    new_err = """            {isListening && <div className="flex items-center gap-2 bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-base text-red-300 animate-pulse">🎙️ 音声認識中... 相手の声を聞かせてください</div>}
            {aiError && """
    ai_block = ai_block.replace(old_err, new_err)

    # 切り返しナビブロックの終わり（</div>の後）を探して直後に挿入
    nav_end_marker = "\n\n          {/* 米山パターン — トークスクリプト */}"
    nav_end = content.find(nav_end_marker)
    if nav_end < 0:
        print("ERROR: nav_end marker not found")
    else:
        # AIブロックを切り返しナビの直後、米山パターンの前に挿入
        content = content[:nav_end] + "\n" + ai_block + content[nav_end:]
        print("AI block moved successfully")

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("saved, lines:", content.count('\n'))
