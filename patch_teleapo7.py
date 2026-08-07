import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

old_start = '          {/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}'
old_end   = '          {/* ── 断り文句別切り返し（IT補助金訴求） ── */}'
start_idx = content.find(old_start)
end_idx   = content.find(old_end)

NL = '\\n'
BT = '`'

def make_vars_js(vars_list):
    items = []
    for tag, text in vars_list:
        t = text.replace('`', '\\`').replace('\n', '\\n')
        items.append('{tag:`' + tag + '`,text:`' + t + '`}')
    return ',\n                      '.join(items)

def make_li(points):
    return '\n                    '.join([f'<li key={{{i}}}>・{p}</li>' for i, p in enumerate(points)])

def make_kw(keywords):
    parts = []
    for k in keywords:
        parts.append(f'<span key=\'{k}\' className="text-xs bg-purple-900/60 text-purple-200 border border-purple-700/50 rounded-lg px-2 py-0.5">{k}</span>')
    return '\n                    '.join(parts)

# ── コピー用テキスト ──
s1_main = '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\\nホテル・旅館様向けのIT補助金のご案内でご連絡しているのですが、\\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」'
s2_main = '「ありがとうございます。実はいま国のIT補助金を使って、\\n自動チェックイン機をKIOSK型なら実質48万円〜、タブレット型なら13万円〜でご導入できる制度がありまして、\\n補助金の申請も弊社が全部代行しています。今日は売り込みではなく、その制度のご案内でご連絡しました。\\n今、2〜3分だけよろしいでしょうか？」'
s3_main = '「最近、うちの周りのホテル様からも夜間の対応とかインバウンドのお客様への対応で\\n大変という声をよく聞くんですが、御社では今、何か運用で課題に感じているところはありますか？」'
s4y_main = '「そうですよね。実は、その課題をIT補助金を使ってうまく解決されているホテル様の事例が手元にあります。\\n資料と補助金の申請スケジュールをメールでお送りしてもいいですか？\\nその後、15分だけいただいて、補助金を使った具体的なご説明ができればと思いまして。」'
s4n_main = '「そうですか。IT補助金って毎年申請枠があるので、タイミングが来たときのために情報だけ持っておいてもらえれば十分です。\\n補助金の概要と製品の資料をメールでお送りしてもいいですか？\\nメールアドレスをいただければ今日中に送ります。」'

s1_vars = make_vars_js([
    ('シンプル版', 'デバイスエージェンシーの米山でございます。IT補助金でご導入いただける自動チェックイン機のご案内です。支配人様おられますか？'),
    ('旅館向け', 'デバイスエージェンシーの米山と申します。旅館・温泉施設様向けにIT補助金を使って自動チェックイン機をご導入いただける件でご連絡しました。女将さんかご支配人様はいらっしゃいますか？'),
    ('インバウンド訴求', 'デバイスエージェンシーの米山でございます。インバウンド対応と人手不足の両方を解消できる補助金活用のご案内でお電話しました。ご担当の方はいらっしゃいますか？'),
    ('繁忙期前', 'デバイスエージェンシーの米山です。繁忙期が来る前にIT補助金を使って自動チェックイン機を入れていただけるご案内でご連絡しました。支配人様はいらっしゃいますか？'),
    ('政策訴求', 'デバイスエージェンシーの米山でございます。政府が今年からホテル・旅館業の省人化を重点支援しておりまして、その補助金活用のご案内でお電話しております。ご担当者様はいらっしゃいますか？'),
])

s1_points = make_li([
    '「IT補助金のご案内」と言うだけで受付に止められにくくなる（売込みと思われない）',
    '「支配人様か担当者様」と二択にすることで名前がなくても取り次ぎを引き出せる',
    '止められたら→「補助金の申請期限がありまして、担当の方に一度ご確認いただけますか」',
    '「何のご用件ですか？」と聞かれたら→「国のIT補助金を活用した自動チェックイン機のご案内です」',
])

