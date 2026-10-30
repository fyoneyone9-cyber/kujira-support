# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_LOG_V1 2026-10-29] PayPay申請の有無と日付を表示する（行指定）。

PayPayは契約に1ヶ月半かかるため、いつ申請したかが納期に直結する。
保存先は dashboard_todos なので再取込で消えない。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_pplog_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
L = io.open(P, encoding="utf-8").read().split("\n")

# L1262 (index 1261) = <div className="flex items-center gap-1.5 flex-wrap">
idx = 1261
assert 'flex items-center gap-1.5 flex-wrap' in L[idx], "mismatch: %r" % L[idx][:80]

I = " " * 32
BLOCK = '''{I}{{/* [PAYPAY_APPLY_LOG_V1 2026-10-29] 申請の有無と日付。
{I}    PayPayは契約に1ヶ月半かかるので、いつ申請したかが納期に直結する。 */}}
{I}{{(() => {{
{I}  const td = it.dashboard_todos || {{}}
{I}  const at = (td['paypay_applied_at'] as string) || ''
{I}  const mid = (td['paypay_mid'] as string) || ''
{I}  const memo = (td['paypay_apply_memo'] as string) || ''
{I}  const today = () => new Date().toISOString().slice(0, 10)
{I}  let days = -1
{I}  if (at) {{
{I}    const dt = new Date(at)
{I}    if (!isNaN(dt.getTime())) days = Math.floor((Date.now() - dt.getTime()) / 86400000)
{I}  }}
{I}  return (
{I}    <div className={{`mb-1.5 rounded px-2 py-1.5 border-2 ${{at ? 'bg-emerald-950/40 border-emerald-600/60' : 'bg-amber-950/40 border-amber-600/60'}}`}}>
{I}      <div className="flex items-center gap-2 flex-wrap">
{I}        <span className="text-sm font-bold">PayPay申請</span>
{I}        {{at ? (
{I}          <>
{I}            <span className="text-sm px-2 py-0.5 rounded bg-emerald-600 text-white font-bold">✅ 申請済</span>
{I}            <span className="text-sm text-slate-200">
{I}              {{at}}
{I}              {{days >= 0 && (
{I}                <span className={{days >= 45 ? 'text-emerald-400 ml-1' : 'text-amber-300 ml-1'}}>
{I}                  （{{days}}日経過{{days < 45 ? ` / 目安45日まであと${{45 - days}}日` : ' ・完了見込み'}}）
{I}                </span>
{I}              )}}
{I}            </span>
{I}          </>
{I}        ) : (
{I}          <span className="text-sm px-2 py-0.5 rounded bg-amber-600 text-white font-bold">⚠ 未申請</span>
{I}        )}}
{I}        <button onClick={{() => {{
{I}          const v = prompt('PayPayを申請した日を入力してください（YYYY-MM-DD）\\n空にすると「未申請」に戻します', at || today())
{I}          if (v === null) return
{I}          saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', v.trim())
{I}        }}}} className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
{I}          {{at ? '✏ 日付を変更' : '📅 申請日を記録'}}
{I}        </button>
{I}        {{!at && (
{I}          <button onClick={{() => saveTodoKey(it.id, it.dashboard_todos, 'paypay_applied_at', today())}}
{I}            className="text-sm px-2 py-0.5 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
{I}            ✅ 今日申請した
{I}          </button>
{I}        )}}
{I}      </div>
{I}      {{at && (
{I}        <div className="mt-1 flex items-center gap-2 flex-wrap text-sm">
{I}          <span className="text-slate-400">加盟店ID:</span>
{I}          <span className="text-slate-100 font-mono">{{mid || '－'}}</span>
{I}          <button onClick={{() => {{
{I}            const v = prompt('PayPayの加盟店ID(MID)を入力してください', mid)
{I}            if (v === null) return
{I}            saveTodoKey(it.id, it.dashboard_todos, 'paypay_mid', v.trim())
{I}          }}}} className="px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">✏</button>
{I}          {{memo && <span className="text-slate-400">／ {{memo}}</span>}}
{I}          <button onClick={{() => {{
{I}            const v = prompt('備考（進捗や連絡内容など）', memo)
{I}            if (v === null) return
{I}            saveTodoKey(it.id, it.dashboard_todos, 'paypay_apply_memo', v.trim())
{I}          }}}} className="px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">📝 備考</button>
{I}        </div>
{I}      )}}
{I}    </div>
{I}  )
{I}}})()}}'''.format(I=I)

L[idx:idx] = BLOCK.split("\n")
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("L%d に挿入" % (idx + 1))
