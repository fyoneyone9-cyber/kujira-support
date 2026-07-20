import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { content, title } = await request.json()
    if (!content) return NextResponse.json({ error: 'content required' }, { status: 400 })

    const prompt = `あなたは社内サポートチームのアシスタントです。
以下はSlackのやり取りです。現場で役立つ詳細な分析レポートを日本語で作成してください。

タイトル: ${title || '(なし)'}

---
${content.slice(0, 8000)}
---

以下の形式で、各セクションを必ず埋めて出力してください。「なし」は禁止です。内容が不明な場合は「やり取りから判断できないため要確認」と書いてください。

## 📌 概要
（このやり取りが発生した背景・状況を3〜5文で詳しく説明する）

## ❗ 問題・課題（必須）
（発生した問題や課題を箇条書きで詳細に記載。症状・エラー内容・影響範囲も含める）
- 
- 

## ✅ 回答・解決策（必須）
（問題に対する回答や対応内容を箇条書きで詳細に記載。誰がどう対応したかも含める）
- 
- 

## 📋 今後の対応・ネクストアクション（必須）
（このやり取りを踏まえて、次に何をすべきか具体的なアクションを箇条書きで記載。担当者・期限・確認事項も含める）
- 
- 

## ⚠️ 注意点・ハマりポイント
（同じ問題が再発しないための注意事項、特に気をつけるべき点）
- 

## 🔗 関連システム・ツール
（やり取りに登場したシステム名・ツール名・URL・機器名など）
-`

    const result = await gemini(prompt)
    return NextResponse.json({ summary: result })
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'AI error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
