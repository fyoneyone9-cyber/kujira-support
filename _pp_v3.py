# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_LOG_V3 2026-10-30] PayPay申請に「不要」を追加する。

指摘:「不要が抜けてる」
  PayPayを導入しない案件のほうが多いのに「未申請」としか出ず、
  全件が要対応に見えてしまう。

3状態にする:
  ⚠ 未申請 (オレンジ) … 対応が必要
  ✅ 申請済 (緑)      … 日付・MID・備考を記録。45日の進捗も表示
  －  不要   (グレー)  … この案件ではPayPayを使わない
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_ppv3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
L = io.open(P, encoding="utf-8").read().split("\n")

st = None
for i, l in enumerate(L):
    if "PAYPAY_APPLY_LOG_V2" in l:
        st = i
        break
assert st is not None, "開始が見つからない"

# 終端 })()} を探す
en = None
for i in range(st, min(st + 90, len(L))):
    if L[i].strip() == "})()}":
        en = i + 1
        break
assert en is not None, "終端が見つからない"
print("置換範囲: L%d-%d (%d行)" % (st + 1, en, en - st))

I = " " * 30
B = '''{I}{{/* [PAYPAY_APPLY_LOG_V3 2026-10-30] PayPay申請の状態。
{I}    機材名に PayPay が無いため機材欄ではなく常時表示する。
{I}    PayPayは契約に1ヶ月半かかるので、いつ申請したかが納期に直結する。
{I}    使わない案件も多いので「不要」を用意する。 */}}
{I}{{(() => {{
{I}  const td = it.dashboard_todos || {{}}
{I}  const at = (td['paypay_applied_at'] as string) || ''
{I}  const mid = (td['paypay_mid'] as string) || ''
{I}  const memo = (td['paypay_apply_memo'] as string) || ''
{I}  const nn = !!td['paypay_not_needed']
{I}  const today = () => new Date().toISOString().slice(0, 10)
{I}  let days = -1
{I}  if (at) {{
{I}    const dt = new Date(at)
{I}    if (!isNaN(dt.getTime())) days = Math.floor((Date.now() - dt.getTime()) / 86400000)
{I}  }}
{I}  const save = (k: string, v: string) => saveTodoKey(it.id, it.dashboard_todos, k, v)
{I}  return (
{I}    <div className={{`mb-1.5 rounded px-2 py-1.5 border-2 ${{
{I}      nn ? 'bg-slate-900/40 border-slate-600/50'
{I}      : at ? 'bg-emerald-950/40 border-emerald-600/60'
{I}           : 'bg-amber-950/40 border-amber-600/60'}}`}}>
{I}      <div className="flex items-center gap-2 flex-wrap">
{I}        <span className="text-sm font-bold">PayPay申請</span>
{I}
{I}        {{nn && (
{I}          <>
{I}            <span className="text-sm px-2 py-0.5 rounded bg-slate-600 text-white font-bold">－ 不要</span>
{I}            <span className="text-sm text-slate-400">この案件ではPayPayを使いません</span>
{I}            <button onClick={{() => save('paypay_not_needed', '')}}
{I}              className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">↩ 戻す</button>
{I}          </>
{I}        )}}
{I}
{I}        {{!nn && at && (
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
{I}            <button onClick={{() => {{
{I}              const v = prompt('PayPayを申請した日（YYYY-MM-DD）\\n空にすると「未申請」に戻します', at)
{I}              if (v === null) return
{I}              save('paypay_applied_at', v.trim())
{I}            }}}} className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">✏ 日付を変更</button>
{I}          </>
{I}        )}}
{I}
{I}        {{!nn && !at && (
{I}          <>
{I}            <span className="text-sm px-2 py-0.5 rounded bg-amber-600 text-white font-bold">⚠ 未申請</span>
{I}            <button onClick={{() => save('paypay_applied_at', today())}}
{I}              className="text-sm px-2 py-0.5 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">✅ 今日申請した</button>
{I}            <button onClick={{() => {{
{I}              const v = prompt('PayPayを申請した日（YYYY-MM-DD）', today())
{I}              if (v === null || !v.trim()) return
{I}              save('paypay_applied_at', v.trim())
{I}            }}}} className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">📅 日付を指定</button>
{I}            <button onClick={{() => save('paypay_not_needed', '1')}}
{I}              className="text-sm px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-300 font-bold">－ 不要</button>
{I}          </>
{I}        )}}
{I}      </div>
{I}
{I}      {{!nn && at && (
{I}        <div className="mt-1 flex items-center gap-2 flex-wrap text-sm">
{I}          <span className="text-slate-400">加盟店ID:</span>
{I}          <span className="text-slate-100 font-mono">{{mid || '－'}}</span>
{I}          <button onClick={{() => {{
{I}            const v = prompt('PayPayの加盟店ID(MID)', mid)
{I}            if (v === null) return
{I}            save('paypay_mid', v.trim())
{I}          }}}} className="px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">✏</button>
{I}          {{memo && <span className="text-slate-400">／ {{memo}}</span>}}
{I}          <button onClick={{() => {{
{I}            const v = prompt('備考（進捗や連絡内容など）', memo)
{I}            if (v === null) return
{I}            save('paypay_apply_memo', v.trim())
{I}          }}}} className="px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">📝 備考</button>
{I}        </div>
{I}      )}}
{I}    </div>
{I}  )
{I}}})()}}'''.format(I=I)

L[st:en] = B.split("\n")
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("patched OK")
