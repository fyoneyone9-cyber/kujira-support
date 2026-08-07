import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

yoneyama_script = r"""
          {/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}
          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <h2 className="text-xl font-bold text-white mb-4">💰 米山パターン — IT補助金訴求型スクリプト</h2>
            <div className="space-y-3">
              {[
                { label: '①', text: '「お忙しいところ恐れ入ります。デバイスエージェンシーの米山でございます。\nホテル・旅館様向けのIT補助金活用でご導入できる自動チェックイン機のご案内でご連絡しました。\nご担当者様かご支配人様はいらっしゃいますでしょうか？」', color: 'blue' },
                { label: '②', text: '「弊社では今、IT補助金の申請を全て弊社が代行する形で、\nKIOSK型が実質48万円〜、タブレット型が13万円〜でご導入いただけています。\n売り込みではなく、補助金活用の情報をお伝えしたくてご連絡しました。」', color: 'yellow' },
                { label: '③ ヒアリング', text: '「インバウンド対応や人手不足など、現在何か運用上の課題はお感じですか？\n例えば、夜間の対応コストや外国語スタッフの確保とか…」', color: 'purple' },
                { label: '④ YES → 提案', text: '「その課題をIT補助金を活用して解決された事例が手元にあります。\n資料だけでもメールでお送りしてもよろしいでしょうか？」', color: 'green' },
                { label: '⑤ NO → 情報だけ提案', text: '「承知しました。IT補助金は毎年申請枠がありますので、\nタイミングが来た時のためだけでも資料をお手元に置いていただければ。\nメールアドレスをお教えいただけますか？今日中にお送りします。」', color: 'slate' },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-4 ${item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' : item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' : item.color === 'purple' ? 'bg-purple-950/40 border border-purple-800/40' : item.color === 'green' ? 'bg-green-950/40 border border-green-800/40' : 'bg-slate-700/50 border border-slate-600/40'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <p className={`text-xs font-bold ${item.color === 'blue' ? 'text-blue-400' : item.color === 'yellow' ? 'text-yellow-400' : item.color === 'purple' ? 'text-purple-400' : item.color === 'green' ? 'text-green-400' : 'text-slate-400'}`}>{item.label}</p>
                    <button onClick={() => copy(item.text, `ym_script_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === `ym_script_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                      {copiedKey === `ym_script_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                  <p className="text-sm text-slate-200 leading-relaxed whitespace-pre-line">{item.text}</p>
                </div>
              ))}
            </div>
          </div>

          {/* ── 断り文句別切り返し（IT補助金訴求） ── */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">🔄 断り文句別 切り返し（IT補助金訴求）</h2>
            <div className="space-y-3">
              {[
                { obj: '「予算がない」「お金がかかる」', res: '「IT補助金を活用していただくと弊社が申請を全て代行しますので、KIOSK型が48万円〜、タブレット型が13万円〜でご導入できます。月額費用も使わない月は0円なので、繁忙期だけのご利用も可能です。資料だけでもご覧になりませんか？」' },
                { obj: '「他社製品を検討・使用中」', res: '「弊社はシリンダー錠対応・完全オーダーメイドカスタマイズという点で差別化できています。またIT補助金の申請代行は弊社の強みです。比較検討の資料としてお送りしてもよろしいでしょうか？」' },
                { obj: '「今は時期が悪い」「来年以降で」', res: '「IT補助金の申請枠は毎年更新されますので、今すぐでなくても情報だけ持っておいていただくと、タイミングが来た時にすぐ動けます。メールアドレスをお教えいただけますか？」' },
                { obj: '「補助金って何ですか？」', res: '「IT導入補助金というもので、中小企業様がITシステムを導入する際に国が費用の最大2/3を補助してくれる制度です。弊社は申請手続きを全て代行しておりますので、御社は書類を揃えていただくだけでOKです。」' },
                { obj: '「無人にはできない」「接客が大切」', res: '「「省人化」のご提案です。チェックイン手続きを機械に任せることで、スタッフが観光案内やお出迎えなど本来の接客に集中できます。IT補助金活用で実質費用も大幅に抑えられますし、資料だけでもいかがでしょうか？」' },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-red-400 mb-2">❌ {item.obj}</p>
                  <div className="flex items-start gap-3">
                    <p className="text-base text-slate-200 leading-relaxed flex-1">✅ {item.res}</p>
                    <button onClick={() => copy(item.res, `ym_obj2_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium flex-shrink-0 transition-colors ${copiedKey === `ym_obj2_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `ym_obj2_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
"""

target = '        </div>\n      )}\n\n      {/* ─── TAB: 米山パターン ─── */}'
replacement = yoneyama_script + '        </div>\n      )}\n\n      {/* ─── TAB: 米山パターン ─── */}'

if target in content:
    content = content.replace(target, replacement, 1)
    print('Inserted successfully')
else:
    print('ERROR: target not found')
    # デバッグ用に周辺を表示
    idx = content.find('TAB: 米山パターン')
    print(repr(content[idx-100:idx+50]))

with open(FILE, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Done')
