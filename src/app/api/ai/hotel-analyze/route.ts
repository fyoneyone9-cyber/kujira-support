import { NextResponse } from 'next/server'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

const KEYS = [
  process.env.GEMINI_API_KEY_1,
  process.env.GEMINI_API_KEY_2,
  process.env.GEMINI_API_KEY_3,
].filter(Boolean) as string[]

const MODEL = 'gemini-2.5-flash'

// Google検索グラウンディング付きGemini呼び出し
async function geminiWithSearch(prompt: string): Promise<string> {
  let lastError: Error | null = null
  for (const key of KEYS) {
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            tools: [{ google_search: {} }],
            generationConfig: { maxOutputTokens: 8192 },
          }),
        }
      )
      if (res.status === 429 || res.status === 503) {
        lastError = new Error(`rate_limit: ${res.status}`)
        continue
      }
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error?.message ?? `HTTP ${res.status}`)
      }
      const data = await res.json()
      return data.candidates?.[0]?.content?.parts?.[0]?.text ?? ''
    } catch (e) {
      if (e instanceof Error && e.message.startsWith('rate_limit')) {
        lastError = e; continue
      }
      throw e
    }
  }
  throw lastError ?? new Error('Gemini API failed')
}

// 通常Gemini（JSON生成用）
async function gemini(prompt: string): Promise<string> {
  let lastError: Error | null = null
  for (const key of KEYS) {
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: { maxOutputTokens: 8192 },
          }),
        }
      )
      if (res.status === 429 || res.status === 503) {
        lastError = new Error(`rate_limit: ${res.status}`); continue
      }
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error?.message ?? `HTTP ${res.status}`)
      }
      const data = await res.json()
      return data.candidates?.[0]?.content?.parts?.[0]?.text ?? ''
    } catch (e) {
      if (e instanceof Error && e.message.startsWith('rate_limit')) {
        lastError = e; continue
      }
      throw e
    }
  }
  throw lastError ?? new Error('Gemini API failed')
}

// フォールバック①: Jina経由クロール
async function jinaFetch(url: string): Promise<string> {
  try {
    const res = await fetch(`https://r.jina.ai/${url}`, {
      headers: { Accept: 'text/plain' },
      signal: AbortSignal.timeout(7000),
    })
    const text = await res.text()
    return text.length > 150 ? text.slice(0, 2500) : ''
  } catch { return '' }
}

