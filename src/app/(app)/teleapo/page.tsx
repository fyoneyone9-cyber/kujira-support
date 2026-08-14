'use client'
import { useState, useCallback, useRef, useEffect } from 'react'

// ── 切り返しデータ（全15カテゴリ）──
const OBJECTION_TREE: Record<string, { label: string; response: string }> = {
  // ── カテゴリ（ラベルのみ）──
  'cat_busy':        { label: '⏰ 今は忙しい', response: '' },
  'cat_nointerest':  { label: '🚫 興味がない', response: '' },
  'cat_other':       { label: '🏢 他社を使っている', response: '' },
  'cat_price':       { label: '💴 高そう・お金がかかる', response: '' },
  'cat_key':         { label: '🔑 カードキーでないとダメ', response: '' },
  'cat_custom':      { label: '🏨 うちの業態に合わない', response: '' },
  'cat_pms':         { label: '💻 PMSと連携できるの？', response: '' },
  'cat_unmanned':    { label: '🚫 無人にはできない', response: '' },
  'cat_person':      { label: '📵 担当者不在', response: '' },
  'cat_email':       { label: '📧 メールが届かない', response: '' },
  'cat_seminar':     { label: '📅 セミナーの案内', response: '' },
  'cat_inbound':     { label: '🌏 インバウンド対応の話', response: '' },
  'cat_size':        { label: '🏡 小規模だから不要では？', response: '' },
  'cat_timing':      { label: '📆 今は検討時期ではない', response: '' },
  'cat_claim':       { label: '😡 かけてくるな（クレーム）', response: '' },

  // ── 今は忙しい ──
  'busy_later':      { label: 'また頃合いを見て連絡する', response: '「承知しました。では、またお時間のよいときにご連絡させていただいてもよろしいでしょうか。いつ頃でしたらよろしいでしょうか。」' },
  'busy_short':      { label: '30秒だけお願いする', response: '「お忙しいところ大変恐れ入ります。30秒だけお時間いただけますでしょうか。資料をメールでお送りするだけでも、させていただければと思っております。」' },
  'busy_task':       { label: 'タスクに控えて後日かける', response: '「かしこまりました。では、後日あらためてご連絡させていただきます。お名前とご連絡先、確認させていただいてよろしいでしょうか。」' },
  'busy_mail':       { label: '今は資料だけメールで送る', response: '「お忙しいところ失礼しました。では資料だけでもメールでお送りさせていただいてもよろしいでしょうか。メールアドレスをいただけるだけで大丈夫です。」' },
  'busy_time_ask':   { label: '今日の後半に再架電を提案', response: '「承知しました。では本日の午後、あらためてお電話してもよろしいでしょうか。一言いただければ十分です。」' },
  'busy_empathy':    { label: '繁忙期であることに共感して次につなぐ', response: '「繁忙期でお忙しい時期にお電話してしまい申し訳ありません。実は繁忙期こそ弊社製品が力を発揮するのですが、落ち着いたタイミングで一度お話しさせていただけますでしょうか。」' },

  // ── 興味がない ──
  'nointerest_reason':    { label: '具体的な理由を聞く', response: '「そうでございますか。差し支えなければ、どのような点でご興味をお持ちになれないか、教えていただけますでしょうか。もしコスト面や業態の問題でしたら、解決できた事例もご用意しております。」' },
  'nointerest_future':    { label: '将来的な可能性を確認', response: '「将来的にも、ご興味はないでしょうか。近年、全国からのお問い合わせが去年よりかなり多くなってきておりまして、業界全体でのスタンダードになりつつあります。参考情報だけでもお送りさせていただければと思います。」' },
  'nointerest_seminar':   { label: 'セミナーに誘う', response: '「弊社は週2回、オンラインの説明会を開催しております（水曜11時・金曜13時）。1時間程度で費用・導入事例なども詳しくご説明できます。ご参加は無料ですので、一度いかがでしょうか。」' },
  'nointerest_flow':      { label: '流行の波を伝える', response: '「最近よくお耳にするかとは思いますが、自動チェックイン機の件になります。全国各地のホテル様で急速に導入が進んでおりまして、業界のスタンダードになりつつある状況でございます。他社様に遅れをとらないためにも、一度ご検討いただけませんか？」' },
  'nointerest_info':      { label: '情報だけでも送る提案', response: '「ご興味がないのは承知しました。ただ、資料だけでもご覧いただけますと、具体的なコストや仕組みがよくわかります。メールアドレスをお教えいただければ今日中にお送りします。」' },
  'nointerest_subsidy':   { label: 'IT補助金の話に切り替える', response: '「製品のご興味より先に、今年のIT補助金の締め切りが近づいているのでご案内しているという側面もございます。補助金申請だけでも弊社が代行できますので、情報だけでも受け取っていただけますでしょうか。」' },
  'nointerest_competitor':{ label: '競合に差をつけられる前に、と訴求', response: '「同じ地域の競合ホテル様がすでに導入されている事例もございます。チェックインのスムーズさは口コミにも影響しますので、情報だけでも持っておいていただけると幸いです。」' },

  // ── 他社使用中 ──
  'other_maker':     { label: 'どのメーカーか聞く', response: '「あ、そうでございましたか。差し支えなければ、どちらのメーカー様をご利用されているか、参考までに教えて頂けますでしょうか。」' },
  'other_compare':   { label: '比較提案に持ち込む', response: '「すでに導入されていらっしゃるのですね。弊社は自社開発のため、他社様にはない機能（シリンダー錠対応・完全オーダーメイドカスタマイズ等）がございます。現状の課題があれば、比較資料としてご覧いただけますでしょうか。」' },
  'other_renewal':   { label: '更新・リプレイス提案', response: '「現在ご利用のシステムの契約更新時期はいつ頃でしょうか。弊社は価格面でもご好評をいただいており、乗り換えを検討されている施設様も増えております。ちょうどそのタイミングで比較検討いただけると幸いです。」' },
  'other_weakness':  { label: '現在の課題・不満を聞く', response: '「現在お使いのシステムで、何か不満な点や「ここがもう少し…」という部分はございますでしょうか。弊社はカスタマイズ性と価格面で選ばれることが多く、改善できる可能性があるかもしれません。」' },
  'other_coexist':   { label: '併用・補完提案をする', response: '「チェックイン機は既存のPMSや管理システムとの連携も可能です。今お使いのシステムはそのままで、チェックイン・精算だけ弊社製品を使っていただく形も選択肢としてございます。」' },

  // ── 価格 ──
  'price_subsidy':        { label: 'IT補助金を案内する', response: '「弊社が補助金申請を代行できます。IT補助金活用でKIOSK型が実質48万円〜、タブレット型は13万円〜でご導入可能です。補助金があれば実質費用がかなり抑えられます。詳しい資料をお送りしてもよろしいでしょうか。」' },
  'price_running':        { label: '月額費用・コスト削減効果を説明', response: '「月額費用はKIOSK型で19,600円（部屋数×100円）、タブレット型は1室500円です。繁忙期のみ使用で使わない月は0円・日割り計算も可能です。一方で、フロントスタッフの人件費削減効果と比べると、多くの施設様で半年〜1年以内に回収されています。」' },
  'price_season':         { label: '季節限定プランを案内', response: '「ご使用にならない月は月額0円になります。繁忙期のみのご利用や、土日祝のみご使用の日割り計算プランもございます。実際の費用感をメールでご案内してもよろしいでしょうか。」' },
  'price_small':          { label: '小規模向け低コストプランを提示', response: '「小規模施設様向けには、タブレット型でご導入いただけます。初期費用はIT補助金活用で13万円〜、月額は1室500円です。一軒家規模の旅館様にも導入実績がございます。」' },
  'price_roi':            { label: '人件費削減ROIを説明する', response: '「仮にフロントスタッフ1名の夜間対応を削減できたとすると、月20〜30万円の人件費削減になります。月額費用と比較すると、多くの施設様で3〜6ヶ月で回収できています。」' },
  'price_subsidy_detail': { label: 'IT補助金の詳細を説明する', response: '「IT導入補助金は中小企業がITシステムを導入する際に国が最大2/3を補助する制度です。弊社は補助金申請の代行から書類作成まで全て対応しており、御社にご負担いただくのは必要書類のご提出のみです。」' },

  // ── カードキー・鍵 ──
  'key_cylinder':    { label: 'シリンダー錠対応をPR', response: '「弊社の強みは、シリンダー錠（物理キー）にも対応可能なことです！別売りのキーボックスを使うことで、精算が完了すると自動でキーボックスが開き、お客様がセルフで鍵をお受け取りいただけます。カードキーへの変更は一切不要です。」' },
  'key_smartlock':   { label: 'クラウドスマートロックを提案', response: '「クラウドスマートロックという選択肢もございます。暗証番号で開錠でき、チェックイン機から排出されるレシートに暗証番号が自動で印字されます。鍵の受け渡しが完全にセルフになります。」' },
  'key_receipt':     { label: 'レシート×対面方式を提案', response: '「もし接客を残したい場合は、チェックイン機で精算まで済ませてレシートを発行し、そのレシートをフロントで鍵と交換するという運用も可能です。対面の接客要素を残しながら、手続きだけ効率化できます。」' },
  'key_keybox':      { label: 'キーボックスの仕組みを説明する', response: '「キーボックスは壁に設置する鍵の収納ボックスで、チェックイン機での精算完了と同時に自動解錠されます。番号錠ではなく自動解錠型なので、お客様が暗証番号を覚える必要がありません。」' },
  'key_cost':        { label: 'カードキー化のコストを比較する', response: '「カードキーへの変更は設備投資が必要ですが、弊社のシリンダー錠対応なら既存の鍵をそのまま使えます。余計な改修費用をかけずにチェックイン機を導入できるのが弊社の強みです。」' },

  // ── 業態・カスタマイズ ──
  'custom_order':    { label: 'オーダーメイドをPR', response: '「普段スタッフが口頭でご説明していることを、チェックイン機にカスタマイズして組み込むことが可能です。弊社は自社開発のため、御社専用のオーダーメイドをご提供できます。他社様には真似のできない強みです。」' },
  'custom_example':  { label: '同業態の導入事例を提示', response: '「弊社では接客の質を落とさずに手続きだけをスマート化して、顧客満足度を上げた事例がございます。同じような業態の施設様の導入事例を資料でお送りしてもよろしいでしょうか。」' },
  'custom_ryokan':   { label: '旅館・温泉施設への対応', response: '「旅館様でも多数ご導入いただいております。日帰り温泉客の受付・精算、朝食券・夕食券の発行など、旅館特有の運用にもカスタマイズ対応できます。お話しだけでもいかがでしょうか。」' },
  'custom_hospi':    { label: 'ホスピタリティを落とさない訴求', response: '「チェックイン機を導入することで、フロントスタッフがチェックイン手続きから解放され、観光案内やお出迎えなどの本来の接客に集中できるようになります。結果としてホスピタリティが向上した施設様も多くいらっしゃいます。」' },
  'custom_demo':     { label: 'デモの実機確認を提案', response: '「実際の操作感が気になるようでしたら、オンラインデモをご用意することも可能です。実際の画面をご覧いただきながら、御社の業態に合う設定をご提案できます。30分程度で済みますが、いかがでしょうか。」' },
  'custom_ui':       { label: 'UI・画面のカスタマイズを説明', response: '「チェックイン画面のUIは御社のブランドに合わせてカスタマイズできます。ロゴや配色、表示する質問項目、宿泊規約の文面なども変更可能です。「うちらしくない」とはなりません。」' },

  // ── PMS連携 ──
  'pms_list':        { label: 'PMS連携実績を案内', response: '「弊社はPMS（ホテルシステム）との連携開発に近年力を入れています。連携実績：ステイシー・スイートブック・ベッド4。現在も複数のPMSと連携開発が進行中です。御社のPMSについても、ぜひ一度ご相談いただけますでしょうか。」' },
  'pms_develop':     { label: '連携開発の意欲を伝える', response: '「お客様のご要望によりかなりの頻度で連携開発が進んでいますので、御社のPMSも今後連携開発を進めることが可能です。まずシステム名をお教えいただけますでしょうか。」' },
  'pms_standalone':  { label: 'PMS連携なしでも使えると伝える', response: '「PMSとの連携がなくても、弊社製品単体でチェックイン・精算・精算書発行まで完結できます。連携がない場合でも、予約番号での照合や手動入力での運用が可能です。まず基本機能を試していただいてから連携を検討する施設様も多いです。」' },
  'pms_api':         { label: 'API連携の仕組みを説明する', response: '「APIが公開されているPMSであれば、弊社との連携開発ができます。御社のPMSのAPI仕様書を確認できれば、連携可能かどうかを弊社エンジニアが確認いたします。PMSのシステム名を教えていただけますでしょうか。」' },

  // ── 無人化 ──
  'unmanned_pr':      { label: '省人化の効果に言い換える', response: '「「無人化」というより、「省人化」「業務効率化」のツールとしてご活用いただいております。フロントスタッフがチェックイン手続きから解放されることで、お客様との会話や観光案内など、本来の接客サービスにより集中できるようになります。」' },
  'unmanned_night':   { label: '夜間・深夜帯の対応として訴求', response: '「特に夜間・深夜帯のチェックインで効果を発揮します。スタッフが不在の時間でも、お客様が自力でチェックインできるため、深夜のフロント対応を大幅に削減できます。」' },
  'unmanned_inbound': { label: 'インバウンドへの対応力', response: '「外国語対応（13か国語）とパスポートスキャン機能により、インバウンドのお客様もスムーズにチェックインできます。言語の壁がなくなることで、スタッフの対応負荷が大幅に減ります。」' },
  'unmanned_hybrid':  { label: 'ハイブリッド運用を提案', response: '「完全無人化ではなく、ハイブリッド運用も可能です。例えば平日昼はフロント対応、深夜や繁忙期はチェックイン機を併用、という形です。状況に合わせて柔軟に使い分けられます。」' },
  'unmanned_elderly': { label: 'お年寄りゲストへの対応を説明', response: '「ご年配のお客様にはスタッフがサポートする運用にしている施設様も多いです。機械が苦手なお客様にはフロントで対応し、それ以外のお客様にはチェックイン機を使っていただく、という使い分けで問題ありません。」' },
  'unmanned_staff':   { label: 'スタッフの仕事がなくならないと説明', response: '「「チェックイン手続きがなくなると、スタッフの仕事がなくなるのでは」とご心配されることがありますが、逆にスタッフが接客・コンシェルジュ・宿泊チェックなど付加価値の高い業務に集中できるようになります。」' },

  // ── 担当者不在 ──
  'person_time':     { label: '折り返し時間を聞く', response: '「そうですか、失礼しました。何時頃にお戻りになりますでしょうか。その時間に改めてご連絡させていただきます。」' },
  'person_front':    { label: 'フロント担当に話す', response: '「では、フロントのご担当の方にお取り次ぎいただけますでしょうか。IT補助金を活用した自動チェックイン機のご案内で、2〜3分だけお時間いただければ幸いです。」' },
  'person_callback':  { label: '折り返し電話をお願いする', response: '「ありがとうございます。お手数ですが、お戻りになりましたらデバイスエージェンシーの米山からご連絡があった旨、お伝えいただけますでしょうか。電話番号は080-3207-8422です。」' },
  'person_msg':      { label: 'メッセージを残す', response: '「承知しました。では、IT補助金を活用した自動チェックイン機の案内でお電話した旨、ご担当者様にお伝えいただけますでしょうか。後ほど改めてご連絡いたします。」' },
  'person_name':     { label: '担当者名を取得する', response: '「ありがとうございます。差し支えなければ、ご担当の方のお名前を教えていただけますでしょうか。次回ご連絡する際にお名前でお呼びできれば幸いです。」' },
  'person_email':    { label: 'メールだけ送る', response: '「では、IT補助金や自動チェックイン機の資料だけでもメールでお送りしてもよろしいでしょうか。メールアドレスをいただければ今日中にお送りします。」' },

  // ── メールが届かない ──
  'email_spam':      { label: '迷惑メールフォルダを確認してもらう', response: '「大変失礼しました。迷惑メールフォルダに振り分けられている可能性がございます。「deviceagency」で検索していただけますでしょうか。」' },
  'email_recheck':   { label: 'メールアドレスを再確認する', response: '「念のため、ご登録のメールアドレスを確認させていただけますでしょうか。入力ミスが発生している可能性がございます。」' },
  'email_resend':    { label: '再送する', response: '「承知しました。今すぐ再度お送りします。もし届かない場合は、別のメールアドレスをご用意いただけますでしょうか。」' },
  'email_domain':    { label: '送信ドメインの確認を依頼', response: '「企業のメールフィルターで弾かれている可能性がございます。IT部門に「deviceagency.co.jp」ドメインからのメールを受信許可していただくようご確認いただけますでしょうか。」' },
  'email_change':    { label: '別の連絡手段を提案', response: '「もし届き続けない場合は、Gmailなど別のアドレスでお受け取りいただくか、LINEやFAXなど別の方法でお送りすることも可能です。いかがでしょうか。」' },

  // ── セミナー ──
  'seminar_when':    { label: 'セミナーの日程を案内', response: '「弊社のオンラインセミナーは毎週水曜11時・金曜13時に開催しております。1時間程度で費用感・補助金活用・実際のデモも見ていただけます。次回の水曜・金曜どちらがご都合よいですか？」' },
  'seminar_content': { label: 'セミナーの内容を説明', response: '「セミナーでは、IT補助金の活用方法・製品デモ・導入事例・費用感・Q&Aをご案内しています。1時間程度で無料です。実際の画面操作もご覧いただけます。」' },
  'seminar_nudge':   { label: 'セミナー参加を後押し', response: '「まずセミナーに参加いただくだけでも構いません。参加=導入決定ではなく、情報収集として多くの施設様にご活用いただいています。次の水曜か金曜、いかがでしょうか。」' },
  'seminar_record':  { label: '録画・アーカイブを案内', response: '「もしリアルタイムが難しければ、録画をお送りすることも可能です。ご都合のよい時間にご覧いただけます。メールアドレスをいただけますか？」' },

  // ── インバウンド ──
  'inbound_lang':    { label: '多言語対応の説明', response: '「弊社のチェックイン機は13か国語に対応しています。お客様が自分の言語でチェックイン操作できるため、スタッフが外国語を話せなくても問題ありません。」' },
  'inbound_passport':{ label: 'パスポートスキャン機能のPR', response: '「パスポートスキャン機能で、外国人旅行者の情報を自動で読み取り・記録できます。手書き宿帳への転記が不要になり、入国管理法対応もスムーズです。」' },
  'inbound_cc':      { label: 'クレジット・国際決済の対応', response: '「海外発行のクレジットカード・交通系ICにも対応しています。インバウンドのお客様が現金なしでもスムーズに精算できます。」' },
  'inbound_demand':  { label: 'インバウンド増加トレンドを訴求', response: '「訪日外国人は2024年から過去最高水準が続いており、今後もさらに増加が見込まれます。今のうちにインバウンド対応を強化しておくことで、口コミ評価の向上にもつながります。」' },

  // ── 小規模 ──
  'size_tablet':     { label: 'タブレット型を提案', response: '「小規模施設様向けにはタブレット型がございます。IT補助金適用後で実質13万円〜でご導入可能です。月額も1室500円からと、小規模でも無理のないプランです。」' },
  'size_other':      { label: '小規模導入事例を紹介', response: '「客室数5室以下の小規模旅館様や民泊施設様にも多数ご導入いただいています。部屋数が少ないほど月額コストも低くなります。」' },
  'size_case':       { label: '費用対効果を説明', response: '「小規模でも夜間のチェックイン対応をセルフ化するだけで、スタッフの深夜対応が大幅に減ります。月額コスト以上のメリットを実感いただいている施設様が多いです。」' },
  'size_future':     { label: '将来的な拡張を見据えた提案', response: '「今は小規模でも、将来的に部屋数を増やしたり複数拠点を持った場合にも、同じシステムをそのまま活用できます。早めに慣れておくのがおすすめです。」' },

  // ── 今は時期ではない ──
  'timing_future':      { label: '将来の検討に向けて情報を残す', response: '「承知しました。では今すぐでなくとも、IT補助金の概要と製品資料だけでも手元に置いておいていただけると、タイミングが来た時にすぐ動けます。メールアドレスをいただけますか？」' },
  'timing_task':        { label: '検討タスクとして残してもらう', response: '「では、来季の検討課題として弊社のご案内を残していただけますでしょうか。改めてご連絡するタイミングはいつ頃がよろしいですか？」' },
  'timing_subsidy':     { label: '補助金の期限を伝えて急かす', response: '「IT補助金の申請枠は毎年更新されますが、年度の締め切りが決まっています。今から動いておくと来年度の申請にも余裕を持って対応できます。」' },
  'timing_competitor':  { label: '競合の動きを伝える', response: '「実は同じ地域の他のホテル様が今年から導入を始めているケースが増えています。チェックインの利便性は口コミ・評価サイトにも影響しますので、早めに情報収集だけでもいかがでしょうか。」' },
  'timing_renovation':  { label: '改修・設備更新タイミングを合わせる', response: '「改修や設備更新をお考えの時期があれば、そのタイミングに合わせてご提案させていただくこともできます。来年・再来年以降でのご検討でも、ぜひお声がけください。」' },

  // ── クレーム ──
  'claim_apology':   { label: 'まず謝罪して鎮める', response: '「大変失礼いたしました。ご迷惑をおかけして申し訳ございません。以後、ご連絡を控えさせていただきます。もしご不明な点等ございましたらいつでもご連絡ください。」' },
  'claim_record':    { label: '架電停止をHubSpotに記録する', response: '（架電クレームとしてHubSpotに記録し、今後の架電対象から除外する。ステータスを「架電クレーム」に変更する）' },
  'claim_freq':      { label: '架電頻度が高い場合の対応', response: '「ご不快をおかけして誠に申し訳ございません。以後は一切ご連絡いたしません。ご迷惑をおかけしました。」（その後すぐに電話を切る）' },
}

