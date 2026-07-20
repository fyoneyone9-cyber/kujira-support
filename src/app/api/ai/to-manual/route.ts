import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { content, title } = await request.json()
    if (!content) return NextResponse.json({ error: 'content required' }, { status: 400 })

    const prompt = `以下はSlackのやり取りです。これを社内マニュアルに変換してください。

タイトル: ${title || '(なし)'}

---
${content.slice(0, 8000)}
---

以下の形式で、誰でも再現できるマニュアルとして出力してください：

## マニュアルタイトル
（簡潔なタイトル）

## 対象
（誰向けのマニュアルか）

## 概要
（何をするマニュアルか）

## 手順
1. 
2. 
3. 
（具体的なステップを番号付きで）

## 注意事項
（ハマりやすいポイント、なければ省略）

## 関連情報
（関連するシステム・ツール・URLなど、なければ省略）`

    const result = await gemini(prompt)

    // タイトルも抽出
    const titleMatch = result.match(/## マニュアルタイトル\n(.+)/)
    const suggestedTitle = titleMatch?.[1]?.trim() ?? title ?? 'マニュアル'

    return NextResponse.json({ manual: result, suggestedTitle })
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'AI error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