s2_vars = make_vars_js([
    ('政府の積極支援を前面に', '政府が今年からホテル・旅館業の省人化に力を入れていて、IT補助金の予算もかなり拡充されているんです。弊社が申請を全部やるので御社のご負担はほとんどなくて、KIOSK型48万円〜で入れていただけます。2〜3分だけいいですか？'),
    ('実績強調', '弊社、今年だけで50施設以上にIT補助金を活用してご導入いただいているんですが、補助金は弊社が全部申請します。KIOSK型48万円〜、タブレット型13万円〜で、実際のコストはかなり抑えられます。少しだけお時間いいですか？'),
    ('人手不足・省人化訴求', '人手不足の対策とコスト削減を同時にできる、IT補助金活用のご案内なんですが。国が今年から省人化投資への支援を強化していて、弊社が申請代行するので実質費用もかなり安く入れられます。2分だけよろしいでしょうか？'),
    ('インバウンド×補助金', 'インバウンドのお客様の対応って今どうされてますか？実はIT補助金を使って13か国語対応のチェックイン機を入れられる制度があって、補助金申請は弊社が全部やります。少しだけお時間いいですか？'),
    ('費用インパクト先出し', '国の補助金で自動チェックイン機が最安13万円で入れられる制度があるのでご案内しているんですが、申請手続きは全部弊社がやります。2〜3分だけよろしいでしょうか？'),
    ('競合差別化', '同じ地域のホテル様がIT補助金でチェックイン機を入れ始めているのでご案内しています。補助金の申請は弊社が全部やりますし、KIOSK型で48万円〜です。少しだけいいですか？'),
])

s2_points = make_li([
    '「売り込みではなく」を明言するだけで警戒心が大きく下がる',
    '金額（48万円〜/13万円〜）を先に言うことで「高いんでしょ」という先入観を防ぐ',
    '「補助金申請は弊社が全部やる」→御社の手間がないことを強調する',
    '「2〜3分」と時間を区切ることで「長くなりそう」という断り口実を潰す',
    '「今年から政府が力を入れている」→時流・緊急性を出してタイミングを作る',
])

s3_vars = make_vars_js([
    ('夜間特化', '深夜や早朝のチェックインって今どうされていますか？夜間スタッフのコストや、対応負担について何か課題はありますか？'),
    ('インバウンド特化', '最近インバウンドのお客様は増えてきていますか？外国語の対応とか、パスポートの確認とかって手間になっていませんか？'),
    ('人手不足特化', '最近スタッフの採用って順調ですか？業界全体で人手不足という話を聞くことが多くて。ワンオペとか繁忙期の対応とか大変じゃないかなと思って。'),
    ('コスト訴求', '繁忙期と閑散期で人件費の差が大きいって施設さん多いんですが、御社はどうですか？繁忙期だけ使えるプランもあるので参考になるかなと思って。'),
    ('PMS・連携', '今どんなホテルシステム（PMS）をお使いですか？チェックイン機との連携ができると運用がかなりスムーズになるので、使っているシステムを聞かせてもらえますか？'),
    ('設備更新タイミング', '今お使いのフロント設備っていつ頃ご導入されたものですか？IT補助金のタイミングと更新時期が合うと費用がかなり抑えられるので聞かせてもらえますか？'),
])

s3_points = make_li([
    '「最近よく聞くんですが」→同業他社の状況を伝えることで安心感と共感を引き出す',
    '具体例（夜間対応・インバウンド等）を出すことで「うちは大丈夫」か「そうなんです」かを引き出しやすくなる',
    '課題が出たら→「実はそれ、IT補助金で解決されているホテル様の事例があります」につなぐ',
    '課題がなければ→「でしたら情報だけ置かせていただければ」とメール送付に切り替える',
])

s3_kw = make_kw(['夜間対応', '鍵渡しの手間', 'インバウンド', '多言語対応', 'スタッフ不足', 'ワンオペ', '繁忙期', '精算ミス', '人件費', 'PMS連携', '設備老朽化', '深夜帯'])

