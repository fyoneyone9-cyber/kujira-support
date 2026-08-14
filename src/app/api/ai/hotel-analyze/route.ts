import { NextResponse } from 'next/server'
import { GoogleGenerativeAI } from '@google/generative-ai'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

const GEMINI_KEYS = [
  process.env.GEMINI_API_KEY_1!,
  process.env.GEMINI_API_KEY_2!,
  process.env.GEMINI_API_KEY_3!,
].filter(Boolean)

async function crawl(url: string): Promise<string> {
  try {
    const res = await fetch(`https://r.jina.ai/${url}`, {
      headers: { Accept: 'text/plain' },
      signal: AbortSignal.timeout(8000),
    })
    return (await res.text()).slice(0, 4000)
  } catch {
    return ''
  }
}

export async function POST(request: Request) {
  const { input } = await request.json()
  if (!input?.trim()) return NextResponse.json({ error: 'input required' }, { status: 400 })

  const isUrl = input.startsWith('http')

  // クロール
  let crawlText = ''
  let reviewText = ''

  if (isUrl) {
    crawlText = await crawl(input)
  }

  // 口コミ（Google検索ベース）
  const hotelName = isUrl ? input : input.trim()
  const reviewUrl = `https://www.google.com/search?q=${encodeURIComponent(hotelName + ' 口コミ 評判 フロント チェックイン')}&hl=ja`
  reviewText = await crawl(reviewUrl)

  const prompt = `あなたはホテル・旅館向け自動チェックイン機の営業担当アシスタントです。
以下の情報から、このホテルへの最適な営業アプローチを分析してください。

【ホテル情報】
${crawlText ? `サイト内容:\n${crawlText}\n` : `ホテル名: ${hotelName}\n`}

【口コミ・評判情報】
${reviewText || '取得できませんでした'}

以下の6パターンから最適なアプローチを1〜2個選び、理由と刺さりポイントを教えてください：
1. 💰 IT補助金全面訴求型
2. 🏨 インバウンド課題共感型
3. 🆚 競合比較・乗り換え訴求型
4. 📊 導入事例・数字訴求型
5. 📋 宿泊名簿・本人確認DX型
6. 🌙 夜間・無人運営訴求型

出力フォーマット（JSON）:
{
  "recommended": ["パターン番号と名前", ...],
  "reason": "このホテルにこのパターンが刺さる理由（2〜3文）",
  "issues": ["口コミ・情報から見えた課題1", "課題2", "課題3"],
  "opening": "受付突破のファーストトーク例（このホテル専用にカスタマイズ）",
  "tips": "このホテルへの架電で特に注意すべきポイント"
}`

  for (const key of GEMINI_KEYS) {
    try {
      const genai = new GoogleGenerativeAI(key)
      const model = genai.getGenerativeModel({ model: 'gemini-1.5-flash' })
      const result = await model.generateContent(prompt)
      const text = result.response.text()
      const jsonMatch = text.match(/\{[\s\S]*\}/)
      if (!jsonMatch) continue
      const data = JSON.parse(jsonMatch[0])
      return NextResponse.json({ ok: true, ...data })
    } catch {
      continue
    }
  }

  return NextResponse.json({ error: 'AI分析に失敗しました' }, { status: 500 })
}
