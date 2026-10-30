import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
with open(path, encoding='utf-8') as f:
    content = f.read()

# 1) UrlSection の props に saveTodoKey を追加
old_type = "type UrlSectionProps = { it: DeliveryItem; patch: (id: string, u: Record<string, unknown>) => void }"
new_type = "type UrlSectionProps = { it: DeliveryItem; patch: (id: string, u: Record<string, unknown>) => void; saveTodoKey: (id: string, todos: Record<string, unknown> | null | undefined, key: string, val: string) => void }"
if old_type in content:
    content = content.replace(old_type, new_type)
    print("type: OK")
else:
    print("type: NOT FOUND")

# 2) UrlSection 関数シグネチャを更新
old_sig = "function UrlSection({ it, patch }: UrlSectionProps) {"
new_sig = "function UrlSection({ it, patch, saveTodoKey }: UrlSectionProps) {"
if old_sig in content:
    content = content.replace(old_sig, new_sig)
    print("sig: OK")
else:
    print("sig: NOT FOUND")

# 3) fields 定義に skipKey を追加
old_fields = """  const fields: { key: keyof DeliveryItem; label: string; color: string }[] = [
    { key: 'slack_url',         label: 'Slack',      color: 'text-blue-400' },
    { key: 'hubspot_url',       label: 'HubSpot',    color: 'text-orange-400' },
    { key: 'process_sheet_url', label: '工程表',     color: 'text-green-400' },
    { key: 'hearing_sheet_url', label: 'ヒアリング', color: 'text-purple-400' },
  ]"""
new_fields = """  const fields: { key: keyof DeliveryItem; label: string; color: string; alertable?: boolean }[] = [
    { key: 'slack_url',         label: 'Slack',      color: 'text-blue-400',    alertable: true },
    { key: 'hubspot_url',       label: 'HubSpot',    color: 'text-orange-400' },
    { key: 'process_sheet_url', label: '工程表',     color: 'text-green-400',   alertable: true },
    { key: 'hearing_sheet_url', label: 'ヒアリング', color: 'text-purple-400',  alertable: true },
  ]"""
if old_fields in content:
    content = content.replace(old_fields, new_fields)
    print("fields: OK")
else:
    print("fields: NOT FOUND")

# 4) 編集行に「不要」トグルボタンを追加
old_row = """              <div key={f.key} className="flex items-center gap-2">
                <span className={`text-xs font-medium w-24 flex-shrink-0 ${f.color}`}>{f.label}</span>
                <input type="url" defaultValue={v} placeholder="https://"
                  onBlur={(e) => { if (e.target.value !== v) patch(it.id, { [f.key]: e.target.value || null }) }}
                  className="flex-1 px-2 py-0.5 text-xs bg-slate-900 border border-slate-600 rounded text-slate-200 placeholder-slate-600"
                />
                {v && <a href={v} target="_blank" rel="noreferrer" className={`text-xs hover:underline flex-shrink-0 ${f.color}`}>開く</a>}
              </div>"""
new_row = """              <div key={f.key} className="flex items-center gap-2">
                <span className={`text-xs font-medium w-24 flex-shrink-0 ${f.color}`}>{f.label}</span>
                <input type="url" defaultValue={v} placeholder="https://"
                  onBlur={(e) => { if (e.target.value !== v) patch(it.id, { [f.key]: e.target.value || null }) }}
                  className="flex-1 px-2 py-0.5 text-xs bg-slate-900 border border-slate-600 rounded text-slate-200 placeholder-slate-600"
                />
                {v && <a href={v} target="_blank" rel="noreferrer" className={`text-xs hover:underline flex-shrink-0 ${f.color}`}>開く</a>}
                {f.alertable && !v && (
                  <button
                    onClick={() => {
                      const skipKey = `${f.key}_skip`
                      const cur = it.dashboard_todos?.[skipKey]
                      saveTodoKey(it.id, it.dashboard_todos, skipKey, cur ? '' : '1')
                    }}
                    className={`text-xs px-2 py-0.5 rounded font-medium transition-colors flex-shrink-0 ${
                      it.dashboard_todos?.[`${f.key}_skip`] ? 'bg-slate-600 text-slate-300' : 'bg-transparent border border-slate-600 text-slate-500 hover:text-slate-300'
                    }`}
                  >
                    {it.dashboard_todos?.[`${f.key}_skip`] ? '✓ 不要' : '不要'}
                  </button>
                )}
              </div>"""
if old_row in content:
    content = content.replace(old_row, new_row)
    print("row: OK")
else:
    print("row: NOT FOUND")

# 5) アラーム条件に _skip チェックを追加
old_a1 = "if (!it.slack_url) ltWarnings.push('SlackリンクがURLセクションに未登録')"
new_a1 = "if (!it.slack_url && !it.dashboard_todos?.['slack_url_skip']) ltWarnings.push('SlackリンクがURLセクションに未登録')"
if old_a1 in content:
    content = content.replace(old_a1, new_a1)
    print("alarm_slack: OK")
else:
    print("alarm_slack: NOT FOUND")

old_a2 = "if (!it.process_sheet_url) ltWarnings.push('工程表リンクが未登録')"
new_a2 = "if (!it.process_sheet_url && !it.dashboard_todos?.['process_sheet_url_skip']) ltWarnings.push('工程表リンクが未登録')"
if old_a2 in content:
    content = content.replace(old_a2, new_a2)
    print("alarm_process: OK")
else:
    print("alarm_process: NOT FOUND")

old_a3 = "if (!it.hearing_sheet_url) ltWarnings.push('ヒアリングシートリンクが未登録')"
new_a3 = "if (!it.hearing_sheet_url && !it.dashboard_todos?.['hearing_sheet_url_skip']) ltWarnings.push('ヒアリングシートリンクが未登録')"
if old_a3 in content:
    content = content.replace(old_a3, new_a3)
    print("alarm_hearing: OK")
else:
    print("alarm_hearing: NOT FOUND")

# 6) UrlSection 呼び出しに saveTodoKey を渡す
old_call = "<UrlSection it={it} patch={patch} />"
new_call = "<UrlSection it={it} patch={patch} saveTodoKey={saveTodoKey} />"
if old_call in content:
    content = content.replace(old_call, new_call)
    print("call: OK")
else:
    print("call: NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n完了")