s4y_vars = make_vars_js([
    ('Zoom提案', '資料送ったあとで、Zoomで15分ほどご説明できれば一番わかりやすいと思うんですが、来週の火曜か水曜どちらかご都合よいですか？'),
    ('セミナー誘導', '毎週水曜11時・金曜13時にオンラインのセミナーをやっていまして、補助金の申請の話や実際の操作も見ていただけます。無料ですし、いかがですか？'),
    ('訪問提案', 'もしよければ実際に製品を見ていただきながらご説明できればと思うのですが、来週ご都合のよい日はありますか？'),
    ('資料のみ（ソフト）', 'まず資料だけ送りますね。補助金の申請スケジュールと導入事例も入っています。メールアドレスを教えてもらえますか？'),
    ('期限訴求でアポ', '補助金の申請枠が早めに締め切られることもあるので、早めに動いた方がいい施設様も多いんです。来週15分だけお時間もらえませんか？'),
    ('事例で引き寄せ', '御社と似た規模のホテル様が補助金を使って入れた事例があるので、その話だけでもお伝えできれば。15分だけZoomでいかがですか？'),
])

s4y_points = make_li([
    '「資料を送る」→「15分だけ」の2段階でアポのハードルを下げる',
    '日程は「来週の火曜か水曜、どちらがご都合よいですか？」と二択で聞く',
    'Zoomでも可と伝えれば地方のホテルも対応できる',
    '「補助金の申請期限がある」→緊急性を出してアポ日程を早める',
])

s4n_vars = make_vars_js([
    ('補助金期限を使う', '今年のIT補助金の申請期限が近づいてきているので、情報だけでも持っておいてもらえると、タイミングが来たときにすぐ動けます。メールアドレスだけ教えていただけますか？'),
    ('競合施設を使う', '同じ地域のホテル様がもう入れ始めているので、口コミの評価に差が出る前に情報だけでも持っておいてもらえれば。今日中にメールで送りますね。'),
    ('繁忙期前を使う', '次の繁忙期が来る前に動けば補助金も間に合いますので、今日は資料だけ送らせてください。メールアドレスを教えてもらえますか？'),
    ('政府の方針を使う', '政府が今年からホテル・旅館業への省人化支援を強化していますので、来年以降も補助金の枠は続く予定です。情報だけ持っておいてもらえると後で役に立ちます。'),
    ('プレッシャーなく', 'わかりました。無理に今すぐ決めてもらおうとは思っていないので、資料だけ送ります。メールアドレスだけいただければ大丈夫です。'),
])

s4n_points = make_li([
    '「資料送付 → 3週間以内に再架電」でインセンティブ対象を狙う',
    'メアドが取れたら御社名・担当者名をHubSpotに記録する',
    '「今日中に送ります」と即行動を約束することで信頼感を出す',
    '「無理に決めてもらわなくていい」→プレッシャーを外して相手の防衛心を下げる',
])