// ── カテゴリ→子ID マッピング ──
const CATEGORY_ITEMS = [
  { id: 'cat_busy',        children: ['busy_later', 'busy_short', 'busy_task', 'busy_mail', 'busy_time_ask', 'busy_empathy'] },
  { id: 'cat_nointerest',  children: ['nointerest_reason', 'nointerest_future', 'nointerest_seminar', 'nointerest_flow', 'nointerest_info', 'nointerest_subsidy', 'nointerest_competitor'] },
  { id: 'cat_other',       children: ['other_maker', 'other_compare', 'other_renewal', 'other_weakness', 'other_coexist'] },
  { id: 'cat_price',       children: ['price_subsidy', 'price_running', 'price_season', 'price_small', 'price_roi', 'price_subsidy_detail'] },
  { id: 'cat_key',         children: ['key_cylinder', 'key_smartlock', 'key_receipt', 'key_keybox', 'key_cost'] },
  { id: 'cat_custom',      children: ['custom_order', 'custom_example', 'custom_ryokan', 'custom_hospi', 'custom_demo', 'custom_ui'] },
  { id: 'cat_pms',         children: ['pms_list', 'pms_develop', 'pms_standalone', 'pms_api'] },
  { id: 'cat_unmanned',    children: ['unmanned_pr', 'unmanned_night', 'unmanned_inbound', 'unmanned_hybrid', 'unmanned_elderly', 'unmanned_staff'] },
  { id: 'cat_person',      children: ['person_time', 'person_front', 'person_callback', 'person_msg', 'person_name', 'person_email'] },
  { id: 'cat_email',       children: ['email_spam', 'email_recheck', 'email_resend', 'email_domain', 'email_change'] },
  { id: 'cat_seminar',     children: ['seminar_when', 'seminar_content', 'seminar_nudge', 'seminar_record'] },
  { id: 'cat_inbound',     children: ['inbound_lang', 'inbound_passport', 'inbound_cc', 'inbound_demand'] },
  { id: 'cat_size',        children: ['size_tablet', 'size_other', 'size_case', 'size_future'] },
  { id: 'cat_timing',      children: ['timing_future', 'timing_task', 'timing_subsidy', 'timing_competitor', 'timing_renovation'] },
  { id: 'cat_claim',       children: ['claim_apology', 'claim_record', 'claim_freq'] },
]

