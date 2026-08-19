-- 引き当てルール シードデータ
-- Supabase SQL Editor に貼り付けて実行: https://supabase.com/dashboard/project/fjkpdejyusnttbhdmyxt/sql/new

create table if not exists assignment_rules (
  id uuid default gen_random_uuid() primary key,
  keyword text not null,
  assignee text not null,
  assignee_email text,
  action text,
  notes text,
  priority integer default 0,
  is_active boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
alter table assignment_rules enable row level security;
do $$ begin
  if not exists (select 1 from pg_policies where tablename='assignment_rules' and policyname='authenticated users can all on assignment_rules') then
    execute 'create policy "authenticated users can all on assignment_rules" on assignment_rules for all using (auth.role() = ''authenticated'') with check (auth.role() = ''authenticated'')';
  end if;
end $$;

truncate table assignment_rules restart identity cascade;

insert into assignment_rules (keyword, assignee, assignee_email, action, notes, priority) values

-- ========== 重要（優先対応） ==========
('【訪問案件】ウルトラプリンター / UTM / HEMS / Hacomono訪問設置', '山本さん（不在時：岡村さん）', null, 'Slack新人Gに新規投稿、山本さん・岡村さんメンション', '！重要', 10),
('リユースPC / 中古PC / メガアウ / イレギュラー支払い', '山本さん', null, 'Slack新人Gに新規投稿、山本さん・岡村さんメンション', '！重要 / 件名に「※田中社長確認 【くじらITサポートサービス】イレギュラー支払依頼」が含まれるメールも対象 / タドコロアヤ様宛営業停止連絡の場合は会社名・HPアドレス確認後に岡村さんへ共有', 10),
('【訪問案件】HEMS交換手配', '山本さん（不在時：岡村さん）', null, 'Slack新人Gに新規投稿、山本さん・岡村さんメンション', '！重要 / HEMS本体は大和ハウス商品。注文書必要。工賃15,000円(税抜)。電力ロガーは別途手配料。', 10),
('【訪問案件】ハルエネでんき', '山本さん（不在時：岡村さん）', null, 'Slack新人Gに新規投稿、山本さん・岡村さんメンション', '！重要', 10),
('ハルエネ電気工事受付（作業員から）', '山本さん（不在時：岡村さん）', null, 'Slack新人Gに新規投稿、KTSで案件検索しその他連絡で報告→BCとMD対応完了', '！重要', 10),

-- ========== 岡田さん ==========
('請求書関連 / 支払い通知書 / 発注書関係', '岡田さん（一部岡村さん）', 'mami_okada@kujira.co.jp', 'MD引き当て（完了にしない）', 'KTS関係はCC泉岡さん / [Misoca]H&H御中分は岡村さん / MDに届くWEB請求書は岡田さん', 5),
('エレコム注文書', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て（完了にしない）、フォルダ：大_サポート', null, 5),
('[Bubble] Invoice', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て（完了にしない）', '英語の請求書', 5),
('作業員から支払いの問い合わせ', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て（完了にしない）', null, 5),
('【依頼】3月期販売手数料実績ご報告期日', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('販売手数料実績ご報告期日', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('裁判所関連', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('[佐川急便] 請求内容確定', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('Web請求書掲載のお知らせ ヤマト運輸', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('[NP掛け払い] 請求書発送', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('【弥生】ご請求金額 / サービス契約自動更新', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', '弥生会計', 5),
('[Misoca]請求書が自動作成', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('【GMOとくとくBB】', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', 'くじら光コラボ料金', 5),
('【GMO-PG】請求金額確定 / 振込金額確定', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', 'チェックイン等の口座引落回収金額案内', 5),
('NTT東日本代理店コード', '岡田さん・岡村さん', 'mami_okada@kujira.co.jp', 'MD引き当て', 'サーモイン 03.NTT東日本‗取次票 保存。最新1件のみ保管、古いものは削除', 5),
('申請番号の手続が「手続終了」 登記・供託', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('【確認依頼】弊社売上分 注文書交付状況確認書', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('【支払明細書Webサービス】帳票公開', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('[Rakuten BillPay] 総合精算書 / billpay-info@billpay.rakuten.co.jp', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('株式会社ベネフィットジャパン / no-reply@onlyservice-2009.jp', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', '毎月各フォルダに1通届く', 5),
('「パートナーシップ構築宣言」取組状況調査', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),
('Bubble（岡田さん）', '岡田さん', 'mami_okada@kujira.co.jp', 'MD引き当て', null, 5),

-- ========== 北浦さん ==========
('銀行からの送金関係', '北浦さん', 'kitaura@kujira.co.jp', 'MD引き当て', null, 5),
('国際宅配便 UPS ジャパン', '北浦さん', 'kitaura@kujira.co.jp', 'MD引き当て', null, 5),
('レースパーツ事業部宛（FAX）', '北浦さん', 'kitaura@kujira.co.jp', 'メールで共有', null, 5),
('2回振り込んでしまった', '北浦さん・岡田さん', 'kitaura@kujira.co.jp', 'MD引き当て', '本当か入金依頼確認→重複なら返金先確認→イレギュラー支払いで返金依頼', 5),
('輸入申告代行手数料・関税等お支払い', '北浦さん', 'kitaura@kujira.co.jp', 'MD引き当て', '近藤義嗣（コンドウヨシツグ）相談役宛FAX。ARRIVAL NOTICEや関税FAXは履歴残して対応済みに。', 5),
('くじらレーシング', '北浦さん', 'kitaura@kujira.co.jp', 'MD引き当て、フォルダ：くじらWEBSHOP', 'レーシングシミュレーター', 5),

-- ========== 泉岡さん ==========
('くじらCRMなど自社製品の不明な内容', '泉岡さん', 'izuoka@kujira.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),
('【新規案件】マックスサポートなど', '泉岡さん', 'izuoka@kujira.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),
('WOB昭和町', '泉岡さん', 'izuoka@kujira.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),
('【スマホ端末故障連絡】白浜彩朝楽', '泉岡さん', 'izuoka@kujira.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),
('お帰り便データ', '泉岡さん', 'izuoka@kujira.co.jp', '直接電話（不在時はLINE）', null, 5),
('国際エキスプレス ARRIVAL NOTICE / 深圳デスクトップ', '泉岡さん', 'izuoka@kujira.co.jp', 'メール直接連絡（PDF添付）、FAXに「日付〇〇共有済み」記載', 'CC岡田さん / 急ぎは電話も可（080-4789-5532）', 5),
('国際エキスプレス_輸入CFS貨物引取り依頼書', '泉岡さん', 'izuoka@kujira.co.jp', 'MD引き当て', 'CC: mami_okada@kujira.co.jp', 5),
('デリバリーオーダー', '泉岡さん', 'izuoka@kujira.co.jp', 'MD引き当て', null, 5),
('モリタ宮田工業', '泉岡さん・田村さん', 'izuoka@kujira.co.jp', 'MD引き当て', 'テレワークブースに利用している消火器メーカー', 5),

-- ========== 田村さん ==========
('テレワークブース / 冷凍宅配ボックス / 宅配ボックス（不具合以外） / スマート宅配ボックス見積', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('AnyManager支払い通知書', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('Stripeアカウント', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('AdvaNceD IoTエレベーターコントローラー 資料請求', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'テレワークブース・エレベーターコントローラーも含む', 5),
('キッチンカーのアドバンスIoT', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('AdvaNceD IoTラゲッジドック', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('EMMC', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('金沢NOW', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('くじらCRM利用者の問い合わせ', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('新規サーモインのお問い合わせ', '田村さん', 'elan1965@gmail.com', 'メールで送信', null, 5),
('【Xserverアカウント】■重要■ SSLサーバー証明書 evodesignhub.com', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可', 5),
('マンションのオートロック一次営業対応', '田村さん', 'elan1965@gmail.com', 'メール直接連絡', 'MDで振り分け不可。ビジネスコールの場合もメールで連絡。', 5),
('スマートロッカーのフランチャイズパートナー向けモデル', '田村さん', 'elan1965@gmail.com', 'Slack新人質問用チャンネルで共有（先方メールアドレスと受信日時・メール文を添付）', null, 5),
('ビズリサーチの会員から資料請求', '田村さん', 'elan1965@gmail.com', 'メール送信、CCにサポートIOT', '社長指示 2025/04/04', 5),
('楽天市場ＥＣコンサルタント', '田村さん', 'elan1965@gmail.com', 'MD担当変更', '担当変更連絡', 5),
('AdvaNceD IoTバゲッジストレージ', '田村さん', 'elan1965@gmail.com', 'MD引き当て', null, 5),

-- ========== 田中社長 ==========
('レーシングシミュレーター補助金 / 販売代理店希望', '田中社長', 'minoru_tanaka@kujira.co.jp', 'MD引き当て', null, 5),
('ホテルWi-Fiトラブルソリューション', '田中社長', 'minoru_tanaka@kujira.co.jp', 'ヒアリング後メール報告', '◆ヒアリング：会社名・担当者名・住所・メールアドレス・電話番号・簡単な状況 / 作業員後のWIFI関係はバックオフィス対応', 5),
('くじら光', '田中社長', 'minoru_tanaka@kujira.co.jp', 'ヒアリング後メール報告', '◆ヒアリング：登録の正式会社名・担当者名・住所・登録電話番号・折り返し先・簡単な状況', 5),
('くじらCRM（新規）', '田中社長', 'minoru_tanaka@kujira.co.jp', 'MD引き当て', '新規案件のみ', 5),
('ふるさと納税', '田中社長', 'minoru_tanaka@kujira.co.jp', 'メール送信', null, 5),
('7NET / 詐欺サイト（https://7net.jeshop.ru.com/）', '田中社長', 'minoru_tanaka@kujira.co.jp', 'MD引き当て・社長に報告', '弊社運営サイトではない詐欺サイト。警察通報済み。お客様にも警察相談を案内。', 5),
('自社WEBサーバー問い合わせ', '田中社長', 'minoru_tanaka@kujira.co.jp', 'MD引き当て', null, 5),

-- ========== 高柳さん ==========
('Makuakeのクラファンプロジェクト', '高柳さん', 'takayanagi@kujira.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),
('ペットフード（レトルトパウチ等）', '高柳さん', 'takayanagi@kujira.co.jp', 'MD引き当て', null, 5),
('弊社の冊子・カタログ作成案件', '高柳さん', 'takayanagi@kujira.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),

-- ========== 堀内さん ==========
('くじら応募', '堀内さん', 'shiromofufactory@gmail.com', 'ヒアリング後メール報告（CC:社長）', '◆ヒアリング：メールアドレスと不具合内容 / 電話での対応は不可', 5),
('アシストジャパン・システム不具合', '堀内さん', 'shiromofufactory@gmail.com', 'MD引き当て', null, 5),

-- ========== 堀越さん ==========
('アンテナ工事関連', '堀越さん', null, 'MD引き当て、フォルダ：北_一条工務店', 'KTSで電話番号検索するとアンテナ工事のお客様で登録あり', 5),
('一条（BC）', '堀越さん', null, 'MD引き当て、フォルダ：北_一条工務店', null, 5),

-- ========== 橋本さん ==========
('AdvaNceD IoTスマートチェックイン 資料請求がありました', '橋本さん', 'tadashi_hashimoto@kujira.co.jp', 'MD引き当て、フォルダ：九地良', '混雑感知システム', 5),
('AdvaNceD IoTスマートチェックイン for クラウドスマートロック ホームページからの資料請求', '橋本さん', 'tadashi_hashimoto@kujira.co.jp', 'MD引き当て、フォルダ：九地良', null, 5),
('スマートオートロック（ホテル系）新規', '橋本さん', 'tadashi_hashimoto@kujira.co.jp', 'ヒアリング後メール報告（CC:社長・野田さん・米山さん）', null, 5),

-- ========== 野田さん ==========
('スマートチェックインforレンタカー', '野田さん', 'shohei_noda@device-agency.co.jp', 'メール転送後コメント記載し対応完了', 'CC: izuoka@device-agency.co.jp', 5),
('マックスサポート案件シート', '野田さん', 'shohei_noda@device-agency.co.jp', 'MD引き当て', null, 5),
('キャップ関連の電話', '野田さん', 'shohei_noda@device-agency.co.jp', 'Slackでローマ様へ確認', null, 5),

-- ========== 岡村さん ==========
('Makuakeストア', '岡村さん', null, 'Slack新人Gに新規投稿、岡村さんメンション', null, 5),
('Indeed採用関連', '岡村さん', null, 'Slack新人Gに新規投稿、岡村さんメンション', null, 5),
('パートナー登録', '岡村さん', null, 'MD引き当て', null, 5),
('パートナー削除', '岡村さん', null, 'MD引き当て', '【全般】業務マニュアル＞電話対応一覧＞120行目参照', 5),
('Cloud Edge / クラウドエッジ', '岡村さん', null, 'Slack新人Gに新規投稿、岡村さんメンション', null, 5),
('ハローワーク / 人事・採用関係', '岡村さん', null, 'Slack新人Gに新規投稿、岡村さんメンション', null, 5),
('[NifMo管理者様へ]', '岡村さん', null, 'Slack新人Gに新規投稿、岡村さんメンション', null, 5),
('スマートロックマンション（玄関）新規', '田村さん', 'elan1965@gmail.com', 'ヒアリング後メール報告（CC:社長・野田さん・米山さん）', null, 5),

-- ========== 武内さん ==========
('キャッシュレスコインランドリー / AdvaNceD IoTキャッシュレス for コインランドリー 資料請求', '武内さん', 'yasushi_takeuchi@device-agency.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),
('コインランドリー連合会', '武内さん', 'yasushi_takeuchi@device-agency.co.jp', 'メール直接連絡', 'MDで振り分け不可', 5),

-- ========== 森田さん ==========
('エレコムWiFi案件 / エレコム案件 / ユアサ商事', '森田さん', 'yoshiteru_morita@kujira.co.jp', 'MD引き当て、フォルダ：大_サポート', 'com@elecom.co.jpとのやり取りメール', 5),
('i-PRO / CCPOST-（数字）代理起票', '森田さん', 'yoshiteru_morita@kujira.co.jp', 'MD引き当て、フォルダ：大_サポート', 'I-PRO、i-pro', 5),

-- ========== 山本さん ==========
('訪問案件全般（UTM・ITサポート等）', '山本さん', null, 'Slack「新人質問用チャンネル」で内容共有', 'Slack新人Gに新規投稿、山本さん・岡村さんメンション', 5),
('補助金関係 / 小規模事業者持続化補助金 / IT導入補助金', '山本さん', null, 'Slack新人Gに新規投稿、山本さんメンション', 'IT導入補助金事務局: info@it-shien.smrj.go.jp は漏れなく担当へ振る', 5),
('助成金について', '山本さん', null, 'Slack新人Gに新規投稿、山本さんメンション', null, 5),
('SPITSS（九地良ITSS）', '山本さん', null, 'Slack新人Gに新規投稿、山本さんメンション', null, 5),
('連絡事項登録のお知らせ（KTS）', '山本さん・岡村さん', null, 'Slack新人Gに新規投稿、山本さん・岡村さんメンション', 'KTSからの作業員連絡事項。内容確認して対応できるものは対応、確認必要なら担当またはクライアントへ確認。', 5),

-- ========== 今津さん ==========
('今津さん宛の連絡', '今津さん', 'kouheiimazu@gmail.com', 'MD引き当て', 'KTS送付先一覧1183行目参照', 5),

-- ========== 杭全さん（アクセア） ==========
('アクセア', '杭全様', 'kumata@accea.co.jp', 'MD引き当て、担当へ連絡', '店舗からの直接連絡は受け付けず。アクセア担当者がヒアリング後に当社へ連絡する予定。社長指示。', 5),
('Bubble accea-locker-app 超過使用通知 / o2cpbox.jp', '対応完了', null, '対応完了', 'アクセアロッカーアプリ超過連絡。自動的に請求書に反映されるため対応不要。', 0),

-- ========== OP全員 ==========
('くまLINEグループ 担当者不明案件', 'OP全員', null, 'メールIDや件名・全文社内周知後にMailDealer対応完了', '担当不明のメールは担当不明受電と同じ', 3),
('デバイス・九地良商材全般の不具合問い合わせ（サーモイン・宅配ボックス・スマートチェックイン等）', 'OP全員', null, '新規→Slackに転記して一次対応、MDコメントに「Slack転記済み」で対応完了 / 継続案件→担当者MD割振りで顧客別フォルダ移動', '◆ヒアリング：社名・物件名・担当者名・製品/サービス名・折り返し先・状況 / BCメールはフォルダ移動なし・対応完了のみ / スマートロッカー新規は田村さん担当（2026/8/5追記）', 3),
('不具合以外の商品案内（スマートチェックイン・スマートロック・ルームタブレット等）', 'OP全員', null, 'ヒアリング後メール報告（橋本さんor田村さんへ、CC:社長・野田さん・米山さん）', '◆ヒアリング：店舗名・担当者名・折り返し先・状況 / MD振り分け後は対応完了にしない / メール転送の場合はコメントに「〇〇さんへ転送済み」記載 / MDによる問い合わせはヒアリングせずに担当変更', 3),
('【新規依頼案件】ご相談', 'OP全員', null, '内容確認して対応', null, 3),
('【新規依頼案件】光回線廃止に伴う通信機器取り外し', 'OP全員', null, '内容確認して対応', null, 3),
('くじらSMSの利用者から問い合わせ', 'OP全員', null, '登録した会社に問い合わせるよう案内', 'くじらSMSはサービス提供のみ。利用者への対応は不可。', 3),
('オレンジスピリッツからの重要なお知らせ / オレンジメール・オレンジフォーム利用者案内', 'OP全員', null, 'LINEグループ「九地良社内周知」にて内容案内', null, 3),
('楽天ショップ関連・Yahooショップ関連 / くじらレーシング / R32ONEOFF', 'OP全員', null, '電話での問い合わせはメール誘導（webshop@kujira.co.jp）', '担当常駐なし。電話→「担当が席を外している」と案内。楽天・Yahooはサイトから問い合わせ依頼。', 3),
('カギ本舗', 'OP全員', null, '対応', null, 3),
('宅配ボックスでエラーが発生しました', 'OP', null, 'Slackに報告・内容に応じて一次対応', null, 3),
('接続ドットコム', 'OP', null, '内容確認して対応', null, 3),
('くじらWEB/作業員マニュアル更新', 'OP全員', null, 'MD対応', null, 3),
('システムについての不具合・問い合わせ', 'OP全員', null, '【全般】業務マニュアル>電話対応一覧45行目参照', null, 3),
('大和ハウス', 'OP全員→岡村さん・山本さんへ報告', null, '未読でフォルダ移動、新人報告用チャンネルで岡村さん・山本さん宛に受信報告', '一度開いたものも未読にしてフォルダ移動', 3),
('[ラクスル]関係', '発注者（DM対応完了）', null, 'ラクスルからのメールは発注した方を担当に振る', '担当不明の場合はチーム内確認。確認できない方へはメール転送。', 3),

-- ========== 対応完了 ==========
('order-update@saisoncard.co.jp / dl@jun.zaq.jp / order-update@ra.net / info@fnxyzld.org / support@giy364.com / support@ugv465.com', '対応完了', null, '対応完了', 'フィッシング詐欺メール（判明分）', 0),
('Halbert-kts@daniels-rose-order.donotrun.com / yasudahitoshi998@toizm.com / press@newsrelea.se', '対応完了', null, '対応完了', 'フィッシング詐欺メール / press@newsrelea.seは社長指示で放置OK', 0),
('インターリンク', '対応完了', null, '対応完了', null, 0),
('【重要】ファミペイ重要なお知らせ / 【行政通知】税金未納について', '対応完了', null, '対応完了', 'スパム・詐欺メール', 0),
('弊社より送付している内容', '対応完了', null, '対応完了', null, 0),
('酸素ボックス 疎通確認メール', '対応完了', null, '対応完了', null, 0),
('【重要なお知らせ】三井住友カードセキュリティチェック', '対応完了', null, '対応完了', '調べたら詐欺メール。内容「三井住友カードご利用いただけなかったお取引」→対応完了でOK', 0),
('【ご意向確認】置き配サービス提供開始 ヤマト運輸', '対応完了', null, '対応完了', null, 0),
('[緊急の連絡】三井住友カードサービスの緊急連絡', '担当者なしでそのまま', null, '担当者なしでそのまま', null, 0),
('法人名：イノベーション', '対応完了', null, '対応完了', 'エキスポ御礼と言ってくる営業電話。社長確認済。', 0),
('hacomonoのo2ボックス関連', '対応完了', null, '対応完了', '高柳さんが対応中。自動割振りされた場合のみ対応完了。', 0),
('エコテクソリューション株式会社 / JET2022年12月度最終棚卸報告依頼', '対応完了', null, '対応完了', '入荷なし・案件なしのため返信不要', 0),
('クラウドレコーディング - 〇〇様が利用可能になりました', '対応完了', null, '対応完了', null, 0),
('お知らせが更新されました グローバルキャスト楽天casa事務局', '対応完了', null, '対応完了', null, 0),
('【Xserverアカウント】新しい端末からのログインがありました', '対応完了', null, '対応完了', null, 0),
('【重要】ログイン画面リニューアル Chatwork', '対応完了', null, '対応完了', null, 0),
('34才 PHPを使用した開発 ITエンジニアのご提案', '対応完了', null, '対応完了', 'スパムメール', 0),
('Dropbox 共有フォルダの先週のアップデート', '対応完了', null, '対応完了', null, 0),
('イプロス', '対応完了', null, '対応完了', null, 0),
('ステイシーテストホテル 事前チェックインのご案内', '対応完了', null, '対応完了', null, 0),
('安全衛生推進者養成講習開催のお知らせ', '迷惑フォルダ', null, '対応不要', '常時雇用10名以下・サービス業のため適用外', 0),
('タイミー', 'OP（社長確認済で断り）', null, '掲載予定なしとお断り', '2024年2月現在掲載なし・今後も予定なし。社長確認済。', 0),
('[orico]情報の有効期限が切れ', 'なし', null, '対応なし（詐欺の可能性）', null, 0),
('日本MアンドAセンター / M&A総合研究所 / ISO情報セキュリティ規格の件', '対応完了', null, '対応完了（営業メール）', null, 0),

-- ========== その他 ==========
('※田中社長確認 受電報告', '田中社長', 'minoru_tanaka@kujira.co.jp', 'MD引き当て', '2週間以上経過したものは対応完了', 5),
('森田さん宛', '森田さん', 'yoshiteru_morita@kujira.co.jp', 'MD引き当て、フォルダ：大_サポート', null, 5),
('くじらSMS不具合（電話対応不可）', 'sms_support@kujira.co.jp', 'sms_support@kujira.co.jp', 'メール誘導（電話対応なし）、CC:社長', null, 5),
('宅配便（九地良宛）', '各所', null, '水日以外なら翌日来てもらう。デバイス宛なら泉岡さんへ確認', null, 3),
('Gビズ', '田中社長・高柳さん', 'minoru_tanaka@kujira.co.jp', 'ヒアリング後メール（TO:社長・CC:高柳さん）', 'yohtani2012topdog@gmail.comには送信不可 / ワンタイムパスワード通知→そのまま / 未登録端末アクセスお知らせ→対応完了', 5),
('株式会社ピカソ様（民泊）・民泊関係で警察から連絡', '周知', null, 'LINE[デバイス×AFP]にて周知報告', null, 5),
('WOB昭和町のガス点検立ち合い依頼', '周知', null, 'LINE[デバイス×AFP]にて周知報告', null, 5),
('タドコロアヤ送付NG', '注意', null, '送付停止リスト確認', 'https://docs.google.com/spreadsheets/d/15lAM15ovCRXRSzsURguhrx0ylmKfBztyVAwwdQe5WoY/', 5),
('ワンコネクトの若林様宛て', 'メールを受けた人が対応', null, '対応', '若林塑宇太様 <souta3010@yahoo.co.jp> 元払い・着払い確認等', 3),
('橋本さん宛のMD', null, null, '九地良へ移動', null, 3);

-- 確認
select assignee, count(*) as 件数 from assignment_rules group by assignee order by 件数 desc;
