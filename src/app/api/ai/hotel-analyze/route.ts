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
    const text = await res.text()
    return text.length > 100 ? text.slice(0, 2500) : ''
  } catch {
    return ''
  }
}

async function searchReviews(hotelName: string): Promise<string> {
  const enc = encodeURIComponent(hotelName)
  const queries = [
    { label: 'じゃらん',         url: `https://www.jalan.net/yado/search/?kwd=${enc}` },
    { label: '楽天トラベル',      url: `https://travel.rakuten.co.jp/keyword/${enc}/` },
    { label: 'TripAdvisor',      url: `https://www.tripadvisor.jp/Search?q=${enc}` },
    { label: 'Google Maps',      url: `https://www.google.com/maps/search/${enc}` },
    { label: '一休.com',         url: `https://www.ikyu.com/search/?pname=${enc}` },
    { label: 'るるぶトラベル',    url: `https://travel.rurouby.co.jp/search/?keyword=${enc}` },
    { label: 'Yahoo!トラベル',   url: `https://travel.yahoo.co.jp/search?kw=${enc}` },
    { label: 'ホテル公式サイト検索', url: `https://r.jina.ai/https://www.google.com/search?q=${enc}+口コミ+チェックイン+フロント+評判&hl=ja` },
  ]

  const results = await Promise.allSettled(queries.map(q => crawl(q.url)))

  return results
    .map((r, i) => {
      if (r.status === 'fulfilled' && r.value.length > 100) {
        return `【${queries[i].label}】\n${r.value}`
      }
      return ''
    })
    .filter(Boolean)
    .join('\n\n')
    .slice(0, 8000)
}

export async function POST(request: Request) {
  const { input } = await request.json()
  if (!input?.trim()) return NextResponse.json({ error: 'input required' }, { status: 400 })

  const isUrl = input.trim().startsWith('http')

  let crawlText = ''
  if (isUrl) {
    crawlText = await crawl(input.trim())
  }

  const hotelName = isUrl
    ? (crawlText.match(/施設名[：:]\s*(.+)/)?.[1] ?? input.trim())
    : input.trim()

  const reviewText = await searchReviews(hotelName)

  const prompt = `あなたはホテル・旅館向け自動チェックイン機の営業担当アシスタントです。
以下の情報から、このホテルへの最適な営業アプローチを分析し、各ステップ専用のカスタムトークを生成してください。

【ホテル情報】
${crawlText ? `サイト内容:\n${crawlText}\n` : `ホテル名/入力: ${hotelName}\n`}

【口コミ・評判情報（じゃらん・楽天・TripAdvisor・一休・Google Maps等）】
${reviewText || '口コミ取得不可。ホテル名・地域・業態（温泉施設なら日帰り対応、小規模旅館なら深夜対応、シティホテルならインバウンドなど）から課題を推定してください。'}

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
  "reason": "このホテルにこのパターンが刺さる理由（2〜3文）",
  "issues": ["口コミ・情報から見えた課題1", "課題2", "課題3"],
  "tips": "このホテルへの架電で特に注意すべきポイント",
  "steps": {
    "step1": "【STEP1 受付突破】このホテル専用トーク。必ず①IT補助金または人手不足補助金が使える旨②補助金申請から導入まで弊社が全て代行する旨を含める",
    "step2": "【STEP2 担当者への第一声】このホテルの課題・業態に合わせた共感トーク（口コミの特徴や地域性を反映）",
    "step3": "【STEP3 ヒアリング】このホテルに刺さりそうな課題を引き出す質問トーク",
    "step4": "【STEP4 課題あり→アポ取り】このホテル専用のアポ獲得トーク",
    "step4b": "【STEP4' 課題なし→情報置き】このホテル専用の資料送付・次回架電につなぐトーク"
  },
  "opening": "step1と同じ内容（後方互換用）"
}`

  try {
    const text = await gemini(prompt)
    const jsonMatch = text.match(/\{[\s\S]*\}/)
    if (!jsonMatch) return NextResponse.json({ error: 'AI応答の解析に失敗しました' }, { status: 500 })
    const data = JSON.parse(jsonMatch[0])
    // 後方互換
    if (!data.opening && data.steps?.step1) data.opening = data.steps.step1
    return NextResponse.json({ ok: true, ...data })
  } catch (e) {
    return NextResponse.json({ error: 'AI分析に失敗しました' }, { status: 500 })
  }
}
