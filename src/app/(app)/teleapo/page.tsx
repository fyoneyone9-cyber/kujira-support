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

  // ── PMSメーカー名 ──
  'cat_pmsname':     { label: '🖥️ PMSメーカー名が出てきた', response: '' },
  'pmsname_nehops':  { label: 'NEHOPS（NEC）', response: '「NECのNEHOPS（ネホップス）ですね。承知しました。連携実績も増えており、弊社からメーカーへ連携依頼することも可能です。ぜひ一度ご相談させてください。」' },
  'pmsname_glovia':  { label: 'GLOVIA smart（富士通）', response: '「富士通のGLOVIA smartですね。承知しました。弊社はリストにないPMSでも諦めず、メーカーへ直接連携依頼して進めております。詳しくはご相談ください。」' },
  'pmsname_wincal':  { label: 'Wincal（アルメックス）', response: '「アルメックス（USEN-ALME）のWincalですね。正直にお伝えすると、アルメックスの場合は基本的にPMSを乗り換えていただくしか連携の方法がない状況です。乗り換えのご検討が可能であればご提供できますが、現状のシステムは変えたくないということであれば、弊社からのご提案自体が難しくなります。その点だけご確認させていただけますか。」' },
  'pmsname_staysee': { label: 'Staysee / AirHost / Beds24', response: '「はい、連携実績がございます。弊社との連携をスムーズに進めることができます。詳しい資料をお送りしてもよろしいでしょうか。」' },
  'pmsname_airhost': { label: 'エアホスト', response: '「エアホストですね。対応しております。PMS・サイトコントローラー問わず対応できますので、ぜひ詳しくお話しさせてください。」' },
  'pmsname_neppan':  { label: 'ねっぱん！', response: '「ねっぱん！はサイトコントローラー版とPMS版がありますが、どちらをお使いでしょうか。2026年1月に楽天トラベルサービスへ合併・改称されましたね。いずれも連携について弊社からご対応できます。」' },
  'pmsname_unknown': { label: '対応リストにないPMS', response: '「リストに載っていないPMSでも諦めません。サイトコントローラー経由でつながるケースも多く、弊社からメーカーへ連携依頼して進めることも可能です。システム名を教えていただけますか？」' },

  // ── 鍵・スマートロック ──
  'cat_locktype':    { label: '🔐 鍵・スマートロックの話題', response: '' },
  'locktype_miwa':   { label: 'MIWAが入っている', response: '「MIWA（美和ロック）ですね。カードロックとスマートロック両方のラインナップがあります。MIWAのスマートロックであれば連携対応可能です。今お使いの機種を確認させていただけますか？」' },
  'locktype_epic':   { label: 'EPICが入っている', response: '「EPICは株式会社エナスピレーションの製品で、カードロックになります。スマートロックとして暗証番号開錠はできませんが、チェックイン機との連携によりカードキー発行の自動化が可能です。」' },
  'locktype_remote': { label: 'RemoteLockが入っている', response: '「RemoteLockは構造計画研究所の製品です。日本の窓口はリモートロックジャパンへ移管されていますね。スマートロック対応ですので、チェックイン機との連携が可能です。」' },
  'locktype_nochange':{ label: '鍵を変えたくない', response: '「今の鍵はそのままで大丈夫です。シリンダー錠の場合はキーボックスをご活用いただき、精算完了後に自動でキーボックスが開く運用が可能です。工事も不要です。」' },
  'locktype_keybox': { label: 'キーボックスの工事が心配', response: '「キーボックスは既存のシリンダー錠をそのままキーボックスに入れるだけです。錠前の交換工事は不要で、壁への取り付けのみです。工事の負担は最小限です。」' },

  // ── 運用・機能 ──
  'cat_operation':   { label: '⚙️ 運用・機能の質問', response: '' },
  'ope_unmanned_mode':{ label: '夜だけ無人にしたい', response: '「無人モードのON/OFFを切り替えることができます。昼間はフロント対応、夜間は端末をメインにする運用も可能です。柔軟にご活用いただけます。」' },
  'ope_checkin_search':{ label: '予約番号を覚えていない客', response: '「予約番号以外にも、お名前・電話番号・メールアドレス・チェックイン日の4通りで検索できます。予約番号がわからないお客様にも対応可能です。」' },
  'ope_id_check':    { label: '本人確認が心配', response: '「本人確認画面が表示され、DMSからスタッフがビデオ通話で承認する仕組みがあります。完全な無人でも本人確認が可能です。」' },
  'ope_cardkey_num': { label: 'カードキーを複数枚出したい', response: '「発行枚数は施設様が自由に設定できます。グループ客など複数名への配布にも対応しています。」' },
  'ope_group':       { label: '団体客・グループの対応', response: '「事前チェックインで代表者様が同行者の分を代理入力できます。また簡易チェックイン機能で代表者以外の入力を省略することも可能です。」' },
  'ope_passport_jp': { label: '日本在住外国人のパスポート', response: '「日本にお住まいの外国籍の方はパスポート撮影をスキップできる設定が可能です。毎回嫌な顔をされるというお悩みも解消できます。」' },
  'ope_kessai':      { label: '決済・精算の方法', response: '「現金・クレジットカード・交通系ICに対応しています。また前日精算や客室精算など精算タイミングも柔軟に設定できます。」' },
  'ope_invoice':     { label: '領収書の再発行', response: '「DMSの管理画面から該当予約を開き、いつでも再発行できます。宛名の省略設定も可能です。」' },
  'ope_stat':        { label: '宿泊旅行統計調査', response: '「宿泊実績定期報告の機能があり、統計調査用のデータをDMSから出力できます。手集計は不要になります。」' },
  'ope_network':     { label: 'LANがない・回線がない', response: '「有線・無線どちらでも構いません。また回線工事が難しい場所には弊社のLTE SIMをご活用いただくことで、回線工事なしで接続できます。固定IPも不要です。」' },
  'ope_season':      { label: '季節営業・閑散期', response: '「シーズン営業のご利用が可能です。動かさない月は月額保守費用を停止できます。ただし端末メーカーへの保守費用は別途かかります。完全にゼロにはなりません。」' },
  'ope_checkout_rush': { label: '朝チェックアウトで混む', response: '「QRコードをお部屋に掲示しておくだけで、お客様がスマホで読み取ってチェックアウトを完了できます。フロントに来る必要がなくなり、朝の混雑が大幅に解消されます。精算なし物件またはチェックイン時精算が前提です。」' },
  'ope_before_checkout': { label: '精算がチェックアウト時に集中する', response: '「前日精算の機能があり、チェックアウト当日ではなく前日に精算を済ませていただく運用が可能です。朝の精算集中を分散でき、チェックアウト時の待ち行列を解消できます。」' },
  'ope_identity':    { label: '本人確認はどうするの（無人時）', response: '「無人モードONのとき、お客様が個人情報を入力し終えるとDMS（管理画面）に呼び出し画面が表示され、スタッフがビデオ通話で対応します。撮影した顔写真をパスポート写真と照合し、「承認する」を押して完了です。現地に人はいませんが、確認する人はいます。」' },
  'ope_kiosk_explain': { label: '「要するに精算機でしょ？」と言われた', response: '「精算は機能の一部です。チェックイン・宿泊者名簿の電子化・鍵の自動発行・多言語対応・統計レポートまで一台に集約できます。精算機との一番の違いは「フロント業務全体を代替できる」点です。」' },
  'ope_deepnight':   { label: '深夜のチェックインが心配', response: '「無人モードをONにして端末を置いておくだけで、深夜でもお客様が自力でチェックイン・精算・鍵の受け取りまで完結できます。スタッフがいなくても完全対応可能です。」' },
  'ope_tourist_stat': { label: '宿泊旅行統計調査が大変', response: '「宿泊実績定期報告の機能があります。チェックインデータから自動で集計でき、DMSから出力するだけです。手集計で丸一日かかっていた作業が不要になります。」' },
  'ope_card_checkin': { label: 'カード読み取りでチェックイン', response: '「カード読み取りアプリを使うと、カードキーをかざすだけで朝食付きかどうかなどお客様の情報が確認できます。スタッフが宿泊者リストを都度確認する手間が省けます。」' },
  'ope_almex_connect': { label: 'アルメックスとの連携はできる？', response: '「アルメックスの場合は、基本的にPMSの乗り換えが前提になります。他のPMSのように弊社からメーカーへ連携依頼を進めることが難しい唯一の例外です。PMSの乗り換えが可能であればご提供できますが、現状維持の場合は残念ながらご提案が難しくなります。」' },
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
  { id: 'cat_pmsname',     children: ['pmsname_nehops', 'pmsname_glovia', 'pmsname_wincal', 'pmsname_staysee', 'pmsname_airhost', 'pmsname_neppan', 'pmsname_unknown'] },
  { id: 'cat_locktype',    children: ['locktype_miwa', 'locktype_epic', 'locktype_remote', 'locktype_nochange', 'locktype_keybox'] },
  { id: 'cat_operation',   children: ['ope_unmanned_mode', 'ope_checkin_search', 'ope_id_check', 'ope_identity', 'ope_cardkey_num', 'ope_group', 'ope_passport_jp', 'ope_kessai', 'ope_invoice', 'ope_stat', 'ope_network', 'ope_season', 'ope_checkout_rush', 'ope_before_checkout', 'ope_kiosk_explain', 'ope_deepnight', 'ope_tourist_stat', 'ope_card_checkin', 'ope_almex_connect'] },
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
  { keywords: ['朝チェックアウト', 'チェックアウトで混む', 'チェックアウト渋滞', 'チェックアウト時間', '朝混む'],
    ids: ['ope_checkout_rush', 'ope_before_checkout'] },
  { keywords: ['精算が集中', '精算が混む', '精算待ち', '前日精算'],
    ids: ['ope_before_checkout', 'ope_checkout_rush'] },
  { keywords: ['深夜', '夜中', '夜遅い', '0時', '深夜対応', '夜間'],
    ids: ['ope_deepnight', 'unmanned_night'] },
  { keywords: ['精算機', '自動精算機', 'それだけ', '要するに', 'ただの'],
    ids: ['ope_kiosk_explain'] },
  { keywords: ['本人確認', '誰でも入れる', '不法', '無人で確認', 'ID確認'],
    ids: ['ope_identity', 'ope_id_check'] },
  { keywords: ['アルメックス', 'Wincal', 'ウィンカル', 'USEN'],
    ids: ['ope_almex_connect', 'pmsname_wincal'] },
  { keywords: ['統計', '宿泊統計', '統計調査', '手集計', '宿泊旅行'],
    ids: ['ope_tourist_stat', 'ope_stat'] },
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
  { id: 'mail',     label: '✉️ メールテンプレ' },
]

