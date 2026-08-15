import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

async function crawl(url: string): Promise<string> {
  try {
    const res = await fetch(`https://r.jina.ai/${url}`, {
      headers: { Accept: 'text/plain' },
      signal: AbortSignal.timeout(8000),
    })
    return (await res.text()).slice(0, 3000)
  } catch {
    return ''
  }
}

async function searchReviews(hotelName: string): Promise<string> {
  const queries = [
    `https://www.jalan.net/yado/search/?kwd=${encodeURIComponent(hotelName)}`,
    `https://travel.rakuten.co.jp/keyword/${encodeURIComponent(hotelName)}/`,
    `https://www.tripadvisor.jp/Search?q=${encodeURIComponent(hotelName)}`,
  ]

  const results = await Promise.allSettled(
    queries.map(url => crawl(url))
  )

  return results
    .map((r, i) => {
      if (r.status === 'fulfilled' && r.value.length > 100) {
        const labels = ['じゃらん', '楽天トラベル', 'TripAdvisor']
        return `【${labels[i]}】\n${r.value}`
      }
      return ''
    })
    .filter(Boolean)
    .join('\n\n')
    .slice(0, 6000)
}

export async function POST(request: Request) {
  const { input } = await request.json()
  if (!input?.trim()) return NextResponse.json({ error: 'input required' }, { status: 400 })

  const isUrl = input.trim().startsWith('http')

  // クロール
  let crawlText = ''
  let reviewText = ''

  if (isUrl) {
    crawlText = await crawl(input.trim())
  }

  // 口コミ検索（じゃらん・楽天トラベル・TripAdvisor）
  const hotelName = isUrl ? (crawlText.match(/施設名[：:]\s*(.+)/)?.[1] ?? input.trim()) : input.trim()
  reviewText = await searchReviews(hotelName)

  const prompt = `あなたはホテル・旅館向け自動チェックイン機の営業担当アシスタントです。
以下の情報から、このホテルへの最適な営業アプローチを分析してください。

【ホテル情報】
${crawlText ? `サイト内容:\n${crawlText}\n` : `ホテル名/入力: ${hotelName}\n`}

【口コミ・評判情報（じゃらん・楽天トラベル・TripAdvisor）】
${reviewText || '口コミサイトからの取得ができませんでした。ホテル名・地域・業態から推測して分析してください。温泉施設なら日帰り客対応、小規模旅館なら深夜対応、シティホテルならインバウンド対応など、業態に合った課題を推定して回答してください。'}

以下の6パターンから最適なアプローチを1〜2個選び、理由と刺さりポイントを教えてください：
1. 💰 IT補助金全面訴求型
2. 🏨 インバウンド課題共感型
3. 🆚 競合比較・乗り換え訴求型
4. 📊 導入事例・数字訴求型
5. 📋 宿泊名簿・本人確認DX型
6. 🌙 夜間・無人運営訴求型

必ずJSON形式のみで出力してください（前後に説明不要）:
{
  "recommended": ["パターン名（例：💰 IT補助金全面訴求型）"],
  "reason": "このホテルにこのパターンが刺さる理由（2〜3文）",
  "issues": ["口コミ・情報から見えた課題1", "課題2", "課題3"],
  "opening": "受付突破のファーストトーク例（ホテル名・地域・業態・口コミの特徴を反映して専用にカスタマイズすること。必ず以下を含めること：①IT補助金または人手不足補助金が使える旨、②補助金申請から導入まで弊社が全て代行する旨）",
  "tips": "このホテルへの架電で特に注意すべきポイント"
}`

  try {
    const text = await gemini(prompt)
    const jsonMatch = text.match(/\{[\s\S]*\}/)
    if (!jsonMatch) return NextResponse.json({ error: 'AI応答の解析に失敗しました' }, { status: 500 })
    const data = JSON.parse(jsonMatch[0])
    return NextResponse.json({ ok: true, ...data })
  } catch (e) {
    return NextResponse.json({ error: 'AI分析に失敗しました' }, { status: 500 })
  }
}
