import { NextRequest, NextResponse } from 'next/server'
import { gemini } from '@/lib/gemini'

export async function POST(req: NextRequest) {
  try {
    const { input, pattern } = await req.json()
    if (!input || typeof input !== 'string') {
      return NextResponse.json({ error: 'input required' }, { status: 400 })
    }

    const systemContext = `
あなたは株式会社デバイスエージェンシーのテレアポ支援AIです。
デバイスエージェンシーは以下の製品を自社開発・販売しています：
- 自動チェックイン機（KIOSK型・タブレット型）
- クラウドスマートロック（暗証番号で開錠）
- ルームタブレット（客室内電話代替）

【製品の強み】
- IT補助金申請を弊社が代行 → KIOSK型が最低48万〜、タブレット型13万〜で導入可能
- シリンダー錠（物理キー）にも対応（キーボックス活用）
- 13か国語対応・パスポートスキャン機能あり（インバウンド対策）
- 自社開発のため完全オーダーメイドカスタマイズ可能
- 使わない期間は月額0円（季節限定利用OK）
- PMS連携実績：ステイシー・スイートブック・ベッド4
- セミナー：毎週水曜11時・金曜13時（無料・Zoom）

【IT補助金の訴求ポイント】
- 中小企業デジタル化補助金・IT導入補助金を活用
- 最大2/3補助で企業負担を大幅削減
- 弊社が申請手続きを全て代行するため手間なし
- 導入後の実質回収期間が大幅短縮

【最新テレアポトレンド】
- 冒頭で「売り込みではない」スタンスを取る（警戒心を下げる）
- ネガティブな本音を先に引き出してから提案（インサイト営業）
- 「IT補助金で実質負担ほぼゼロ」を最初に伝えるのが2025年トレンド
- 「業界スタンダードになりつつある」という流行り訴求
- 同業他社の導入事例を具体的に挙げる
- 「まず情報だけ」の低コミットメント提案

パターン: ${
  pattern === 'yoneyama' ? '米山パターン（IT補助金全面訴求型）— 補助金で実質負担ゼロを前面に出す' :
  pattern === 'price' ? '価格・コスト訴求型 — 月額・季節限定・回収期間でコスパを訴求' :
  pattern === 'inbound' ? 'インバウンド訴求型 — 13か国語対応・パスポートスキャンでインバウンド需要に応える' :
  pattern === 'case' ? '導入事例訴求型 — 同業他社の具体的な導入事例・成果で安心感を与える' :
  pattern === 'urgency' ? '緊急性訴求型 — 補助金締切・競合導入済み・業界スタンダード化で今すぐ感を出す' :
  '米山パターン（IT補助金全面訴求型）'
}
`

    const prompt = `${systemContext}

【相手の発言】
「${input}」

この発言に対して、以下のJSON形式で3つの切り返しトークを生成してください。

{
  "suggestions": [
    {
      "label": "ボタン表示用の短いラベル（10文字以内）",
      "talk": "実際のトーク文（自然な敬語で50〜100文字程度）",
      "point": "このトークのポイント（15文字以内）"
    }
  ]
}

条件：
- IT補助金の訴求を積極的に含める
- デバイスエージェンシーの具体的な製品・価格を活用する
- 相手の懸念に直接応えてから提案につなげる
- JSONのみ返答（説明文不要）`

    const raw = await gemini(prompt)

    // JSONを抽出
    const jsonMatch = raw.match(/\{[\s\S]*\}/)
    if (!jsonMatch) {
      return NextResponse.json({ error: 'parse_error', raw }, { status: 500 })
    }
    const result = JSON.parse(jsonMatch[0])
    return NextResponse.json(result)
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'unknown error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
