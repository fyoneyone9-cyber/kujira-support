'use client'

import { useEffect, useState, useCallback } from 'react'

type AssignmentRule = {
  id: string
  keyword: string
  assignee: string
  assignee_email: string | null
  action: string | null
  notes: string | null
  priority: number
}

const ACTION_COLOR: Record<string, string> = {
  '対応完了': 'bg-slate-700 text-slate-400',
  '対応不要': 'bg-slate-700 text-slate-500',
  '迷惑フォルダ': 'bg-slate-700 text-slate-500',
  '担当者なしでそのまま': 'bg-slate-700 text-slate-500',
}

const ASSIGNEE_COLOR: Record<string, string> = {
  '岡田さん（一部岡村さん）': 'bg-purple-500/20 text-purple-300',
  '岡田さん': 'bg-purple-500/20 text-purple-300',
  '北浦さん': 'bg-cyan-500/20 text-cyan-300',
  '泉岡さん': 'bg-orange-500/20 text-orange-300',
  '田村さん': 'bg-pink-500/20 text-pink-300',
  '田中社長': 'bg-red-500/20 text-red-300',
  '高柳さん': 'bg-yellow-500/20 text-yellow-300',
  '堀内さん': 'bg-green-500/20 text-green-300',
  '堀越さん': 'bg-teal-500/20 text-teal-300',
  '橋本さん': 'bg-blue-500/20 text-blue-300',
  '野田さん': 'bg-indigo-500/20 text-indigo-300',
  '岡村さん': 'bg-violet-500/20 text-violet-300',
  '武内さん': 'bg-amber-500/20 text-amber-300',
  '森田さん': 'bg-lime-500/20 text-lime-300',
  '山本さん': 'bg-sky-500/20 text-sky-300',
  '今津さん': 'bg-rose-500/20 text-rose-300',
  'OP全員': 'bg-slate-500/20 text-slate-300',
  'OP': 'bg-slate-500/20 text-slate-300',
  '対応完了': 'bg-slate-700 text-slate-400',
  '対応不要': 'bg-slate-700 text-slate-500',
  '迷惑フォルダ': 'bg-slate-700 text-slate-500',
  '担当者なしでそのまま': 'bg-slate-700 text-slate-500',
}

function getAssigneeColor(assignee: string): string {
  for (const [key, val] of Object.entries(ASSIGNEE_COLOR)) {
    if (assignee.includes(key)) return val
  }
  return 'bg-blue-500/20 text-blue-300'
}

