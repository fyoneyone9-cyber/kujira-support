import { NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

export async function POST(request: Request) {
  const { title, category, audience } = await request.json()
  if (!title?.trim()) return NextResponse.json({ error: 'タイトルが必要です' }, { status: 400 })

  const isInternal = audience === 'internal'

  const prompt = isInternal
    ? `あなたは業務マニュアル作成の専門家です。
以下のタイトル・カテゴリに基づき、**社内スタッフ向け**の業務マニュアルをマークダウン形式で作成してください。

タイトル：${title}
カテゴリ：${category || '未設定'}

要件：
- 対象：社内スタッフ（業務知識がある前提）
- 専門用語・略語はそのまま使用してOK
- 具体的な手順・注意事項・よくあるミスを含める
- ## 見出し、箇条書き、番号付きリストを活用
- 「担当者は〜する」「確認すること」など業務的な表現
- 分量：400〜800文字程度

マークダウン本文のみ出力してください（前後の説明不要）。`
    : `あなたは顧客向けマニュアル作成の専門家です。
以下のタイトル・カテゴリに基づき、**顧客・エンドユーザー向け**のわかりやすいマニュアルをマークダウン形式で作成してください。

タイトル：${title}
カテゴリ：${category || '未設定'}

要件：
- 対象：IT知識が少ない一般の方
- 専門用語は使わず、やさしい言葉で説明
- 「〜してください」「〜をタップします」など丁寧で親しみやすい表現
- ステップごとに番号付きで説明
- 困ったときの対処法・お問い合わせ先を末尾に追加
- 分量：400〜800文字程度

マークダウン本文のみ出力してください（前後の説明不要）。`

  try {
    const content = await gemini(prompt)
    return NextResponse.json({ ok: true, content })
  } catch {
    return NextResponse.json({ error: 'AI生成に失敗しました' }, { status: 500 })
  }
}
