# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_LOG_V3 2026-10-30] PayPay申請に「不要」を追加する。

指摘:「不要が抜けてる」
  PayPayを導入しない案件のほうが多いのに、
  「未申請」としか出ないので全件が要対応に見えてしまう。

状態を3つにする:
  未申請 (オレンジ)  … 対応が必要
  申請済 (緑)        … 日付・MID・備考を記録
  不要   (グレー)    … この案件ではPayPayを使わない

保存先: dashboard_todos.paypay_not_needed = '1'
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_ppnn_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """                                  const at = (td['paypay_applied_at'] as string) || ''
                                  const mid = (td['paypay_mid'] as string) || ''
                                  const memo = (td['paypay_apply_memo'] as string) || ''"""
assert s.count(OLD) == 1, "anchor1: %d" % s.count(OLD)
NEW = """                                  const at = (td['paypay_applied_at'] as string) || ''
                                  const mid = (td['paypay_mid'] as string) || ''
                                  const memo = (td['paypay_apply_memo'] as string) || ''
                                  // [V3] PayPayを使わない案件のほうが多いので「不要」を用意する
                                  const nn = !!td['paypay_not_needed']"""
s = s.replace(OLD, NEW, 1)

# 枠の色を3状態に
OLD2 = """                                    <div className={`mb-1.5 rounded px-2 py-1.5 border-2 ${at ? 'bg-emerald-950/40 border-emerald-600/60' : 'bg-amber-950/40 border-amber-600/60'}`}>"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """                                    <div className={`mb-1.5 rounded px-2 py-1.5 border-2 ${
                                      nn ? 'bg-slate-900/40 border-slate-600/50'
                                      : at ? 'bg-emerald-950/40 border-emerald-600/60'
                                           : 'bg-amber-950/40 border-amber-600/60'}`}>"""
s = s.replace(OLD2, NEW2, 1)

# バッジとボタン
OLD3 = """                                        {at ? (
                                          <>
                                            <span className="text-sm px-2 py-0.5 rounded bg-emerald-600 text-white font-bold">✅ 申請済</span>"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """                                        {nn ? (
                                          <>
                                            <span className="text-sm px-2 py-0.5 rounded bg-slate-600 text-white font-bold">－ 不要</span>
                                            <span className="text-sm text-slate-400">この案件ではPayPayを使いません</span>
                                            <button onClick={() => saveTodoKey(it.id, it.dashboard_todos, 'paypay_not_needed', '')}
                                              className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                              ↩ 戻す
                                            </button>
                                          </>
                                        ) : at ? (
                                          <>
                                            <span className="text-sm px-2 py-0.5 rounded bg-emerald-600 text-white font-bold">✅ 申請済</span>"""
s = s.replace(OLD3, NEW3, 1)

# 未申請時に「不要」ボタンを足す
OLD4 = """                                        {!at && (
                                          <button onClick={() => saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', today())}
                                            className="text-sm px-2 py-0.5 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                            ✅ 今日申請した
                                          </button>
                                        )}"""
assert s.count(OLD4) == 1, "anchor4"
NEW4 = """                                        {!at && !nn && (
                                          <>
                                            <button onClick={() => saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', today())}
                                              className="text-sm px-2 py-0.5 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                              ✅ 今日申請した
                                            </button>
                                            <button onClick={() => saveTodoKey(it.id, it.dashboard_todos, 'paypay_not_needed', '1')}
                                              className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-300 font-bold">
                                              － 不要
                                            </button>
                                          </>
                                        )}"""
s = s.replace(OLD4, NEW4, 1)

# 「不要」のときは日付変更ボタンも隠す
OLD5 = """                                        <button onClick={() => {
                                          const v = prompt('PayPayを申請した日を入力してください（YYYY-MM-DD）\\n空にすると「未申請」に戻します', at || today())
                                          if (v === null) return
                                          saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', v.trim())
                                        }} className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                          {at ? '✏ 日付を変更' : '📅 申請日を記録'}
                                        </button>"""
assert s.count(OLD5) == 1, "anchor5"
NEW5 = """                                        {!nn && (
                                          <button onClick={() => {
                                            const v = prompt('PayPayを申請した日を入力してください（YYYY-MM-DD）\\n空にすると「未申請」に戻します', at || today())
                                            if (v === null) return
                                            saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', v.trim())
                                          }} className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                            {at ? '✏ 日付を変更' : '📅 申請日を記録'}
                                          </button>
                                        )}"""
s = s.replace(OLD5, NEW5, 1)

# 詳細行は申請済のときだけ
s = s.replace("""                                      {at && (
                                        <div className="mt-1 flex items-center gap-2 flex-wrap text-sm">""",
              """                                      {at && !nn && (
                                        <div className="mt-1 flex items-center gap-2 flex-wrap text-sm">""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
