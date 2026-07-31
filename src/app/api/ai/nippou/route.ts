import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { content } = await request.json()
    if (!content) return NextResponse.json({ error: 'content required' }, { status: 400 })

    const prompt = `あなたは日報作成アシスタントです。
以下はSlackのやり取りです。このやり取りから、社内提出用の日報【業務内容】セクションを作成してください。

---
${content.slice(0, 8000)}
---

以下のルールに従って出力してください：

1. 業務内容を箇条書きで列挙する
2. 各業務に所要時間（例: 2.0h）を付ける
3. 合計時間が実労働時間（8.0h）になるように調整する
4. 業務内容は簡潔かつ具体的に（1行）
5. 余計な説明・前置き・マークダウン装飾は一切不要
6. 出力形式は以下のとおり厳守：

【業務内容】
- 業務A 2.0h
- 業務B 3.0h
- 業務C 3.0h

合計：8.0h`

    const result = await gemini(prompt)
    return NextResponse.json({ nippou: result })
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'AI error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
