import { NextRequest, NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export async function POST(req: NextRequest) {
  const { emailContent, tone } = await req.json()
  if (!emailContent?.trim()) {
    return NextResponse.json({ error: 'メール本文を入力してください' }, { status: 400 })
  }

  const toneLabel =
    tone === 'formal' ? '丁寧・フォーマル' :
    tone === 'casual' ? '簡潔・カジュアル' :
    '標準的なビジネス'

  const prompt = `あなたはサポート担当の米山です。以下の受信メールに対して、日本語で返信メールを作成してください。

【返信者情報】
- 差出人：米山 文隆（Humitaka Yoneyama）
- メールアドレス：humitaka_yoneyama@device-agency.co.jp
- CC：support@and-iot.jp
- 所属：株式会社デバイスエージェンシー サポート担当

【トーン】${toneLabel}

【受信したメール】
${emailContent}

【出力形式】
返信メール本文のみを出力してください（件名・To/CCヘッダー不要）。
末尾に署名を含めてください：

米山 文隆
株式会社デバイスエージェンシー サポート担当
E-mail: humitaka_yoneyama@device-agency.co.jp`

  try {
    const reply = await gemini(prompt)
    return NextResponse.json({ reply })
  } catch (e) {
    return NextResponse.json({ error: e instanceof Error ? e.message : 'AI生成に失敗しました' }, { status: 500 })
  }
}
