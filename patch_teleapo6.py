import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 米山スクリプトセクション全体を差し替える
old_start = '          {/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}'
old_end = '          {/* ── 断り文句別切り返し（IT補助金訴求） ── */}'

start_idx = content.find(old_start)
end_idx = content.find(old_end)

new_section = r"""          {/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}
          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <div className="flex items-center gap-3 mb-5">
              <span className="text-2xl">💰</span>
              <div>
                <h2 className="text-xl font-bold text-white">米山パターン — IT補助金訴求型スクリプト</h2>
                <p className="text-sm text-yellow-400/80 mt-0.5">補助金申請代行を前面に出し、コスト障壁を最初に取り除くアプローチ</p>
              </div>
            </div>
            <div className="space-y-4">

              {/* STEP 1 */}
              <div className="bg-blue-950/40 border border-blue-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-blue-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 1</span>
                    <span className="text-blue-300 font-bold text-sm">受付突破 — 担当者につなぐ</span>
                  </div>
                  <button onClick={() => copy('「お忙しいところ恐れ入ります。デバイスエージェンシーの米山でございます。\nホテル・旅館様向けのIT補助金活用でご導入できる自動チェックイン機のご案内でご連絡しました。\nご担当者様かご支配人様はいらっしゃいますでしょうか？」', 'ym_s1')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s1' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s1' ? '✅' : '📋'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">「お忙しいところ恐れ入ります。デバイスエージェンシーの米山でございます。{'\n'}ホテル・旅館様向けのIT補助金活用でご導入できる自動チェックイン機のご案内でご連絡しました。{'\n'}ご担当者様かご支配人様はいらっしゃいますでしょうか？」</p>
                {/* バリエーション */}
                <div className="border-t border-blue-800/30 bg-blue-900/20 px-4 py-3">
                  <p className="text-xs text-blue-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {[
                      { tag: '簡潔版', text: '「デバイスエージェンシーの米山でございます。IT補助金でご導入できる自動チェックイン機のご案内です。ご担当の方はいらっしゃいますか？」' },
                      { tag: '旅館向け', text: '「デバイスエージェンシーの米山と申します。旅館・温泉施設様向けにIT補助金を活用した自動チェックイン機をご案内しております。女将さまもしくはご支配人様はいらっしゃいますでしょうか？」' },
                      { tag: '繁忙期訴求', text: '「デバイスエージェンシーの米山でございます。夏の繁忙期に合わせて、IT補助金でご導入いただける自動チェックイン機のご案内でお電話しました。ご担当者様はいらっしゃいますか？」' },
                    ].map((v, i) => (
                      <div key={i} className="flex items-start gap-2 bg-blue-950/40 rounded-lg p-2">
                        <span className="text-xs text-blue-400 font-bold bg-blue-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s1v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s1v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s1v${i}` ? '✅' : '📋'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-blue-900/30 px-4 py-2 border-t border-blue-800/30">
                  <p className="text-xs text-blue-300 font-bold mb-1">💡 受付突破のポイント</p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    <li>・「IT補助金活用」を最初に言う → 売込みではなく補助金情報として通りやすい</li>
                    <li>・「ご担当者様か支配人様」と二択にすることで取次ぎを引き出す</li>
                    <li>・受付に止められたら「補助金の締め切りがあるのでご担当者様に確認していただけますか」</li>
                  </ul>
                </div>
              </div>

              {/* STEP 2 */}
              <div className="bg-yellow-950/40 border border-yellow-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-yellow-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 2</span>
                    <span className="text-yellow-300 font-bold text-sm">担当者への第一声 — IT補助金を前面に</span>
                  </div>
                  <button onClick={() => copy('「ありがとうございます。弊社では今、IT補助金の申請を全て弊社が代行する形で、KIOSK型が実質48万円〜、タブレット型が13万円〜でご導入いただけています。\n今日は売り込みではなく、補助金活用の情報をお伝えしたくてご連絡しました。\n今お時間2〜3分よろしいでしょうか？」', 'ym_s2')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s2' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s2' ? '✅' : '📋'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">「ありがとうございます。弊社では今、IT補助金の申請を全て弊社が代行する形で、KIOSK型が実質48万円〜、タブレット型が13万円〜でご導入いただけています。{'\n'}今日は売り込みではなく、補助金活用の情報をお伝えしたくてご連絡しました。{'\n'}今お時間2〜3分よろしいでしょうか？」</p>
                <div className="border-t border-yellow-800/30 bg-yellow-900/20 px-4 py-3">
                  <p className="text-xs text-yellow-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {[
                      { tag: '実績強調', text: '「弊社では今年だけで50施設以上にIT補助金を活用してご導入いただいております。補助金申請は全て弊社が代行しますので、御社にご負担はほとんどございません。2〜3分だけお時間いただけますか？」' },
                      { tag: '費用インパクト先出し', text: '「KIOSK型が実質48万円、タブレット型が13万円でご導入できる補助金のご案内です。申請手続きは弊社が全部やりますので、御社は書類を揃えるだけです。少しだけお時間いただけますか？」' },
                      { tag: '人手不足訴求', text: '「人手不足対策とコスト削減を同時に解決できる補助金活用のご案内です。IT補助金の申請を弊社が代行するので、実質負担を大幅に抑えてご導入できます。今お時間2分ほどよろしいでしょうか？」' },
                    ].map((v, i) => (
                      <div key={i} className="flex items-start gap-2 bg-yellow-950/40 rounded-lg p-2">
                        <span className="text-xs text-yellow-400 font-bold bg-yellow-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s2v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s2v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s2v${i}` ? '✅' : '📋'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-yellow-900/30 px-4 py-2 border-t border-yellow-800/30">
                  <p className="text-xs text-yellow-300 font-bold mb-1">💡 ポイント</p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    <li>・「売り込みではなく」を明言して警戒心を下げる</li>
                    <li>・具体的な金額（48万円〜/13万円〜）を早めに出して興味を引く</li>
                    <li>・「2〜3分」と時間を区切ることで話を聞いてもらいやすくなる</li>
                  </ul>
                </div>
              </div>

              {/* STEP 3 */}
              <div className="bg-purple-950/40 border border-purple-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-purple-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 3</span>
                    <span className="text-purple-300 font-bold text-sm">ヒアリング — 課題を引き出す</span>
                  </div>
                  <button onClick={() => copy('「最近、業界全体でインバウンド対応や人手不足のお声をよくお聞きするのですが、御社では現在、何か運用上の課題はお感じですか？\n例えば、夜間のチェックイン対応や、外国語スタッフの確保、繁忙期の人員確保とか…」', 'ym_s3')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s3' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s3' ? '✅' : '📋'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">「最近、業界全体でインバウンド対応や人手不足のお声をよくお聞きするのですが、御社では現在、何か運用上の課題はお感じですか？{'\n'}例えば、夜間のチェックイン対応や、外国語スタッフの確保、繁忙期の人員確保とか…」</p>
                <div className="border-t border-purple-800/30 bg-purple-900/20 px-4 py-3">
                  <p className="text-xs text-purple-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {[
                      { tag: 'シンプル版', text: '「現在、フロント業務で何か課題に感じていることはございますか？例えば夜間対応とか人員のことなど。」' },
                      { tag: 'インバウンド特化', text: '「最近インバウンドのお客様は増えていらっしゃいますか？外国語対応やパスポート確認などで課題はございませんか？」' },
                      { tag: 'コスト訴求', text: '「繁忙期と閑散期で人件費の差が大きいと感じていらっしゃいますか？弊社の製品は繁忙期だけご利用いただくプランもございまして。」' },
                      { tag: '夜間特化', text: '「深夜帯のチェックインはどのように対応されていますか？夜間スタッフのコストや対応負担について課題はございますか？」' },
                    ].map((v, i) => (
                      <div key={i} className="flex items-start gap-2 bg-purple-950/40 rounded-lg p-2">
                        <span className="text-xs text-purple-400 font-bold bg-purple-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s3v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s3v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s3v${i}` ? '✅' : '📋'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-purple-900/30 px-4 py-2 border-t border-purple-800/30">
                  <p className="text-xs text-purple-300 font-bold mb-1">💡 拾うべき課題キーワード</p>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {['夜間対応', '鍵渡しの手間', 'インバウンド', '多言語対応', 'スタッフ不足', 'ワンオペ', '繁忙期', '精算ミス', '人件費', 'PMS連携'].map(k => (
                      <span key={k} className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">{k}</span>
                    ))}
                  </div>
                </div>
              </div>

              {/* STEP 4 YES */}
              <div className="bg-green-950/40 border border-green-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-green-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 4</span>
                    <span className="text-green-300 font-bold text-sm">課題あり → 事例提案 → アポ取り</span>
                  </div>
                  <button onClick={() => copy('「そうですよね。実は、その課題をIT補助金を活用してうまく解決されているホテル様の事例が手元にあります。\n詳しい資料と補助金の申請スケジュールをメールでお送りしてもよろしいでしょうか？\nその後、15分ほどお時間いただいて、補助金活用の具体的なご説明ができればと思いまして。」', 'ym_s4y')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s4y' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s4y' ? '✅' : '📋'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">「そうですよね。実は、その課題をIT補助金を活用してうまく解決されているホテル様の事例が手元にあります。{'\n'}詳しい資料と補助金の申請スケジュールをメールでお送りしてもよろしいでしょうか？{'\n'}その後、15分ほどお時間いただいて、補助金活用の具体的なご説明ができればと思いまして。」</p>
                <div className="border-t border-green-800/30 bg-green-900/20 px-4 py-3">
                  <p className="text-xs text-green-400 font-bold mb-2">🔀 バリエーション（アポ取りパターン）</p>
                  <div className="space-y-2">
                    {[
                      { tag: 'Zoom提案', text: '「資料をお送りした後、Zoomで15分ほどご説明できればと思います。来週の火曜か水曜、どちらがご都合よいですか？」' },
                      { tag: '訪問提案', text: '「もし可能でしたら、実際に製品のデモをお見せしながらご説明させていただきたいです。来週ご都合のよい日程を教えていただけますか？」' },
                      { tag: 'セミナー誘導', text: '「毎週水曜11時・金曜13時にオンラインセミナーを開催しております。事例や補助金の詳細もご説明できます。ご参加いかがでしょうか？」' },
                      { tag: '資料のみ（アポなし）', text: '「まず資料だけお送りします。補助金の申請スケジュールと導入事例も入っています。メールアドレスをお教えください。」' },
                    ].map((v, i) => (
                      <div key={i} className="flex items-start gap-2 bg-green-950/40 rounded-lg p-2">
                        <span className="text-xs text-green-400 font-bold bg-green-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s4v${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s4v${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s4v${i}` ? '✅' : '📋'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-green-900/30 px-4 py-2 border-t border-green-800/30">
                  <p className="text-xs text-green-300 font-bold mb-1">💡 アポ獲得のコツ</p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    <li>・「資料送付 → その後15分」の2段階でハードルを下げる</li>
                    <li>・日程は「来週の火曜か水曜、どちらがご都合よいですか？」と二択で聞く</li>
                    <li>・Zoomでも可と伝えることで地方ホテルも対応できる</li>
                  </ul>
                </div>
              </div>

              {/* STEP 4' NO */}
              <div className="bg-slate-700/50 border border-slate-600/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-slate-600 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 4'</span>
                    <span className="text-slate-300 font-bold text-sm">課題なし → 情報だけ置いて次につなぐ</span>
                  </div>
                  <button onClick={() => copy('「承知しました。IT補助金は毎年申請枠がありますので、タイミングが来た時のためだけでも情報をお手元に置いていただければ。\n補助金の概要と弊社製品の資料をメールでお送りしてもよろしいでしょうか？\nメールアドレスをお教えいただければ、今日中にお送りします。」', 'ym_s4n')} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === 'ym_s4n' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                    {copiedKey === 'ym_s4n' ? '✅' : '📋'}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">「承知しました。IT補助金は毎年申請枠がありますので、タイミングが来た時のためだけでも情報をお手元に置いていただければ。{'\n'}補助金の概要と弊社製品の資料をメールでお送りしてもよろしいでしょうか？{'\n'}メールアドレスをお教えいただければ、今日中にお送りします。」</p>
                <div className="border-t border-slate-600/30 bg-slate-600/20 px-4 py-3">
                  <p className="text-xs text-slate-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {[
                      { tag: '補助金期限を使う', text: '「今年のIT補助金の申請期限が近づいております。今すぐでなくてもよいのですが、情報だけでも持っておいていただくとタイミングが来た時にすぐ動けます。メールアドレスをいただけますか？」' },
                      { tag: '競合施設を使う', text: '「実は同じ地域のホテル様がすでに導入されています。口コミの評価にも差が出てきておりますので、ご参考までに資料だけでもご覧いただけますか？」' },
                      { tag: '繁忙期前を使う', text: '「次の繁忙期が来る前に情報だけでも。今ご導入されると繁忙期に間に合いますし、補助金申請も間に合います。メールアドレスを教えていただけますか？」' },
                    ].map((v, i) => (
                      <div key={i} className="flex items-start gap-2 bg-slate-700/50 rounded-lg p-2">
                        <span className="text-xs text-slate-300 font-bold bg-slate-600/80 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{v.tag}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed">{v.text}</p>
                        <button onClick={() => copy(v.text, `ym_s4nv${i}`)} className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${copiedKey === `ym_s4nv${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}`}>{copiedKey === `ym_s4nv${i}` ? '✅' : '📋'}</button>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-slate-600/30 px-4 py-2 border-t border-slate-600/30">
                  <p className="text-xs text-slate-400 font-bold mb-1">💡 ポイント</p>
                  <ul className="text-xs text-slate-400 space-y-0.5">
                    <li>・「資料送付 → 3週間以内に再架電」でインセンティブ対象を狙う</li>
                    <li>・メアドが取れたら「御社名・担当者名・受け取り確認連絡」をHubSpotに記録</li>
                  </ul>
                </div>
              </div>

            </div>
          </div>

          """

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_section + content[end_idx:]
    print(f'Replaced. Final size: {len(content)}')
else:
    print(f'ERROR: start={start_idx}, end={end_idx}')

with open(FILE, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Done')
