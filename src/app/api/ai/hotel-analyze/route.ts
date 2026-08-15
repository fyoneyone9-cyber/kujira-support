import { NextResponse } from 'next/server'
import { companyContext } from '@/lib/company'

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
            generationConfig: { maxOutputTokens: 16384, temperature: 0.3 },
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
  const prompt = `あなたはホテル向け自動チェックイン機（AdvaNceD IoT）の営業担当AIです。
施設情報をもとに最適な営業アプローチと各STEPのトークをJSON形式のみで出力してください。

${companyContext()}

【施設名】${hotelName}
【収集情報】${reviewInfo.slice(0, 3000)}

6パターンから優先度順に1〜3個選択（recommendedは優先度順）:
1.💰IT補助金全面訴求型 2.🏨インバウンド課題共感型 3.🆚競合比較型 4.📊導入事例訴求型 5.📋宿泊名簿DX型 6.🌙夜間・無人運営型

以下のJSON形式のみで出力（説明文・コードブロック不要）:
{"recommended":["パターン名"],"reason":"刺さる理由2〜3文","issues":["AIが見つけた具体的課題1","課題2","課題3"],"tips":"架電注意ポイント","steps":{"step1":"【受付突破】架電者=株式会社デバイスエージェンシーの米山。短く・自信を持って・目的をぼかす（補助金活用の件など）。禁止：情報収集していたところ/困っているのでは/締め切り煽り/ご案内があって/ご連絡いたしました。最後は必ず「ご支配人様か、ご担当者様はいらっしゃいますでしょうか？」","step2":"【担当者第一声＋ヒアリング】米山固定。口コミ・収集情報から見つけた課題（issuesの内容）を踏まえた共感の一声から入り、そのままヒアリング質問につなげる。例：「実は○○についてお客様の声を拝見しまして…実際のところ、夜間対応やスタッフの負担はいかがでしょうか？」のように、AIが見つけた課題を具体的に質問に組み込む","step3":"※step2に統合済み（空文字列でOK）","step4":"【アポ取り】課題が確認できた場合。解決策＋補助金活用＋代行の強みを組み合わせてアポ獲得","step4b":"【情報置き】課題なし・今は不要の場合。資料送付・次回架電につなぐトーク"},"opening":"step1と同内容"}`

  try {
    const text = await gemini(prompt)
    // ```json ... ``` ブロックも含めて抽出
    const jsonMatch = text.match(/```json\s*([\s\S]*?)```/) || text.match(/(\{[\s\S]*\})/)
    const jsonStr = jsonMatch?.[1] ?? jsonMatch?.[0]
    if (!jsonStr) {
      console.error('JSON not found in response:', text.slice(0, 500))
      return NextResponse.json({ error: 'AI応答の解析に失敗しました' }, { status: 500 })
    }
    let data: Record<string, unknown>
    try {
      data = JSON.parse(jsonStr)
    } catch (parseErr) {
      console.error('JSON parse error:', parseErr, jsonStr.slice(0, 300))
      return NextResponse.json({ error: 'AI応答のJSON解析に失敗しました' }, { status: 500 })
    }
    if (!data.opening && (data.steps as Record<string, string>)?.step1) {
      data.opening = (data.steps as Record<string, string>).step1
    }
    return NextResponse.json({ ok: true, ...data })
  } catch (e) {
    console.error('hotel-analyze error:', e)
    return NextResponse.json({ error: `AI分析に失敗しました: ${e instanceof Error ? e.message : String(e)}` }, { status: 500 })
  }
}
