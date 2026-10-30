# -*- coding: utf-8 -*-
"""[HEARING_SHEET_BUILDER_V3 2026-10-29] シート名を雛形の正解リストに合わせる。

検証 _verify_sheet_names.py / _check_flow_names.py の結果:
  フローチャートと必須確認①が指す遷移先 = 雛形に存在すべきシート(15種、両者完全一致):
    必須確認①②③ / PMS / スマートロック / カードキー / シリンダー錠 /
    現金決済 / 端末カード決済 / スマホカード決済 / PayPay決済 /
    プリンタ / ルームタブレット / フロントチェックイン / 事前チェックイン /
    デイユース / 工事 / IT導入補助金

現行コードのバグ:
  1. 🔴「スマートロック①②③」と3枚に分けていたが、フロー上は「スマートロック」1種。
     実ファイルは①②の2枚しか無く、③は存在しない。
     → Geminiに存在しないシートを指示すると勝手に創作してしまう。
     雛形の実体(①②)に合わせて2枚にする。
  2. 🔴 PayPay決済が判定リストから欠落。hasPaypay は計算しているのに
     ラベルが「スマホカード決済」になっており、PayPay決済シートが永久に出なかった。
     スマホカード決済とPayPay決済は雛形上も別シート。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_sheetnames3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                    ...(hasLock2   ? [{ label: 'スマートロック①', reason: 'スマートロックあり' },
                                     { label: 'スマートロック②', reason: 'スマートロックあり' },
                                     { label: 'スマートロック③', reason: 'スマートロックあり' }] : []),
                    ...(hasCard    ? [{ label: 'カードキー',       reason: 'カードキーあり' }] : []),
                    ...(hasCyli    ? [{ label: 'シリンダー錠',     reason: 'シリンダー錠あり' }] : []),
                    ...(hasP400    ? [{ label: '端末カード決済',   reason: 'P400あり' }] : []),
                    ...(hasPaycube ? [{ label: '現金決済',         reason: 'PayCubeあり' }] : []),
                    ...(hasPaypay  ? [{ label: 'スマホカード決済', reason: 'PayPayあり' }] : []),"""
assert s.count(OLD) == 1, "anchor"

NEW = """                    // [HEARING_SHEET_BUILDER_V3 2026-10-29] シート名は雛形の実体に合わせること。
                    //   存在しないシート名を出すと Gemini が勝手に設問を創作する。
                    //   雛形の実シート: スマートロック①② (③は存在しない)
                    ...(hasLock2   ? [{ label: 'スマートロック①', reason: 'スマートロックあり' },
                                     { label: 'スマートロック②', reason: 'スマートロックあり' }] : []),
                    ...(hasCard    ? [{ label: 'カードキー',       reason: 'カードキーあり' }] : []),
                    ...(hasCyli    ? [{ label: 'シリンダー錠',     reason: 'シリンダー錠あり' }] : []),
                    ...(hasP400    ? [{ label: '端末カード決済',   reason: 'P400あり' }] : []),
                    ...(hasPaycube ? [{ label: '現金決済',         reason: 'PayCubeあり' }] : []),
                    // ⚠ スマホカード決済と PayPay決済 は雛形上の別シート。
                    //   V2までは hasPaypay に「スマホカード決済」を割り当てており、
                    //   PayPay決済シートが一度も出力されない不具合になっていた。
                    ...(hasPaypay  ? [{ label: 'PayPay決済',       reason: 'PayPayあり' }] : []),
                    ...(hasSumaho  ? [{ label: 'スマホカード決済', reason: 'スマホ決済あり' }] : []),"""
s = s.replace(OLD, NEW, 1)

# hasSumaho の定義を追加
OLD2 = """                  const hasPaypay  = equip.some(e => /paypay|pay.?pay/i.test(e.name || '')  || /paypay|pay.?pay/i.test(e.value || ''))"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = OLD2 + """
                  // [HEARING_SHEET_BUILDER_V3] スマホカード決済(QR/タッチ等)。雛形では別シート。
                  const SUMAHO_PAT = /スマホカード|スマホ決済|QR決済|タッチ決済|stripe|square/i
                  const hasSumaho  = equip.some(e => SUMAHO_PAT.test(e.name || '') || SUMAHO_PAT.test(e.value || ''))"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