function RuleModal({ rule, onClose }: { rule: AssignmentRule; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div
        className="bg-slate-800 rounded-2xl border border-slate-700 w-full max-w-lg"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between p-6 border-b border-slate-700">
          <div>
            {rule.priority >= 10 && <span className="text-red-400 text-xs font-bold mr-2">！重要</span>}
            <h2 className="text-base font-bold text-white mt-1">{rule.keyword}</h2>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white ml-4 text-xl">✕</button>
        </div>
        <div className="p-6 space-y-4">
          <div>
            <p className="text-xs text-slate-500 mb-1">担当者</p>
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getAssigneeColor(rule.assignee)}`}>
              {rule.assignee}
            </span>
            {rule.assignee_email && (
              <p className="text-slate-400 text-xs mt-1">{rule.assignee_email}</p>
            )}
          </div>
          {rule.action && (
            <div>
              <p className="text-xs text-slate-500 mb-1">対応方法</p>
              <p className="text-white text-sm bg-slate-700/50 rounded-xl px-4 py-3 whitespace-pre-wrap">{rule.action}</p>
            </div>
          )}
          {rule.notes && (
            <div>
              <p className="text-xs text-slate-500 mb-1">備考・注意事項</p>
              <p className="text-slate-300 text-sm bg-yellow-900/20 border border-yellow-700/30 rounded-xl px-4 py-3 whitespace-pre-wrap">{rule.notes}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function AssignmentPage() {
  const [rules, setRules] = useState<AssignmentRule[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedAssignee, setSelectedAssignee] = useState('all')
  const [selectedRule, setSelectedRule] = useState<AssignmentRule | null>(null)

  const fetchRules = useCallback(async () => {
    setLoading(true)
    const params = new URLSearchParams()
    if (searchQuery) params.set('q', searchQuery)
    const res = await fetch(`/api/assignment-rules?${params}`)
    const data = await res.json()
    setRules(data.rules || [])
    setLoading(false)
  }, [searchQuery])

  useEffect(() => {
    const t = setTimeout(fetchRules, searchQuery ? 300 : 0)
    return () => clearTimeout(t)
  }, [fetchRules, searchQuery])

  // 担当者一覧（動的生成）
  const assignees = Array.from(new Set(rules.map(r => {
    // 複合担当者は最初の名前だけ取る
    return r.assignee.split('（')[0].split('・')[0].split('、')[0].trim()
  }))).sort()

  const filtered = selectedAssignee === 'all'
    ? rules
    : rules.filter(r => r.assignee.includes(selectedAssignee))

  // 重要ルールを分離
  const important = filtered.filter(r => r.priority >= 10)
  const normal = filtered.filter(r => r.priority < 10 && r.priority > 0)
  const done = filtered.filter(r => r.priority === 0)

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">📬 引き当てシート</h1>
        <p className="text-slate-400 text-sm mt-1">メール・電話の担当者振り分けルール一覧</p>
      </div>

      {/* Search */}
      <div className="mb-5">
        <input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="キーワード・担当者・対応方法で検索..."
          className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      </div>

      {/* 担当者フィルター */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedAssignee('all')}
          className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-colors ${
            selectedAssignee === 'all' ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-white border border-slate-700'
          }`}
        >すべて</button>
        {assignees.map(a => (
          <button
            key={a}
            onClick={() => setSelectedAssignee(selectedAssignee === a ? 'all' : a)}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-colors ${
              selectedAssignee === a ? 'bg-blue-600 text-white' : `${getAssigneeColor(a)} border border-transparent hover:opacity-80`
            }`}
          >{a}</button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-16"><p className="text-slate-400">読み込み中...</p></div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 bg-slate-800 rounded-2xl border border-slate-700">
          <p className="text-4xl mb-3">🔍</p>
          <p className="text-slate-400">該当するルールが見つかりません</p>
          {searchQuery && <button onClick={() => setSearchQuery('')} className="mt-3 text-sm text-blue-400">検索をクリア</button>}
        </div>
      ) : (
        <div className="space-y-8">
          {/* 重要 */}
          {important.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-red-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                ❗ 優先対応 <span className="text-slate-600 font-normal normal-case">({important.length}件)</span>
              </h2>
              <div className="space-y-2">
                {important.map(r => <RuleRow key={r.id} rule={r} onClick={() => setSelectedRule(r)} />)}
              </div>
            </div>
          )}

          {/* 通常 */}
          {normal.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                📋 担当者振り分けルール <span className="text-slate-600 font-normal normal-case">({normal.length}件)</span>
              </h2>
              <div className="space-y-2">
                {normal.map(r => <RuleRow key={r.id} rule={r} onClick={() => setSelectedRule(r)} />)}
              </div>
            </div>
          )}

          {/* 対応完了系 */}
          {done.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                ✅ 対応完了・スパム <span className="text-slate-600 font-normal normal-case">({done.length}件)</span>
              </h2>
              <div className="space-y-2">
                {done.map(r => <RuleRow key={r.id} rule={r} onClick={() => setSelectedRule(r)} />)}
              </div>
            </div>
          )}
        </div>
      )}

      {selectedRule && <RuleModal rule={selectedRule} onClose={() => setSelectedRule(null)} />}
    </div>
  )
}

function RuleRow({ rule, onClick }: { rule: AssignmentRule; onClick: () => void }) {
  const isDone = rule.priority === 0
  return (
    <button
      onClick={onClick}
      className={`w-full text-left flex items-center gap-4 px-4 py-3 rounded-xl border transition-colors group ${
        isDone
          ? 'bg-slate-800/50 border-slate-700/50 hover:bg-slate-700/50'
          : rule.priority >= 10
          ? 'bg-red-950/30 border-red-800/40 hover:bg-red-950/50'
          : 'bg-slate-800 border-slate-700 hover:bg-slate-700'
      }`}
    >
      {rule.priority >= 10 && <span className="text-red-400 text-xs font-bold shrink-0">！</span>}
      <p className={`flex-1 text-sm ${isDone ? 'text-slate-500' : 'text-slate-200'} group-hover:text-white transition-colors line-clamp-1`}>
        {rule.keyword}
      </p>
      <span className={`shrink-0 text-xs px-2.5 py-1 rounded-full font-medium ${getAssigneeColor(rule.assignee)}`}>
        {rule.assignee.length > 15 ? rule.assignee.slice(0, 15) + '…' : rule.assignee}
      </span>
      {rule.action && (
        <span className={`shrink-0 hidden md:inline text-xs px-2 py-0.5 rounded ${ACTION_COLOR[rule.action] || 'bg-blue-500/10 text-blue-300'}`}>
          {rule.action.split('\n')[0].slice(0, 15)}{rule.action.length > 15 ? '…' : ''}
        </span>
      )}
    </button>
  )
}