// フォールバック②: DuckDuckGo instant answer API
async function duckduckgoSearch(query: string): Promise<string> {
  try {
    const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_redirect=1&no_html=1`
    const res = await fetch(url, { signal: AbortSignal.timeout(6000) })
    const data = await res.json()
    const parts = [
      data.Abstract,
      data.Answer,
      ...(data.RelatedTopics ?? []).slice(0, 5).map((t: { Text?: string }) => t.Text ?? ''),
    ].filter(Boolean)
    return parts.join('\n').slice(0, 2000)
  } catch { return '' }
}

export async function POST(request: Request) {
  const { input } = await request.json()
  if (!input?.trim()) return NextResponse.json({ error: 'input required' }, { status: 400 })

  const hotelName = input.trim()

  // Step1: 3段階フォールバックで口コミ・施設情報を収集
  let reviewInfo = ''

  // 方法①: Gemini Google検索グラウンディング（最強・リアルタイム）
  try {
    reviewInfo = await geminiWithSearch(
      `「${hotelName}」という宿泊施設について、以下の情報をWeb検索して日本語でまとめてください：
・施設の種類・規模・客室数・立地・特徴
・じゃらん・楽天トラベル・TripAdvisor・Google・一休などの口コミ・評判（チェックイン・フロント対応・スタッフ・待ち時間に関するものを重点的に）
・インバウンド客の多さ・夜間・深夜チェックインの対応状況・スタッフ人手不足に関する情報
できるだけ具体的に、口コミの内容も引用してまとめてください。`
    )
  } catch { /* fall through */ }

  // 方法②: Jina並列クロール（じゃらん・楽天・TripAdvisor）
  if (!reviewInfo || reviewInfo.length < 100) {
    const enc = encodeURIComponent(hotelName)
    const jinaTargets = [
      { label: 'じゃらん', url: `https://www.jalan.net/yado/search/?kwd=${enc}` },
      { label: '楽天トラベル', url: `https://travel.rakuten.co.jp/keyword/${enc}/` },
      { label: 'TripAdvisor', url: `https://www.tripadvisor.jp/Search?q=${enc}` },
      { label: 'Yahoo!トラベル', url: `https://travel.yahoo.co.jp/search?kw=${enc}` },
    ]
    const results = await Promise.allSettled(jinaTargets.map(t => jinaFetch(t.url)))
    reviewInfo = results
      .map((r, i) => r.status === 'fulfilled' && r.value ? `【${jinaTargets[i].label}】\n${r.value}` : '')
      .filter(Boolean).join('\n\n').slice(0, 5000)
  }

  // 方法③: DuckDuckGo instant answer
  if (!reviewInfo || reviewInfo.length < 100) {
    reviewInfo = await duckduckgoSearch(`${hotelName} 口コミ 評判 チェックイン`)
  }

  // Step2: 分析・トーク生成
  const prompt = `あなたはホテル・旅館向け自動チェックイン機の営業担当アシスタントです。
以下の施設情報・口コミ情報をもとに、最適な営業アプローチと各ステップのカスタムトークを生成してください。

【施設名】${hotelName}

【Web検索で収集した施設情報・口コミ】
${reviewInfo}

6パターンから最適アプローチを優先度順（1位から）に1〜3個選び、各ステップのカスタムトークを生成してください。recommendedは必ず優先度の高い順に並べること：
1. 💰 IT補助金全面訴求型
2. 🏨 インバウンド課題共感型
3. 🆚 競合比較・乗り換え訴求型
4. 📊 導入事例・数字訴求型
5. 📋 宿泊名簿・本人確認DX型
6. 🌙 夜間・無人運営訴求型

必ずJSON形式のみで出力（前後に説明不要）:
{
  "recommended": ["パターン名"],
  "reason": "このホテルにこのパターンが刺さる理由（口コミの具体的な内容を引用しながら2〜3文）",
  "issues": ["口コミ・情報から見えた具体的な課題1", "課題2", "課題3"],
  "tips": "このホテルへの架電で特に注意すべきポイント",
  "steps": {
    "step1": "【STEP1 受付突破のみ】推奨パターン全てを組み合わせた1本の受付突破トーク。架電者は必ず「株式会社デバイスエージェンシーの米山」固定。プレースホルダー禁止。①IT補助金または人手不足補助金が使える旨②補助金申請から導入まで弊社が全て代行する旨を自然に盛り込む。絶対禁止：「情報が見当たらない」「困っているのではないか」「お困りごとがあるのではないか」など。あくまで業界トレンドや補助金締め切りを理由に架電する形にする。「ご連絡いたしました」禁止→「ご連絡させていただきました」を使う。トークの最後は必ず「ご支配人様か、ご担当者様はいらっしゃいますでしょうか？」で締める",
    "step2": "【STEP2 担当者への第一声】架電者は「米山」固定。推奨パターン全ての訴求を組み合わせた共感トーク。口コミの具体的な内容を反映する",
    "step3": "【STEP3 ヒアリング】推奨パターン全てに対応する課題を引き出せる質問トーク",
    "step4": "【STEP4 課題あり→アポ取り】推奨パターン全ての解決策を組み合わせたアポ獲得トーク",
    "step4b": "【STEP4' 課題なし→情報置き】推奨パターン全ての訴求を盛り込んだ資料送付・次回架電トーク"
  },
  "opening": "step1と同じ内容（後方互換用）"
}`

  try {
    const text = await gemini(prompt)
    const jsonMatch = text.match(/\{[\s\S]*\}/)
    if (!jsonMatch) return NextResponse.json({ error: 'AI応答の解析に失敗しました' }, { status: 500 })
    const data = JSON.parse(jsonMatch[0])
    if (!data.opening && data.steps?.step1) data.opening = data.steps.step1
    return NextResponse.json({ ok: true, ...data })
  } catch (e) {
    return NextResponse.json({ error: 'AI分析に失敗しました' }, { status: 500 })
  }
}