const MEMO_CATEGORIES = [
  { id: 'subsidy',   label: '💰 補助金' },
  { id: 'objection', label: '🔄 断り切り返し' },
  { id: 'pms',       label: '💻 PMS・システム' },
  { id: 'script',    label: '📞 トーク気づき' },
  { id: 'other',     label: '📌 その他' },
]

type TeleapoMemo = { id: string; content: string; category: string; created_at: string }

export default function TeleapoPage() {
  const [activeTab, setActiveTab] = useState('script')
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
  const [stepNavOpen, setStepNavOpen] = useState<boolean[]>([true, false, false, false, false])
  const toggleStepNav = (i: number) => setStepNavOpen(prev => prev.map((v, idx) => idx === i ? !v : v))
  const [ymPattern, setYmPattern] = useState<number>(0)

  // ── ホテル分析 ──
  const [hotelInput, setHotelInput] = useState('')
  const [hotelAnalyzing, setHotelAnalyzing] = useState(false)
  const [hotelResult, setHotelResult] = useState<{
    recommended: string[]
    reason: string
    issues: string[]
    opening: string
    tips: string
    steps?: {
      step1?: string
      step2?: string
      step3?: string
      step4?: string
      step4b?: string
    }
  } | null>(null)
  const [hotelError, setHotelError] = useState<string | null>(null)

  const analyzeHotel = async () => {
    if (!hotelInput.trim()) return
    setHotelAnalyzing(true)
    setHotelResult(null)
    setHotelError(null)
    try {
      const res = await fetch('/api/ai/hotel-analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: hotelInput }),
      })
      const data = await res.json()
      if (data.error) setHotelError(data.error)
      else setHotelResult(data)
    } catch {
      setHotelError('通信エラーが発生しました')
    } finally {
      setHotelAnalyzing(false)
    }
  }
  const [stepSearch, setStepSearch] = useState<string[]>(['', '', '', '', ''])
  const updateStepSearch = (i: number, val: string) => setStepSearch(prev => prev.map((v, idx) => idx === i ? val : v))
  const [stepMemoInput, setStepMemoInput] = useState<string[]>(['', '', '', '', ''])
  const updateStepMemoInput = (i: number, val: string) => setStepMemoInput(prev => prev.map((v, idx) => idx === i ? val : v))
  const [stepMemoSaving, setStepMemoSaving] = useState<boolean[]>([false, false, false, false, false])
  const saveStepMemo = async (i: number, stepLabel: string) => {
    const content = stepMemoInput[i].trim()
    if (!content) return
    setStepMemoSaving(prev => prev.map((v, idx) => idx === i ? true : v))
    try {
      await fetch('/api/teleapo-memo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: `[${stepLabel}] ${content}`, category: 'script' }),
      })
      updateStepMemoInput(i, '')
    } finally {
      setStepMemoSaving(prev => prev.map((v, idx) => idx === i ? false : v))
    }
  }

  // ── ノウハウメモ ──
  const [memos, setMemos] = useState<TeleapoMemo[]>([])
  const [memosLoaded, setMemosLoaded] = useState(false)
  const [memoInput, setMemoInput] = useState('')
  const [memoCat, setMemoCat] = useState('other')
  const [memoSaving, setMemoSaving] = useState(false)
  const [memoFilter, setMemoFilter] = useState('all')

  const loadMemos = useCallback(async () => {
    const res = await fetch('/api/teleapo-memo')
    if (!res.ok) return
    const data = await res.json()
    setMemos(data.memos ?? [])
    setMemosLoaded(true)
  }, [])

  const saveMemo = useCallback(async () => {
    if (!memoInput.trim()) return
    setMemoSaving(true)
    try {
      const res = await fetch('/api/teleapo-memo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: memoInput, category: memoCat }),
      })
      if (res.ok) {
        const data = await res.json()
        setMemos(prev => [data.memo, ...prev])
        setMemoInput('')
      }
    } finally {
      setMemoSaving(false)
    }
  }, [memoInput, memoCat])

  const deleteMemo = useCallback(async (id: string) => {
    await fetch('/api/teleapo-memo', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id }),
    })
    setMemos(prev => prev.filter(m => m.id !== id))
  }, [])

  useEffect(() => {
    if (activeTab === 'memo' && !memosLoaded) loadMemos()
  }, [activeTab, memosLoaded, loadMemos])

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
        if (transcript.trim().length >= 80) {
          fetchAiSuggestions(transcript, aiPattern)
        }
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

          {/* ホテル分析 */}
          <div className="bg-slate-800 rounded-2xl border border-cyan-800/40 p-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">🏨</span>
              <div>
                <h2 className="text-xl font-bold text-white">ホテル分析 — 最適アプローチ提案</h2>
                <p className="text-sm text-cyan-300/70 mt-0.5">ホテル名またはURLを入力すると、AIが最適な営業パターンと口コミ課題を分析します</p>
              </div>
            </div>
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                value={hotelInput}
                onChange={e => setHotelInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && analyzeHotel()}
                placeholder="例：ホテル〇〇 海老名 または https://..."
                className="flex-1 bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-base text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
              />
              <button onClick={analyzeHotel} disabled={hotelAnalyzing || !hotelInput.trim()}
                className="px-5 py-3 bg-cyan-700 hover:bg-cyan-600 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-xl font-bold transition-colors text-base whitespace-nowrap">
                {hotelAnalyzing ? '⏳ 分析中...' : '🔍 分析'}
              </button>
            </div>

            {hotelAnalyzing && (
              <div className="text-center py-6 text-cyan-400 animate-pulse">
                <div className="text-3xl mb-2">🤖</div>
                <p className="text-base">口コミ・サイト情報を収集してAI分析中...</p>
              </div>
            )}

            {hotelError && (
              <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 text-red-300 text-base">⚠️ {hotelError}</div>
            )}

            {hotelResult && (
              <div className="space-y-4">
                {/* 推奨パターン */}
                <div className="bg-cyan-950/40 border border-cyan-700/40 rounded-xl p-4">
                  <p className="text-sm font-bold text-cyan-400 mb-3">🎯 推奨アプローチ（おすすめ順）</p>
                  <div className="flex flex-col gap-3 mb-3">
                    {hotelResult.recommended.map((r, ri) => {
                      const patternMap: Record<string, number> = {
                        'IT補助金': 0, '補助金全面': 0,
                        'インバウンド': 1,
                        '競合': 2, '乗り換え': 2,
                        '導入事例': 3, '数字': 3,
                        '宿泊名簿': 4, '本人確認': 4,
                        '夜間': 5, '無人': 5,
                      }
                      const patIdx = Object.entries(patternMap).find(([k]) => r.includes(k))?.[1] ?? -1
                      const rankLabels = ['🥇 第1位', '🥈 第2位', '🥉 第3位']
                      const rankColors = [
                        'bg-yellow-500 text-slate-900',
                        'bg-slate-400 text-slate-900',
                        'bg-orange-700 text-white',
                      ]
                      return (
                        <div key={ri} className="flex items-center gap-3">
                          <span className={`text-xs font-black px-2 py-1 rounded-lg whitespace-nowrap ${rankColors[ri] ?? 'bg-slate-600 text-white'}`}>
                            {rankLabels[ri] ?? `第${ri + 1}位`}
                          </span>
                          <span className="px-3 py-1.5 bg-cyan-700 text-white rounded-lg text-sm font-bold flex-1">{r}</span>
                          {patIdx >= 0 && (
                            <button
                              onClick={() => { setYmPattern(patIdx); const el = document.getElementById('ym-pattern-section'); el?.scrollIntoView({ behavior: 'smooth' }) }}
                              className="px-3 py-1.5 bg-yellow-600 hover:bg-yellow-500 text-white rounded-lg text-sm font-bold transition-colors whitespace-nowrap">
                              架電 ↓
                            </button>
                          )}
                        </div>
                      )
                    })}
                  </div>
                  <p className="text-base text-slate-200 leading-relaxed">{hotelResult.reason}</p>
                </div>

                {/* 口コミから見えた課題 */}
                {hotelResult.issues?.length > 0 && (
                  <div className="bg-red-950/30 border border-red-700/30 rounded-xl p-4">
                    <p className="text-sm font-bold text-red-400 mb-2">⚠️ 口コミ・情報から見えた課題</p>
                    <ul className="space-y-1">
                      {hotelResult.issues.map((issue, i) => (
                        <li key={i} className="text-base text-slate-200 flex items-start gap-2">
                          <span className="text-red-400 flex-shrink-0">•</span>{issue}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* カスタムトーク */}
                <div className="bg-green-950/40 border border-green-700/40 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-bold text-green-400">💬 このホテル専用 受付突破トーク</p>
                    <button onClick={() => copy(hotelResult.opening, 'hotel_opening')}
                      className={`text-xs px-3 py-1.5 rounded-lg font-bold transition-colors ${copiedKey === 'hotel_opening' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                      {copiedKey === 'hotel_opening' ? '✅' : '📋 コピー'}
                    </button>
                  </div>
                  <p className="text-base text-white leading-relaxed whitespace-pre-wrap">{hotelResult.opening}</p>
                </div>

                {/* 注意ポイント */}
                <div className="bg-yellow-950/30 border border-yellow-700/30 rounded-xl p-4">
                  <p className="text-sm font-bold text-yellow-400 mb-1">💡 架電時の注意ポイント</p>
                  <p className="text-base text-slate-200 leading-relaxed">{hotelResult.tips}</p>
                </div>
              </div>
            )}
          </div>

          {/* 米山パターン — トークスクリプト */}
          {(() => {
            const YM_PATTERNS = [
              {
                name: '💰 IT補助金全面訴求型',
                desc: '政府の積極支援・補助金申請代行を前面に出し、コスト障壁を最初に取り除くアプローチ',
                steps: [
                  { label: 'STEP 1｜受付突破', color: 'blue',
                    text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\nホテル・旅館様向けのIT補助金のご案内でご連絡しているのですが、\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」',
                    point: 'IT補助金のご案内と言うだけで受付に止められにくくなる。「支配人様か担当者様」と二択にすることで名前がなくても取り次ぎを引き出せる。止められたら→「補助金の申請期限がありまして、担当の方に一度ご確認いただけますか」' },
                  { label: 'STEP 2｜担当者への第一声', color: 'yellow',
                    text: '「ありがとうございます。実はいま国のIT補助金を使って、\n自動チェックイン機をKIOSK型なら実質48万円〜、タブレット型なら13万円〜でご導入できる制度がありまして、\n補助金の申請も弊社が全部代行しています。今日は売り込みではなく、その制度のご案内でご連絡しました。\n今、2〜3分だけよろしいでしょうか？」',
                    point: '「売り込みではなく」を明言するだけで警戒心が大きく下がる。金額を先に言うことで「高いんでしょ」という先入観を防ぐ。「2〜3分」と時間を区切ることで断り口実を潰す。' },
                  { label: 'STEP 3｜ヒアリング', color: 'purple',
                    text: '「最近、うちの周りのホテル様からも夜間の対応とかインバウンドのお客様への対応で\n大変という声をよく聞くんですが、御社では今、何か運用で課題に感じているところはありますか？」',
                    point: '具体例（夜間対応・インバウンド等）を出すことで課題を引き出しやすくなる。課題が出たら→「IT補助金で解決されているホテル様の事例があります」につなぐ。課題がなければ→メール送付に切り替える。' },
                  { label: 'STEP 4｜課題あり → アポ取り', color: 'green',
                    text: '「そうですよね。実は、その課題をIT補助金を使ってうまく解決されているホテル様の事例が手元にあります。\n資料と補助金の申請スケジュールをメールでお送りしてもいいですか？\nその後、15分だけいただいて、補助金を使った具体的なご説明ができればと思いまして。」',
                    point: '「資料を送る」→「15分だけ」の2段階でアポのハードルを下げる。日程は「来週の火曜か水曜、どちらがご都合よいですか？」と二択で聞く。' },
                  { label: "STEP 4'｜課題なし → 情報置き", color: 'slate',
                    text: '「そうですか。IT補助金って毎年申請枠があるので、タイミングが来たときのために情報だけ持っておいてもらえれば十分です。\n補助金の概要と製品の資料をメールでお送りしてもいいですか？\nメールアドレスをいただければ今日中に送ります。」',
                    point: '「資料送付 → 3週間以内に再架電」でインセンティブ対象を狙う。「今日中に送ります」と即行動を約束することで信頼感を出す。' },
                ],
              },
              {
                name: '🏨 インバウンド課題共感型',
                desc: '外国人客対応の苦労に共感してから製品メリットを提示。インバウンドが多い施設に刺さる。',
                steps: [
                  { label: 'STEP 1｜受付突破', color: 'blue',
                    text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\nインバウンドのお客様対応についてご案内があってお電話しているのですが、\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」',
                    point: '「インバウンド対応」は今どの施設も頭を悩ませているキーワード。受付の方も共感しやすく取り次いでもらいやすい。' },
                  { label: 'STEP 2｜共感で入る', color: 'yellow',
                    text: '「ありがとうございます。最近、外国人のお客様が増えて、言葉の壁でチェックイン対応に時間がかかるというお声をよく伺うのですが、御社でもそういった場面はありますか？」',
                    point: 'まず相手に話させる。「ある」と言えばそのまま課題→提案へ。「ない」と言えば「実は13か国語対応で今後のインバウンド増加にも備えられる」と将来訴求へ切り替える。' },
                  { label: 'STEP 3｜13か国語対応訴求', color: 'purple',
                    text: '「弊社の自動チェックイン機は13か国語に対応しておりまして、パスポートをかざすだけで外国人のお客様も自分でチェックインできる仕組みになっています。\nスタッフの方が英語や中国語を話せなくても対応できます。\nIT補助金を使うと実質13万円〜でご導入できるのですが、資料だけでも見ていただけますか？」',
                    point: '「スタッフが語学堪能でなくてもOK」は強い訴求点。実際の導入事例（インバウンド比率が高い地域の施設）があれば添えると説得力が増す。' },
                  { label: 'STEP 4｜セミナーへ誘導', color: 'green',
                    text: '「毎週水曜11時・金曜13時にZoomで無料セミナーを開催しています。\n30分ほどで実際の画面操作もご覧いただけますので、ご都合のよい日程はございますか？\nオンラインですので全国どこからでもご参加いただけます。」',
                    point: 'セミナーへの誘導は「アポ」より心理的ハードルが低い。「勉強会として」と伝えると参加しやすくなる。' },
                  { label: "STEP 4'｜資料送付で締め", color: 'slate',
                    text: '「では、13か国語対応の機能説明とインバウンド対応事例をまとめた資料をお送りします。\nメールアドレスをいただければ今日中にお送りしますので、お時間のある時にご覧いただけますか？」',
                    point: '資料にはパスポートスキャン・多言語対応のスクリーンショットを入れると視覚的に伝わりやすい。' },
                ],
              },
              {
                name: '🆚 競合比較・乗り換え訴求型',
                desc: '他社システムを使っている施設への切り口。「比較するだけ」のハードルで入り込む。',
                steps: [
                  { label: 'STEP 1｜受付突破', color: 'blue',
                    text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\n自動チェックイン機のご利用状況についてご確認でお電話しているのですが、\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」',
                    point: '「ご利用状況の確認」という言い方で「すでに他社使ってます」という返答を想定済みのスタンスを取る。' },
                  { label: 'STEP 2｜他社利用を確認', color: 'yellow',
                    text: '「ありがとうございます。現在、自動チェックイン機やスマートロックは何かご利用でしょうか？\nもしすでにご利用であれば、比較のご参考として弊社の料金と機能をお伝えするだけでも構いません。」',
                    point: '「すでに使ってます」→「比較の参考に」で会話を続ける。「使っていない」→補助金訴求型に切り替える。' },
                  { label: 'STEP 3｜差別化3点訴求', color: 'purple',
                    text: '「弊社は①完全オーダーメイドのカスタマイズ対応、②月額0円の閑散期プラン、③IT補助金申請の完全代行という3点で、既存の製品と差別化しています。\n特に月額費用を使わない月は0円にできる点は、他社にはほぼない仕組みです。\n今の月額費用と比較してみてもいいですか？」',
                    point: '「月額0円」は強烈な差別化ポイント。「今の費用より安くなるかもしれない」という期待感で話を続けてもらう。' },
                  { label: 'STEP 4｜乗り換え前提のアポ', color: 'green',
                    text: '「契約期間がいつ終わるかによりますが、次の更新前に一度比較していただくのが一番です。\n15分だけZoomで実際の画面をお見せすることもできますが、いかがでしょうか？\n来週の火曜か水曜はいかがですか？」',
                    point: '「契約更新前に情報収集」という文脈で会うことの合理性を作る。今すぐ乗り換えとは言わず、選択肢を広げるだけと伝える。' },
                  { label: "STEP 4'｜情報置きで締め", color: 'slate',
                    text: '「では、他社との機能・価格比較表をまとめた資料をお送りします。\n今すぐ変える必要はありませんが、次の更新タイミングで選択肢に入れていただければ十分です。\nメールアドレスをいただけますか？」',
                    point: '比較表は「弊社が勝っている点」を視覚的に並べる。PMS連携実績・補助金代行・月額0円の3点を軸にする。' },
                ],
              },
              {
                name: '📊 導入事例・数字訴求型',
                desc: '「実際に導入した施設の結果」から入るROI重視アプローチ。決裁権者への刺さりが強い。',
                steps: [
                  { label: 'STEP 1｜受付突破', color: 'blue',
                    text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\nチェックイン業務の省人化についてご案内があってお電話しているのですが、\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」',
                    point: '「省人化」は経営層に刺さるキーワード。人件費削減・スタッフ配置見直しを考えている施設に響きやすい。' },
                  { label: 'STEP 2｜事例から入る', color: 'yellow',
                    text: '「ありがとうございます。先月も神奈川県のホテル様に自動チェックイン機をご導入いただいたのですが、\nフロントの夜間対応スタッフをゼロにできて、月30万円以上のコスト削減になったとご報告いただきました。\n御社でも夜間フロントのコストは課題になっていますか？」',
                    point: '具体的な地域・数字を出すことで信憑性が上がる。「ゼロにできた」という結果は強い。施設規模や地域が近いほど刺さる。' },
                  { label: 'STEP 3｜ROI計算を一緒にする', color: 'purple',
                    text: '「例えばフロントスタッフが夜間に1名いる場合、時給1,200円×8時間×30日で月28万円以上かかります。\nIT補助金でKIOSK型を実質48万円でご導入いただくと、2か月以内に回収できる計算になります。\n御社の今の夜間体制はどのような感じですか？」',
                    point: '「2か月で回収」という数字はインパクトが大きい。相手の実情を聞きながら、その施設専用の数字にカスタマイズすると説得力が増す。' },
                  { label: 'STEP 4｜事例資料 → アポ', color: 'green',
                    text: '「実際の導入事例（コスト削減額・スタッフ配置の変化）をまとめた資料があります。\nお送りした上で、具体的な導入シミュレーションを15分でご説明できればと思いますが、いかがでしょうか？」',
                    point: '「シミュレーション」という言葉でアポの目的を具体化する。「見積もり」より心理的ハードルが低い。' },
                  { label: "STEP 4'｜数字だけ置いて次へ", color: 'slate',
                    text: '「では、導入事例と月別コスト比較表をメールでお送りします。\n数字で見ていただく方が分かりやすいと思いますので、ご確認いただけましたら、また改めてご連絡してもよろしいでしょうか？」',
                    point: '再架電の許可を取ることが重要。「また改めて」と言うことで次回の架電を断りにくくする。' },
                ],
              },
              {
                name: '📋 宿泊名簿・本人確認DX型',
                desc: '手書き名簿・身分証コピーなどアナログ業務のDX化から入る。法令対応・業務効率化に刺さる。',
                steps: [
                  { label: 'STEP 1｜受付突破', color: 'blue',
                    text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\n宿泊者名簿のデジタル化についてご案内があってお電話しているのですが、\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」',
                    point: '「宿泊者名簿」は旅館業法の義務。「デジタル化」という言葉は義務対応＋効率化の両方に響く。担当者にも刺さりやすい。' },
                  { label: 'STEP 2｜手書き名簿の課題に共感', color: 'yellow',
                    text: '「ありがとうございます。旅館業法で宿泊者名簿の管理が義務になっていますが、まだ紙・手書きで対応されているホテル様も多くて、管理の手間や紛失リスクを心配されているお声をよくお聞きします。御社ではどのような形で名簿を管理されていますか？」',
                    point: '法的義務（旅館業法）に触れることで「他人事」から「自分事」にする。現状を聞くことで課題が自然に出てくる。' },
                  { label: 'STEP 3｜システム自動化訴求', color: 'purple',
                    text: '「弊社の自動チェックイン機は、チェックイン時にパスポートや免許証をスキャンするだけで、宿泊者名簿が自動で作成・保存されます。手書き不要・転記不要で、行政への提出もデータで対応できます。外国人のお客様もパスポートをかざすだけで本人確認が完了します。\nIT補助金を使うと実質13万円〜でご導入できるのですが、いかがでしょうか？」',
                    point: '「手書き不要・転記不要」はスタッフの工数削減として伝わる。外国人本人確認（パスポートスキャン）は差別化ポイント。法令対応+効率化の二重メリットを強調する。' },
                  { label: 'STEP 4｜デモ・資料送付でアポ', color: 'green',
                    text: '「実際に名簿が自動作成される画面をZoomでご覧いただくことができます。15分ほどで「うちで使えるか」のイメージがつくと思いますが、今週か来週でご都合はいかがでしょうか？先に資料だけお送りすることも可能です。」',
                    point: '画面デモは「紙がデータに変わる」ことを視覚的に見せるのが最効果。名簿一覧・検索・CSV出力の流れを見せると刺さる。' },
                  { label: "STEP 4'｜法令対応資料で締め", color: 'slate',
                    text: '「では、旅館業法対応の宿泊者名簿デジタル化と、本人確認フローをまとめた資料をお送りします。IT補助金の概要も一緒にお送りしますので、メールアドレスをいただけますか？」',
                    point: '「法令対応」という文脈で送る資料は開封率が高い。旅館業法の改正情報（直近のもの）があれば添えると説得力が増す。' },
                ],
              },
              {
                name: '🌙 夜間・無人運営訴求型',
                desc: '深夜対応・無人フロントの課題から入る。小規模施設・民宿・ペンションに刺さりやすい。',
                steps: [
                  { label: 'STEP 1｜受付突破', color: 'blue',
                    text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\n夜間・深夜のフロント対応についてご案内があってお電話しているのですが、\nご支配人様か、オーナー様はいらっしゃいますでしょうか？」',
                    point: '「夜間対応」は宿泊施設の普遍的な悩み。オーナー兼フロントの小規模施設に特に刺さる。' },
                  { label: 'STEP 2｜夜間の苦労に共感', color: 'yellow',
                    text: '「ありがとうございます。夜遅いチェックインや深夜の問い合わせで、スタッフが起きて対応しているという施設様からよくお聞きするのですが、御社ではいかがですか？」',
                    point: '小規模施設のオーナーは自分が深夜対応していることが多い。「分かってくれている」という共感を作ることが重要。' },
                  { label: 'STEP 3｜無人モード訴求', color: 'purple',
                    text: '「弊社の自動チェックイン機には「無人モード」という機能があって、深夜帯は機械がチェックインを自動で行います。\nスマートロックと連携すれば、フロントがいなくてもお客様がセルフでお部屋に入れます。\nIT補助金で実質13万円〜でご導入できますので、今の深夜対応のコストと比べると…」',
                    point: 'スマートロック連携は「完全無人化」のイメージを作る。「フロントがいなくていい」という解放感を強調する。' },
                  { label: 'STEP 4｜デモ見せるアポ', color: 'green',
                    text: '「実際の無人チェックインの流れをZoomで画面共有しながらご覧いただくことができます。\n15分ほどで「うちでも使えるか」のイメージがついていただけると思いますが、今週か来週でご都合はいかがでしょうか？」',
                    point: 'デモを見せると「具体的に使えるイメージ」が湧く。映像・画面で見せる方が口頭説明より断然伝わりやすい。' },
                  { label: "STEP 4'｜深夜対応コスト比較で締め", color: 'slate',
                    text: '「では、深夜対応コストの削減シミュレーションと、無人チェックインの手順をまとめた資料をお送りします。\n今すぐでなくても、参考資料として持っておいていただければと思います。\nメールアドレスをいただけますか？」',
                    point: '「今すぐでなくても」でプレッシャーを外す。小規模オーナーは即決できないケースが多いので、資料→再架電のサイクルで関係を作る。' },
                ],
              },
            ]
            const pat = YM_PATTERNS[ymPattern]
            const colorClass = (c: string) => ({
              blue: { bg: 'bg-blue-950/40 border border-blue-800/40', text: 'text-blue-400' },
              yellow: { bg: 'bg-yellow-950/40 border border-yellow-800/40', text: 'text-yellow-400' },
              purple: { bg: 'bg-purple-950/40 border border-purple-800/40', text: 'text-purple-400' },
              green: { bg: 'bg-green-950/40 border border-green-800/40', text: 'text-green-400' },
              slate: { bg: 'bg-slate-700/50 border border-slate-600/40', text: 'text-slate-400' },
            }[c] ?? { bg: 'bg-slate-700/50 border border-slate-600/40', text: 'text-slate-400' })

            return (
              <div id="ym-pattern-section" className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-3xl">💰</span>
                  <div>
                    <h2 className="text-xl font-bold text-white">米山パターン</h2>
                    <p className="text-base text-yellow-300/80 mt-0.5">{pat.desc}</p>
                  </div>
                </div>

                {/* パターン切り替えタブ */}
                <div className="flex flex-wrap gap-2 mb-5 pb-4 border-b border-slate-700">
                  {YM_PATTERNS.map((p, idx) => (
                    <button key={idx} onClick={() => setYmPattern(idx)}
                      className={`text-sm px-3 py-2 rounded-xl font-bold transition-all ${ymPattern === idx ? 'bg-yellow-600 text-white shadow-lg scale-105' : 'bg-slate-700 text-slate-300 hover:bg-slate-600 border border-slate-600'}`}>
                      {p.name}
                    </button>
                  ))}
                </div>

                <div className="space-y-3">
                  {pat.steps.map((item, i) => {
                    const cc = colorClass(item.color)
                    const stepLabels = ['STEP 1', 'STEP 2', 'STEP 3', 'STEP 4', 'STEP 4\'']
                    const isOpen = stepNavOpen[i]
                    const stepKeys = ['step1', 'step2', 'step3', 'step4', 'step4b'] as const
                    const customTalk = hotelResult
                      ? (hotelResult.steps?.[stepKeys[i]] ?? (i === 0 ? hotelResult.opening : ''))
                      : ''
                    return (
                      <div key={i} className={`rounded-2xl border ${isOpen ? 'border-slate-500' : 'border-slate-700/50'} overflow-hidden`}>
                        {/* ── アコーディオンヘッダー ── */}
                        <button
                          onClick={() => toggleStepNav(i)}
                          className={`w-full flex items-center gap-4 px-5 py-4 text-left transition-colors ${isOpen ? cc.bg : 'bg-slate-800/80 hover:bg-slate-800'}`}>
                          {/* STEP番号バッジ */}
                          <span className={`flex-shrink-0 w-16 h-10 rounded-xl flex items-center justify-center text-sm font-black ${isOpen ? 'bg-white/20 text-white' : 'bg-slate-700 text-slate-300'}`}>
                            {stepLabels[i]}
                          </span>
                          {/* ラベル */}
                          <span className={`flex-1 text-base font-bold ${isOpen ? cc.text : 'text-slate-300'}`}>{item.label}</span>
                          {/* AI提案ありバッジ */}
                          {customTalk && <span className="text-xs px-2 py-1 rounded-full bg-cyan-700/60 text-cyan-300 font-bold flex-shrink-0">🏨 AI提案あり</span>}
                          <span className={`text-slate-400 flex-shrink-0 ${isOpen ? 'rotate-180' : ''} transition-transform`}>▼</span>
                        </button>

                        {/* ── 展開コンテンツ ── */}
                        {isOpen && (
                          <div className={`${cc.bg} border-t border-slate-600/40`}>
                            {/* AI専用トーク（常時最上部・目立つ） */}
                            {customTalk && (
                              <div className="px-5 pt-4 pb-2">
                                <div className="bg-cyan-950/70 border border-cyan-500/60 rounded-xl p-4">
                                  <div className="flex items-center justify-between mb-3">
                                    <p className="text-sm font-black text-cyan-400 tracking-wide">🏨 {stepLabels[i]}｜このホテル専用AIトーク</p>
                                    <button onClick={() => copy(customTalk, `hotel_step_${i}`)}
                                      className={`text-sm px-3 py-1.5 rounded-lg font-bold transition-colors ${copiedKey === `hotel_step_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                      {copiedKey === `hotel_step_${i}` ? '✅ コピー済' : '📋 コピー'}
                                    </button>
                                  </div>
                                  <p className="text-lg text-cyan-100 leading-relaxed whitespace-pre-wrap">{customTalk}</p>
                                </div>
                              </div>
                            )}

                            {/* AI課題・注意（折りたたみ） */}
                            {hotelResult && (hotelResult.issues?.length > 0 || hotelResult.tips) && i === 0 && (
                              <div className="px-5 py-2 grid grid-cols-1 gap-2">
                                {hotelResult.issues?.length > 0 && (
                                  <details className="group">
                                    <summary className="cursor-pointer text-sm font-bold text-red-400 px-3 py-2 bg-red-950/30 rounded-lg list-none flex items-center justify-between">
                                      <span>⚠️ AIが見つけた課題 ({hotelResult.issues.length}件)</span>
                                      <span className="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
                                    </summary>
                                    <ul className="mt-2 space-y-1 px-3">
                                      {hotelResult.issues.map((issue, ii) => (
                                        <li key={ii} className="text-sm text-slate-200 flex items-start gap-2">
                                          <span className="text-red-400 flex-shrink-0">•</span>{issue}
                                        </li>
                                      ))}
                                    </ul>
                                  </details>
                                )}
                                {hotelResult.tips && (
                                  <details className="group">
                                    <summary className="cursor-pointer text-sm font-bold text-yellow-400 px-3 py-2 bg-yellow-950/30 rounded-lg list-none flex items-center justify-between">
                                      <span>💡 架電注意ポイント</span>
                                      <span className="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
                                    </summary>
                                    <p className="mt-2 px-3 text-sm text-slate-200 leading-relaxed">{hotelResult.tips}</p>
                                  </details>
                                )}
                              </div>
                            )}

                            {/* 標準トーク（折りたたみ） */}
                            <div className="px-5 py-2">
                              <details className="group">
                                <summary className="cursor-pointer text-sm font-bold text-slate-400 px-3 py-2 bg-slate-700/50 rounded-lg list-none flex items-center justify-between hover:bg-slate-700">
                                  <span>📄 標準トーク（米山パターン）</span>
                                  <span className="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
                                </summary>
                                <div className="mt-2 px-3">
                                  <div className="flex items-center justify-between mb-2">
                                    <p className={`text-xs font-bold ${cc.text}`}>{item.label}</p>
                                    <button onClick={() => copy(item.text, `ym_${ymPattern}_${i}`)}
                                      className={`text-xs px-2 py-1 rounded-lg font-bold transition-colors ${copiedKey === `ym_${ymPattern}_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                      {copiedKey === `ym_${ymPattern}_${i}` ? '✅' : '📋'}
                                    </button>
                                  </div>
                                  <p className="text-base text-slate-100 leading-relaxed whitespace-pre-line mb-2">{item.text}</p>
                                  <p className="text-sm text-slate-400 leading-relaxed border-t border-slate-600/40 pt-2">💡 {item.point}</p>
                                </div>
                              </details>
                            </div>

                            {/* 切り返しナビ（折りたたみ） */}
                            <div className="px-5 pt-2 pb-4">
                              <details className="group">
                                <summary className="cursor-pointer text-sm font-bold text-blue-300 px-3 py-2 bg-blue-900/30 rounded-lg list-none flex items-center justify-between hover:bg-blue-900/50">
                                  <span>⚡ 切り返しナビ</span>
                                  <span className="text-slate-500 group-open:rotate-180 transition-transform">▼</span>
                                </summary>
                                <div className="mt-3 bg-slate-900/60 rounded-xl p-4 space-y-4">(
                            <div className="mt-3 bg-slate-900/60 rounded-xl p-4 space-y-4">
                              {/* 切り返しナビ */}
                              <div>
                                <div className="flex flex-wrap gap-2 mb-3">
                                  {CATEGORY_ITEMS.map(cat => (
                                    <button key={cat.id} onClick={() => selectCat(cat.id)}
                                      className={`px-4 py-3 rounded-xl text-base font-bold transition-all ${selectedCat === cat.id ? 'bg-blue-600 text-white shadow-lg scale-105' : 'bg-slate-700 text-slate-200 hover:bg-slate-600 border border-slate-600'}`}>
                                      {OBJECTION_TREE[cat.id]?.label}
                                    </button>
                                  ))}
                                </div>
                                {selectedCat && (
                                  <div className="border-t border-slate-700 pt-3">
                                    <div className="flex flex-wrap gap-2 mb-3">
                                      {CATEGORY_ITEMS.find(c => c.id === selectedCat)?.children.map(childId => (
                                        <button key={childId} onClick={() => selectResponse(childId)}
                                          className={`px-4 py-3 rounded-xl text-base font-bold transition-all ${selectedResponse === childId ? 'bg-green-600 text-white shadow-lg scale-105' : 'bg-slate-700/70 text-slate-200 hover:bg-slate-600 border border-slate-600'}`}>
                                          {OBJECTION_TREE[childId]?.label}
                                        </button>
                                      ))}
                                    </div>
                                    {selectedResponse && (
                                      <div className="bg-green-950/60 border border-green-700/70 rounded-xl p-4">
                                        <div className="flex items-center justify-between mb-2">
                                          <p className="text-sm text-green-400 font-bold">💬 切り返しトーク</p>
                                          <button onClick={() => copy(OBJECTION_TREE[selectedResponse]?.response || '', `step_nav_${i}`)}
                                            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${copiedKey === `step_nav_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                                            {copiedKey === `step_nav_${i}` ? '✅' : '📋'}
                                          </button>
                                        </div>
                                        <p className="text-base text-white leading-relaxed">{OBJECTION_TREE[selectedResponse]?.response}</p>
                                      </div>
                                    )}
                                  </div>
                                )}
                              </div>

                              {/* キーワード検索 */}
                              <div className="border-t border-slate-700 pt-3">
                                <p className="text-xs text-slate-400 font-bold mb-2">🔍 キーワードで検索</p>
                                <input
                                  type="text"
                                  value={stepSearch[i]}
                                  onChange={e => updateStepSearch(i, e.target.value)}
                                  placeholder="例：予算・他社・深夜・インバウンド"
                                  className="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
                                />
                                {stepSearch[i] && (() => {
                                  const hits = suggestByKeyword(stepSearch[i])
                                  return hits.length > 0 ? (
                                    <div className="mt-2 space-y-2">
                                      {hits.slice(0, 3).map(id => (
                                        <div key={id} className="bg-slate-800 rounded-lg p-3">
                                          <p className="text-xs font-bold text-slate-300 mb-1">{OBJECTION_TREE[id]?.label}</p>
                                          <div className="flex items-start gap-2">
                                            <p className="text-sm text-slate-200 flex-1 leading-relaxed">{OBJECTION_TREE[id]?.response}</p>
                                            <button onClick={() => copy(OBJECTION_TREE[id]?.response || '', `sw_${i}_${id}`)}
                                              className={`text-xs px-2 py-1 rounded flex-shrink-0 transition-colors ${copiedKey === `sw_${i}_${id}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                                              {copiedKey === `sw_${i}_${id}` ? '✅' : '📋'}
                                            </button>
                                          </div>
                                        </div>
                                      ))}
                                    </div>
                                  ) : (
                                    <div className="mt-2">
                                      <p className="text-xs text-slate-500 mb-2">該当なし — AIに聞く？</p>
                                      <button
                                        onClick={() => { setAiInput(stepSearch[i]); fetchAiSuggestions(stepSearch[i], 'yoneyama') }}
                                        disabled={aiLoading}
                                        className="w-full px-3 py-2 bg-purple-700 hover:bg-purple-600 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2">
                                        {aiLoading ? '⏳ 生成中...' : '🤖 AI切り返しサジェストを起動'}
                                      </button>
                                      {/* AI結果表示 */}
                                      {aiLoading && <div className="text-center py-4 text-purple-400 animate-pulse text-sm mt-2">🤖 生成中...</div>}
                                      {aiError && <div className="mt-2 text-xs text-red-400">⚠️ {aiError}</div>}
                                      {aiSuggestions.length > 0 && (
                                        <div className="mt-3 space-y-3">
                                          <p className="text-sm text-purple-400 font-bold">💡 AI推奨切り返し</p>
                                          {aiSuggestions.map((s, si) => (
                                            <div key={si} className="bg-purple-950/60 border border-purple-700/50 rounded-xl p-4">
                                              <p className="text-base text-purple-300 font-bold mb-2">{s.label}</p>
                                              <p className="text-base text-white leading-relaxed mb-3">{s.talk}</p>
                                              <button onClick={() => copy(s.talk, `ai_step_${i}_${si}`)}
                                                className={`text-sm px-3 py-1.5 rounded-lg font-bold transition-colors ${copiedKey === `ai_step_${i}_${si}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                                                {copiedKey === `ai_step_${i}_${si}` ? '✅' : '📋 コピー'}
                                              </button>
                                            </div>
                                          ))}
                                        </div>
                                      )}
                                    </div>
                                  )
                                })()}
                              </div>

                              {/* メモ保存 */}
                              <div className="border-t border-slate-700 pt-3">
                                <p className="text-xs text-slate-400 font-bold mb-2">💾 気づきをメモ保存</p>
                                <div className="flex gap-2">
                                  <input
                                    type="text"
                                    value={stepMemoInput[i]}
                                    onChange={e => updateStepMemoInput(i, e.target.value)}
                                    onKeyDown={e => e.key === 'Enter' && saveStepMemo(i, item.label)}
                                    placeholder="例：「深夜対応は困ってる」→無人モード訴求が刺さった"
                                    className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
                                  />
                                  <button
                                    onClick={() => saveStepMemo(i, item.label)}
                                    disabled={stepMemoSaving[i] || !stepMemoInput[i].trim()}
                                    className="px-3 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-lg text-xs font-bold transition-colors whitespace-nowrap">
                                    {stepMemoSaving[i] ? '保存中' : '💾 保存'}
                                  </button>
                                </div>
                              </div>
                            </div>
                          </details>
                            </div>

                            {/* メモ欄 */}
                            <div className="px-5 pb-4">
                              <textarea value={stepMemos[i]} onChange={e => updateMemo(i, e.target.value)}
                                placeholder="例：「予算がない」と言われた。補助金で突破できた。"
                                rows={2}
                                className="w-full bg-slate-900/60 border border-slate-600/60 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 resize-none" />
                            </div>
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })()}

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
          {/* 業界知識：PMS・SC・スマートロック・カードロック */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">🏨 業界システム知識（必須）</h2>
            <div className="space-y-4">
              <div className="bg-blue-950/40 border border-blue-800/40 rounded-xl p-5">
                <p className="text-base font-bold text-blue-300 mb-3">📋 PMS（ホテル基幹システム）</p>
                <div className="space-y-2">
                  {[
                    { maker: 'NEHOPS', detail: 'NEC製。「ネホップス」と読む。' },
                    { maker: 'GLOVIA smart', detail: '富士通製。' },
                    { maker: 'Wincal', detail: 'アルメックス製。USENグループ。' },
                    { maker: 'Staysee / AirHost / Beds24', detail: '連携実績あり。対応済み。' },
                    { maker: 'ねっぱん！', detail: '旧シーナッツ→バリューコマース吸収→2026年1月 楽天トラベルサービスへ合併・改称。SC版とPMS版あり。' },
                    { maker: 'ダイナテック', detail: '→バリューコマースに吸収合併。' },
                  ].map((r, i) => (
                    <div key={i} className="flex gap-3 items-start text-base">
                      <span className="text-blue-400 font-bold w-44 flex-shrink-0">{r.maker}</span>
                      <span className="text-slate-300">{r.detail}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-purple-950/40 border border-purple-800/40 rounded-xl p-5">
                <p className="text-base font-bold text-purple-300 mb-3">📋 サイトコントローラー（SC）</p>
                <p className="text-base text-slate-300">手間いらず / ねっぱん！（サイトコントローラー版）/ らく通with / TLリンカーン</p>
              </div>
              <div className="bg-green-950/40 border border-green-800/40 rounded-xl p-5">
                <p className="text-base font-bold text-green-300 mb-3">🔐 スマートロック（暗証番号で開錠）</p>
                <p className="text-base text-slate-300 mb-2">SwitchBot / RemoteLock（構造計画研究所→リモートロックジャパン） / EPIC（エナスピレーション）/ TTLock</p>
                <p className="text-xs text-slate-400">※EPICはカードロックではなく「スマートロック」に分類される点に注意</p>
              </div>
              <div className="bg-yellow-950/40 border border-yellow-800/40 rounded-xl p-5">
                <p className="text-base font-bold text-yellow-300 mb-3">🗝️ カードロック（カードキー発行）</p>
                <p className="text-base text-slate-300">MIWA（美和ロック）/ GOAL / LEGEND / ASSA ABLOY</p>
              </div>
              <div className="bg-red-950/40 border border-red-800/40 rounded-xl p-5">
                <p className="text-base font-bold text-red-300 mb-3">⚠️ 競合メーカー</p>
                <div className="space-y-2">
                  {[
                    { name: 'アルメックス（Wincal）', detail: '自動精算機も出しているので、その領域では競合。PMSとしても使われる。' },
                    { name: 'その他チェックイン機メーカー', detail: '他社製品は実質「精算機」でフロント業務が残るケースが多い。弊社は無人化に特化。' },
                  ].map((r, i) => (
                    <div key={i} className="flex gap-3 items-start text-base">
                      <span className="text-red-400 font-bold w-52 flex-shrink-0">{r.name}</span>
                      <span className="text-slate-300">{r.detail}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* 機能・運用クイックリファレンス */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">⚙️ 機能・運用クイックリファレンス</h2>
            <div className="space-y-3">
              {[
                { q: '固定IPは必要？', a: '不要。有線・無線どちらでも可。回線がない場所はLTE SIM対応。' },
                { q: '予約番号を忘れた客の検索方法は？', a: '4通り：予約番号・お名前・電話番号・メールアドレス（+チェックイン日）。' },
                { q: '本人確認はどうする？', a: '本人確認画面が表示され、DMSからビデオ通話で承認。完全無人でも対応可。' },
                { q: 'カードキーは何枚出せる？', a: '施設が自由に枚数を設定できる。グループ客も対応。' },
                { q: '無人化は完全にしなければいけない？', a: 'いいえ。無人モードはON/OFF切り替え可。昼有人・夜無人などハイブリッド運用OK。' },
                { q: '鍵を変えたくない場合は？', a: '今の鍵はそのままでOK。シリンダー錠→キーボックスを使えば工事不要。' },
                { q: '閑散期・シーズン営業の費用は？', a: '月額保守費用は停止可。端末メーカーへの保守費用は別途必要。完全ゼロにはならない。' },
                { q: '宿泊旅行統計調査（手集計をやめたい）', a: '宿泊実績定期報告機能でDMSからデータ出力可。手集計不要。' },
                { q: '日本在住の外国人にパスポートを出させると嫌がる', a: '日本にお住まいの外国籍の方はパスポートスキャンをスキップできる設定が可能。' },
                { q: '団体客の代表者が全員分入力したい', a: '事前チェックインで代表者が同行者分を代理入力可。簡易チェックインで省略も可。' },
                { q: '鍵の一時預かり・返却の自動化', a: '「鍵の一時預かり／返却」機能あり。返却時の確認ごと自動化できる。' },
                { q: '連携していないPMSがある', a: 'リストにないPMSでも諦めない。弊社からメーカーへ連携依頼して進める。' },
                { q: '宿泊者名簿（クラウドで大丈夫？）', a: '名簿は営業者の事務所に備えることも法律上認められており、クラウド保存でOK。' },
                { q: '将来のロードマップは？', a: '動画マニュアルをAIアバター化し、バーチャルフロントへ進化させる予定。' },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/40 rounded-xl p-4">
                  <p className="text-sm font-bold text-yellow-400 mb-1">Q. {item.q}</p>
                  <p className="text-base text-slate-200">A. {item.a}</p>
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

      {/* ─── TAB: ノウハウメモ ─── */}
      {activeTab === 'memo' && (
        <div className="space-y-6">
          {/* 入力エリア */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">📝 気づき・ノウハウを記録する</h2>
            <div className="flex gap-2 mb-3 flex-wrap">
              {MEMO_CATEGORIES.map(cat => (
                <button key={cat.id} onClick={() => setMemoCat(cat.id)}
                  className={`text-sm px-3 py-1.5 rounded-full font-medium transition-colors ${memoCat === cat.id ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                  {cat.label}
                </button>
              ))}
            </div>
            <textarea
              value={memoInput}
              onChange={e => setMemoInput(e.target.value)}
              placeholder="例：「補助金の申請期限があります」と言うだけで受付突破率が上がる。支配人か担当者の二択にするとどちらかに繋いでもらいやすい。"
              rows={4}
              className="w-full bg-slate-700 text-white rounded-xl px-4 py-3 text-base placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
            <div className="flex justify-between items-center mt-3">
              <span className="text-sm text-slate-400">{memoInput.length}文字</span>
              <button onClick={saveMemo} disabled={memoSaving || !memoInput.trim()}
                className="px-5 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-xl font-bold transition-colors text-sm">
                {memoSaving ? '保存中…' : '💾 保存'}
              </button>
            </div>
          </div>

          {/* フィルタ */}
          <div className="flex gap-2 flex-wrap">
            <button onClick={() => setMemoFilter('all')}
              className={`text-sm px-3 py-1.5 rounded-full font-medium transition-colors ${memoFilter === 'all' ? 'bg-slate-500 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
              すべて
            </button>
            {MEMO_CATEGORIES.map(cat => (
              <button key={cat.id} onClick={() => setMemoFilter(cat.id)}
                className={`text-sm px-3 py-1.5 rounded-full font-medium transition-colors ${memoFilter === cat.id ? 'bg-slate-500 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                {cat.label}
              </button>
            ))}
          </div>

          {/* メモ一覧 */}
          {!memosLoaded ? (
            <div className="text-center text-slate-400 py-12">読み込み中…</div>
          ) : memos.filter(m => memoFilter === 'all' || m.category === memoFilter).length === 0 ? (
            <div className="text-center text-slate-500 py-12 bg-slate-800 rounded-2xl border border-slate-700">
              <p className="text-4xl mb-3">📭</p>
              <p>まだメモがありません。気づきを記録しよう！</p>
            </div>
          ) : (
            <div className="space-y-3">
              {memos
                .filter(m => memoFilter === 'all' || m.category === memoFilter)
                .map(memo => {
                  const cat = MEMO_CATEGORIES.find(c => c.id === memo.category)
                  return (
                    <div key={memo.id} className="bg-slate-800 rounded-2xl border border-slate-700 p-5">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-300">
                          {cat?.label ?? memo.category}
                        </span>
                        <div className="flex items-center gap-3">
                          <span className="text-xs text-slate-500">
                            {new Date(memo.created_at).toLocaleDateString('ja-JP', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                          </span>
                          <button onClick={() => deleteMemo(memo.id)}
                            className="text-xs text-slate-600 hover:text-red-400 transition-colors">
                            🗑
                          </button>
                        </div>
                      </div>
                      <p className="text-base text-slate-200 leading-relaxed whitespace-pre-wrap">{memo.content}</p>
                    </div>
                  )
                })}
            </div>
          )}
        </div>
      )}

    </div>
  )
}
