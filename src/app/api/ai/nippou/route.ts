import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { content } = await request.json()
    if (!content) return NextResponse.json({ error: 'content required' }, { status: 400 })

    const prompt = `あなたは日報作成アシスタントです。
以下のSlackのやりとりや業務メモから、日報用の【業務内容】セクションを作成してください。

---
${content.slice(0, 8000)}
---

以下のルールに従って出力してください：

1. 業務内容を箇条書きで列挙する
2. 工数（時間）は一切記載しない
3. 各業務内容は簡潔かつ具体的に（1行）
4. 余計な説明・外枠・マークダウン装飾は一切不要
5. 出力形式は以下のとおり厳守：

【業務内容】
- 業務A
- 業務B
- 業務C`

    const result = await gemini(prompt)
    return NextResponse.json({ nippou: result })
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'AI error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
