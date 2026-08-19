'use client'

import { useEffect, useState, useCallback } from 'react'

type MailTemplate = {
  id: string
  category: string
  name: string
  purpose: string | null
  subject: string | null
  to_address: string | null
  cc_address: string | null
  body: string | null
  notes: string | null
}

const CATEGORY_ICONS: Record<string, string> = {
  '導入支援': '🚀',
  'タブレット': '📱',
  'P400': '💳',
  'PayCube': '🏧',
  'PayPay': '💰',
  'スマートロック不具合': '🔑',
  '定期ヒアリング': '📞',
  '導入事例写真': '📸',
  'その他': '📄',
  'LEGEND': '🗝️',
  'ペイジェント': '💳',
  '電話対応': '☎️',
}

function CopyButton({ text, label }: { text: string; label: string }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <button
      onClick={handleCopy}
      className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors ${
        copied
          ? 'bg-green-600 text-white'
          : 'bg-slate-600 hover:bg-slate-500 text-slate-200'
      }`}
    >
      {copied ? '✅ コピー済み' : `📋 ${label}をコピー`}
    </button>
  )
}

function TemplateModal({ template, onClose }: { template: MailTemplate; onClose: () => void }) {
  return (
    <div
      className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-800 rounded-2xl border border-slate-700 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-700">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded-full">
                {CATEGORY_ICONS[template.category] || '📧'} {template.category}
              </span>
            </div>
            <h2 className="text-xl font-bold text-white">{template.name}</h2>
            {template.purpose && (
              <p className="text-slate-400 text-sm mt-1">{template.purpose}</p>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white ml-4 text-xl leading-none"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5">
          {/* 宛先情報 */}
          {(template.to_address || template.cc_address) && (
            <div className="bg-slate-700/50 rounded-xl p-4 space-y-2 text-sm">
              {template.to_address && (
                <div className="flex gap-2">
                  <span className="text-slate-400 w-6 shrink-0">TO</span>
                  <span className="text-white">{template.to_address}</span>
                </div>
              )}
              {template.cc_address && (
                <div className="flex gap-2">
                  <span className="text-slate-400 w-6 shrink-0">CC</span>
                  <span className="text-white">{template.cc_address}</span>
                </div>
              )}
            </div>
          )}

          {/* 件名 */}
          {template.subject && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">件名</p>
                <CopyButton text={template.subject} label="件名" />
              </div>
              <div className="bg-slate-700/50 rounded-xl px-4 py-3">
                <p className="text-white text-sm">{template.subject}</p>
              </div>
            </div>
          )}

          {/* 本文 */}
          {template.body && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">本文</p>
                <CopyButton text={template.body} label="本文" />
              </div>
              <div className="bg-slate-900 rounded-xl px-4 py-3 border border-slate-700">
                <pre className="text-sm text-slate-200 whitespace-pre-wrap font-sans leading-relaxed">
                  {template.body}
                </pre>
              </div>
            </div>
          )}

          {/* 注意事項 */}
          {template.notes && (
            <div className="bg-yellow-900/20 border border-yellow-700/50 rounded-xl px-4 py-3">
              <p className="text-xs font-medium text-yellow-400 mb-1">⚠️ 注意事項</p>
              <p className="text-yellow-200 text-sm whitespace-pre-wrap">{template.notes}</p>
            </div>
          )}

          {!template.subject && !template.body && (
            <div className="text-center py-8">
              <p className="text-4xl mb-2">📝</p>
              <p className="text-slate-400 text-sm">本文は別途 Mail Dealer のテンプレートを参照してください</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function MailTemplatesPage() {
  const [templates, setTemplates] = useState<MailTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTemplate, setSelectedTemplate] = useState<MailTemplate | null>(null)

  const fetchTemplates = useCallback(async () => {
    setLoading(true)
    const params = new URLSearchParams()
    if (selectedCategory !== 'all') params.set('category', selectedCategory)
    if (searchQuery) params.set('q', searchQuery)
    const res = await fetch(`/api/mail-templates?${params}`)
    const data = await res.json()
    setTemplates(data.templates || [])
    setLoading(false)
  }, [selectedCategory, searchQuery])

  useEffect(() => {
    const timer = setTimeout(fetchTemplates, searchQuery ? 300 : 0)
    return () => clearTimeout(timer)
  }, [fetchTemplates, searchQuery])

  // カテゴリ一覧（固定順）
  const categories = [
    '導入支援', 'タブレット', 'P400', 'PayCube', 'PayPay',
    'スマートロック不具合', '定期ヒアリング', '導入事例写真',
    '電話対応', 'その他', 'LEGEND', 'ペイジェント',
  ]

  // カテゴリ別にグループ化
  const grouped = templates.reduce<Record<string, MailTemplate[]>>((acc, t) => {
    if (!acc[t.category]) acc[t.category] = []
    acc[t.category].push(t)
    return acc
  }, {})

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">📧 メールテンプレート</h1>
        <p className="text-slate-400 text-sm mt-1">よく使うメールの定型文・テンプレート集</p>
      </div>

      {/* Search */}
      <div className="mb-5">
        <input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="テンプレート名・用途・本文で検索..."
          className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedCategory('all')}
          className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
            selectedCategory === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-slate-800 text-slate-400 hover:text-white border border-slate-700'
          }`}
        >
          すべて
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(selectedCategory === cat ? 'all' : cat)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
              selectedCategory === cat
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white border border-slate-700'
            }`}
          >
            {CATEGORY_ICONS[cat] || '📧'} {cat}
          </button>
        ))}
      </div>

      {/* Templates */}
      {loading ? (
        <div className="text-center py-16">
          <p className="text-slate-400">読み込み中...</p>
        </div>
      ) : templates.length === 0 ? (
        <div className="text-center py-16 bg-slate-800 rounded-2xl border border-slate-700">
          <p className="text-4xl mb-3">📭</p>
          <p className="text-slate-400">テンプレートが見つかりません</p>
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="mt-3 text-sm text-blue-400 hover:text-blue-300"
            >
              検索をクリア
            </button>
          )}
        </div>
      ) : selectedCategory === 'all' && !searchQuery ? (
        // カテゴリ別グループ表示
        <div className="space-y-8">
          {categories.map((cat) => {
            const items = grouped[cat]
            if (!items || items.length === 0) return null
            return (
              <div key={cat}>
                <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <span>{CATEGORY_ICONS[cat] || '📧'}</span>
                  {cat}
                  <span className="text-slate-600 font-normal normal-case">({items.length}件)</span>
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {items.map((t) => (
                    <button
                      key={t.id}
                      onClick={() => setSelectedTemplate(t)}
                      className="text-left bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl p-4 transition-colors group"
                    >
                      <p className="font-medium text-white group-hover:text-blue-300 transition-colors text-sm">
                        {t.name}
                      </p>
                      {t.purpose && (
                        <p className="text-slate-500 text-xs mt-1 line-clamp-1">{t.purpose}</p>
                      )}
                      {t.subject && (
                        <p className="text-slate-400 text-xs mt-2 line-clamp-1">
                          <span className="text-slate-600">件名：</span>{t.subject}
                        </p>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )
          })}
          {/* 残りのカテゴリ（固定順にないもの） */}
          {Object.keys(grouped).filter(c => !categories.includes(c)).map((cat) => {
            const items = grouped[cat]
            return (
              <div key={cat}>
                <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
                  {CATEGORY_ICONS[cat] || '📧'} {cat}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {items.map((t) => (
                    <button
                      key={t.id}
                      onClick={() => setSelectedTemplate(t)}
                      className="text-left bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl p-4 transition-colors group"
                    >
                      <p className="font-medium text-white group-hover:text-blue-300 transition-colors text-sm">
                        {t.name}
                      </p>
                      {t.purpose && (
                        <p className="text-slate-500 text-xs mt-1 line-clamp-1">{t.purpose}</p>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        // フラット表示（検索時・カテゴリ絞り込み時）
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {templates.map((t) => (
            <button
              key={t.id}
              onClick={() => setSelectedTemplate(t)}
              className="text-left bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl p-4 transition-colors group"
            >
              <div className="flex items-start gap-2">
                <span className="text-lg shrink-0">{CATEGORY_ICONS[t.category] || '📧'}</span>
                <div>
                  <p className="font-medium text-white group-hover:text-blue-300 transition-colors text-sm">
                    {t.name}
                  </p>
                  <span className="text-xs text-blue-400 bg-blue-400/10 px-1.5 py-0.5 rounded mt-1 inline-block">
                    {t.category}
                  </span>
                  {t.purpose && (
                    <p className="text-slate-500 text-xs mt-1 line-clamp-1">{t.purpose}</p>
                  )}
                </div>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Modal */}
      {selectedTemplate && (
        <TemplateModal
          template={selectedTemplate}
          onClose={() => setSelectedTemplate(null)}
        />
      )}
    </div>
  )
}
