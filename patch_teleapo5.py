import sys
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

old_tree_start = "const OBJECTION_TREE: Record<string, { label: string; response: string }> = {"
old_tree_end = "}\n\nconst CATEGORY_ITEMS = ["
old_cat_end = "  { id: 'cat_claim',      children: ['claim_apology', 'claim_record'] },\n]"

# 新しいOBJECTION_TREEとCATEGORY_ITEMSに差し替える
new_tree = r"""const OBJECTION_TREE: Record<string, { label: string; response: string }> = {
  // ── カテゴリ ──
  'cat_busy':        { label: '⏰ 今は忙しい', response: '' },
  'cat_nointerest':  { label: '😐 興味がない', response: '' },
  'cat_other':       { label: '🏢 他社を使っている', response: '' },
  'cat_price':       { label: '💴 高そう・お金がかかる', response: '' },
  'cat_key':         { label: '🔑 カードキーでないとダメ', response: '' },
  'cat_custom':      { label: '🏨 うちの業態に合わない', response: '' },
  'cat_pms':         { label: '💻 PMSと連携できる？', response: '' },
  'cat_unmanned':    { label: '🚫 無人にはできない', response: '' },
  'cat_person':      { label: '📵 担当者不在', response: '' },
  'cat_email':       { label: '📧 メールが届かない', response: '' },
  'cat_seminar':     { label: '📅 セミナーの案内', response: '' },
  'cat_inbound':     { label: '🌏 インバウンド対応は？', response: '' },
  'cat_size':        { label: '🏡 小規模だから不要では？', response: '' },
  'cat_timing':      { label: '📆 今は検討時期ではない', response: '' },
  'cat_claim':       { label: '😡 かけてくるな（クレーム）', response: '' },

  // ── 今は忙しい ──
  'busy_later':        { label: 'いつ頃なら大丈夫か確認する', response: '「承知いたしました。では、またお時間のよいときにご連絡させていただいてもよろしいでしょうか？いつ頃でしたらよろしいでしょうか？」' },
  'busy_short':        { label: '30秒だけお願いする', response: '「お忙しいところ大変恐れ入ります。30秒だけお時間いただけますでしょうか。資料をメールでお送りするだけでも、させていただければと思っております。」' },
  'busy_task':         { label: 'タスクに控えて後日かける', response: '「かしこまりました。では、後日あらためてご連絡させていただきます。〇〇様のお名前とご連絡先、確認させていただいてよろしいでしょうか？」' },
  'busy_mail':         { label: '今は資料だけメールで送る', response: '「お忙しいところ失礼いたしました。では資料だけでもメールでお送りさせていただいてもよろしいでしょうか？メールアドレスをいただけるだけで大丈夫です。」' },
  'busy_time_ask':     { label: '今日の後半に再架電を提案', response: '「承知しました。では本日の午後〇時頃にあらためてお電話してもよろしいでしょうか？2〜3分だけいただければ十分です。」' },
  'busy_empathy':      { label: '繁忙期であることに共感して次につなぐ', response: '「繁忙期でお忙しい時期にお電話してしまい申し訳ありません。実は繁忙期こそ弊社製品が力を発揮するのですが、落ち着いたタイミングで一度お話しさせていただけますでしょうか？」' },

  // ── 興味がない ──
  'nointerest_reason':   { label: '具体的な理由を聞く', response: '「そうでございますか。差し支えなければ、どのような点でご興味をお持ちになれないか、教えていただけますでしょうか？もしコスト面や業態の問題でしたら、解決できた事例もご用意しております。」' },
  'nointerest_future':   { label: '将来的な可能性を確認', response: '「将来的にも、ご興味はないでしょうか？近年、全国からのお問い合わせが去年よりかなり多くなってきておりまして、業界全体でのスタンダードになりつつあります。参考情報だけでもお送りさせていただければと思います。」' },
  'nointerest_seminar':  { label: 'セミナーに誘う', response: '「弊社は週2回、オンラインの説明会を開催しております（水曜11時・金曜13時）。1時間程度で費用・導入事例なども詳しくご説明できます。ご参加は無料ですので、一度いかがでしょうか？」' },
  'nointerest_flow':     { label: '流行の波を伝える', response: '「最近よくお耳にするかとは思いますが、自動チェックイン機の件になります。全国各地のホテル様で急速に導入が進んでおりまして、業界のスタンダードになりつつある状況でございます。他社様に遅れをとらないためにも、一度ご検討いただけませんか？」' },
  'nointerest_info':     { label: '情報だけでも送る提案', response: '「ご興味がないのは承知いたしました。ただ、資料だけでもご覧いただけますと、具体的なコストや仕組みがよくわかります。メールアドレスをお教えいただければ今日中にお送りいたします。」' },
  'nointerest_subsidy':  { label: 'IT補助金の話に切り替える', response: '「製品のご興味より先に、今年のIT補助金の締め切りが近づいているのでご案内しているという側面もございます。補助金申請だけでも弊社が代行できますので、情報だけでも受け取っていただけますでしょうか？」' },
  'nointerest_competitor': { label: '競合に差をつけられる前に、と訴求', response: '「同じ地域の競合ホテル様がすでに導入されている事例もございます。チェックインのスムーズさは口コミにも影響しますので、情報だけでも持っておいていただけると幸いです。」' },

  // ── 他社使用中 ──
  'other_maker':       { label: 'どのメーカーか聞く', response: '「あ、そうでございましたか。差し支えなければ、どちらのメーカー様をご利用されているか、参考までに教えて頂けますでしょうか？」' },
  'other_compare':     { label: '比較提案に持ち込む', response: '「すでに導入されていらっしゃるのですね。弊社は自社開発のため、他社様にはない機能（シリンダー錠対応・完全オーダーメイドカスタマイズ等）がございます。現状の課題があれば、比較資料としてご覧いただけますでしょうか？」' },
  'other_renewal':     { label: '更新・リプレイス提案', response: '「現在ご利用のシステムの契約更新時期はいつ頃でしょうか？弊社は価格面でもご好評をいただいており、乗り換えを検討されている施設様も増えております。ちょうどそのタイミングで比較検討いただけると幸いです。」' },
  'other_weakness':    { label: '現在の課題・不満を聞く', response: '「現在お使いのシステムで、何か不満な点や「ここがもう少し…」という部分はございますでしょうか？弊社はカスタマイズ性と価格面で選ばれることが多く、改善できる可能性があるかもしれません。」' },
  'other_coexist':     { label: '併用・補完提案をする', response: '「チェックイン機は既存のPMSや管理システムとの連携も可能です。今お使いのシステムはそのままで、チェックイン・清算だけ弊社製品を使っていただく形も選択肢としてございます。」' },

  // ── 価格 ──
  'price_subsidy':     { label: 'IT補助金を案内する', response: '「弊社が補助金申請を代行できます。IT補助金活用でKIOSK筐体が最安48万円〜、タブレット型は13万円〜でご導入可能です。補助金があれば実質費用がかなり抑えられます。詳しい資料をお送りしてもよろしいでしょうか？」' },
  'price_running':     { label: '月額費用・コスト削減効果を説明', response: '「月額費用はKIOSK型で19,600円＋部屋数×200円、タブレット型は1室500円です。繁忙期のみ使用で使わない月は0円、日割り計算も可能です。一方で、フロントスタッフの人件費削減効果と比べると、多くの施設様で半年〜1年以内に回収されています。」' },
  'price_season':      { label: '季節限定プランを案内', response: '「ご使用にならない月は月額0円になります。繁忙期のみのご利用や、土日祝のみご使用の日割り計算プランもございます。実際の費用感をメールでご案内してもよろしいでしょうか？」' },
  'price_small':       { label: '小規模向け低コストプランを提示', response: '「小規模施設様向けには、タブレット型でご導入いただけます。初期費用はIT補助金活用で13万円〜、月額は1室500円です。一軒家や小規模旅館様にも導入実績がございます。」' },
  'price_roi':         { label: '人件費削減ROIを説明する', response: '「仮にフロントスタッフ1名の夜間対応を削減できたとすると、月20〜30万円の人件費削減になります。月額費用と比較すると、多くの施設様で3〜6ヶ月で回収できています。」' },
  'price_subsidy_detail': { label: 'IT補助金の詳細を説明する', response: '「IT導入補助金は中小企業がITシステムを導入する際に国が最大2/3を補助する制度です。弊社は補助金申請の代行から書類作成まで全て対応しており、御社にご負担いただくのは必要書類のご提出のみです。」' },

  // ── カードキー・鍵 ──
  'key_cylinder':      { label: 'シリンダー錠対応をPR', response: '「弊社の強みは、シリンダー錠（物理キー）にも対応可能なことです！別売りのキーボックスを使うことで、清算が完了すると自動でキーボックスが開き、お客様がセルフで鍵をお受け取りいただけます。カードキーへの変更は一切不要です。」' },
  'key_smartlock':     { label: 'クラウドスマートロックを提案', response: '「クラウドスマートロックという選択肢もございます。暗証番号で開錠でき、チェックイン機から排出されるレシートに暗証番号が自動で印字されます。鍵の受け渡しが完全にセルフになります。」' },
  'key_receipt':       { label: 'レシート×対面方式を提案', response: '「もし接客を残したい場合は、チェックイン機で清算まで済ませてレシートを発行し、そのレシートをフロントで鍵と交換するという運用も可能です。対面の接客要素を残しながら、手続きだけ効率化できます。」' },
  'key_keybox':        { label: 'キーボックスの仕組みを説明する', response: '「キーボックスは壁に設置する鍵の収納ボックスで、チェックイン機での清算完了と同時に自動解錠されます。番号錠ではなく自動解錠型なので、お客様が暗証番号を覚える必要がありません。」' },
  'key_cost':          { label: 'カードキー化のコストを比較する', response: '「カードキーへの変更は設備投資が必要ですが、弊社のシリンダー錠対応なら既存の鍵をそのまま使えます。余計な改修費用をかけずにチェックイン機を導入できるのが弊社の強みです。」' },

  // ── 業態・カスタマイズ ──
  'custom_order':      { label: 'オーダーメイドをPR', response: '「普段スタッフが口頭でご説明していることを、チェックイン機にカスタマイズして組み込むことが可能です。弊社は自社開発のため、御社専用のオーダーメイドをご提供できます。他社様には真似のできない強みです。」' },
  'custom_example':    { label: '同業態の導入事例を提示', response: '「弊社では接客の質を落とさずに手続きだけをスマート化して、顧客満足度を上げた事例がございます。同じような業態の施設様の導入事例を資料でお送りしてもよろしいでしょうか？」' },
  'custom_ryokan':     { label: '旅館・温泉施設への対応', response: '「旅館様でも多数ご導入いただいております。日帰り温泉客の受付・清算、朝食券・夕食券の発行など、旅館特有の運用にもカスタマイズ対応できます。お話しだけでもいかがでしょうか？」' },
  'custom_hospi':      { label: 'ホスピタリティを落とさない訴求', response: '「チェックイン機を導入することで、フロントスタッフがチェックイン手続きから解放され、観光案内やお出迎えなどの本来の接客に集中できるようになります。結果としてホスピタリティが向上した施設様も多くいらっしゃいます。」' },
  'custom_demo':       { label: 'デモ機・実機確認を提案', response: '「実際の操作感が気になるようでしたら、オンラインデモをご用意することも可能です。実際の画面をご覧いただきながら、御社の業態に合う設定をご提案できます。30分程度で済みますが、いかがでしょうか？」' },
  'custom_ui':         { label: 'UI・画面のカスタマイズを説明', response: '「チェックイン画面のUIは御社のブランドに合わせてカスタマイズできます。ロゴや色味、表示する質問項目、宿泊約款の内容なども変更可能です。「うちらしくない」とはなりません。」' },

  // ── PMS連携 ──
  'pms_list':          { label: 'PMS連携実績を案内', response: '「弊社はPMS（ホテルシステム）との連携開発に近年力を入れています。連携実績：ステイシー・スイートブック・ベッツ24。現在も複数のPMSと連携開発が進行中です。御社のPMSについても、ぜひ一度ご相談いただけますでしょうか？」' },
  'pms_develop':       { label: '連携開発の意欲を伝える', response: '「お客様のご要望によりかなりの頻度で連携開発が進んでいますので、御社のPMSも今後連携開発を進めることが可能です。まずはシステム名をお教えいただけますでしょうか？」' },
  'pms_standalone':    { label: 'PMS連携なしでも使えると伝える', response: '「PMSとの連携がなくても、弊社製品単体でチェックイン・清算・精算書発行まで完結できます。連携がない場合でも、予約番号での照合や手動入力での運用が可能です。まず基本機能を試していただいてから連携を検討する施設様も多いです。」' },
  'pms_api':           { label: 'API連携の仕組みを説明する', response: '「APIが公開されているPMSであれば、弊社との連携開発ができます。御社のPMSのAPI仕様書を確認できれば、連携可能かどうかを弊社エンジニアが確認いたします。PMSのシステム名を教えていただけますでしょうか？」' },

  // ── 無人化 ──
  'unmanned_pr':       { label: '省人化・効率化に言い換える', response: '「「無人化」というより、「省人化」・「業務効率化」のツールとしてご活用いただいております。フロントスタッフがチェックイン手続きから解放されることで、お客様との会話や観光案内など、本来の接客サービスにより集中できるようになります。」' },
  'unmanned_night':    { label: '夜間・深夜帯の対応として訴求', response: '「特に夜間や深夜帯のチェックインで効果を発揮します。スタッフが不在の時間でも、お客様が自分でチェックインできるため、深夜のフロント対応を大幅に削減できます。」' },
  'unmanned_inbound':  { label: 'インバウンドへの対応力', response: '「外国語対応（13か国語）とパスポートスキャン機能により、インバウンドのお客様もスムーズにチェックインできます。言語の壁がなくなることで、スタッフの対応負担が大幅に減ります。」' },
  'unmanned_hybrid':   { label: 'ハイブリッド運用を提案', response: '「完全無人化ではなく、ハイブリッド運用も可能です。例えば平日昼はフロント対応、深夜や繁忙期はチェックイン機を併用、という形です。状況に合わせて柔軟に使い分けられます。」' },
  'unmanned_elderly':  { label: 'お年寄りゲストへの対応を説明', response: '「ご年配のお客様にはスタッフがサポートする運用にしている施設様も多いです。機械が苦手なお客様にはフロントで対応し、それ以外のお客様にはチェックイン機を使っていただく、という使い分けで問題ありません。」' },
  'unmanned_staff':    { label: 'スタッフの仕事がなくならないと説明', response: '「チェックイン手続きがなくなる分、スタッフの仕事がなくなるのでは？とご心配されることがありますが、逆にスタッフが接客・コンシェルジュ・清掃チェックなど付加価値の高い業務に集中できるようになります。」' },

  // ── 担当者不在 ──
  'person_time':       { label: 'いつ頃いるか確認する', response: '「承知いたしました。失礼いたしました。何時（何日）ごろでしたら担当の支配人様とお話できますでしょうか？」' },
  'person_front':      { label: 'フロントに資料送付をお願いする', response: '「では、フロントの方にお願いして、担当の支配人様にご一読いただけるよう資料をメールでお送りしてもよろしいでしょうか？よろしければメールアドレスをお教えいただけますか？（フロントの方のお名前も頂戴できますと幸いです。）」' },
  'person_callback':   { label: 'かけ直しをお願いする', response: '「ありがとうございます。では〇〇（時間帯）にあらためてお電話させていただきます。よろしくお願いいたします。」' },
  'person_msg':        { label: 'フロントに伝言をお願いする', response: '「よろしければ、「デバイスエージェンシーの〇〇より、自動チェックイン機のご案内でお電話がありました」とお伝えいただけますでしょうか？後ほどあらためてご連絡させていただきます。」' },
  'person_name':       { label: '担当者名を聞いておく', response: '「よろしければ、担当されている支配人様のお名前を教えていただけますでしょうか？次回ご連絡する際にお名前でお呼びできますので。」' },
  'person_best_time':  { label: '架電しやすい曜日・時間を聞く', response: '「支配人様がお電話に出やすい曜日や時間帯はございますでしょうか？なるべくご都合に合わせてご連絡したいと思いまして。」' },

  // ── メール未着 ──
  'email_spam':        { label: '迷惑メールを確認してもらう', response: '「もしかしますと迷惑メールフォルダに入っている可能性がございます。「迷惑メールでないことを報告」をクリックしていただきますと、今後は受信ボックスに届くようになります。」' },
  'email_recheck':     { label: 'アドレスを再確認する', response: '「念のためメールアドレスをもう一度ご確認させていただけますでしょうか？正しいアドレスでも届かない場合は、一度フロントの方のアドレスから弊社へ送信していただくと、今後スムーズに送受信できるようになります。」' },
  'email_resend':      { label: 'こちらから再送する', response: '「承知いたしました。再度お送りいたします。件名は「〇〇様　自動チェックイン機のご案内」でお送りしますので、ご確認いただけますでしょうか。もし届かなければお電話でご連絡ください。」' },
  'email_domain':      { label: 'ドメイン拒否の可能性を案内', response: '「ご利用のメールサーバーがdeviceagency.co.jpドメインを拒否している可能性がございます。IT担当者様に「@deviceagency.co.jpからのメールを許可する設定」をご確認いただけますでしょうか？」' },
  'email_change':      { label: '別のアドレスを使う提案', response: '「もし届かない場合、Gmailなど別のメールアドレスをお持ちでしたら、そちらにお送りすることもできます。個人アドレスでも構いません。」' },

  // ── セミナー ──
  'seminar_when':      { label: 'セミナー日程を案内する', response: '「オンラインセミナーは毎週水曜日11時〜・金曜日13時〜開催しております（1時間程度・参加無料）。ご都合に合わせて別日のご案内も可能ですので、ご希望の日時をお教えください。」' },
  'seminar_content':   { label: 'セミナー内容を説明する', response: '「セミナーでは、実際の操作デモ・価格・補助金・導入事例・PMSとの連携などを1時間でご説明いたします。個別のご質問もその場でお答えできます。ZoomのURLをお送りいたしますので、メールアドレスをいただけますでしょうか？」' },
  'seminar_nudge':     { label: 'まず資料→後でセミナー提案', response: '「まず資料だけでもご覧いただき、ご興味があればセミナーにもお気軽にご参加いただける形でいかがでしょうか？資料をお送りするだけなら1分で済みます。メールアドレスをいただけますか？」' },
  'seminar_record':    { label: '録画視聴の提案', response: '「もしセミナーの日程が合わない場合、録画動画をお送りすることも可能です。ご都合のよい時間にご覧いただけます。メールアドレスをいただければ今日中にお送りします。」' },

  // ── インバウンド ──
  'inbound_lang':      { label: '多言語対応（13か国語）を説明', response: '「弊社の自動チェックイン機は13か国語に対応しております。外国語が苦手なスタッフ様でも、インバウンドのお客様に対応できます。パスポートスキャン・本人確認もチェックイン機で完結します。」' },
  'inbound_passport':  { label: 'パスポートスキャン機能を説明', response: '「インバウンド対応として、パスポートスキャンと顔写真撮影による本人確認機能がございます。外国籍のお客様の情報を自動で取得・記録できるため、フロントの手間が大幅に減ります。」' },
  'inbound_cc':        { label: '外国クレジットカード対応を説明', response: '「海外発行のクレジットカードや非接触決済（Apple Pay・Google Pay等）にも対応しております。インバウンドのお客様がスムーズに決済できるため、支払いトラブルが減ります。」' },
  'inbound_demand':    { label: 'インバウンド増加トレンドを伝える', response: '「2025年以降もインバウンド需要は増加傾向にあります。今のうちに多言語対応・非接触決済・パスポートスキャンを整備しておくことで、競合施設との差別化につながります。」' },

  // ── 小規模 ──
  'size_tablet':       { label: 'タブレット型を提案', response: '「小規模施設様にはタブレット型がございます。初期費用はIT補助金活用で13万円〜、月額は1室500円から。一軒家（シングルプラン）でも49,800円〜でご導入いただけます。」' },
  'size_other':        { label: 'ルームタブレット・スマートロックを提案', response: '「部屋数が少ない施設様でも、ルームタブレット（内線電話・月額1室100円〜）やクラウドスマートロックなど、チェックイン機以外の製品もご活用いただけます。組み合わせることで業務効率が上がります。」' },
  'size_case':         { label: '小規模施設の導入事例を提示', response: '「実は5室以下の小規模旅館様でも多数導入いただいております。特に1〜2名でワンオペされている施設様からは「深夜のチェックイン対応がなくなり体が楽になった」というお声をよくいただきます。」' },
  'size_future':       { label: '将来の拡張を見越して提案', response: '「今は小規模でも、将来的に客室を増やす予定があれば、今からシステムを整えておくとスムーズに拡張できます。タブレット型は1室単位で追加できますので、成長に合わせてご利用いただけます。」' },

  // ── 検討時期ではない ──
  'timing_future':     { label: '将来のために情報だけ送る', response: '「承知いたしました。ご検討の時期にぜひご参考いただければと思いますので、資料だけでもお送りさせていただけますでしょうか？今すぐでなくても、情報として持っておいていただくだけで大丈夫です。」' },
  'timing_task':       { label: '再架電タスクを設定する', response: '「わかりました。では、ご検討の時期に合わせてあらためてご連絡させていただきます。〇〇月頃にご連絡してもよろしいでしょうか？」' },
  'timing_subsidy':    { label: 'IT補助金の期限を伝えて動機づけ', response: '「実は今年のIT補助金の申請枠は早めに締め切られる可能性がございます。ご検討が先になる場合でも、補助金申請だけ先に進めておくことで費用を大幅に抑えられますので、早めにご相談いただけると幸いです。」' },
  'timing_competitor': { label: '競合が先に動く可能性を伝える', response: '「地域の競合ホテル様が先に導入されると、口コミやOTAの評価に差が出ることもございます。ご検討時期が来た際にスムーズに動けるよう、今のうちに資料だけでも持っておいていただけますでしょうか？」' },
  'timing_renovation': { label: '次の改修・リフォームに合わせる提案', response: '「次の設備改修やリフォームのタイミングに合わせてご導入いただく施設様も多いです。そのタイミングでご連絡いただければ、補助金の最新情報とともにご提案できますので、資料だけ持っておいていただけますか？」' },

  // ── クレーム ──
  'claim_apology':     { label: 'まず謝罪する', response: '「大変失礼いたしました。ご迷惑をおかけして申し訳ございません。今後はご連絡を控えさせていただきます。ありがとうございました。」（→ 架電クレームにステージ変更してHubSpotに記録する）' },
  'claim_record':      { label: 'HubSpotに記録して終了', response: '（電話を丁重に終了し、HubSpotの取引ステージを「架電クレーム」に変更する。タスクは削除。今後の架電対象から除外する。）' },
  'claim_freq':        { label: '架電頻度の謝罪と頻度調整の提案', response: '「たびたびご連絡してしまい大変失礼いたしました。以後のご連絡の頻度を大幅に減らすよう対応いたします。もし一切ご不要でしたら、その旨おっしゃいください。今後は一切ご連絡を控えさせていただきます。」' },
}

const CATEGORY_ITEMS = [
  { id: 'cat_busy',       children: ['busy_later', 'busy_short', 'busy_task', 'busy_mail', 'busy_time_ask', 'busy_empathy'] },
  { id: 'cat_nointerest', children: ['nointerest_reason', 'nointerest_future', 'nointerest_seminar', 'nointerest_flow', 'nointerest_info', 'nointerest_subsidy', 'nointerest_competitor'] },
  { id: 'cat_other',      children: ['other_maker', 'other_compare', 'other_renewal', 'other_weakness', 'other_coexist'] },
  { id: 'cat_price',      children: ['price_subsidy', 'price_running', 'price_season', 'price_small', 'price_roi', 'price_subsidy_detail'] },
  { id: 'cat_key',        children: ['key_cylinder', 'key_smartlock', 'key_receipt', 'key_keybox', 'key_cost'] },
  { id: 'cat_custom',     children: ['custom_order', 'custom_example', 'custom_ryokan', 'custom_hospi', 'custom_demo', 'custom_ui'] },
  { id: 'cat_pms',        children: ['pms_list', 'pms_develop', 'pms_standalone', 'pms_api'] },
  { id: 'cat_unmanned',   children: ['unmanned_pr', 'unmanned_night', 'unmanned_inbound', 'unmanned_hybrid', 'unmanned_elderly', 'unmanned_staff'] },
  { id: 'cat_person',     children: ['person_time', 'person_front', 'person_callback', 'person_msg', 'person_name', 'person_best_time'] },
  { id: 'cat_email',      children: ['email_spam', 'email_recheck', 'email_resend', 'email_domain', 'email_change'] },
  { id: 'cat_seminar',    children: ['seminar_when', 'seminar_content', 'seminar_nudge', 'seminar_record'] },
  { id: 'cat_inbound',    children: ['inbound_lang', 'inbound_passport', 'inbound_cc', 'inbound_demand'] },
  { id: 'cat_size',       children: ['size_tablet', 'size_other', 'size_case', 'size_future'] },
  { id: 'cat_timing',     children: ['timing_future', 'timing_task', 'timing_subsidy', 'timing_competitor', 'timing_renovation'] },
  { id: 'cat_claim',      children: ['claim_apology', 'claim_record', 'claim_freq'] },
]"""

# 古いOBJECTION_TREE + CATEGORY_ITEMSを新しいものに差し替える
old_start_marker = "const OBJECTION_TREE: Record<string, { label: string; response: string }> = {"
old_end_marker = "  { id: 'cat_claim',      children: ['claim_apology', 'claim_record'] },\n]"

start_idx = content.find(old_start_marker)
end_idx = content.find(old_end_marker) + len(old_end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_tree + content[end_idx:]
    print(f"Replaced. New length: {len(content)}")
else:
    print(f"ERROR: start={start_idx}, end={end_idx}")

with open(FILE, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Done')
