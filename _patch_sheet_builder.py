# -*- coding: utf-8 -*-
"""[HEARING_SHEET_BUILDER_V1 2026-10-29]
「ヒアリングシート雛形を、必要なものだけに絞った新規シートとして作らせる」
Gemini用プロンプトを生成するボタンを追加する。

背景: 既存の「🤖 Geminiプロンプト生成」は “お客様への事前準備ナビゲート” 用で、
      シートそのものを作る用途ではなかった。雛形は全機材分の設問が入っているため、
      案件ごとに不要な設問を手で消す作業が発生していた。

あわせて、社内フローチャート
 (ヒアリングシート（ひな形・閲覧用） - （社内用）フローチャート.csv)
と現行判定のズレを修正する:
  - フローには「デイユース」「工事(LAN/電源不可)」「IT導入補助金」の分岐があるが
    現行の hearingSheets には無い → 補助金は判定材料が無いので“確認事項”として出す
  - フロント/事前チェックインは現行 `...(true ? ...)` のベタ追加で reason が形骸化
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_sheetbuilder_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ------------------------------------------------------------------ 1) 判定にフロー準拠の項目を追加
OLD1 = """                    { label: '事前チェックイン', reason: '全物件推奨' },
                    ...(true       ? [{ label: 'フロントチェックイン', reason: '有人対応がある場合' }] : []),
                  ]"""
assert s.count(OLD1) == 1, "anchor1"
NEW1 = """                    { label: '事前チェックイン', reason: '全物件推奨' },
                    { label: 'フロントチェックイン', reason: '有人対応がある場合' },
                    // [HEARING_SHEET_BUILDER_V1] 社内フローチャートにある分岐のうち、
                    //   機材情報だけでは判定できないもの。ヒアリングで確認する前提で候補に出す。
                    { label: 'デイユース', reason: '日帰り利用がある場合（要確認）' },
                    { label: '工事', reason: 'LANケーブル・電源が設置不可の場合（要確認）' },
                    { label: 'IT導入補助金', reason: '補助金を利用する場合（要確認）' },
                  ]"""
s = s.replace(OLD1, NEW1, 1)

# ------------------------------------------------------------------ 2) シート作成用プロンプト + ボタン
OLD2 = """                          return (
                            <div className="flex items-center gap-2 flex-wrap pt-1 border-t border-slate-700/50">
                              <button
                                onClick={() => {
                                  navigator.clipboard.writeText(promptText)"""
assert s.count(OLD2) == 1, "anchor2"

NEW2 = """                          // [HEARING_SHEET_BUILDER_V1 2026-10-29]
                          //   雛形スプレッドシートから「この案件に必要なシートだけ」を抜き出して
                          //   新規シートを作らせるためのプロンプト。
                          //   既存の promptText はお客様向けの準備ナビゲートで用途が別。
                          const sheetPrompt = `あなたはホテル向けスマートチェックインシステム「AdvaNceD IoT」の導入支援担当です。
以下の案件について、ヒアリングシートの雛形から【必要なシートだけ】を抜き出した新しいスプレッドシートを作成してください。

【雛形（閲覧用）】
${TMPL}

【案件情報】
- 会社名: ${it.client_name || '未入力'}
- 設置住所: ${it.install_address || '未入力'}
- 担当者: ${it.contact_name || '未入力'}
- 納品予定日: ${it.delivery_due_date || '未入力'}
- 導入機材: ${equip.map((e: Equipment) => [e.name, e.value].filter(Boolean).join(' ')).join('、') || '未入力'}

【必要なシート（機材構成から自動判定済み）】
${hearingSheets.map((x, i) => `${i + 1}. ${x.label}  ← ${x.reason}`).join('\\n')}

【作成ルール】
1. 上記リストにあるシートだけを含めること。雛形にある他のシートは作らない。
2. シートの順番は上記の番号どおりにすること。
3. 各シートの設問は雛形の文言をそのまま使い、勝手に言い換えたり省略したりしないこと。
4. 「要確認」と書かれたシートは、該当するか不明なため最後にまとめ、
   シート名の先頭に【要確認】を付けること。該当しなければ削除してよい旨を備考に書くこと。
5. 既に判明している下記の情報は、該当セルにあらかじめ記入しておくこと。
${knownInfo.map(k => `   - ${k.label}: ${k.value}`).join('\\n')}
6. 記入が必要なセルは空欄のまま残し、背景色を薄い黄色にして「お客様記入欄」とわかるようにすること。
7. 先頭に「表紙」シートを作り、会社名・住所・担当者・納品予定日・導入機材・各シートの一覧を記載すること。

【出力】
作成したスプレッドシートのURLを教えてください。
もしスプレッドシートを直接作成できない場合は、シートごとに表形式（Markdown）で出力してください。`

                          return (
                            <div className="flex items-center gap-2 flex-wrap pt-1 border-t border-slate-700/50">
                              <button
                                onClick={() => {
                                  navigator.clipboard.writeText(sheetPrompt)
                                    .then(() => alert('\\u2705 シート作成プロンプトをコピーしました！\\n\\nGemini ( https://gemini.google.com ) に貼り付けてください。\\n必要な' + hearingSheets.length + 'シートだけの新規スプレッドシートを作成します。'))
                                    .catch(() => alert('コピー失敗。手動でコピーしてください。'))
                                }}
                                className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white text-xs rounded-lg font-bold transition-colors"
                                title="雛形から必要なシートだけを抜き出した新規スプレッドシートをGeminiに作らせます"
                              >
                                📝 必要シートだけ作成（{hearingSheets.length}枚）
                              </button>
                              <button
                                onClick={() => {
                                  navigator.clipboard.writeText(promptText)"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
