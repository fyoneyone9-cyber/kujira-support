'use client'

const sections = [
  {
    title: '📚 自習テキスト',
    color: 'border-blue-600',
    headerBg: 'bg-blue-900/40',
    items: [
      { label: '全章（1冊）', url: 'https://drive.google.com/file/d/1Ry3_fRPItw2VeCk2j5EsJhC7REOpSY05/view' },
      { label: '第0章 はじめに', url: 'https://drive.google.com/file/d/1pwhtinSlMlo0Agd04xGwAIpD_IdlbeVJ/view' },
      { label: '第1章 1日目ツール', url: 'https://drive.google.com/file/d/1iQuOjgJn0_BmFWXjlttDlMsvrTvezkSy/view' },
      { label: '第2章 2日目商品とトーク', url: 'https://drive.google.com/file/d/1tFVqInJgcD6ht80K5MmR0lmVgfNGuwIJ/view' },
      { label: '第3章 3〜6日目', url: 'https://drive.google.com/file/d/1Ron8iIeT5RIMNeQVykdcwebx6r_OBol3/view' },
      { label: '付録', url: 'https://drive.google.com/file/d/1zac4d11vhalcohPWvQ7qQMnzQKvvtzlC/view' },
    ],
  },
  {
    title: '🛠️ 1日目（ツール）',
    color: 'border-green-600',
    headerBg: 'bg-green-900/40',
    items: [
      { label: 'Pマーク教育資料', url: 'https://drive.google.com/file/d/1GbyXWpGtZMrjsoamiYLJbLMuL7BDSj4M/view' },
      { label: 'メール・Backlog初期設定方法', url: 'https://drive.google.com/file/d/1kQ67v_lJaFX-RatVsEWhpNbYZ7ijDy07/view' },
      { label: 'HubSpotテレアポ業務 システムマニュアル', url: 'https://drive.google.com/file/d/11gy5bgY8fGIFjXQ_5OmGA0f__1ucHsic/view' },
      { label: 'HubSpotテレアポ チートシート', url: 'https://drive.google.com/file/d/1na4Yv7D8QbQbOgN4BY4Nj6igDC-DE2Fn/view' },
      { label: 'Zoomフォン設定方法（発信方法）', url: 'https://drive.google.com/file/d/1OtSxGRHQUaZok3Vy9YQ4tvRHQJxJs-P9/view' },
    ],
  },
  {
    title: '💼 2日目以降（商品・トーク・商談）',
    color: 'border-orange-600',
    headerBg: 'bg-orange-900/40',
    items: [
      { label: 'テレアポ業務マニュアル（動画つき）', url: 'https://docs.google.com/spreadsheets/d/1yRGRme6Xcq1rxzMe2UO6ZMU4Z7Vfyg9pEUc4JNdFrn8/edit' },
      { label: 'スマートチェックイン システムマニュアル ver1.14', url: 'https://drive.google.com/file/d/1snflbcGfiBET3DlwgGd9H0MOhObRZhn7/view' },
      { label: 'スマートチェックイン ご提案資料 V4', url: 'https://drive.google.com/file/d/1KdbNqi9CJPe6L45aS3FOldwYp4Qw5szp/view' },
      { label: 'スマートロックとDMSについて（はじめに読む）', url: 'https://drive.google.com/file/d/1sXUH7xGMwE9rwSkWbx6PmpIhhLJc5aBx/view' },
      { label: 'DMSとスマートロックの連携手順', url: 'https://drive.google.com/file/d/1wf8KbEVrW_WmT_t6tjLolikEVJN2rPd2/view' },
      { label: 'ゲートウェイについて', url: 'https://drive.google.com/file/d/1Z8jo5o75kvTmb6iyUTIKiDZwxe9i-KTL/view' },
      { label: '見積の実例（熊本ホテル）', url: 'https://drive.google.com/file/d/15I53EaSY1bIIWyGlj0DaBuNln8GG1Tz4/view' },
      { label: 'ヒアリングシート（ひな形）', url: 'https://docs.google.com/spreadsheets/d/16uW0WLwx-H-KWpCl2zHDstRuQsfcnFyLyLxbRV-_s5E/' },
    ],
  },
]

export default function OnboardingPage() {
  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold text-white">🎓 新人教育</h1>
        <p className="text-slate-400 text-sm mt-1">研修資料・マニュアルへのリンク集</p>
      </div>

      {sections.map(sec => (
        <div key={sec.title} className={`border ${sec.color} rounded-xl overflow-hidden`}>
          <div className={`${sec.headerBg} px-4 py-3`}>
            <h2 className="text-white font-bold text-base">{sec.title}</h2>
          </div>
          <div className="divide-y divide-slate-700/50">
            {sec.items.map(item => (
              <a
                key={item.label}
                href={item.url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-3 px-4 py-3 hover:bg-slate-700/40 transition-colors group"
              >
                <span className="text-slate-400 group-hover:text-white text-base flex-1">{item.label}</span>
                <span className="text-slate-500 group-hover:text-blue-400 text-xs flex-shrink-0">開く →</span>
              </a>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
