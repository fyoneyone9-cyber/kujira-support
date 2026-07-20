import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { content, title } = await request.json()
    if (!content) return NextResponse.json({ error: 'content required' }, { status: 400 })

    const prompt = `以下はSlackのやり取りです。日本語で要約してください。

タイトル: ${title || '(なし)'}

---
${content.slice(0, 8000)}
---

以下の形式で出力してください：

## 概要
（2〜3文で何のやり取りか）

## 判明した問題・課題
（箇条書き、なければ「なし」）

## 解決策・対応内容
（箇条書き、なければ「なし」）

## 次のアクション
（箇条書き、なければ「なし」）`

    const result = await gemini(prompt)
    return NextResponse.json({ summary: result })
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'AI error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
