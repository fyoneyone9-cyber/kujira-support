'use client'
import { useState, useCallback } from 'react'

// 切り返しデータ
const OBJECTION_TREE: Record<string, { label: string; response: string }> = {
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
  'busy_later':   { label: 'いつ頃なら大丈夫か確認する', response: '「承知いたしました。では、またお時間のよいときにご連絡させていただいてもよろしいでしょうか？いつ頃でしたらよろしいでしょうか？」' },
  'busy_short':   { label: '30秒だけお願いする', response: '「お忙しいところ大変恐れ入ります。30秒だけお時間いただけますでしょうか。資料をメールでお送りするだけでも、させていただければと思っております。」' },
  'busy_task':    { label: 'タスクに控えて後日かける', response: '「かしこまりました。では、後日あらためてご連絡させていただきます。〇〇様のお名前とご連絡先、確認させていただいてよろしいでしょうか？」' },

  // ── 興味がない ──
  'nointerest_reason':   { label: '具体的な理由を聞く', response: '「そうでございますか。差し支えなければ、どのような点でご興味をお持ちになれないか、教えていただけますでしょうか？もしコスト面や業態の問題でしたら、解決できた事例もご用意しております。」' },
  'nointerest_future':   { label: '将来的な可能性を確認', response: '「将来的にも、ご興味はないでしょうか？近年、全国からのお問い合わせが去年よりかなり多くなってきておりまして、業界全体でのスタンダードになりつつあります。参考情報だけでもお送りさせていただければと思います。」' },
  'nointerest_seminar':  { label: 'セミナーに誘う', response: '「弊社は週2回、オンラインの説明会を開催しております（水曜11時・金曜13時）。1時間程度で費用・導入事例なども詳しくご説明できます。ご参加は無料ですので、一度いかがでしょうか？」' },
  'nointerest_flow':     { label: '流行の波を伝える', response: '「最近よくお耳にするかとは思いますが、自動チェックイン機の件になります。全国各地のホテル様で急速に導入が進んでおりまして、業界のスタンダードになりつつある状況でございます。他社様に遅れをとらないためにも、一度ご検討いただけませんか？」' },
  'nointerest_info':     { label: '情報だけでも送る提案', response: '「ご興味がないのは承知いたしました。ただ、資料だけでもご覧いただけますと、具体的なコストや仕組みがよくわかります。メールアドレスをお教えいただければ今日中にお送りいたします。」' },

  // ── 他社使用中 ──
  'other_maker':    { label: 'どのメーカーか聞く', response: '「あ、そうでございましたか。差し支えなければ、どちらのメーカー様をご利用されているか、参考までに教えて頂けますでしょうか？」' },
  'other_compare':  { label: '比較提案に持ち込む', response: '「すでに導入されていらっしゃるのですね。弊社は自社開発のため、他社様にはない機能（シリンダー錠対応・完全オーダーメイドカスタマイズ等）がございます。現状の課題があれば、比較資料としてご覧いただけますでしょうか？」' },
  'other_renewal':  { label: '更新・リプレイス提案', response: '「現在ご利用のシステムの契約更新時期はいつ頃でしょうか？弊社は価格面でもご好評をいただいており、乗り換えを検討されている施設様も増えております。ちょうどそのタイミングで比較検討いただけると幸いです。」' },

  // ── 価格 ──
  'price_subsidy':  { label: 'IT補助金を案内する', response: '「弊社が補助金申請を代行できます。IT補助金活用でKIOSK筐体が最安48万円〜、タブレット型は13万円〜でご導入可能です。補助金があれば実質費用がかなり抑えられます。詳しい資料をお送りしてもよろしいでしょうか？」' },
  'price_running':  { label: '月額費用・コスト削減効果を説明', response: '「月額費用はKIOSK型で19,600円＋部屋数×200円、タブレット型は1室500円です。繁忙期のみ使用で使わない月は0円、日割り計算も可能です。一方で、フロントスタッフの人件費削減効果と比べると、多くの施設様で半年〜1年以内に回収されています。」' },
  'price_season':   { label: '季節限定プランを案内', response: '「ご使用にならない月は月額0円になります。繁忙期のみのご利用や、土日祝のみご使用の日割り計算プランもございます。実際の費用感をメールでご案内してもよろしいでしょうか？」' },
  'price_small':    { label: '小規模向け低コストプランを提示', response: '「小規模施設様向けには、タブレット型でご導入いただけます。初期費用はIT補助金活用で13万円〜、月額は1室500円です。一軒家や小規模旅館様にも導入実績がございます。」' },

  // ── カードキー・鍵 ──
  'key_cylinder':   { label: 'シリンダー錠対応をPR', response: '「弊社の強みは、シリンダー錠（物理キー）にも対応可能なことです！別売りのキーボックスを使うことで、清算が完了すると自動でキーボックスが開き、お客様がセルフで鍵をお受け取りいただけます。カードキーへの変更は一切不要です。」' },
  'key_smartlock':  { label: 'クラウドスマートロックを提案', response: '「クラウドスマートロックという選択肢もございます。暗証番号で開錠でき、チェックイン機から排出されるレシートに暗証番号が自動で印字されます。鍵の受け渡しが完全にセルフになります。」' },
  'key_receipt':    { label: 'レシート×対面方式を提案', response: '「もし接客を残したい場合は、チェックイン機で清算まで済ませてレシートを発行し、そのレシートをフロントで鍵と交換するという運用も可能です。対面の接客要素を残しながら、手続きだけ効率化できます。」' },

  // ── 業態・カスタマイズ ──
  'custom_order':   { label: 'オーダーメイドをPR', response: '「普段スタッフが口頭でご説明していることを、チェックイン機にカスタマイズして組み込むことが可能です。弊社は自社開発のため、御社専用のオーダーメイドをご提供できます。他社様には真似のできない強みです。」' },
  'custom_example': { label: '同業態の導入事例を提示', response: '「弊社では接客の質を落とさずに手続きだけをスマート化して、顧客満足度を上げた事例がございます。同じような業態の施設様の導入事例を資料でお送りしてもよろしいでしょうか？」' },
  'custom_ryokan':  { label: '旅館・温泉施設への対応', response: '「旅館様でも多数ご導入いただいております。日帰り温泉客の受付・清算、朝食券・夕食券の発行など、旅館特有の運用にもカスタマイズ対応できます。お話しだけでもいかがでしょうか？」' },
  'custom_hospi':   { label: 'ホスピタリティを落とさない訴求', response: '「チェックイン機を導入することで、フロントスタッフがチェックイン手続きから解放され、観光案内やお出迎えなどの本来の接客に集中できるようになります。結果としてホスピタリティが向上した施設様も多くいらっしゃいます。」' },

  // ── PMS連携 ──
  'pms_list':       { label: 'PMS連携実績を案内', response: '「弊社はPMS（ホテルシステム）との連携開発に近年力を入れています。連携実績：ステイシー・スイートブック・ベッツ24。現在も複数のPMSと連携開発が進行中です。御社のPMSについても、ぜひ一度ご相談いただけますでしょうか？」' },
  'pms_develop':    { label: '連携開発の意欲を伝える', response: '「お客様のご要望によりかなりの頻度で連携開発が進んでいますので、御社のPMSも今後連携開発を進めることが可能です。まずはシステム名をお教えいただけますでしょうか？」' },

  // ── 無人化 ──
  'unmanned_pr':    { label: '省人化・効率化に言い換える', response: '「「無人化」というより、「省人化」・「業務効率化」のツールとしてご活用いただいております。フロントスタッフがチェックイン手続きから解放されることで、お客様との会話や観光案内など、本来の接客サービスにより集中できるようになります。」' },
  'unmanned_night': { label: '夜間・深夜帯の対応として訴求', response: '「特に夜間や深夜帯のチェックインで効果を発揮します。スタッフが不在の時間でも、お客様が自分でチェックインできるため、深夜のフロント対応を大幅に削減できます。」' },
  'unmanned_inbound': { label: 'インバウンドへの対応力', response: '「外国語対応（13か国語）とパスポートスキャン機能により、インバウンドのお客様もスムーズにチェックインできます。言語の壁がなくなることで、スタッフの対応負担が大幅に減ります。」' },

  // ── 担当者不在 ──
  'person_time':    { label: 'いつ頃いるか確認する', response: '「承知いたしました。失礼いたしました。何時（何日）ごろでしたら担当の支配人様とお話できますでしょうか？」' },
  'person_front':   { label: 'フロントに資料送付をお願いする', response: '「では、フロントの方にお願いして、担当の支配人様にご一読いただけるよう資料をメールでお送りしてもよろしいでしょうか？よろしければメールアドレスをお教えいただけますか？（フロントの方のお名前も頂戴できますと幸いです。）」' },
  'person_callback':{ label: 'かけ直しをお願いする', response: '「ありがとうございます。では〇〇（時間帯）にあらためてお電話させていただきます。よろしくお願いいたします。」' },
  'person_msg':     { label: 'フロントに伝言をお願いする', response: '「よろしければ、「デバイスエージェンシーの〇〇より、自動チェックイン機のご案内でお電話がありました」とお伝えいただけますでしょうか？後ほどあらためてご連絡させていただきます。」' },

  // ── メール未着 ──
  'email_spam':     { label: '迷惑メールを確認してもらう', response: '「もしかしますと迷惑メールフォルダに入っている可能性がございます。「迷惑メールでないことを報告」をクリックしていただきますと、今後は受信ボックスに届くようになります。」' },
  'email_recheck':  { label: 'アドレスを再確認する', response: '「念のためメールアドレスをもう一度ご確認させていただけますでしょうか？正しいアドレスでも届かない場合は、一度フロントの方のアドレスから弊社へ送信していただくと、今後スムーズに送受信できるようになります。」' },
  'email_resend':   { label: 'こちらから再送する', response: '「承知いたしました。再度お送りいたします。件名は「〇〇様　自動チェックイン機のご案内」でお送りしますので、ご確認いただけますでしょうか。もし届かなければお電話でご連絡ください。」' },

  // ── セミナー ──
  'seminar_when':   { label: 'セミナー日程を案内する', response: '「オンラインセミナーは毎週水曜日11時〜・金曜日13時〜開催しております（1時間程度・参加無料）。ご都合に合わせて別日のご案内も可能ですので、ご希望の日時をお教えください。」' },
  'seminar_content':{ label: 'セミナー内容を説明する', response: '「セミナーでは、実際の操作デモ・価格・補助金・導入事例・PMSとの連携などを1時間でご説明いたします。個別のご質問もその場でお答えできます。ZoomのURLをお送りいたしますので、メールアドレスをいただけますでしょうか？」' },
  'seminar_nudge':  { label: 'まず資料→後でセミナー提案', response: '「まず資料だけでもご覧いただき、ご興味があればセミナーにもお気軽にご参加いただける形でいかがでしょうか？資料をお送りするだけなら1分で済みます。メールアドレスをいただけますか？」' },

  // ── インバウンド ──
  'inbound_lang':   { label: '多言語対応（13か国語）を説明', response: '「弊社の自動チェックイン機は13か国語に対応しております。外国語が苦手なスタッフ様でも、インバウンドのお客様に対応できます。パスポートスキャン・本人確認もチェックイン機で完結します。」' },
  'inbound_passport':{ label: 'パスポートスキャン機能を説明', response: '「インバウンド対応として、パスポートスキャンと顔写真撮影による本人確認機能がございます。外国籍のお客様の情報を自動で取得・記録できるため、フロントの手間が大幅に減ります。」' },

  // ── 小規模 ──
  'size_tablet':    { label: 'タブレット型を提案', response: '「小規模施設様にはタブレット型がございます。初期費用はIT補助金活用で13万円〜、月額は1室500円から。一軒家（シングルプラン）でも49,800円〜でご導入いただけます。」' },
  'size_other':     { label: 'ルームタブレット・スマートロックを提案', response: '「部屋数が少ない施設様でも、ルームタブレット（内線電話・月額1室100円〜）やクラウドスマートロックなど、チェックイン機以外の製品もご活用いただけます。組み合わせることで業務効率が上がります。」' },

  // ── 検討時期ではない ──
  'timing_future':  { label: '将来のために情報だけ送る', response: '「承知いたしました。ご検討の時期にぜひご参考いただければと思いますので、資料だけでもお送りさせていただけますでしょうか？今すぐでなくても、情報として持っておいていただくだけで大丈夫です。」' },
  'timing_task':    { label: '再架電タスクを設定する', response: '「わかりました。では、ご検討の時期に合わせてあらためてご連絡させていただきます。〇〇月頃にご連絡してもよろしいでしょうか？」' },

  // ── クレーム ──
  'claim_apology':  { label: 'まず謝罪する', response: '「大変失礼いたしました。ご迷惑をおかけして申し訳ございません。今後はご連絡を控えさせていただきます。ありがとうございました。」（→ 架電クレームにステージ変更してHubSpotに記録する）' },
  'claim_record':   { label: 'HubSpotに記録して終了', response: '（電話を丁重に終了し、HubSpotの取引ステージを「架電クレーム」に変更する。タスクは削除。今後の架電対象から除外する。）' },
}

