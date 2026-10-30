# -*- coding: utf-8 -*-
path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ---- JITBOX JSXブロック ----
jitbox_block = """                      {/* JITBOX配送情報（備考にJITBOXが含まれる場合） */}
                      {hasJitbox(it) && (() => {
                        const jit = getJitboxLeadDays(it.install_address)
                        const _today = new Date(); _today.setHours(0,0,0,0)
                        const _due = new Date(it.delivery_due_date); _due.setHours(0,0,0,0)
                        const _deadline = new Date(_due)
                        _deadline.setDate(_deadline.getDate() - jit.days - 1)
                        const deadlineStr = _deadline.toISOString().slice(0,10)
                        const daysToDeadline = Math.ceil((_deadline.getTime()-_today.getTime())/86400000)
                        const isOverdue = daysToDeadline < 0
                        const isUrgent = !isOverdue && daysToDeadline <= 3
                        return (
                          <div className={`flex flex-col gap-2 mt-2 pt-2 border-t ${isOverdue ? 'border-red-500' : isUrgent ? 'border-orange-500' : 'border-slate-700/50'}`}>
                            <div className={`flex flex-col gap-1.5 px-3 py-2 rounded-lg ${isOverdue ? 'bg-red-950/50 border border-red-500' : isUrgent ? 'bg-orange-950/50 border border-orange-500' : 'bg-slate-800/60 border border-slate-700'}`}>
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className="text-lg font-bold text-white">\U0001f69a JITBOX\u914d\u9001\u60c5\u5831\uff08\u5927\u962a\u767a\uff09</span>
                                {isOverdue && <span className="text-sm px-2 py-0.5 rounded-full bg-red-600 text-white font-bold">\u624b\u914d\u671f\u9650\u8d85\u904e\uff01</span>}
                                {isUrgent && <span className="text-sm px-2 py-0.5 rounded-full bg-orange-500 text-white font-bold">\u624b\u914d\u671f\u9650\u307e\u3067{daysToDeadline}\u65e5</span>}
                              </div>
                              <div className="text-base text-slate-300 space-y-0.5">
                                <p>\U0001f4e6 \u6240\u8981\u65e5\u6570\uff1a<strong className="text-white">{jit.days}\u65e5</strong> <span className="text-slate-400 text-sm">\uff08{jit.note}\uff09</span></p>
                                <p>\u23f0 \u624b\u914d\u7de0\u3081\u5207\u308a\uff1a<strong className={isOverdue ? 'text-red-300' : isUrgent ? 'text-orange-300' : 'text-white'}>{deadlineStr}</strong><span className="text-slate-400 ml-2 text-sm">\uff08{isOverdue ? `${-daysToDeadline}\u65e5\u8d85\u904e` : `\u6b8b${daysToDeadline}\u65e5`} \uff0f \u524d\u65e5\u307e\u3067\u306b\u624b\u914d\u5fc5\u8981\uff09</span></p>
                                <p className="text-slate-400 text-sm">\u26a0\ufe0f \u65e5\u795d\u307e\u305f\u304e\u30fb\u96e2\u5cf6\u30fb2\u6642\u9593\u5e45JIT\u6307\u5b9a\u306f\u5225\u9014\u78ba\u8a8d\u3002\u6642\u9593\u5916(18:01\uff5e20:00)\u306f+3,000\u5186\u524d\u5f8c\u3002</p>
                              </div>
                              <button onClick={() => toggleJitboxOrdered(it)} disabled={!!it.locked} className={`self-start text-base px-4 py-1.5 rounded-full font-bold border transition-colors whitespace-nowrap ${it.jitbox_ordered ? 'bg-green-700 border-green-500 text-white' : 'bg-slate-700/60 border-slate-600 text-slate-300 hover:bg-slate-600'} ${it.locked ? 'opacity-50 cursor-not-allowed' : ''}`}>
                                {it.jitbox_ordered ? '\u2705 JITBOX\u624b\u914d\u6e08\u307f' : '\u2610 JITBOX\u624b\u914d\u6e08\u307f\u306b\u3059\u308b'}
                              </button>
                            </div>
                          </div>
                        )
                      })()}

"""

# 管理スプレッドシートボタン追加（工程管理表ボタンの直後）
mgmt_btn_addition = """                      <a
                        href="https://docs.google.com/spreadsheets/d/1FxK4x534LV2sGY54KKtbow1W6iLT0Z_YTzg_R8ba8Go/edit?gid=0#gid=0"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white text-base rounded-lg font-medium transition-colors whitespace-nowrap text-center"
                      >
                        \U0001f4ca \u7ba1\u7406\u30b9\u30d7\u30ec\u30c3\u30c9\u30b7\u30fc\u30c8
                      </a>
"""

# JITBOXブロックの挿入ポイント：確認済みマークブロックの直後
marker = '                      {/* \u30c0\u30c3\u30b7\u30e5\u30dc\u30fc\u30c9\u5074\u30e1\u30e2\uff08CSV\u518d\u53d6\u8fbc\u3057\u3066\u3082\u4fdd\u6301\u3055\u308c\u308b\uff09 */'
if marker in content:
    content = content.replace(marker, jitbox_block + marker, 1)
    print('JITBOX block inserted OK')
else:
    # fallback: textareaの直後
    import re
    # 確認済みマークブロックの文字コード変換
    marker2 = '{/* \u78ba\u8a8d\u6e08\u307f\u30de\u30fc\u30af */'
    if marker2 in content:
        content = content.replace(marker2, jitbox_block + marker2, 1)
        print('JITBOX block inserted at fallback OK')
    else:
        # さらにfallback: min-h の後ろ
        idx = content.find('min-h-[2.2rem]')
        if idx != -1:
            end_of_textarea = content.find('\n                    </div>\n                  </div>', idx)
            if end_of_textarea != -1:
                insert_pt = end_of_textarea + len('\n                    </div>\n                  </div>')
                content = content[:insert_pt] + '\n' + jitbox_block + content[insert_pt:]
                print('JITBOX block inserted at textarea fallback OK')
            else:
                print('ERROR: textarea end not found')
        else:
            print('ERROR: all insertion points failed')

# 工程管理表ボタンを探してその後に管理スプレッドシートボタンを追加
process_btn_end = '                        \U0001f6e0\ufe0f \u5de5\u7a0b\u7ba1\u7406\u8868\n                      </a>\n                      <button\n                        onClick={() => markChecked(it)}'
replacement_end = '                        \U0001f6e0\ufe0f \u5de5\u7a0b\u7ba1\u7406\u8868\n                      </a>\n' + mgmt_btn_addition + '                      <button\n                        onClick={() => markChecked(it)}'

if process_btn_end in content:
    content = content.replace(process_btn_end, replacement_end, 1)
    print('Management spreadsheet button added OK')
else:
    print('ERROR: process_btn_end not found')
    # デバッグ
    idx = content.find('\U0001f6e0\ufe0f \u5de5\u7a0b\u7ba1\u7406\u8868')
    print(f'  kouei button found at: {idx}')
    if idx != -1:
        print(repr(content[idx-50:idx+100]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
