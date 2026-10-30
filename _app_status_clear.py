# -*- coding: utf-8 -*-
"""[APPLICATION_IMPORT_V3 2026-10-29] 取り込み済みか一目で分かるようにする。

指摘:「取り込み済みかどうかわからん」
  ✓取込済 の小さなバッジだけで、未取込のときは何も出ていなかった。

対策:
  ・未取込 = 枠をオレンジにして「⚠ 未取込」を大きく表示
  ・取込済 = 枠を緑にして「✅ 取込済」+ 取り込んだ内容を一覧表示
  ・取込日時も記録して表示する
  ・再取り込みボタンの文言も状態で変える
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_appstat_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

start = s.index("{/* [APPLICATION_IMPORT_V1 2026-10-29] 申込書(.xlsx)の取り込み。")
end = s.index("{/* [CLIENT_EMAIL_V1 2026-10-29] お客様メールアドレス。")

NEW = """{/* [APPLICATION_IMPORT_V3 2026-10-29] 申込書(.xlsx)の取り込み。
                                  ⚠ CSV由来の機材構成は上書きしない。dashboard_todos に追加情報として保存する。 */}
                              {(() => {
                                const td = it.dashboard_todos || {}
                                const S = (k: string) => (td[k] as string) || ''
                                const got = !!S('app_facility') || !!S('app_rooms') || !!S('app_contact')
                                const at = S('app_imported_at')

                                const handle = async (e: React.ChangeEvent<HTMLInputElement>) => {
                                  const f = e.target.files?.[0]
                                  if (!f) return
                                  try {
                                    const fd = new FormData()
                                    fd.append('file', f)
                                    const res = await fetch('/api/delivery/parse-application', { method: 'POST', body: fd })
                                    if (!res.ok) { alert('読み取りに失敗しました: ' + res.status); return }
                                    const d = await res.json()
                                    const patch: Record<string, string> = {}
                                    if (d.facility) patch['app_facility'] = d.facility
                                    if (d.rooms) patch['app_rooms'] = d.rooms
                                    if (d.contact) patch['app_contact'] = d.contact
                                    if (d.tel) patch['app_tel'] = d.tel
                                    if (d.email) patch['app_email'] = d.email
                                    if (d.due) patch['app_due'] = d.due
                                    if (d.billingAddress) patch['app_billing'] = d.billingAddress
                                    if (d.clientAddress) patch['app_client_addr'] = d.clientAddress
                                    if (d.siteAddress) patch['app_site_addr'] = d.siteAddress
                                    if (d.equips) patch['app_equips'] = JSON.stringify(d.equips)
                                    if (d.email && !S('client_email')) patch['client_email'] = d.email
                                    patch['app_imported_at'] = new Date().toISOString().slice(0, 16).replace('T', ' ')
                                    for (const [k, v] of Object.entries(patch)) {
                                      await saveTodoKey(it.id, it.dashboard_todos, k, v)
                                    }
                                    const eq = Object.entries(d.equips || {}).map(([k, v]) => `${k}×${v}`).join(' / ')
                                    alert(`✅ 申込書を取り込みました\\n\\n` +
                                      `施設名: ${d.facility || '-'}\\n` +
                                      `客室数: ${d.rooms || '-'}室\\n` +
                                      `担当者: ${d.contact || '-'}\\n` +
                                      `電話:   ${d.tel || '-'}\\n` +
                                      `メール: ${d.email || '-'}\\n` +
                                      `納品日: ${d.due || '-'}\\n\\n` +
                                      `申込書の機材: ${eq || '-'}\\n` +
                                      `※CSVの機材構成は変更していません`)
                                  } catch (err) {
                                    alert('取り込みに失敗しました: ' + err)
                                  } finally {
                                    e.target.value = ''
                                  }
                                }

                                return (
                                  <div className={`w-full mb-2 rounded-lg px-3 py-2.5 border-2 ${
                                    got ? 'bg-emerald-950/30 border-emerald-600/60'
                                        : 'bg-amber-950/30 border-amber-600/60'}`}>
                                    <div className="flex items-center gap-2 flex-wrap">
                                      <span className="text-base font-bold">📄 申込書</span>
                                      {got ? (
                                        <span className="text-base px-2.5 py-0.5 rounded bg-emerald-600 text-white font-bold">
                                          ✅ 取込済
                                        </span>
                                      ) : (
                                        <span className="text-base px-2.5 py-0.5 rounded bg-amber-600 text-white font-bold">
                                          ⚠ 未取込
                                        </span>
                                      )}
                                      {at && <span className="text-sm text-slate-400">（{at}）</span>}
                                      <label className={`text-base px-4 py-2 rounded-lg text-white font-bold cursor-pointer transition-colors shadow ${
                                        got ? 'bg-slate-700 hover:bg-slate-600' : 'bg-indigo-600 hover:bg-indigo-500'}`}>
                                        {got ? '🔄 取り込み直す' : '📥 申込書(.xlsx)を選ぶ'}
                                        <input type="file" accept=".xlsx" className="hidden" onChange={handle} />
                                      </label>
                                    </div>

                                    {got ? (
                                      <div className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-sm text-slate-200">
                                        <span>🏨 施設名: <b>{S('app_facility') || '－'}</b></span>
                                        <span>🛏 客室数: <b>{S('app_rooms') ? S('app_rooms') + '室' : '－'}</b></span>
                                        <span>👤 担当者: <b>{S('app_contact') || '－'}</b></span>
                                        <span>📞 電話: <b>{S('app_tel') || '－'}</b></span>
                                        <span>📧 メール: <b>{S('app_email') || '－'}</b></span>
                                        <span>📅 納品希望: <b>{S('app_due') || '－'}</b></span>
                                      </div>
                                    ) : (
                                      <p className="text-sm text-amber-200 mt-1.5">
                                        申込書を取り込むと、施設名・客室数・担当者・納品希望日が自動で入ります。<br />
                                        <span className="text-slate-400">※ CSVの機材構成は変更しません</span>
                                      </p>
                                    )}
                                  </div>
                                )
                              })()}
                              """
s = s[:start] + NEW + s[end:]
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