const CATEGORY_ITEMS = [
  { id: 'cat_busy',       children: ['busy_later', 'busy_short', 'busy_task'] },
  { id: 'cat_nointerest', children: ['nointerest_reason', 'nointerest_future', 'nointerest_seminar', 'nointerest_flow', 'nointerest_info'] },
  { id: 'cat_other',      children: ['other_maker', 'other_compare', 'other_renewal'] },
  { id: 'cat_price',      children: ['price_subsidy', 'price_running', 'price_season', 'price_small'] },
  { id: 'cat_key',        children: ['key_cylinder', 'key_smartlock', 'key_receipt'] },
  { id: 'cat_custom',     children: ['custom_order', 'custom_example', 'custom_ryokan', 'custom_hospi'] },
  { id: 'cat_pms',        children: ['pms_list', 'pms_develop'] },
  { id: 'cat_unmanned',   children: ['unmanned_pr', 'unmanned_night', 'unmanned_inbound'] },
  { id: 'cat_person',     children: ['person_time', 'person_front', 'person_callback', 'person_msg'] },
  { id: 'cat_email',      children: ['email_spam', 'email_recheck', 'email_resend'] },
  { id: 'cat_seminar',    children: ['seminar_when', 'seminar_content', 'seminar_nudge'] },
  { id: 'cat_inbound',    children: ['inbound_lang', 'inbound_passport'] },
  { id: 'cat_size',       children: ['size_tablet', 'size_other'] },
  { id: 'cat_timing',     children: ['timing_future', 'timing_task'] },
  { id: 'cat_claim',      children: ['claim_apology', 'claim_record'] },
]

