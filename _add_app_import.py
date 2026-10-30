# -*- coding: utf-8 -*-
"""[APPLICATION_IMPORT_V1 2026-10-29] 申込書の取り込みUIを追加する。

⚠ 重要: CSV由来の機材構成(equipment列)には一切触らない。
  申込書は「追加情報」として dashboard_todos に保存する。
  → 再取込で消えない / CSVの情報も消さない

保存先 (すべて dashboard_todos):
  app_facility     施設名（これまで住所で代用していた）
  app_rooms        客室数
  app_contact      申込書上の担当者名
  app_tel          担当者電話
  app_email        担当者メール
  app_due          納品希望日
  app_billing      請求書送付先
  app_client_addr  契約者住所
  app_equips       申込書の機材構成(JSON) ※参考情報。CSVは上書きしない
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_appimport_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

ANCHOR = """                              {/* [CLIENT_EMAIL_V1 2026-10-29] お客様メールアドレス。"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = """                              {/* [APPLICATION_IMPORT_V1 2026-10-29] 申込書(.xlsx)の取り込み。
                                  ⚠ CSV由来の機材構成は上書きしない。dashboard_todos に追加情報として保存する。 */}
                              {(() => {
                                const td = it.dashboard_todos || {}
                                const got = !!td['app_facility'] || !!td['app_rooms']
                                return (
                                  <div className="w-full mb-2 bg-indigo-950/30 border border-indigo-800/50 rounded-lg px-2.5 py-2">
                                    <div className="flex items-center gap-2 flex-wrap">
                                      <span className="text-sm text-indigo-300 font-bold">📄 申込書から取り込み:</span>
                                      <label className="text-sm px-2.5 py-1 rounded bg-indigo-700 hover:bg-indigo-600 text-white font-bold cursor-pointer transition-colors">
                                        📥 申込書(.xlsx)を選ぶ
                                        <input type="file" accept=".xlsx" className="hidden"
                                          onChange={async e => {
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
                                              // お客様メールが未入力なら申込書の値を入れる
                                              if (d.email && !td['client_email']) patch['client_email'] = d.email
                                              let n = 0
                                              for (const [k, v] of Object.entries(patch)) {
                                                await saveTodoKey(it.id, it.dashboard_todos, k, v)
                                                n++
                                              }
                                              const eq = Object.entries(d.equips || {})
                                                .map(([k, v]) => `${k}×${v}`).join(' / ')
                                              alert(`✅ 申込書を取り込みました（${n}項目）\\n\\n` +
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
                                          }} />
                                      </label>
                                      {got && <span className="text-xs text-emerald-400">✓ 取込済</span>}
                                    </div>
                                    {got && (
                                      <div className="mt-1.5 text-xs text-slate-300 flex flex-wrap gap-x-3 gap-y-0.5">
                                        {td['app_facility'] ? <span>🏨 {String(td['app_facility'])}</span> : null}
                                        {td['app_rooms'] ? <span>🛏 {String(td['app_rooms'])}室</span> : null}
                                        {td['app_contact'] ? <span>👤 {String(td['app_contact'])}</span> : null}
                                        {td['app_tel'] ? <span>📞 {String(td['app_tel'])}</span> : null}
                                        {td['app_due'] ? <span>📅 希望 {String(td['app_due'])}</span> : null}
                                      </div>
                                    )}
                                    <p className="text-xs text-slate-500 mt-1">
                                      施設名・客室数・担当者・納品希望日などを取り込みます（CSVの機材構成はそのまま）
                                    </p>
                                  </div>
                                )
                              })()}
                              {/* [CLIENT_EMAIL_V1 2026-10-29] お客様メールアドレス。"""
s = s.replace(ANCHOR, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