// ── キーワード→切り返しIDマッピング ──
const KEYWORD_MAP: Array<{ keywords: string[]; ids: string[] }> = [
  { keywords: ['忙しい', 'いそが', '今は', 'また今度', '後で', 'あとで', '手が離', 'タイミング悪', '時間ない'],
    ids: ['busy_later', 'busy_short', 'busy_task'] },
  { keywords: ['興味ない', '興味がない', '必要ない', '結構です', 'いらない', '要らない', '不要', 'ニーズがない', '考えてない'],
    ids: ['nointerest_reason', 'nointerest_future', 'nointerest_info', 'nointerest_seminar'] },
  { keywords: ['他社', '他のメーカー', '既に', 'すでに', '導入済み', '使ってる', '使っている', '入れてる', '入れている', 'もう使'],
    ids: ['other_maker', 'other_compare', 'other_renewal'] },
  { keywords: ['高い', 'たかい', '高そう', 'お金', '費用', 'コスト', '予算', '値段', '料金', '安くなる'],
    ids: ['price_subsidy', 'price_running', 'price_season', 'price_small'] },
  { keywords: ['補助金', 'IT補助', '助成'],
    ids: ['price_subsidy'] },
  { keywords: ['カードキー', 'カード', '鍵', 'かぎ', 'シリンダー', '物理キー', 'ドア'],
    ids: ['key_cylinder', 'key_smartlock', 'key_receipt'] },
  { keywords: ['業態', '合わない', 'うちには', '旅館', '民宿', '温泉', 'ゲストハウス', 'ホステル', '小規模', '規模が小さ'],
    ids: ['custom_order', 'custom_example', 'custom_ryokan', 'size_tablet'] },
  { keywords: ['pms', 'PMS', 'ホテルシステム', 'システム連携', '予約システム', 'ステイシー', 'スイートブック', 'ベッド4'],
    ids: ['pms_list', 'pms_develop'] },
  { keywords: ['無人', 'むじん', 'スタッフいない', '人がいない', '接客できない', '対面'],
    ids: ['unmanned_pr', 'unmanned_night', 'unmanned_inbound'] },
  { keywords: ['担当', 'たんとう', '不在', 'ふざい', '支配人', 'いない', '席を外', 'おりません', '出かけ'],
    ids: ['person_time', 'person_front', 'person_callback', 'person_msg'] },
  { keywords: ['メール', '届かない', '受け取れない', '迷惑', 'spam', '来ない', 'こない'],
    ids: ['email_spam', 'email_recheck', 'email_resend'] },
  { keywords: ['セミナー', '説明会', 'zoom', 'zoomで', 'オンライン', '参加', '日程'],
    ids: ['seminar_when', 'seminar_content', 'seminar_nudge'] },
  { keywords: ['外国', '英語', '中国語', '韓国語', 'インバウンド', '外国人', '訪日', 'パスポート', '多言語'],
    ids: ['inbound_lang', 'inbound_passport'] },
  { keywords: ['小さい', '小規模', '部屋数少', '客室少', '一軒家', 'シングル', '数室', '数部屋'],
    ids: ['size_tablet', 'size_other'] },
  { keywords: ['今は検討', '検討中ではない', '時期ではない', 'まだ先', 'そのうち', '来年', '再来年', '予算が'],
    ids: ['timing_future', 'timing_task'] },
  { keywords: ['かけるな', '電話しないで', 'もうかけ', '迷惑', 'クレーム', '怒', 'おこ', '二度と'],
    ids: ['claim_apology', 'claim_record'] },
]

