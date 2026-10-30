# -*- coding: utf-8 -*-
"""[CLIENT_EMAIL_V1 2026-10-29] お客様メールアドレスの入力欄を追加する。

要望: ヒアリングシートの自動入力にメールを使いたいが専用列が無い。
      作業員連絡先から拾う暫定対応だったので、正式な入力欄を作る。

保存先: dashboard_todos.client_email
  → CSV由来の列ではないので再取込で消えない（012の方針に従う）
  → DDL不要
  → SIBLING_SYNC の同期対象に入れる（同じ現場なら担当者は同じはず）
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_email_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# 1) 設定コピーのメール取得元を dashboard_todos.client_email 優先にする
OLD1 = """                                        // メールは専用列が無いので作業員連絡先から拾う
                                        email: (it.worker_contacts || []).map(w => w?.email).find(Boolean) || '',"""
assert s.count(OLD1) == 1, "anchor1"
NEW1 = """                                        // [CLIENT_EMAIL_V1] 手入力したお客様メール優先、無ければ作業員連絡先
                                        email: (it.dashboard_todos?.['client_email'] as string)
                                          || (it.worker_contacts || []).map(w => w?.email).find(Boolean) || '',"""
s = s.replace(OLD1, NEW1, 1)

# 2) 入力欄をヒアリングシート欄の先頭に追加
ANCHOR = """                              {/* [HEARING_XLSX_V1 2026-10-29] Gemini"""
assert s.count(ANCHOR) == 1, "anchor2: %d" % s.count(ANCHOR)
NEW2 = """                              {/* [CLIENT_EMAIL_V1 2026-10-29] お客様メールアドレス。
                                  dashboard_todos に保存するので再取込で消えない。 */}
                              <div className="w-full flex items-center gap-2 mb-2">
                                <span className="text-sm text-slate-400 font-bold whitespace-nowrap">📧 お客様メール:</span>
                                <input
                                  type="email"
                                  defaultValue={(it.dashboard_todos?.['client_email'] as string) || ''}
                                  placeholder="ヒアリングシートに自動入力されます（例: info@example.com）"
                                  onBlur={e => {
                                    const v = e.target.value.trim()
                                    const cur = (it.dashboard_todos?.['client_email'] as string) || ''
                                    if (v !== cur) saveTodoKey(it.id, it.dashboard_todos, 'client_email', v)
                                  }}
                                  className="flex-1 min-w-[220px] text-sm px-2 py-1 bg-slate-900 border border-slate-600 rounded text-slate-100 placeholder-slate-600 focus:border-blue-500 focus:outline-none"
                                />
                                {(it.dashboard_todos?.['client_email'] as string) && (
                                  <span className="text-xs text-emerald-400 whitespace-nowrap">✓ 保存済</span>
                                )}
                              </div>
                              {/* [HEARING_XLSX_V1 2026-10-29] Gemini"""
s = s.replace(ANCHOR, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