// ── キーワード→切り返しIDマッピング ──────────────────────────────
// 相手の発言に含まれそうなキーワードから推奨する切り返しIDを返す
const KEYWORD_MAP: Array<{ keywords: string[]; ids: string[] }> = [
  { keywords: ['忙しい', 'いそが', '今は', 'また今度', '後で', 'あとで', '手が離せ', 'タイミング悪', '時間ない'],
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
  { keywords: ['業態', '合わない', '合わない', 'うちには', '旅館', '民泊', '温泉', 'ゲストハウス', 'ホステル', '小規模', '規模が小さ'],
    ids: ['custom_order', 'custom_example', 'custom_ryokan', 'size_tablet'] },
  { keywords: ['pms', 'PMS', 'ホテルシステム', 'システム連携', '予約システム', 'ステイシー', 'スイートブック', 'ベッツ'],
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
  const matched = new Map<string, number>() // id → スコア
  for (const rule of KEYWORD_MAP) {
    for (const kw of rule.keywords) {
      if (lower.includes(kw.toLowerCase())) {
        for (const id of rule.ids) {
          matched.set(id, (matched.get(id) ?? 0) + 1)
        }
      }
    }
  }
  // スコア順にソート、上位6件まで
  return [...matched.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([id]) => id)
}
// ─────────────────────────────────────────────────────────────

type AiSuggestion = { label: string; talk: string; point: string }

const TABS = [
  { id: 'hubspot', label: '📊 HubSpot手順', icon: '📊' },
  { id: 'script', label: '📞 トークスクリプト', icon: '📞' },
  { id: 'yoneyama', label: '💰 米山パターン', icon: '💰' },
  { id: 'status', label: '🏷️ ステータス一覧', icon: '🏷️' },
  { id: 'knowledge', label: '💡 商品知識', icon: '💡' },
  { id: 'checklist', label: '✅ チェックリスト', icon: '✅' },
  { id: 'mail', label: '✉️ メールテンプレ', icon: '✉️' },
]

export default function TeleapoPage() {
  const [activeTab, setActiveTab] = useState('hubspot')
  const [copiedKey, setCopiedKey] = useState<string | null>(null)
  const [selectedCat, setSelectedCat] = useState<string | null>(null)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const suggestions = suggestByKeyword(searchInput)

  // ── AI サジェスト (Gemini) ──
  const [aiInput, setAiInput] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState<AiSuggestion[]>([])
  const [aiError, setAiError] = useState<string | null>(null)
  const [aiSelectedIdx, setAiSelectedIdx] = useState<number | null>(null)
  const [aiPattern, setAiPattern] = useState<'yoneyama' | 'hashimoto'>('yoneyama')

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

  // ── 米山パターン用 AI input ──
  const [yoneyamaInput, setYoneyamaInput] = useState('')
  const [yoneyamaLoading, setYoneyamaLoading] = useState(false)
  const [yoneyamaSuggestions, setYoneyamaSuggestions] = useState<AiSuggestion[]>([])
  const [yoneyamaError, setYoneyamaError] = useState<string | null>(null)
  const [yoneyamaSelectedIdx, setYoneyamaSelectedIdx] = useState<number | null>(null)

  const fetchYoneyamaSuggestions = useCallback(async (text: string) => {
    if (!text.trim()) return
    setYoneyamaLoading(true)
    setYoneyamaError(null)
    setYoneyamaSuggestions([])
    setYoneyamaSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern: 'yoneyama' }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setYoneyamaSuggestions(data.suggestions ?? [])
    } catch (e) {
      setYoneyamaError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setYoneyamaLoading(false)
    }
  }, [])

  // ── メモ欄 ──
  const MEMO_KEY = 'teleapo_memo'
  const MEMO_SAVES_KEY = 'teleapo_memo_saves'
  const [memoText, setMemoText] = useState<string>(() => {
    if (typeof window === 'undefined') return ''
    return localStorage.getItem(MEMO_KEY) ?? ''
  })
  const [savedMemos, setSavedMemos] = useState<Array<{ ts: string; text: string }>>(() => {
    if (typeof window === 'undefined') return []
    try { return JSON.parse(localStorage.getItem(MEMO_SAVES_KEY) ?? '[]') } catch { return [] }
  })
  const [memoSaved, setMemoSaved] = useState(false)
  const [memoOpen, setMemoOpen] = useState(false)

  const saveMemo = () => {
    if (!memoText.trim()) return
    localStorage.setItem(MEMO_KEY, memoText)
    const now = new Date()
    const ts = `${now.getMonth()+1}/${now.getDate()} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`
    const next = [{ ts, text: memoText }, ...savedMemos].slice(0, 10) // 最大10件
    setSavedMemos(next)
    localStorage.setItem(MEMO_SAVES_KEY, JSON.stringify(next))
    setMemoSaved(true)
    setTimeout(() => setMemoSaved(false), 2000)
  }

  const deleteSavedMemo = (i: number) => {
    const next = savedMemos.filter((_, idx) => idx !== i)
    setSavedMemos(next)
    localStorage.setItem(MEMO_SAVES_KEY, JSON.stringify(next))
  }

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
        <p className="text-slate-400 text-sm mt-1">株式会社デバイスエージェンシー ／ 自動チェックイン機 架電業務マニュアル</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 border border-slate-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* ─── TAB: HubSpot手順 ─── */}
      {activeTab === 'hubspot' && (
        <div className="space-y-6">

          {/* フロー */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            {[
              { step: '1', title: 'ビュー設定', desc: 'テーブルビューに切替・フィルター設定', color: 'blue' },
              { step: '2', title: '列の編集', desc: '前回の連絡・優先度を追加してソート', color: 'purple' },
              { step: '3', title: '対象選定', desc: '優先度「高」「中」はスキップ・上から順に', color: 'yellow' },
              { step: '4', title: '架電・更新', desc: '担当者変更→電話→ステージ更新', color: 'green' },
            ].map(item => (
              <div key={item.step} className="bg-slate-800 rounded-2xl border border-slate-700 p-5">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold mb-3 ${
                  item.color === 'blue' ? 'bg-blue-600 text-white' :
                  item.color === 'purple' ? 'bg-purple-600 text-white' :
                  item.color === 'yellow' ? 'bg-yellow-600 text-white' : 'bg-green-600 text-white'
                }`}>{item.step}</div>
                <p className="text-white font-bold text-sm mb-1">{item.title}</p>
                <p className="text-slate-400 text-xs leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* STEP1 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white">1</span>
                <h2 className="text-base font-bold text-white">ビューの設定とフィルター</h2>
              </div>
              <div className="space-y-3">
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-blue-400 mb-2">① テーブルビューに切り替え</p>
                  <p className="text-sm text-slate-300">HubSpot CRM の「取引」画面を開き、表示形式を<span className="text-blue-300 font-medium">「テーブルビュー」</span>に変更する。</p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-blue-400 mb-2">② 詳細フィルターを設定</p>
                  <p className="text-sm text-slate-300 mb-2">「楽天トラベル（未架電）」＋「担当者：未割り当て」または「不在」でフィルター</p>
                  <div className="bg-slate-900 rounded-lg px-3 py-2">
                    <p className="text-yellow-300 text-sm font-medium">楽天トラベル（不在）（スマートチェックイン）</p>
                  </div>
                </div>
              </div>
            </div>

            {/* STEP2 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-purple-600 rounded-full flex items-center justify-center text-xs font-bold text-white">2</span>
                <h2 className="text-base font-bold text-white">表示列の編集と並び替え</h2>
              </div>
              <div className="space-y-3">
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-purple-400 font-bold mb-1">① 「前回の連絡」を追加</p>
                  <p className="text-sm text-slate-300">「列を編集」から「前回の連絡」を検索して追加。</p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-purple-400 font-bold mb-1">② 「優先度」を追加</p>
                  <p className="text-sm text-slate-300">同様に「優先度」を追加。架電スキップの判断に使う。</p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-purple-400 font-bold mb-1">③ 「前回の連絡」で昇順ソート</p>
                  <p className="text-sm text-slate-300">矢印をクリックし、<span className="text-white font-medium">過去のものから順（昇順）</span>に並び替え。</p>
                </div>
              </div>
            </div>

            {/* STEP3 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-yellow-600 rounded-full flex items-center justify-center text-xs font-bold text-white">3</span>
                <h2 className="text-base font-bold text-white">架電対象の選定ルール</h2>
              </div>
              <div className="space-y-3">
                <div className="bg-red-950/50 border border-red-800/50 rounded-xl p-4">
                  <p className="text-xs text-red-400 font-bold mb-1">⚠️ スキップ</p>
                  <p className="text-sm text-slate-300">優先度<span className="text-red-300 font-bold">「高」または「中」</span>は架電不要。進行中案件の可能性が高い。</p>
                </div>
                <div className="bg-green-950/50 border border-green-800/50 rounded-xl p-4">
                  <p className="text-xs text-green-400 font-bold mb-1">✅ 架電順序</p>
                  <p className="text-sm text-slate-300">リストの<span className="text-green-300 font-bold">上から順番</span>に架電を進める。</p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-slate-400 font-bold mb-1">💡 効率化テク</p>
                  <p className="text-sm text-slate-300">ブラウザのタブを複製しておくと、リスト画面と詳細画面を素早く行き来できる。</p>
                </div>
              </div>
            </div>

            {/* STEP4 */}
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-7 h-7 bg-green-600 rounded-full flex items-center justify-center text-xs font-bold text-white">4</span>
                <h2 className="text-base font-bold text-white">架電の実施フロー</h2>
              </div>
              <div className="space-y-3">
                <div className="bg-red-950/50 border border-red-800/50 rounded-xl p-4">
                  <p className="text-xs text-red-400 font-bold mb-1">★ 必須：担当者変更</p>
                  <p className="text-sm text-slate-300">架電前に必ず担当者を<span className="text-red-300 font-bold">「自分の名前」</span>に変更！</p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-green-400 font-bold mb-1">① 電話をかける</p>
                  <p className="text-sm text-slate-300">通話ボタン →「電話をかける」をクリックして発信。</p>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-xs text-green-400 font-bold mb-1">② 取引ステージを更新</p>
                  <div className="flex gap-2 flex-wrap mt-1">
                    {['楽天トラベル（不在）', 'お断り', '資料送付', '本社へ', '架電クレーム', '他社製品使用'].map(s => (
                      <span key={s} className="text-xs bg-slate-600/60 text-slate-300 border border-slate-500 rounded-lg px-2 py-0.5">{s}</span>
                    ))}
                  </div>
                </div>
                <div className="bg-yellow-950/50 border border-yellow-800/50 rounded-xl p-4">
                  <p className="text-xs text-yellow-400 font-bold mb-1">📌 不在時は必ずタスク設定</p>
                  <p className="text-sm text-slate-300">いる時間帯・日を聞き出し【アクティビティ】→【タスク】を必ず設定すること。</p>
                </div>
              </div>
            </div>
          </div>

          {/* 資料送付フロー */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">📧 資料送付に至った場合の手順</h2>
            <ol className="space-y-2">
              {[
                '取引の物件を表示→概要から下にスクロール→「コンタクト」を開く',
                'コンタクトのプレビューを開き、Eメール欄にアドレスを入力',
                '担当者の【姓】に「〇〇」、【名】に「様」を追記',
                '電話番号の追加がある場合は「携帯番号」に追記',
                '「チェックイン機資料送付」の定型文をコピペして送付',
                '資料送付メール作成時は【挿入】→【署名】で署名を自動入力',
                '取引ステージを【資料送付】に変更',
                '会社プレビュー→【会社の担当者】に自分の名前を入力',
                'リードステータスを「資料送付3週間」または「資料送付インセンなし」に変更',
                'タスク期限を3週間後に設定（件名：「資料送付 〇/〇」）',
              ].map((item, i) => (
                <li key={i} className="flex gap-3 text-sm text-slate-300">
                  <span className="w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0 mt-0.5">{i + 1}</span>
                  {item}
                </li>
              ))}
            </ol>
            <div className="mt-4 bg-red-950/50 border border-red-800/50 rounded-xl p-3">
              <p className="text-xs text-red-400 font-bold">⚠️ インセン条件：受付・担当者の名前を両方聞けて初めて100円。メモ例：【担当受付共に〇●】</p>
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: トークスクリプト ─── */}
      {activeTab === 'script' && (
        <div className="space-y-6">

          {/* ── 切り返しナビ ── */}
          <div className="bg-slate-800 rounded-2xl border border-blue-800/40 p-6">
            <h2 className="text-xl font-bold text-white mb-1">⚡ 切り返しナビ</h2>
            <p className="text-sm text-slate-400 mb-5">相手の反応をクリック → 対応方法を選ぶ → トークが表示されます</p>

            {/* カテゴリボタン */}
            <div className="flex flex-wrap gap-3 mb-5">
              {CATEGORY_ITEMS.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => selectCat(cat.id)}
                  className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${
                    selectedCat === cat.id
                      ? 'bg-blue-600 text-white shadow-lg scale-105'
                      : 'bg-slate-700 text-slate-200 hover:bg-slate-600 hover:text-white border border-slate-500'
                  }`}
                >
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
                    <button
                      key={childId}
                      onClick={() => selectResponse(childId)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${
                        selectedResponse === childId
                          ? 'bg-green-600 text-white shadow-lg scale-105'
                          : 'bg-slate-700/70 text-slate-200 hover:bg-slate-600 hover:text-white border border-slate-500'
                      }`}
                    >
                      {OBJECTION_TREE[childId]?.label}
                    </button>
                  ))}
                </div>

                {/* トーク表示 */}
                {selectedResponse && (
                  <div className="bg-green-950/60 border-2 border-green-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <p className="text-base text-green-400 font-bold">💬 切り返しトーク</p>
                      <button
                        onClick={() => copy(OBJECTION_TREE[selectedResponse]?.response || '', 'objection')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${
                          copiedKey === 'objection' ? 'bg-green-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                        }`}
                      >
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

          {/* ── 米山パターン（IT補助金訴求型）スクリプト ── */}
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
                <div className="bg-green-900/30 px-4 py-2 border-t border-green-800/30">
                  <p className="text-xs text-green-300 font-bold mb-1">💡 アポ獲得のコツ</p>
                  <ul className="text-xs text-slate-300 space-y-0.5">
                    <li>・「資料送付 → その後15分」の2段階でハードルを下げる</li>
                    <li>・日程は「来週の火曜か水曜、どちらがご都合よいですか？」と二択で聞く</li>
                    <li>・Zoomでも可と伝えることで地方ホテルも対応できる</li>
                  </ul>
                </div>
              </div>

              {/* STEP 4 NO */}
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

          {/* ── AI切り返しサジェスト (Gemini API) ── */}
          <div className="bg-slate-900 rounded-2xl border border-purple-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">🤖 AI切り返しサジェスト</h2>
              <span className="text-xs bg-purple-900/60 border border-purple-700/50 text-purple-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-sm text-slate-400 mb-4">相手が言ったことをそのまま入力 → AIがデバイスエージェンシーの製品切り返しを表示</p>
            <div className="flex gap-2 mb-4">
              <button onClick={() => setAiPattern('yoneyama')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'yoneyama' ? 'bg-yellow-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💰 米山パターン（IT補助金訴求）
              </button>
              <button onClick={() => setAiPattern('hashimoto')}
                className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === 'hashimoto' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 border border-slate-600'}`}>
                💬 橋本パターン（ヒアリング型）
              </button>
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
              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${aiLoading ? 'bg-purple-900 text-purple-400 cursor-wait' : aiInput.trim() ? 'bg-purple-600 hover:bg-purple-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {aiLoading ? '⏳ 生成中...' : '✨ AI提案'}
              </button>
            </div>
            {aiError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-sm text-red-300">⚠️ {aiError}</div>}
            {aiLoading && <div className="text-center py-8 text-purple-400"><div className="text-2xl mb-2 animate-pulse">🤖</div><p className="text-sm">Gemini AIが切り返しを生成中...</p></div>}
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
                        <p className="text-xs text-purple-300/70 mt-0.5">📌 {aiSuggestions[aiSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(aiSuggestions[aiSelectedIdx!].talk, 'ai_suggest')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'ai_suggest' ? 'bg-purple-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'ai_suggest' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{aiSuggestions[aiSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* ── メモ欄 ── */}
          <div className="bg-slate-900 rounded-2xl border border-amber-800/50 p-6">
            {/* ヘッダー */}
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-bold text-white">📝 架電メモ</h2>
                <p className="text-sm text-slate-400 mt-0.5">通話中のメモ・気になった点を記録。一時保存すると履歴に残ります。</p>
              </div>
              <button
                onClick={() => setMemoOpen(o => !o)}
                className="text-slate-400 hover:text-white text-sm px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 hover:border-slate-500 transition-colors"
              >
                {memoOpen ? '▲ 閉じる' : '▼ 開く'}
              </button>
            </div>

            {memoOpen && (
              <div className="space-y-4">
                {/* テキストエリア */}
                <textarea
                  value={memoText}
                  onChange={e => {
                    setMemoText(e.target.value)
                    localStorage.setItem(MEMO_KEY, e.target.value)
                  }}
                  rows={6}
                  placeholder={`通話メモをここに入力...\n例）\n・担当：山田支配人\n・懸念：コスト、シリンダー錠\n・次回：9/5 14:00 再架電`}
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl px-4 py-3 text-base text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/30 resize-none leading-relaxed font-mono"
                />

                {/* ボタン行 */}
                <div className="flex flex-wrap gap-3 items-center">
                  <button
                    onClick={saveMemo}
                    disabled={!memoText.trim()}
                    className={`px-6 py-3 rounded-xl text-base font-bold transition-all ${
                      memoSaved
                        ? 'bg-green-600 text-white'
                        : memoText.trim()
                          ? 'bg-amber-600 hover:bg-amber-500 text-white'
                          : 'bg-slate-700 text-slate-500 cursor-not-allowed'
                    }`}
                  >
                    {memoSaved ? '✅ 保存済み' : '💾 一時保存'}
                  </button>
                  <button
                    onClick={() => copy(memoText, 'memo')}
                    disabled={!memoText.trim()}
                    className={`px-6 py-3 rounded-xl text-base font-bold transition-all ${
                      copiedKey === 'memo'
                        ? 'bg-blue-600 text-white'
                        : memoText.trim()
                          ? 'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600'
                          : 'bg-slate-800 text-slate-600 cursor-not-allowed border border-slate-700'
                    }`}
                  >
                    {copiedKey === 'memo' ? '✅ コピー済み' : '📋 コピー'}
                  </button>
                  {memoText && (
                    <button
                      onClick={() => { setMemoText(''); localStorage.removeItem(MEMO_KEY) }}
                      className="px-4 py-3 rounded-xl text-sm text-slate-400 hover:text-red-400 hover:bg-red-950/30 border border-slate-700 transition-colors"
                    >
                      🗑 クリア
                    </button>
                  )}
                </div>

                {/* 保存履歴 */}
                {savedMemos.length > 0 && (
                  <div className="border-t border-slate-700 pt-4">
                    <p className="text-sm font-bold text-slate-300 mb-3">🕐 保存履歴（最大10件）</p>
                    <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
                      {savedMemos.map((m, i) => (
                        <div key={i} className="bg-slate-800 rounded-xl border border-slate-700 px-4 py-3">
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-xs text-amber-400 font-bold">{m.ts}</span>
                            <div className="flex gap-2">
                              <button
                                onClick={() => { setMemoText(m.text); localStorage.setItem(MEMO_KEY, m.text) }}
                                className="text-xs text-blue-400 hover:text-blue-300 px-2 py-0.5 rounded bg-blue-950/40 border border-blue-800/40"
                              >
                                復元
                              </button>
                              <button
                                onClick={() => copy(m.text, `saved_${i}`)}
                                className="text-xs text-slate-400 hover:text-white px-2 py-0.5 rounded bg-slate-700/60 border border-slate-600"
                              >
                                {copiedKey === `saved_${i}` ? '✅' : '📋'}
                              </button>
                              <button
                                onClick={() => deleteSavedMemo(i)}
                                className="text-xs text-red-400 hover:text-red-300 px-2 py-0.5 rounded bg-red-950/40 border border-red-800/40"
                              >
                                削除
                              </button>
                            </div>
                          </div>
                          <p className="text-sm text-slate-300 whitespace-pre-line leading-relaxed line-clamp-3">{m.text}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>


        </div>
      )}

      {/* ─── TAB: 米山パターン ─── */}
      {activeTab === 'yoneyama' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-yellow-900/40 to-orange-900/40 border border-yellow-700/50 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">💰</span>
              <div>
                <h2 className="text-xl font-bold text-white">米山パターン — IT補助金全面訴求型</h2>
                <p className="text-sm text-yellow-300/80 mt-0.5">IT補助金を前面に出し、2025年テレアポトレンドを反映したスクリプト</p>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl border border-yellow-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">🤖 AI切り返し（米山パターン専用）</h2>
              <span className="text-xs bg-yellow-900/60 border border-yellow-700/50 text-yellow-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-sm text-slate-400 mb-4">相手の発言を入力 → IT補助金訴求を含む切り返しをAIが生成</p>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🎤</span>
                <input type="text" value={yoneyamaInput} onChange={e => setYoneyamaInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchYoneyamaSuggestions(yoneyamaInput)}
                  placeholder="例：「予算がない」「他社で検討中」「今は時期が悪い」"
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500 focus:ring-2 focus:ring-yellow-500/30" />
                {yoneyamaInput && <button onClick={() => { setYoneyamaInput(''); setYoneyamaSuggestions([]); setYoneyamaSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">×</button>}
              </div>
              <button onClick={() => fetchYoneyamaSuggestions(yoneyamaInput)} disabled={!yoneyamaInput.trim() || yoneyamaLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${yoneyamaLoading ? 'bg-yellow-900 text-yellow-400 cursor-wait' : yoneyamaInput.trim() ? 'bg-yellow-600 hover:bg-yellow-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {yoneyamaLoading ? '⏳ 生成中...' : '✨ AI提案'}
              </button>
            </div>
            {yoneyamaError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-sm text-red-300">⚠️ {yoneyamaError}</div>}
            {yoneyamaLoading && <div className="text-center py-8 text-yellow-400"><div className="text-2xl mb-2 animate-pulse">🤖</div><p className="text-sm">Gemini AIが米山パターンで生成中...</p></div>}
            {yoneyamaSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-yellow-400 font-bold mb-3">💡 AI推奨切り返し ({yoneyamaSuggestions.length}件)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {yoneyamaSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setYoneyamaSelectedIdx(yoneyamaSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${yoneyamaSelectedIdx === i ? 'bg-yellow-600 text-white shadow-lg scale-105' : 'bg-yellow-900/50 text-yellow-200 hover:bg-yellow-700 hover:text-white border border-yellow-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {yoneyamaSelectedIdx !== null && yoneyamaSuggestions[yoneyamaSelectedIdx] && (
                  <div className="bg-yellow-950/60 border-2 border-yellow-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-yellow-400 font-bold">💬 {yoneyamaSuggestions[yoneyamaSelectedIdx].label}</p>
                        <p className="text-xs text-yellow-300/70 mt-0.5">📌 {yoneyamaSuggestions[yoneyamaSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(yoneyamaSuggestions[yoneyamaSelectedIdx!].talk, 'yoneyama_ai')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'yoneyama_ai' ? 'bg-yellow-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'yoneyama_ai' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{yoneyamaSuggestions[yoneyamaSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">📞 米山パターン — トークスクリプト</h2>
            <div className="space-y-3">
              {[
                { label: '① オープニング（受付突破）', color: 'blue', text: '「お忙しいところ恐れ入ります。デバイスエージェンシーの米山でございます。本日は、ホテル・旅館様向けのIT補助金活用でご導入できる自動チェックイン機のご案内でご連絡しました。ご担当者様かご支配人様はいらっしゃいますでしょうか？」' },
                { label: '② IT補助金を前面に出す', color: 'yellow', text: '「弊社では今、IT補助金の申請を全て弊社が代行する形で、自動チェックイン機をお手頃な価格でご導入いただけています。KIOSK型が実質48万円〜、タブレット型が13万円〜とご好評いただいておりまして。売り込みではなく、補助金活用の情報をお伝えしたくてご連絡しました。」' },
                { label: '③ ヒアリング', color: 'purple', text: '「最近、業界全体でインバウンド対応や人手不足のお声をよくお聞きするのですが、御社では現在、何か運用上の課題はお感じですか？」' },
                { label: '④ YES → 提案', color: 'green', text: '「そうですよね。その課題をIT補助金を活用して解決された事例が手元にあります。資料だけでもメールでお送りしてもよろしいでしょうか？」' },
                { label: '⑤ NO → 情報だけ提案', color: 'slate', text: '「承知しました。IT補助金は毎年申請枠がありますので、タイミングが来た時のためだけでも資料をお手元に置いていただければ。メールアドレスをお教えいただけますか？」' },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-4 ${item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' : item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' : item.color === 'purple' ? 'bg-purple-950/40 border border-purple-800/40' : item.color === 'green' ? 'bg-green-950/40 border border-green-800/40' : 'bg-slate-700/50 border border-slate-600/40'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <p className={`text-xs font-bold ${item.color === 'blue' ? 'text-blue-400' : item.color === 'yellow' ? 'text-yellow-400' : item.color === 'purple' ? 'text-purple-400' : item.color === 'green' ? 'text-green-400' : 'text-slate-400'}`}>{item.label}</p>
                    <button onClick={() => copy(item.text, `ym_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === `ym_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                      {copiedKey === `ym_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                  <p className="text-sm text-slate-200 leading-relaxed">{item.text}</p>
                </div>
              ))}
            </div>
          </div>

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
                  <p className="text-sm font-bold text-red-400 mb-2">❌ {item.obj}</p>
                  <div className="flex items-start gap-3">
                    <p className="text-base text-slate-200 leading-relaxed flex-1">✅ {item.res}</p>
                    <button onClick={() => copy(item.res, `ym_obj_${i}`)} className={`text-xs px-3 py-1 rounded-lg font-medium flex-shrink-0 transition-colors ${copiedKey === `ym_obj_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
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
            <h2 className="text-base font-bold text-white mb-4">✅ 使用するステータス（取引ステージ）</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
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
                        <span className={`text-xs font-medium px-2 py-1 rounded-lg ${
                          row.badge === 'blue' ? 'bg-blue-900/60 text-blue-300' :
                          row.badge === 'green' ? 'bg-green-900/60 text-green-300' :
                          row.badge === 'yellow' ? 'bg-yellow-900/60 text-yellow-300' :
                          row.badge === 'red' ? 'bg-red-900/60 text-red-300' :
                          row.badge === 'purple' ? 'bg-purple-900/60 text-purple-300' :
                          'bg-slate-700 text-slate-300'
                        }`}>{row.status}</span>
                      </td>
                      <td className="text-slate-300 py-3 text-sm">{row.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">🔒 リードステータスの種別</h2>
            <div className="space-y-3">
              {[
                { label: '資料送付3週間以内', desc: 'タスクを設定。件名「資料送付 〇/〇」。期限は3週間後。資料送付数の計算に使う。', color: 'blue' },
                { label: '資料送付インセンティブなし', desc: 'アポイントを取りに行くためにタスクを設定。担当者・受付の双方の名前を聞けなかった場合はインセンなし。', color: 'yellow' },
                { label: '資料送付＋セミナー参加', desc: 'セミナー参加インセンティブ獲得時。取引ステージは【セミナー予定】へ。', color: 'green' },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-4 ${
                  item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' :
                  item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' :
                  'bg-green-950/40 border border-green-800/40'
                }`}>
                  <p className={`text-xs font-bold mb-1 ${
                    item.color === 'blue' ? 'text-blue-400' :
                    item.color === 'yellow' ? 'text-yellow-400' : 'text-green-400'
                  }`}>{item.label}</p>
                  <p className="text-sm text-slate-300">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: 商品知識 ─── */}
      {activeTab === 'knowledge' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">🏨 製品ラインナップ</h2>
              <div className="space-y-3">
                {[
                  { name: '自動チェックイン機（KIOSK型）', desc: 'すべての清算機能あり。申込から3ヶ月で手配可能。', badge: 'blue' },
                  { name: '自動チェックイン機（タブレット型）', desc: '小規模施設・民泊向け。申込から1ヶ月で手配可能。', badge: 'green' },
                  { name: 'クラウドスマートロック', desc: '暗証番号で開錠。チェックイン機と連動してレシートに暗証番号を印字。', badge: 'purple' },
                  { name: 'ルームタブレット', desc: '内線電話機能。スタッフの名前表示・多言語対応。月額1室100円。', badge: 'yellow' },
                ].map((p, i) => (
                  <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                    <p className={`text-xs font-bold mb-1 ${
                      p.badge === 'blue' ? 'text-blue-400' : p.badge === 'green' ? 'text-green-400' :
                      p.badge === 'purple' ? 'text-purple-400' : 'text-yellow-400'
                    }`}>{p.name}</p>
                    <p className="text-sm text-slate-300">{p.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">💰 価格・費用感</h2>
              <div className="space-y-3">
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-blue-400 mb-2">初期費用（IT補助金活用時）</p>
                  <ul className="text-sm text-slate-300 space-y-1">
                    <li>・KIOSK型：<span className="text-white font-bold">48万円〜</span></li>
                    <li>・タブレット型：<span className="text-white font-bold">13万円〜</span></li>
                    <li>・一軒家（シングルプラン）：<span className="text-white font-bold">49,800円〜</span></li>
                    <li className="text-xs text-slate-500">※補助金申請は弊社が行う</li>
                  </ul>
                </div>
                <div className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-sm font-bold text-green-400 mb-2">月額費用</p>
                  <ul className="text-sm text-slate-300 space-y-1">
                    <li>・KIOSK型：19,600円＋部屋数×200円</li>
                    <li>・タブレット型：500円×部屋数</li>
                    <li>・使用しない月は<span className="text-green-300 font-medium">月額0円</span></li>
                    <li>・土日祝のみ使用の日割り計算も可能</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">❓ よくある質問と回答</h2>
              <div className="space-y-3">
                {[
                  { q: 'PMSと連携できるの？', a: '弊社はPMSとの連携開発に近年力を入れています。実績：ステイシー、スイートブック、ベッツ24。お客様の要望によりかなりの頻度で開発連携が進んでいますので、御社のPMSも今後連携開発を進めます。' },
                  { q: 'カードキーに変えないといけない？', a: '弊社の売りはシリンダー錠（物理キー）に対応可能なこと。別売りのキーボックスで清算後にキーが自動開放される。キーボックスなしでもレシートをフロントで鍵と交換する対面接客も残せる。' },
                  { q: '「無人」にできますか？', a: '⚠️「無人」というワードはNG。「省人化・業務効率化」と表現する。フロントスタッフの業務を削減し、接客サービスに集中できる環境を作ることをPRする。' },
                  { q: 'インバウンド対応は？', a: '多言語対応（12〜13か国語）、パスポートスキャン・本人確認機能あり。インバウンド対策に非常に有効。' },
                ].map((item, i) => (
                  <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                    <p className="text-sm font-bold text-yellow-400 mb-2">Q: {item.q}</p>
                    <p className="text-base text-slate-200 leading-relaxed">A: {item.a}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <h2 className="text-base font-bold text-white mb-4">📣 業務指導・重要ポイント</h2>
              <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                {[
                  '資料送付後3週間以内の再架電を徹底。100円のインセンより5,000円のアポイントを狙う執着心を持つ。',
                  '「将来的にご興味ありますか？」で提案する。「今導入してますか？」はNG。',
                  '支配人につながったら「お時間よろしいでしょうか？」はNG（マナー問題）。「自動チェックイン機の件で」と言った時点で興味なければ切られる。',
                  '流行り・世の中の流れを使うトーク：「最近よくお耳にするかとは思いますが」「全国からのお問い合わせが去年よりかなり多くなってきておりまして」を挿入。',
                  '質問がある＝興味がある。質問があった先は優先度を「中」または「高」に変更する。',
                  'info@宛の資料送付：件名に「〇〇様 自動チェックイン機の件」と入力する（スルーされる確率が減る）。',
                  '資料送付メールに署名とカタログを必ず付ける。カタログの添付漏れに注意。',
                  'シリンダー錠対応などの強みをPRしてから資料送付に持っていく。いきなり資料送付はNG。',
                  '「。」で区切るなど、話し方をゆっくりわかりやすく。',
                  '担当者不在が多い場合はフロントに資料送付をお願いする。',
                  '組織決済案件は必ず報告。切り口がありそうなら逐一報告。',
                  '資料送付メールの開封状況を確認。開封歴なし→迷惑メール確認・アドレス確認。',
                  '部屋数が少ないところにはルームタブレット・スマートロックも合わせて提案。',
                ].map((item, i) => (
                  <div key={i} className="flex gap-2 text-xs text-slate-300 bg-slate-700/30 rounded-lg p-3">
                    <span className="text-blue-400 font-bold flex-shrink-0">{i + 1}.</span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: チェックリスト ─── */}
      {activeTab === 'checklist' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">✅ 架電業務チェックリスト</h2>
            <div className="space-y-2">
              {[
                '発信前に担当者を自分の名前に変更したか',
                '架電後、ステージを正しく変更したか（不在／断り／本社へ／クレーム／他社製品使用）',
                '不在時は「いる時間帯・日」を聞き、タスクを設定したか',
                '資料送付時：メールアドレス・姓名（〇〇様）・携帯番号を入力したか',
                '資料送付メールに署名とカタログを付けたか',
                'info@宛は件名に「〇〇様 自動チェックイン機の件」と入れたか',
                '会社の担当者（自分名）とリードステータスを変更したか',
                '資料送付タスクの期限を3週間後に設定したか（つながりやすい時間帯も考慮）',
                '受付・担当者の名前を両方聞いたか（インセン条件：メモ【担当受付共に〇●】等）',
                '質問があった先は優先度を「中」または「高」に変更したか',
                '資料送付後3週間以内に再架電したか',
                '資料送付メールの開封状況を確認したか',
                '「無人」というワードを使っていないか',
                '切り口や質問があった案件を逐一報告したか',
              ].map((item, i) => (
                <label key={i} className="flex items-start gap-3 p-3 bg-slate-700/40 rounded-xl cursor-pointer hover:bg-slate-700 transition-colors">
                  <input type="checkbox" className="w-4 h-4 accent-blue-500 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-slate-300">{item}</span>
                </label>
              ))}
            </div>
          </div>

          {/* 重要ポイント早見表 */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">📌 重要ポイント早見表</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-slate-400 font-medium py-2 pr-4 whitespace-nowrap">項目</th>
                    <th className="text-left text-white font-medium py-2">内容</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50">
                  {[
                    { label: '対象取引ステージ', value: '楽天トラベル（不在）（スマートチェックイン）', highlight: true },
                    { label: '追加する表示列', value: '「前回の連絡」「優先度」' },
                    { label: 'ソート基準', value: '「前回の連絡」日時の昇順（過去から）' },
                    { label: 'スキップ条件', value: '優先度が「高」または「中」のレコード', highlight: true },
                    { label: '架電順序', value: 'リストの上から順番' },
                    { label: '架電前の必須作業', value: '取引担当者を自分の名前に変更（★絶対忘れずに）', highlight: true },
                    { label: '架電後の作業', value: '取引ステージを結果に応じて更新' },
                    { label: 'セミナー開催日', value: '水曜11:00〜 ／ 金曜13:00〜（ZOOM）', highlight: true },
                    { label: 'インセン条件', value: '受付・担当者の名前を両方聞けて100円' },
                  ].map((row, i) => (
                    <tr key={i}>
                      <td className="text-slate-400 py-3 pr-4 whitespace-nowrap font-medium">{row.label}</td>
                      <td className={`py-3 ${row.highlight ? 'text-yellow-300 font-medium' : 'text-slate-300'}`}>{row.value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: メールテンプレ ─── */}
      {activeTab === 'mail' && (
        <div className="space-y-6">
          {[
            {
              key: 'zoom',
              title: '📅 ZOOMミーティング案内メール',
              content: `お世話になっております。
(株)デバイスエージェンシーの〇〇でございます。
お打ち合わせのお時間をいただけますこと、感謝申し上げます。
標記の件につきまして、下記のとおりWebミーティング（ZOOM）をご案内申し上げます。

記
日時：2026年〇月〇日（〇）〇〇：00～
形式：オンライン（ZOOM）
ZOOM入室URL：https://us06web.zoom.us/j/84410321175?pwd=YklablhmOGIwQ0tCQmJXN0hnak9UZz09
※当日はお時間になりましたら、上記URLよりご入室をお願いいたします。
ご多忙の折、恐縮ではございますが、当日は何卒よろしくお願い申し上げます。`,
            },
            {
              key: 'checkin',
              title: '📧 資料送付メール（チェックイン機）',
              content: `支配人 様

お世話になります。
本日は自動チェックイン機の件でお電話ありがとうございました。
今後のインバウンド対策や、人手不足、利益率向上、業務効率化の面で大変良い評価をいただいております。
また、価格面につきましても皆様に大変ご好評をいただいております。

●人手不足・業務効率化対策
フロントの人員削減、無人化が可能に。スタッフの業務負担の軽減⇔お客様のストレス緩和

●カードキー以外にも対応
ルームカードキー以外にも、スマートロックや物理キー（シリンダー錠）にも対応可能です。（オプションキーボックスの併用）

●ホスピタリティーの向上
事前チェックインシステムなどを利用することで、フロントでの事務的オペレーションを削減⇔お客様との対話時間が増え、館内施設や観光案内などの接客サービスをより一層手厚く行うことが可能に。

●多種多様なカスタマイズ
朝食券の発行や日帰り温泉客の受付・清算などのデイユース機能に加え、施設のニーズに応じて様々なカスタマイズに取り組んでいます。

●インバウンド対応
外国語対応（13ヵ国語）。パスポートスキャン、本人確認も可能です。

【初期費用について】
AdvaNceD IoT チェックイン筐体費用＋初期設定費用→IT補助金活用で1,330,000円～
※シリンダー錠にも対応可能です。
※小規模向けタブレット型は1台約16万円～で導入可能。

【月額費用について】
・使用しない月は0円になります。（季節限定特別料金帯）
・ルーム利用料（×部屋数1～20室まで）一部屋×500円
・3年目以降はルーム利用料200円×部屋数

※商品の説明会セミナーもオンラインで毎週2回開催しております。（1時間程度）
・水曜日：11：00～
・金曜日：13：00～
ご希望の日時がございましたら、ご返信ください。

WEB版はこちらです「AdvaNceD IoT スマートチェックイン」
https://and-iot.jp/dms-cardlock`,
            },
            {
              key: 'tablet',
              title: '📧 ルームタブレット資料送付メール',
              content: `お世話になっております。デバイスエージェンシー橋本でございます。
先ほどのお話でルームタブレット（内線電話）の資料をお送りします。

ルームタブレットは、クラウドシステムのセットです。運営の効率化とコスト削減を実現できます。

メリット：
・スタッフの方がフロントから離れていても、移動しながら対応できます。
・ゲスト様からの着信が一目でわかります。（例：「305の田中様」と表示）
・多言語表示が可能で、インバウンド対策にも。
・宿泊関連の情報を全てタブレットに集約でき、ペーパーレス化が可能。
・タブレットやスマホの端末初期費用は0円（システム初期費用100,000円＋端末登録費用1台19,800円が別途）。
・月額料金は1室100円。IT補助金活用で御社負担が月額費用も含め約1/3に。

弊社では他にもホテル施設向けの自社開発製品を提供しております。
https://and-iot.jp/`,
            },
            {
              key: 'sign',
              title: '✍️ 署名テンプレート',
              content: `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
お世話になっております。
株式会社デバイスエージェンシー 〇〇〇
〒550-0015
大阪市西区南堀江4-17-18 原田ビルディング1F
TEL:06-6585-9865 FAX:06-6585-9875
Email: （自分のアドレス）
DA   www.device-agency.co.jp
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
            },
          ].map(tpl => (
            <div key={tpl.key} className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-base font-bold text-white">{tpl.title}</h2>
                <button
                  onClick={() => copy(tpl.content, tpl.key)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    copiedKey === tpl.key
                      ? 'bg-green-600 text-white'
                      : 'bg-slate-700 hover:bg-slate-600 text-slate-300'
                  }`}
                >
                  {copiedKey === tpl.key ? '✅ コピー済み' : '📋 コピー'}
                </button>
              </div>
              <pre className="text-xs text-slate-300 bg-slate-900 rounded-xl p-4 whitespace-pre-wrap leading-relaxed max-h-64 overflow-y-auto">{tpl.content}</pre>
            </div>
          ))}

          {/* Zoom Phone連携 */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">📱 Zoom Phone × HubSpot 連携手順</h2>
            <div className="space-y-2">
              {[
                'HubSpotにログイン→マーケットプレイス（家アイコン）を開く',
                '「Zoom」で検索→「Zoom Phone for HubSpot」→「アプリをインストール」',
                'Zoom Webポータルのログイン画面でZoomPhoneが有効なIDでログイン',
                '「株式会社デバイスエージェンシー」をマーク→「アカウント選択」',
                'チェックボックスにチェック→「アプリを接続」→「Confirm」→「確認する」',
                '「サインインに成功しました」と表示されれば完了',
                '★重要：Zoom Webポータル→電話→設定→発信者ID（無人チェックイン営業）を選択',
              ].map((item, i) => (
                <div key={i} className="flex gap-3 text-sm text-slate-300 bg-slate-700/40 rounded-lg p-3">
                  <span className="w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0">{i + 1}</span>
                  {item}
                </div>
              ))}
            </div>
            <div className="mt-4 bg-yellow-950/50 border border-yellow-800/50 rounded-xl p-4">
              <p className="text-sm font-bold text-yellow-400 mb-2">⚠️ 連携がうまくいかない場合</p>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>・ZOOMワークプレイスをサインアウト→サインインし直す</li>
                <li>・HubSpotのコールもサインアウト→サインインし直す</li>
                <li>・HubSpot上部の電話マークアイコンからサインイン→別タブで「ZOOMフォン」選択→Googleでログイン</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* 参考資料リンク */}
      <div className="mt-6 bg-slate-800 rounded-2xl border border-slate-700 p-5">
        <p className="text-xs text-slate-400 font-medium mb-3">📁 参考資料</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <a href="https://app-na2.hubspot.com/contacts/39705134/objects/0-3/views/353515006/list" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-orange-900/30 hover:bg-orange-900/50 border border-orange-800/50 rounded-xl transition-colors group">
            <span className="text-lg">🟠</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-orange-300 transition-colors">HubSpot 架電リスト</p>
              <p className="text-slate-500 text-xs">取引一覧（楽天トラベルフィルター済）</p>
            </div>
          </a>
          <a href="https://us02web.zoom.us/myhome" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-blue-900/30 hover:bg-blue-900/50 border border-blue-800/50 rounded-xl transition-colors group">
            <span className="text-lg">📹</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-blue-300 transition-colors">Zoom マイホーム</p>
              <p className="text-slate-500 text-xs">架電・セミナー用 Zoom</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1F2ycU3glbgrJCOkLRKHg86ROWggkbYOZXxhA2vco84o/edit?gid=767829959#gid=767829959" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-lg">📊</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-blue-300 transition-colors">テレアポ業務マニュアル（スプレッドシート）</p>
              <p className="text-slate-500 text-xs">テレアポ業務マニュアル改正シート</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1WnwEhp2Db9lDHNw8qp_h2ZjhMY-mZG9TXcAAh6RX59w/edit?gid=1927965581#gid=1927965581" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-3 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-lg">📋</span>
            <div>
              <p className="text-white text-xs font-medium group-hover:text-blue-300 transition-colors">アウトバウンド管理簿</p>
              <p className="text-slate-500 text-xs">【スマートチェックイン】架電管理</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  )
}
