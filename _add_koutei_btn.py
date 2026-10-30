# -*- coding: utf-8 -*-
"""[KOUTEI_XLSX_V1] 工程管理表のダウンロードボタンを追加する。
機材構成から不要な工程行を自動で削る。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_koutei_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

ANCHOR = """                                    <p className="text-[11px] text-slate-500 mt-1">
                                      ※ 添付するもの: ①上の「📥 Excelで作成」のヒアリングシート ②「📎 設置準備PDF」
                                    </p>"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = ANCHOR + """
                                    {/* [KOUTEI_XLSX_V1 2026-10-29] 工程管理表（不要工程を自動削除） */}
                                    <div className="flex items-center gap-1.5 flex-wrap mt-2 pt-2 border-t border-slate-700/50">
                                      <span className="text-[11px] text-slate-400 font-bold">🗂 工程管理表:</span>
                                      <button
                                        onClick={async () => {
                                          try {
                                            const res = await fetch('/api/delivery/koutei-xlsx', {
                                              method: 'POST',
                                              headers: { 'Content-Type': 'application/json' },
                                              body: JSON.stringify({
                                                info: {
                                                  client: it.client_name || '',
                                                  property: it.install_address || '',
                                                  due: it.delivery_due_date || '',
                                                },
                                                flags: {
                                                  pms: hasPms2,
                                                  cardkey: hasCard,
                                                  smartlock: hasLock2,
                                                  keybox: equipItems.some(e => /キーボックス|keybox/i.test(e.name || '')),
                                                  kiosk: equipItems.some(e => /KIOSK|キオスク/i.test((e.name || '') + (e.value || ''))),
                                                  kiosk_desk: equipItems.some(e => /卓上/.test((e.name || '') + (e.value || ''))),
                                                  roomtablet: hasTablet,
                                                  surface: equipItems.some(e => /surface/i.test((e.name || '') + (e.value || ''))),
                                                  tablet: equipItems.some(e => /タブレット/.test(e.name || '')) && !hasTablet,
                                                  p400: hasP400,
                                                  paycube: hasPaycube,
                                                  paypay: hasPaypay,
                                                  sumaho: hasSumaho,
                                                  passport: equipItems.some(e => /パスポート/.test(e.name || '')),
                                                  hojokin: false,
                                                },
                                              }),
                                            })
                                            if (!res.ok) { alert('生成に失敗しました: ' + res.status); return }
                                            const kept = res.headers.get('X-Rows-Kept')
                                            const removed = res.headers.get('X-Rows-Removed')
                                            const blob = await res.blob()
                                            const url = URL.createObjectURL(blob)
                                            const a = document.createElement('a')
                                            a.href = url
                                            a.download = `工程管理_${it.client_name || ''}.xlsx`
                                            document.body.appendChild(a); a.click(); a.remove()
                                            URL.revokeObjectURL(url)
                                            alert(`✅ 工程管理表を作成しました\\n残した工程: ${kept}行 / 不要として削除: ${removed}行`)
                                          } catch (e) {
                                            alert('生成に失敗しました: ' + e)
                                          }
                                        }}
                                        className="text-[11px] px-2 py-1 rounded bg-cyan-700 hover:bg-cyan-600 text-white font-bold transition-colors"
                                        title="この案件の機材構成に無い工程を削除したExcelを作成します">
                                        📥 工程管理表を作成
                                      </button>
                                      <a href="https://docs.google.com/spreadsheets/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/edit?gid=159741708#gid=159741708"
                                        target="_blank" rel="noreferrer"
                                        className="text-[11px] px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors">
                                        📄 原本を開く
                                      </a>
                                      <span className="text-[11px] text-slate-500">
                                        ※ 使わない機材の工程行を自動で削除します
                                      </span>
                                    </div>"""
s = s.replace(ANCHOR, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