function suggestByKeyword(input: string): string[] {
  if (!input.trim()) return []
  const lower = input.toLowerCase()
  const matched = new Map<string, number>()
  for (const rule of KEYWORD_MAP) {
    if (rule.keywords.some(kw => lower.includes(kw))) {
      for (const id of rule.ids) {
        matched.set(id, (matched.get(id) ?? 0) + 1)
      }
    }
  }
  return Array.from(matched.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([id]) => id)
}

type AiSuggestion = { label: string; talk: string; point: string }

const TABS = [
  { id: 'hubspot',   label: '📊 HubSpot手順' },
  { id: 'script',   label: '📞 トークスクリプト' },
  { id: 'status',   label: '🏷️ ステータス一覧' },
  { id: 'knowledge',label: '💡 商品知識' },
  { id: 'checklist',label: '✅ チェックリスト' },
  { id: 'mail',     label: '✉️ メールテンプレ' },
]

export default function TeleapoPage() {
  const [activeTab, setActiveTab] = useState('hubspot')
  const [copiedKey, setCopiedKey] = useState<string | null>(null)
  const [selectedCat, setSelectedCat] = useState<string | null>(null)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const suggestions = suggestByKeyword(searchInput)

  const [aiInput, setAiInput] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState<AiSuggestion[]>([])
  const [aiError, setAiError] = useState<string | null>(null)
  const [aiSelectedIdx, setAiSelectedIdx] = useState<number | null>(null)
  const [aiPattern, setAiPattern] = useState<string>('yoneyama')
  const [stepMemos, setStepMemos] = useState<string[]>(['', '', '', '', ''])
  const updateMemo = (i: number, val: string) => setStepMemos(prev => prev.map((m, idx) => idx === i ? val : m))

  const fetchAiSuggestions = useCallback(async (text: string, pattern: string) => {
    if (!text.trim()) return
    setAiLoading(true)
    setAiError(null)
    setAiSuggestions([])
    setAiSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setAiSuggestions(data.suggestions ?? [])
    } catch (e) {
      setAiError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setAiLoading(false)
    }
  }, [])

  // 音声認識
  const [isListening, setIsListening] = useState(false)
  const recognitionRef = useRef<any>(null)

  const startListening = useCallback(() => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SR) { alert('このブラウザは音声認識に対応していません（Chrome推奨）'); return }
    const recog = new SR()
    recog.lang = 'ja-JP'
    recog.continuous = false
    recog.interimResults = true
    recog.onstart = () => setIsListening(true)
    recog.onresult = (e: any) => {
      const transcript = Array.from(e.results).map((r: any) => r[0].transcript).join('')
      setAiInput(transcript)
      if (e.results[e.results.length - 1].isFinal) {
        setIsListening(false)
        fetchAiSuggestions(transcript, aiPattern)
      }
    }
    recog.onerror = () => setIsListening(false)
    recog.onend = () => setIsListening(false)
    recognitionRef.current = recog
    recog.start()
  }, [aiPattern, fetchAiSuggestions])

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop()
    setIsListening(false)
  }, [])

  const copy = (text: string, key: string) => {
    navigator.clipboard.writeText(text)
    setCopiedKey(key)
    setTimeout(() => setCopiedKey(null), 2000)
  }

  const selectCat = (id: string) => {
    setSelectedCat(id === selectedCat ? null : id)
    setSelectedResponse(null)
  }

  const selectResponse = (id: string) => {
    setSelectedResponse(id === selectedResponse ? null : id)
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">テレアポ</h1>
        <p className="text-base text-slate-400 mt-1">株式会社デバイスエージェンシー ｜ スマートチェックイン架電</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {TABS.map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'
            }`}>
            {tab.label}
          </button>
        ))}
      </div>

      {/* 参考資料リンク */}
      <div className="mb-6 bg-slate-800 rounded-2xl border border-slate-700 p-5">
        <p className="text-base text-slate-300 font-bold mb-4">📁 参考資料</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <a href="https://app-na2.hubspot.com/contacts/39705134/objects/0-3/views/353515006/list" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-orange-900/30 hover:bg-orange-900/50 border border-orange-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">🟠</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-orange-300 transition-colors">HubSpot 架電リスト</p>
              <p className="text-slate-400 text-sm">取引一覧（楽天トラベルフィルター済）</p>
            </div>
          </a>
          <a href="https://us02web.zoom.us/myhome" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-blue-900/30 hover:bg-blue-900/50 border border-blue-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">📹</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-blue-300 transition-colors">Zoom マイホーム</p>
              <p className="text-slate-400 text-sm">架電・セミナー用 Zoom</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1F2ycU3glbgrJCOkLRKHg86ROWggkbYOZXxhA2vco84o/edit?gid=767829959#gid=767829959" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">📊</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-blue-300 transition-colors">テレアポ業務マニュアル</p>
              <p className="text-slate-400 text-sm">テレアポ業務マニュアル改正シート</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1WnwEhp2Db9lDHNw8qp_h2ZjhMY-mZG9TXcAAh6RX59w/edit?gid=1927965581#gid=1927965581" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">📋</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-blue-300 transition-colors">アウトバウンド管理簿</p>
              <p className="text-slate-400 text-sm">【スマートチェックイン】架電管理</p>
            </div>
          </a>
        </div>
      </div>

      {/* ─── TAB: HubSpot手順 ─── */}
      {activeTab === 'hubspot' && (
        <div className="space-y-6">

          {/* 電話してください4箱 */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xl">📞</span>
              <h2 className="text-xl font-bold text-white">電話してください — 4つの箱（上から順に）</h2>
            </div>
            <p className="text-sm text-slate-400 mb-5">左から2〜5番目のステージが対象。まずこれを消化する。</p>
            <div className="space-y-4">
              {[
                {
                  num: '①', stage: 'AIテレアポ結果', count: '1,237件', color: 'green',
                  icon: '🤖',
                  what: 'AIが電話して何らかの結果が出た先。担当者につながった・資料送付になった・また連絡する、など。',
                  how: '録音を再生するかメモを読んで、前回の話を確認してから電話する。前回の文脈を踏まえて話せるため、いちばん成果につながりやすい。',
                },
                {
                  num: '②', stage: 'IVR（突破待ち）', count: '283件', color: 'yellow',
                  icon: '📟',
                  what: '「1を押してください〜」という自動音声でAIが止まってしまった先。相手のホテルには問題なし。',
                  how: '人の手で番号を押して担当者までつなぐ。つながれば通常どおり話せる。',
                },
                {
                  num: '③', stage: 'AIへの着信折り返し', count: '49件', color: 'blue',
                  icon: '📲',
                  what: 'こちらからかけた際に出られず、相手から折り返してきた先。向こうから連絡してくれている。',
                  how: 'すぐ電話する。つながりやすく、話を聞いてもらえる可能性が高い。',
                },
                {
                  num: '④', stage: '本社及びチェーン本部（人が架電）', count: '110件', color: 'purple',
                  icon: '🏢',
                  what: '複数ホテルをまとめている本部。1件決まれば傘下ホテルにまとめて広がる可能性がある。',
                  how: 'アポインターが担当。代表電話への取り次ぎが必要で、AIでは突破できないと判断された案件。',
                },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-5 border ${
                  item.color === 'green' ? 'bg-green-950/40 border-green-800/40' :
                  item.color === 'yellow' ? 'bg-yellow-950/40 border-yellow-800/40' :
                  item.color === 'blue' ? 'bg-blue-950/40 border-blue-800/40' :
                  'bg-purple-950/40 border-purple-800/40'
                }`}>
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-2xl">{item.icon}</span>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className={`text-base font-bold ${
                          item.color === 'green' ? 'text-green-400' :
                          item.color === 'yellow' ? 'text-yellow-400' :
                          item.color === 'blue' ? 'text-blue-400' : 'text-purple-400'
                        }`}>{item.num}</span>
                        <span className="text-base font-bold text-white">{item.stage}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${
                          item.color === 'green' ? 'bg-green-800/60 text-green-300' :
                          item.color === 'yellow' ? 'bg-yellow-800/60 text-yellow-300' :
                          item.color === 'blue' ? 'bg-blue-800/60 text-blue-300' : 'bg-purple-800/60 text-purple-300'
                        }`}>{item.count}</span>
                      </div>
                    </div>
                  </div>
                  <p className="text-sm text-slate-400 mb-2">📋 {item.what}</p>
                  <p className="text-base text-slate-100">✅ {item.how}</p>
                </div>
              ))}
            </div>
          </div>

          {/* あとで */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-1">⏳ あとで — 上の4箱を消化したら</h2>
            <p className="text-sm text-slate-400 mb-4">かける先が少なくなってきたら進む</p>
            <div className="space-y-3">
              {[
                { stage: 'メルマガ配信（見込顧客）', count: '208件', desc: 'メールは送っているが、まだ電話で話せていない先' },
                { stage: '将来的見込顧客', count: '142件', desc: '今すぐではないが、いずれ可能性がある先' },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-4 bg-slate-700/50 rounded-xl p-4">
                  <div className="flex-1">
                    <p className="text-base font-bold text-white">{item.stage}</p>
                    <p className="text-sm text-slate-400 mt-0.5">{item.desc}</p>
                  </div>
                  <span className="text-sm font-bold text-slate-300 bg-slate-600 px-3 py-1 rounded-lg">{item.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* 触らなくてOK */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-1">🚫 触らなくてOK — AIが担当する箱</h2>
            <p className="text-sm text-slate-400 mb-4">電話する必要なし</p>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-slate-400 font-medium py-2 pr-4">箱の名前</th>
                    <th className="text-left text-slate-400 font-medium py-2 pr-4">件数</th>
                    <th className="text-left text-slate-400 font-medium py-2">理由</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50">
                  {[
                    { stage: 'これから架電（未架電）', count: '16,367件', reason: 'すべてAIが順番にかける' },
                    { stage: 'AIテレアポ架電中', count: '2,453件', reason: '今AIがかけている途中' },
                    { stage: '留守番電話', count: '25件', reason: '後日AIがかけ直す' },
                    { stage: '電話不出', count: '656件', reason: '何度かけても出ない。AIが再挑戦' },
                  ].map((row, i) => (
                    <tr key={i}>
                      <td className="py-2.5 pr-4 text-slate-300 font-medium">{row.stage}</td>
                      <td className="py-2.5 pr-4 text-slate-400">{row.count}</td>
                      <td className="py-2.5 text-slate-400">{row.reason}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* メモ必須ルール */}
          <div className="bg-yellow-950/40 rounded-2xl border border-yellow-700/50 p-6">
            <h2 className="text-base font-bold text-yellow-300 mb-3">⚠️ 電話後のメモ — 必須</h2>
            <p className="text-base text-slate-200 leading-relaxed mb-4">電話が終わったら、どんな話だったかを<span className="text-yellow-300 font-bold">必ずメモに残す</span>。次にかける人（AIも含む）が同じ話を繰り返さずに済み、お客様に「何度もかかってくる」と思われずに済む。</p>
            <div className="space-y-3">
              {[
                { label: 'AI結果フォロー後', text: '前回AIが話した内容を確認済み。担当者：〇〇様。今回の反応：〇〇。次のアクション：〇〇。' },
                { label: 'IVR突破後', text: 'IVR突破して担当者に接続。担当者：〇〇様。反応：〇〇。次回：〇〇。' },
                { label: '折り返し対応後', text: 'お客様から折り返しあり。担当者：〇〇様。内容：〇〇。次のアクション：〇〇。' },
                { label: '本部対応後', text: '本部（〇〇様）と話せた。傘下ホテル数：〇〇。反応：〇〇。次回：〇〇。' },
              ].map((item, i) => (
                <div key={i} className="bg-slate-800/60 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-bold text-yellow-400">{item.label}</p>
                    <button onClick={() => copy(item.text, `hs_${i}`)}
                      className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === `hs_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `hs_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                  <p className="text-base text-slate-200">{item.text}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

      {/* ─── TAB: トークスクリプト ─── */}
      {activeTab === 'script' && (
        <div className="space-y-6">

          {/* ⚡ 切り返しナビ（ボタン形式） */}
          <div className="bg-slate-800 rounded-2xl border border-blue-800/40 p-6">
            <h2 className="text-xl font-bold text-white mb-1">⚡ 切り返しナビ</h2>
            <p className="text-base text-slate-400 mb-5">相手の反応をクリック → 対応方法を選ぶ → トークが表示される</p>

            {/* カテゴリボタン */}
            <div className="flex flex-wrap gap-3 mb-5">
              {CATEGORY_ITEMS.map(cat => (
                <button key={cat.id} onClick={() => selectCat(cat.id)}
                  className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${
                    selectedCat === cat.id
                      ? 'bg-blue-600 text-white shadow-lg scale-105'
                      : 'bg-slate-700 text-slate-200 hover:bg-slate-600 hover:text-white border border-slate-600'
                  }`}>
                  {OBJECTION_TREE[cat.id]?.label}
                </button>
              ))}
            </div>

            {/* サブ選択 */}
            {selectedCat && (
              <div className="border-t border-slate-700 pt-5">
                <p className="text-base text-blue-400 font-bold mb-4">どう対応しますか？</p>
                <div className="flex flex-wrap gap-3 mb-5">
                  {CATEGORY_ITEMS.find(c => c.id === selectedCat)?.children.map(childId => (
                    <button key={childId} onClick={() => selectResponse(childId)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${
                        selectedResponse === childId
                          ? 'bg-green-600 text-white shadow-lg scale-105'
                          : 'bg-slate-700/70 text-slate-200 hover:bg-slate-600 hover:text-white border border-slate-600'
                      }`}>
                      {OBJECTION_TREE[childId]?.label}
                    </button>
                  ))}
                </div>

                {/* トーク表示 */}
                {selectedResponse && (
                  <div className="bg-green-950/60 border-2 border-green-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <p className="text-base text-green-400 font-bold">💬 切り返しトーク</p>
                      <button onClick={() => copy(OBJECTION_TREE[selectedResponse]?.response || '', 'objection')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'objection' ? 'bg-green-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'objection' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">
                      {OBJECTION_TREE[selectedResponse]?.response}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>


          {/* AI切り返し */}
          <div className="bg-slate-900 rounded-2xl border border-purple-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">🤖 AI切り返しサジェスト</h2>
              <span className="text-xs bg-purple-900/60 border border-purple-700/50 text-purple-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-base text-slate-400 mb-4">相手が言ったことをそのまま入力 → AIがデバイスエージェンシーの製品切り返しを表示</p>
            <div className="flex flex-wrap gap-2 mb-4">
              {[
                { id: 'yoneyama', label: '💰 IT補助金訴求', active: 'bg-yellow-600' },
                { id: 'price',    label: '💴 価格・コスト訴求', active: 'bg-green-600' },
                { id: 'inbound',  label: '🌏 インバウンド訴求', active: 'bg-blue-600' },
                { id: 'case',     label: '🏨 導入事例訴求', active: 'bg-purple-600' },
                { id: 'urgency',  label: '⏰ 緊急性訴求', active: 'bg-red-600' },
              ].map(p => (
                <button key={p.id} onClick={() => setAiPattern(p.id)}
                  className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === p.id ? `${p.active} text-white` : 'bg-slate-700 text-slate-300 border border-slate-600 hover:bg-slate-600'}`}>
                  {p.label}
                </button>
              ))}
            </div>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🎤</span>
                <input type="text" value={aiInput} onChange={e => setAiInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchAiSuggestions(aiInput, aiPattern)}
                  placeholder="例：「もう他社のシステム入れてます」「今は忙しくて」「高そうだな」"
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30" />
                {aiInput && <button onClick={() => { setAiInput(''); setAiSuggestions([]); setAiSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">×</button>}
              </div>
              <button
                onClick={isListening ? stopListening : startListening}
                className={`px-4 py-4 rounded-xl text-xl transition-all flex-shrink-0 ${isListening ? 'bg-red-600 text-white animate-pulse' : 'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600'}`}
                title={isListening ? '停止' : 'マイク入力'}>
                {isListening ? '⏹️' : '🎙️'}
              </button>
              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${aiLoading ? 'bg-purple-900 text-purple-400 cursor-wait' : aiInput.trim() ? 'bg-purple-600 hover:bg-purple-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {aiLoading ? '⏳ 生成中...' : '✨ AI提案'}
              </button>
            </div>
            {isListening && <div className="flex items-center gap-2 bg-red-950/40 border border-red-700/40 rounded-xl p-4 mb-4 text-base text-red-300 animate-pulse">🎙️ 音声認識中… 相手の声を聞かせてください</div>}
            {aiError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-base text-red-300">⚠️ {aiError}</div>}
            {aiLoading && <div className="text-center py-8 text-purple-400"><div className="text-2xl mb-2 animate-pulse">🤖</div><p className="text-base">Gemini AIが切り返しを生成中...</p></div>}
            {aiSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-purple-400 font-bold mb-3">💡 AI推奨切り返し ({aiSuggestions.length}件)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {aiSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setAiSelectedIdx(aiSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${aiSelectedIdx === i ? 'bg-purple-600 text-white shadow-lg scale-105' : 'bg-purple-900/50 text-purple-200 hover:bg-purple-700 hover:text-white border border-purple-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {aiSelectedIdx !== null && aiSuggestions[aiSelectedIdx] && (
                  <div className="bg-purple-950/60 border-2 border-purple-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-purple-400 font-bold">💬 {aiSuggestions[aiSelectedIdx].label}</p>
                        <p className="text-sm text-purple-300/70 mt-0.5">📌 {aiSuggestions[aiSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(aiSuggestions[aiSelectedIdx!].talk, 'ai_talk')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'ai_talk' ? 'bg-purple-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'ai_talk' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{aiSuggestions[aiSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* キーワード検索 */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-3">🔍 キーワードで切り返しを検索</h2>
            <input type="text" value={searchInput} onChange={e => setSearchInput(e.target.value)}
              placeholder="例：予算・他社・忙しい・インバウンド・補助金"
              className="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-base text-white placeholder-slate-500 focus:outline-none focus:border-blue-500" />
            {suggestions.length > 0 && (
              <div className="mt-3 space-y-2">
                {suggestions.map(id => (
                  <div key={id} className="bg-slate-700/60 rounded-xl p-4">
                    <p className="text-sm font-bold text-slate-300 mb-1">{OBJECTION_TREE[id].label}</p>
                    <div className="flex items-start gap-3">
                      <p className="text-base text-slate-200 flex-1">{OBJECTION_TREE[id].response}</p>
                      <button onClick={() => copy(OBJECTION_TREE[id].response, `search_${id}`)}
                        className={`text-xs px-3 py-1 rounded-lg flex-shrink-0 transition-colors ${copiedKey === `search_${id}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                        {copiedKey === `search_${id}` ? '✅' : '📋'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 米山パターン — トークスクリプト */}
          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <div className="flex items-center gap-3 mb-5">
              <span className="text-3xl">💰</span>
              <div>
                <h2 className="text-xl font-bold text-white">米山パターン — IT補助金全面訴求型</h2>
                <p className="text-base text-yellow-300/80 mt-0.5">政府の積極支援・補助金申請代行を前面に出し、コスト障壁を最初に取り除くアプローチ</p>
              </div>
            </div>
            <div className="space-y-4">
              {[
                {
                  label: 'STEP 1｜受付突破 — 担当者につなぐ',
                  color: 'blue',
                  text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\nホテル・旅館様向けのIT補助金のご案内でご連絡しているのですが、\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」',
                  point: 'IT補助金のご案内と言うだけで受付に止められにくくなる。「支配人様か担当者様」と二択にすることで名前がなくても取り次ぎを引き出せる。止められたら→「補助金の申請期限がありまして、担当の方に一度ご確認いただけますか」',
                },
                {
                  label: 'STEP 2｜担当者への第一声 — 自然な補助金訴求',
                  color: 'yellow',
                  text: '「ありがとうございます。実はいま国のIT補助金を使って、\n自動チェックイン機をKIOSK型なら実質48万円〜、タブレット型なら13万円〜でご導入できる制度がありまして、\n補助金の申請も弊社が全部代行しています。今日は売り込みではなく、その制度のご案内でご連絡しました。\n今、2〜3分だけよろしいでしょうか？」',
                  point: '「売り込みではなく」を明言するだけで警戒心が大きく下がる。金額（48万円〜/13万円〜）を先に言うことで「高いんでしょ」という先入観を防ぐ。「2〜3分」と時間を区切ることで断り口実を潰す。',
                },
                {
                  label: 'STEP 3｜ヒアリング — 課題を自然に引き出す',
                  color: 'purple',
                  text: '「最近、うちの周りのホテル様からも夜間の対応とかインバウンドのお客様への対応で\n大変という声をよく聞くんですが、御社では今、何か運用で課題に感じているところはありますか？」',
                  point: '具体例（夜間対応・インバウンド等）を出すことで課題を引き出しやすくなる。課題が出たら→「IT補助金で解決されているホテル様の事例があります」につなぐ。課題がなければ→メール送付に切り替える。',
                },
                {
                  label: 'STEP 4｜課題あり → 事例提案 → アポ取り',
                  color: 'green',
                  text: '「そうですよね。実は、その課題をIT補助金を使ってうまく解決されているホテル様の事例が手元にあります。\n資料と補助金の申請スケジュールをメールでお送りしてもいいですか？\nその後、15分だけいただいて、補助金を使った具体的なご説明ができればと思いまして。」',
                  point: '「資料を送る」→「15分だけ」の2段階でアポのハードルを下げる。日程は「来週の火曜か水曜、どちらがご都合よいですか？」と二択で聞く。Zoomでも可と伝えれば地方のホテルも対応できる。',
                },
                {
                  label: "STEP 4'｜課題なし → 情報だけ置いて次につなぐ",
                  color: 'slate',
                  text: '「そうですか。IT補助金って毎年申請枠があるので、タイミングが来たときのために情報だけ持っておいてもらえれば十分です。\n補助金の概要と製品の資料をメールでお送りしてもいいですか？\nメールアドレスをいただければ今日中に送ります。」',
                  point: '「資料送付 → 3週間以内に再架電」でインセンティブ対象を狙う。「今日中に送ります」と即行動を約束することで信頼感を出す。「無理に決めてもらわなくていい」→プレッシャーを外して防衛心を下げる。',
                },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-5 ${
                  item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' :
                  item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' :
                  item.color === 'purple' ? 'bg-purple-950/40 border border-purple-800/40' :
                  item.color === 'green' ? 'bg-green-950/40 border border-green-800/40' :
                  'bg-slate-700/50 border border-slate-600/40'
                }`}>
                  <div className="flex items-center justify-between mb-3">
                    <p className={`text-base font-bold ${
                      item.color === 'blue' ? 'text-blue-400' :
                      item.color === 'yellow' ? 'text-yellow-400' :
                      item.color === 'purple' ? 'text-purple-400' :
                      item.color === 'green' ? 'text-green-400' : 'text-slate-400'
                    }`}>{item.label}</p>
                    <button onClick={() => copy(item.text, `ym_${i}`)}
                      className={`text-sm px-3 py-1.5 rounded-lg font-medium transition-colors ${copiedKey === `ym_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                      {copiedKey === `ym_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                  <p className="text-base text-slate-100 leading-relaxed whitespace-pre-line mb-3">{item.text}</p>
                  <p className="text-sm text-slate-400 leading-relaxed border-t border-slate-600/50 pt-3 mb-3">💡 {item.point}</p>
                  <div className="border-t border-slate-600/40 pt-3">
                    <p className="text-xs text-slate-500 mb-1">📝 メモ（このステップの反応・気づき）</p>
                    <textarea
                      value={stepMemos[i]}
                      onChange={e => updateMemo(i, e.target.value)}
                      placeholder="例：「予算がない」と言われた。補助金で突破できた。"
                      rows={2}
                      className="w-full bg-slate-900/60 border border-slate-600/60 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 resize-none"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* IT補助金断り文句別切り返し */}
          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <h2 className="text-base font-bold text-white mb-4">🔄 断り文句別 切り返し（IT補助金訴求）</h2>
            <div className="space-y-3">
              {[
                { obj: '「予算がない」「お金がかかる」', res: '「そうですよね。実はIT補助金を活用していただくと、弊社が申請を全て代行しますので、KIOSK型が48万円〜、タブレット型が13万円〜でご導入できます。月額費用も使わない月は0円なので、繁忙期だけのご利用も可能です。資料だけでもご覧になりませんか？」' },
                { obj: '「他社製品を検討・使用中」', res: '「弊社はシリンダー錠対応・完全オーダーメイドカスタマイズという点で差別化できています。またIT補助金の申請代行は弊社の強みです。比較検討の資料としてお送りしてもよろしいでしょうか？」' },
                { obj: '「今は時期が悪い」「来年以降で」', res: '「IT補助金の申請枠は毎年更新されますので、今すぐでなくても情報だけ持っておいていただくと、タイミングが来た時にすぐ動けます。今日中に資料をメールでお送りするだけですので、メールアドレスをお教えいただけますか？」' },
                { obj: '「補助金って何ですか？」', res: '「IT導入補助金というもので、中小企業様がITシステムを導入する際に国が費用の最大2/3を補助してくれる制度です。弊社は申請手続きを全て代行しておりますので、御社は書類を揃えていただくだけでOKです。」' },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-base font-bold text-red-400 mb-2">❌ {item.obj}</p>
                  <div className="flex items-start gap-3">
                    <p className="text-base text-slate-200 leading-relaxed flex-1">✅ {item.res}</p>
                    <button onClick={() => copy(item.res, `ym_obj_${i}`)}
                      className={`text-xs px-3 py-1 rounded-lg font-medium flex-shrink-0 transition-colors ${copiedKey === `ym_obj_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `ym_obj_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

      {/* ─── TAB: ステータス一覧 ─── */}
      {activeTab === 'status' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">✅ 使用するステータス（取引ステージ）</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-base">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-slate-400 font-medium py-2 pr-4">ステータス</th>
                    <th className="text-left text-slate-400 font-medium py-2">用途</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50">
                  {[
                    { status: '楽天トラベル（未架電）', desc: 'ターゲットリスト', badge: 'blue' },
                    { status: '楽天トラベル（不在）', desc: '担当者不在時（資料送付後の不在は移動不要）', badge: 'yellow' },
                    { status: '楽天トラベル（断り）', desc: '断られた場合', badge: 'red' },
                    { status: '楽天トラベル（本社へ）', desc: '本社が決済の場合', badge: 'purple' },
                    { status: '楽天トラベル（1回目）', desc: '1回目のアプローチ', badge: 'slate' },
                    { status: '資料送付', desc: '架電後に資料送付に至った場合', badge: 'green' },
                    { status: '架電クレーム', desc: '「かけてくるな」など言われた場合', badge: 'red' },
                    { status: '架電リスト（他社製品使用）', desc: 'すでに他社製品を導入済みの場合', badge: 'slate' },
                    { status: '連絡不可・IVR', desc: '閉業や電話番号が使われていない場合', badge: 'slate' },
                    { status: 'セミナー予定', desc: 'アポイント獲得〜当日まで', badge: 'green' },
                    { status: 'セミナー参加', desc: '実際に参加した場合', badge: 'green' },
                    { status: 'セミナーキャンセル', desc: 'キャンセルが発生した場合', badge: 'red' },
                  ].map((row, i) => (
                    <tr key={i}>
                      <td className="py-3 pr-4">
                        <span className={`text-sm font-medium px-2 py-1 rounded-lg ${
                          row.badge === 'blue' ? 'bg-blue-900/60 text-blue-300' :
                          row.badge === 'green' ? 'bg-green-900/60 text-green-300' :
                          row.badge === 'yellow' ? 'bg-yellow-900/60 text-yellow-300' :
                          row.badge === 'red' ? 'bg-red-900/60 text-red-300' :
                          row.badge === 'purple' ? 'bg-purple-900/60 text-purple-300' :
                          'bg-slate-700 text-slate-300'
                        }`}>{row.status}</span>
                      </td>
                      <td className="text-slate-300 py-3 text-base">{row.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: 商品知識 ─── */}
      {activeTab === 'knowledge' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">💡 製品ラインナップ</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { name: 'KIOSK型 自動チェックイン機', price: '実質48万円〜（IT補助金適用後）', features: ['13か国語対応', 'パスポートスキャン', 'クレジット・交通系IC決済', '領収書発行', 'PMS連携'] },
                { name: 'タブレット型 自動チェックイン機', price: '実質13万円〜（IT補助金適用後）', features: ['省スペース', 'フロント補助として活用', 'シリンダー錠対応', '小規模旅館向け'] },
                { name: 'クラウドスマートロック', price: '別途見積もり', features: ['暗証番号で開錠', 'スマホアプリ対応', 'シリンダー錠も可', '遠隔管理'] },
                { name: 'ルームタブレット', price: '別途見積もり', features: ['客室内電話代替', 'アメニティ注文', 'チェックアウト対応', '多言語対応'] },
              ].map((p, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-5 border border-slate-600">
                  <p className="text-base font-bold text-white mb-1">{p.name}</p>
                  <p className="text-yellow-400 text-sm font-bold mb-3">{p.price}</p>
                  <ul className="space-y-1">
                    {p.features.map((f, j) => (
                      <li key={j} className="text-base text-slate-300 flex items-center gap-2">
                        <span className="text-green-400 text-xs">✓</span> {f}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">🔑 訴求ポイント（必ず覚える）</h2>
            <div className="space-y-3">
              {[
                { icon: '💰', title: 'IT補助金申請代行', desc: '中小企業デジタル化補助金・IT導入補助金を活用。最大2/3補助。申請手続きは弊社が全て代行。' },
                { icon: '🌏', title: '13か国語対応', desc: 'インバウンド対策に最適。パスポートスキャン機能で外国人チェックインもスムーズ。' },
                { icon: '🔧', title: '完全オーダーメイド', desc: '自社開発のためカスタマイズ自由。PMS連携実績：ステイシー・スイートブック・ベッド4。' },
                { icon: '📅', title: '月額0円プラン', desc: '使わない期間は月額0円。季節限定利用OK。閑散期のコスト負担なし。' },
                { icon: '📹', title: '無料セミナー', desc: '毎週水曜11時・金曜13時。Zoomで無料参加可。全国対応。' },
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-4 p-4 bg-slate-700/40 rounded-xl">
                  <span className="text-2xl flex-shrink-0">{item.icon}</span>
                  <div>
                    <p className="text-base font-bold text-white">{item.title}</p>
                    <p className="text-base text-slate-300 mt-1">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: チェックリスト ─── */}
      {activeTab === 'checklist' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">✅ 架電前チェックリスト</h2>
            <div className="space-y-2">
              {[
                '施設名・電話番号・過去の接触履歴をHubSpotで確認した',
                'トークスクリプトを一度声に出して確認した',
                'Zoomなど架電ツールが起動している',
                'メモ帳（HubSpot）を開いている',
                '資料送付用のメールテンプレートを準備している',
                'セミナー日程（今週分）を把握している',
              ].map((item, i) => (
                <label key={i} className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-700/40 cursor-pointer">
                  <input type="checkbox" className="w-5 h-5 rounded accent-blue-500" />
                  <span className="text-base text-slate-200">{item}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">✅ 架電後チェックリスト</h2>
            <div className="space-y-2">
              {[
                'HubSpotのステータスを更新した',
                '担当者名・反応・次のアクションをメモした',
                '資料送付の場合：メールを今日中に送った',
                'アポ獲得の場合：セミナーURLをメールで送った',
                '断りの場合：「楽天トラベル（断り）」に変更した',
              ].map((item, i) => (
                <label key={i} className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-700/40 cursor-pointer">
                  <input type="checkbox" className="w-5 h-5 rounded accent-blue-500" />
                  <span className="text-base text-slate-200">{item}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: メールテンプレ ─── */}
      {activeTab === 'mail' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">✉️ メールテンプレート</h2>
            <div className="space-y-4">
              {[
                {
                  label: '資料送付メール',
                  subject: '【IT補助金活用】自動チェックイン機のご案内 / デバイスエージェンシー',
                  body: `〇〇様

先ほどはお電話ありがとうございました。
デバイスエージェンシーの米山でございます。

ご案内いたしました自動チェックイン機の資料をお送りします。

【製品概要】
・KIOSK型：IT補助金適用後 実質48万円〜
・タブレット型：IT補助金適用後 実質13万円〜
・補助金申請は弊社が全て代行
・13か国語対応・使わない月は月額0円

【無料セミナーのご案内】
毎週水曜11時・金曜13時（Zoom・無料）
ご都合のよい日時をお教えください。

ご不明点がありましたらお気軽にご連絡ください。

─────────────────────────
株式会社デバイスエージェンシー
米山 文貴
TEL: 080-3207-8422
─────────────────────────`,
                },
                {
                  label: 'セミナー案内メール',
                  subject: '【無料セミナーご案内】自動チェックイン機 × IT補助金 / デバイスエージェンシー',
                  body: `〇〇様

この度はセミナーへのご参加ありがとうございます。
デバイスエージェンシーの米山でございます。

以下の日時でZoomセミナーを開催いたします。

【セミナー詳細】
日時：〇月〇日（〇）〇〇:〇〇〜
形式：Zoom（オンライン・無料）
内容：IT補助金活用方法 / 製品デモ / Q&A

ZoomミーティングURL：
https://us02web.zoom.us/j/XXXXXXXXXX

ご参加をお待ちしております。

─────────────────────────
株式会社デバイスエージェンシー
米山 文貴
─────────────────────────`,
                },
              ].map((tmpl, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-5">
                  <div className="flex items-center justify-between mb-3">
                    <p className="text-base font-bold text-white">{tmpl.label}</p>
                    <div className="flex gap-2">
                      <button onClick={() => copy(tmpl.subject, `subj_${i}`)}
                        className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${copiedKey === `subj_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                        {copiedKey === `subj_${i}` ? '✅件名' : '📋 件名'}
                      </button>
                      <button onClick={() => copy(tmpl.body, `body_${i}`)}
                        className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${copiedKey === `body_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                        {copiedKey === `body_${i}` ? '✅本文' : '📋 本文'}
                      </button>
                    </div>
                  </div>
                  <p className="text-sm text-slate-400 mb-1">件名：</p>
                  <p className="text-base text-blue-300 mb-3">{tmpl.subject}</p>
                  <pre className="text-base text-slate-200 leading-relaxed whitespace-pre-wrap font-sans">{tmpl.body}</pre>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  )
}
