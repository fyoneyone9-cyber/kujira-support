import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { content } = await request.json()
    if (!content) return NextResponse.json({ error: 'content required' }, { status: 400 })

    const prompt = `あなたはサポート担当者のアシスタントです。
以下は顧客から届いたメールです。要点を整理して日本語で要約してください。

---
${content.slice(0, 8000)}
---

以下の形式で出力してください。

## 📧 差出人・件名
（メール本文から読み取れる差出人名・件名。不明な場合は「記載なし」）

## 📌 要件・依頼内容
（顧客が何を求めているか、何を伝えてきたかを3〜5文で要約）

## ❗ 問題・困っていること
（顧客が抱えている問題や課題を箇条書きで記載。なければ「特になし」）
- 

## ✅ 必要な対応
（このメールに対してすべき対応を箇条書きで記載）
- 

## ⏰ 緊急度・優先度
（緊急・高・中・低のいずれかを判断して、その理由も一言で）

## 💬 推奨返信ポイント
（返信する際に盛り込むべきポイントを箇条書きで）
- `

    const result = await gemini(prompt)
    return NextResponse.json({ summary: result })
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'AI error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
