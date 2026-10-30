# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_LOG_V1 2026-10-29] PayPay申請の有無と日付を記録・表示する。

要望:「PayPay申請済みの有無コマに表示して。ありの場合いつ申請したかなど」

PayPay は契約に1ヶ月半かかるため、いつ申請したかが重要。
申請していないと納期に間に合わない。

保存先 (dashboard_todos):
  paypay_applied_at  申請日 (YYYY-MM-DD)
  paypay_mid         加盟店ID（取得できたら）
  paypay_apply_memo  備考

いずれも dashboard_todos なので再取込で消えない。
同一現場なら同じ申請なので SIBLING_SYNC の対象にする。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_ppapply_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

ANCHOR = """                                <div className="flex items-center gap-1.5 flex-wrap">
                                  <span className="text-sm text-rose-300 font-bold">📨 PayPay利用申請:</span>"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = """                                {/* [PAYPAY_APPLY_LOG_V1 2026-10-29] 申請の有無と日付。
                                    PayPayは契約に1ヶ月半かかるので、いつ申請したかが納期に直結する。 */}
                                {(() => {
                                  const td = it.dashboard_todos || {}
                                  const at = (td['paypay_applied_at'] as string) || ''
                                  const mid = (td['paypay_mid'] as string) || ''
                                  const memo = (td['paypay_apply_memo'] as string) || ''
                                  const today = () => new Date().toISOString().slice(0, 10)
                                  // 申請から何日経ったか（1ヶ月半=45日が目安）
                                  let days = -1
                                  if (at) {
                                    const d = new Date(at)
                                    if (!isNaN(d.getTime())) {
                                      days = Math.floor((Date.now() - d.getTime()) / 86400000)
                                    }
                                  }
                                  return (
                                    <div className={`mb-1.5 rounded px-2 py-1.5 border-2 ${
                                      at ? 'bg-emerald-950/30 border-emerald-600/60'
                                         : 'bg-amber-950/30 border-amber-600/60'}`}>
                                      <div className="flex items-center gap-2 flex-wrap">
                                        <span className="text-sm font-bold">PayPay申請</span>
                                        {at ? (
                                          <>
                                            <span className="text-sm px-2 py-0.5 rounded bg-emerald-600 text-white font-bold">
                                              ✅ 申請済
                                            </span>
                                            <span className="text-sm text-slate-200">
                                              {at}
                                              {days >= 0 && (
                                                <span className={days >= 45 ? 'text-emerald-400 ml-1' : 'text-amber-300 ml-1'}>
                                                  （{days}日経過{days < 45 ? ` / 目安45日まであと${45 - days}日` : ' ・完了見込み'}）
                                                </span>
                                              )}
                                            </span>
                                          </>
                                        ) : (
                                          <span className="text-sm px-2 py-0.5 rounded bg-amber-600 text-white font-bold">
                                            ⚠ 未申請
                                          </span>
                                        )}
                                        <button onClick={() => {
                                          const v = prompt(
                                            'PayPayを申請した日を入力してください（YYYY-MM-DD）\\n空にすると「未申請」に戻します',
                                            at || today())
                                          if (v === null) return
                                          saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', v.trim())
                                        }}
                                          className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                          {at ? '✏ 日付を変更' : '📅 申請日を記録'}
                                        </button>
                                        {!at && (
                                          <button onClick={() => saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', today())}
                                            className="text-sm px-2 py-0.5 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                            ✅ 今日申請した
                                          </button>
                                        )}
                                      </div>
                                      {at && (
                                        <div className="mt-1 flex items-center gap-2 flex-wrap text-sm">
                                          <span className="text-slate-400">加盟店ID(MID):</span>
                                          <span className="text-slate-100 font-mono">{mid || '－'}</span>
                                          <button onClick={() => {
                                            const v = prompt('PayPayの加盟店ID(MID)を入力してください', mid)
                                            if (v === null) return
                                            saveTodoKey(it.id, it.dashboard_todos, 'paypay_mid', v.trim())
                                          }}
                                            className="px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">
                                            ✏
                                          </button>
                                          {memo && <span className="text-slate-400">／ {memo}</span>}
                                          <button onClick={() => {
                                            const v = prompt('備考（進捗や連絡内容など）', memo)
                                            if (v === null) return
                                            saveTodoKey(it.id, it.dashboard_todos, 'paypay_apply_memo', v.trim())
                                          }}
                                            className="px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">
                                            📝 備考
                                          </button>
                                        </div>
                                      )}
                                    </div>
                                  )
                                })()}
                                <div className="flex items-center gap-1.5 flex-wrap">
                                  <span className="text-sm text-rose-300 font-bold">📨 PayPay利用申請:</span>"""
s = s.replace(ANCHOR, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
