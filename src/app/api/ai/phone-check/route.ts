import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { phone } = await request.json()
    if (!phone) return NextResponse.json({ error: 'phone required' }, { status: 400 })

    const prompt = `あなたは迷惑電話・詐欺電話の専門家です。
以下の電話番号について、迷惑電話・詐欺電話・営業電話の可能性を判定してください。

電話番号: ${phone}

判定の観点:
- 0120/0800: フリーダイヤル（営業電話に多い）
- 050: IP電話（詐欺に悪用されることがある）
- 国際番号(+1, +44等): 国際詐欺の可能性
- 番号の構成（市外局番の実在性、番号の長さ）
- 一般的に報告されている迷惑電話番号の特徴

以下のJSON形式のみで出力（説明文・コードブロック不要）:
{"verdict":"判定結果（✅ 正常な番号 / ⚠️ 営業電話の可能性あり / 🚨 詐欺・迷惑電話の可能性が高い）","reason":"判断根拠を1〜2文で","recommend":"推奨対応（そのまま対応してOK / 折り返し不要・様子見 / 無視・対応完了 など）"}`

    const text = await gemini(prompt)
    const cleaned = text.replace(/^```json\s*/, '').replace(/\s*```$/, '').trim()
    const data = JSON.parse(cleaned)
    return NextResponse.json(data)
  } catch (e) {
    return NextResponse.json({ error: e instanceof Error ? e.message : 'AI error' }, { status: 500 })
  }
}