new_section = f"""          {{/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}}
          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <div className="flex items-center gap-3 mb-5">
              <span className="text-2xl">💰</span>
              <div>
                <h2 className="text-xl font-bold text-white">米山パターン — IT補助金訴求型スクリプト</h2>
                <p className="text-sm text-yellow-400/80 mt-0.5">政府の積極支援・補助金申請代行を前面に出し、コスト障壁を最初に取り除くアプローチ</p>
              </div>
            </div>
            <div className="space-y-4">

              {{/* STEP 1 */}}
              <div className="bg-blue-950/40 border border-blue-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-blue-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 1</span>
                    <span className="text-blue-300 font-bold text-sm">受付突破 — 担当者につなぐ</span>
                  </div>
                  <button onClick={{() => copy(`{s1_main}`, 'ym_s1')}} className={{`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${{copiedKey === 'ym_s1' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}}`}}>
                    {{copiedKey === 'ym_s1' ? '✅' : '📋'}}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{{`{s1_main}`}}</p>
                <div className="border-t border-blue-800/30 bg-blue-900/20 px-4 py-3">
                  <p className="text-xs text-blue-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {{[{s1_vars}].map((v,i) => (
                      <div key={{i}} className="flex items-start gap-2 bg-blue-950/40 rounded-lg p-2">
                        <span className="text-xs text-blue-400 font-bold bg-blue-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{{v.tag}}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{{v.text}}</p>
                        <button onClick={{() => copy(v.text, `ym_s1v${{i}}`)}} className={{`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${{copiedKey === `ym_s1v${{i}}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}}`}}>{{copiedKey === `ym_s1v${{i}}` ? '✅' : '📋'}}</button>
                      </div>
                    ))}}
                  </div>
                </div>
                <div className="bg-blue-900/30 px-4 py-2 border-t border-blue-800/30">
                  <p className="text-xs text-blue-300 font-bold mb-1">💡 受付突破のポイント</p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    {s1_points}
                  </ul>
                </div>
              </div>

              {{/* STEP 2 */}}
              <div className="bg-yellow-950/40 border border-yellow-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-yellow-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 2</span>
                    <span className="text-yellow-300 font-bold text-sm">担当者への第一声 — 自然な補助金訴求</span>
                  </div>
                  <button onClick={{() => copy(`{s2_main}`, 'ym_s2')}} className={{`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${{copiedKey === 'ym_s2' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}}`}}>
                    {{copiedKey === 'ym_s2' ? '✅' : '📋'}}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{{`{s2_main}`}}</p>
                <div className="border-t border-yellow-800/30 bg-yellow-900/20 px-4 py-3">
                  <p className="text-xs text-yellow-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {{[{s2_vars}].map((v,i) => (
                      <div key={{i}} className="flex items-start gap-2 bg-yellow-950/40 rounded-lg p-2">
                        <span className="text-xs text-yellow-400 font-bold bg-yellow-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{{v.tag}}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{{v.text}}</p>
                        <button onClick={{() => copy(v.text, `ym_s2v${{i}}`)}} className={{`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${{copiedKey === `ym_s2v${{i}}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}}`}}>{{copiedKey === `ym_s2v${{i}}` ? '✅' : '📋'}}</button>
                      </div>
                    ))}}
                  </div>
                </div>
                <div className="bg-yellow-900/30 px-4 py-2 border-t border-yellow-800/30">
                  <p className="text-xs text-yellow-300 font-bold mb-1">💡 ポイント</p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    {s2_points}
                  </ul>
                </div>
              </div>

              {{/* STEP 3 */}}
              <div className="bg-purple-950/40 border border-purple-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-purple-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 3</span>
                    <span className="text-purple-300 font-bold text-sm">ヒアリング — 課題を自然に引き出す</span>
                  </div>
                  <button onClick={{() => copy(`{s3_main}`, 'ym_s3')}} className={{`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${{copiedKey === 'ym_s3' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}}`}}>
                    {{copiedKey === 'ym_s3' ? '✅' : '📋'}}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{{`{s3_main}`}}</p>
                <div className="border-t border-purple-800/30 bg-purple-900/20 px-4 py-3">
                  <p className="text-xs text-purple-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {{[{s3_vars}].map((v,i) => (
                      <div key={{i}} className="flex items-start gap-2 bg-purple-950/40 rounded-lg p-2">
                        <span className="text-xs text-purple-400 font-bold bg-purple-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{{v.tag}}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{{v.text}}</p>
                        <button onClick={{() => copy(v.text, `ym_s3v${{i}}`)}} className={{`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${{copiedKey === `ym_s3v${{i}}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}}`}}>{{copiedKey === `ym_s3v${{i}}` ? '✅' : '📋'}}</button>
                      </div>
                    ))}}
                  </div>
                </div>
                <div className="bg-purple-900/30 px-4 py-2 border-t border-purple-800/30">
                  <p className="text-xs text-purple-300 font-bold mb-1">💡 ヒアリングのポイント</p>
                  <ul className="text-xs text-slate-300 space-y-0.5 mb-2">
                    {s3_points}
                  </ul>
                  <p className="text-xs text-purple-300 font-bold mb-1">拾うべきキーワード</p>
                  <div className="flex flex-wrap gap-1.5">
                    {s3_kw}
                  </div>
                </div>
              </div>

              {{/* STEP 4 YES */}}
              <div className="bg-green-950/40 border border-green-800/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-green-700 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 4</span>
                    <span className="text-green-300 font-bold text-sm">課題あり → 事例提案 → アポ取り</span>
                  </div>
                  <button onClick={{() => copy(`{s4y_main}`, 'ym_s4y')}} className={{`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${{copiedKey === 'ym_s4y' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}}`}}>
                    {{copiedKey === 'ym_s4y' ? '✅' : '📋'}}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{{`{s4y_main}`}}</p>
                <div className="border-t border-green-800/30 bg-green-900/20 px-4 py-3">
                  <p className="text-xs text-green-400 font-bold mb-2">🔀 バリエーション（アポ取りパターン）</p>
                  <div className="space-y-2">
                    {{[{s4y_vars}].map((v,i) => (
                      <div key={{i}} className="flex items-start gap-2 bg-green-950/40 rounded-lg p-2">
                        <span className="text-xs text-green-400 font-bold bg-green-900/60 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{{v.tag}}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{{v.text}}</p>
                        <button onClick={{() => copy(v.text, `ym_s4v${{i}}`)}} className={{`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${{copiedKey === `ym_s4v${{i}}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}}`}}>{{copiedKey === `ym_s4v${{i}}` ? '✅' : '📋'}}</button>
                      </div>
                    ))}}
                  </div>
                </div>
                <div className="bg-green-900/30 px-4 py-2 border-t border-green-800/30">
                  <p className="text-xs text-green-300 font-bold mb-1">💡 アポ獲得のコツ</p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    {s4y_points}
                  </ul>
                </div>
              </div>

              {{/* STEP 4' NO */}}
              <div className="bg-slate-700/50 border border-slate-600/40 rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 pt-4 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-slate-600 text-white text-xs font-bold px-2 py-0.5 rounded-full">STEP 4&apos;</span>
                    <span className="text-slate-300 font-bold text-sm">課題なし → 情報だけ置いて次につなぐ</span>
                  </div>
                  <button onClick={{() => copy(`{s4n_main}`, 'ym_s4n')}} className={{`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${{copiedKey === 'ym_s4n' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}}`}}>
                    {{copiedKey === 'ym_s4n' ? '✅' : '📋'}}
                  </button>
                </div>
                <p className="text-base text-white leading-relaxed whitespace-pre-line px-4 pb-3">{{`{s4n_main}`}}</p>
                <div className="border-t border-slate-600/30 bg-slate-600/20 px-4 py-3">
                  <p className="text-xs text-slate-400 font-bold mb-2">🔀 バリエーション</p>
                  <div className="space-y-2">
                    {{[{s4n_vars}].map((v,i) => (
                      <div key={{i}} className="flex items-start gap-2 bg-slate-700/50 rounded-lg p-2">
                        <span className="text-xs text-slate-300 font-bold bg-slate-600/80 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">{{v.tag}}</span>
                        <p className="text-sm text-slate-200 flex-1 leading-relaxed whitespace-pre-line">{{v.text}}</p>
                        <button onClick={{() => copy(v.text, `ym_s4nv${{i}}`)}} className={{`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${{copiedKey === `ym_s4nv${{i}}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-400'}}`}}>{{copiedKey === `ym_s4nv${{i}}` ? '✅' : '📋'}}</button>
                      </div>
                    ))}}
                  </div>
                </div>
                <div className="bg-slate-600/30 px-4 py-2 border-t border-slate-600/30">
                  <p className="text-xs text-slate-400 font-bold mb-1">💡 ポイント</p>
                  <ul className="text-xs text-slate-400 space-y-0.5">
                    {s4n_points}
                  </ul>
                </div>
              </div>

            </div>
          </div>

          """

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_section + content[end_idx:]
    print(f'Replaced. Size: {len(content)}')
else:
    print(f'ERROR start={start_idx} end={end_idx}')

with open(FILE, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Done')
