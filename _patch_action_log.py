# -*- coding: utf-8 -*-
"""[INTEG_ACTION_LOG_V1 2026-10-29]
「要対応（PMS未連携 / スマートロック未連携）」に対して、
いつ・どんなアクションを取ったかを記録するメモ欄を各行の直下に追加する。

要望: 「要対応が出てきた時、どのようなアクションをいつとっているか、メモ欄を近くに追加して欲しい」

設計:
 - 保存先は dashboard_todos（import-csv が触らない安全地帯）。DDL不要。
   キー: integ_log_pms_linked / integ_log_smartlock_linked
 - 単なる自由記述ではなく「日付 + 本文」の履歴として積む。
   いつ取った行動かが後から分かる必要があるため。
 - よくある対応はワンタップで追記できるクイックボタンを置く
   （電話した / メール送った / 先方確認待ち / 設定完了）。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_actionlog_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------- 1) IntegRow を wrapper 化
OLD = """                  const IntegRow = ({ label, field, val }: { label: string; field: 'pms_linked' | 'smartlock_linked'; val: boolean | null | undefined }) => {
                    const warn = val === null && days21 !== null && days21 <= 21 && days21 > 0
                    const over = val === null && days21 !== null && days21 <= 0
                    return (
                      <div className={`flex items-center gap-3 flex-wrap rounded-lg px-3 py-2 ${val === true ? 'bg-green-950/40 border border-green-800' : warn ? 'bg-orange-950/50 border border-orange-700' : 'bg-slate-800/50 border border-slate-700'}`}>"""
assert s.count(OLD) == 1, "anchor1"

NEW = """                  // [INTEG_ACTION_LOG_V1 2026-10-29] 要対応に対する「いつ・何をしたか」の記録。
                  //   保存先は dashboard_todos（import-csvが触らないので再取込で消えない）。
                  const IntegActionLog = ({ field }: { field: 'pms_linked' | 'smartlock_linked' }) => {
                    const logKey = `integ_log_${field}`
                    const log = (it.dashboard_todos?.[logKey] as string) || ''
                    const today = new Date().toISOString().slice(0, 10)
                    const append = (text: string) => {
                      const line = `${today} ${text}`
                      saveTodoKey(it.id, it.dashboard_todos, logKey, log ? `${log}\\n${line}` : line)
                    }
                    return (
                      <div className="mt-1.5 pl-3 border-l-2 border-slate-600 space-y-1">
                        <div className="flex items-center gap-1.5 flex-wrap">
                          <span className="text-[11px] text-slate-400 font-bold">\\u{1F4DD} 対応履歴:</span>
                          {['電話した', 'メール送った', '先方確認待ち', '資料送付', '設定完了'].map(q => (
                            <button key={q} onClick={() => append(q)}
                              className="text-[11px] px-1.5 py-0.5 rounded bg-slate-700 hover:bg-blue-700 text-slate-300 hover:text-white transition-colors"
                              title={`「${today} ${q}」を追記`}>+{q}</button>
                          ))}
                        </div>
                        <textarea
                          defaultValue={log}
                          onBlur={(e) => { if (e.target.value !== log) saveTodoKey(it.id, it.dashboard_todos, logKey, e.target.value) }}
                          rows={log ? Math.min(6, log.split('\\n').length + 1) : 2}
                          placeholder={`例: ${today} 担当者に架電、PMS側の設定待ち`}
                          className="w-full text-xs bg-slate-900/70 border border-slate-700 rounded px-2 py-1 text-slate-200 placeholder-slate-600 focus:border-blue-500 focus:outline-none resize-y"
                        />
                        {log && (
                          <p className="text-[11px] text-slate-500">
                            最終更新: {log.split('\\n').filter(Boolean).slice(-1)[0]?.slice(0, 10) || '-'}
                          </p>
                        )}
                      </div>
                    )
                  }

                  const IntegRow = ({ label, field, val }: { label: string; field: 'pms_linked' | 'smartlock_linked'; val: boolean | null | undefined }) => {
                    const warn = val === null && days21 !== null && days21 <= 21 && days21 > 0
                    const over = val === null && days21 !== null && days21 <= 0
                    return (
                      <div className={`rounded-lg px-3 py-2 ${val === true ? 'bg-green-950/40 border border-green-800' : warn ? 'bg-orange-950/50 border border-orange-700' : 'bg-slate-800/50 border border-slate-700'}`}>
                      <div className="flex items-center gap-3 flex-wrap">"""
s = s.replace(OLD, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("step1 done")
