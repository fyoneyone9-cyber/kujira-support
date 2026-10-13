'use client'
import { useState, useEffect } from 'react'

export default function BackupButton() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<string | null>(null)
  const [backups, setBackups] = useState<string[]>([])

  const fetchBackups = async () => {
    const r = await fetch('/api/backup')
    const d = await r.json()
    setBackups(d.backups || [])
  }

  useEffect(() => { fetchBackups() }, [])

  const handleBackup = async () => {
    setLoading(true)
    setResult(null)
    try {
      const r = await fetch('/api/backup', { method: 'POST' })
      const d = await r.json()
      if (d.ok) {
        setResult(`✅ バックアップ完了: ${d.backup}`)
        fetchBackups()
      } else {
        setResult(`❌ エラー: ${d.error}`)
      }
    } catch (e: any) {
      setResult(`❌ エラー: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800 border border-slate-600 rounded-2xl p-4 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-white font-bold text-sm">🗂 バックアップ（3世代）</h2>
        <button
          onClick={handleBackup}
          disabled={loading}
          className="px-4 py-2 bg-amber-600 hover:bg-amber-500 disabled:bg-slate-600 text-white text-sm font-bold rounded-xl transition-colors"
        >
          {loading ? '実行中...' : '💾 今すぐバックアップ'}
        </button>
      </div>
      {result && (
        <p className="text-sm text-slate-300 mb-2">{result}</p>
      )}
      {backups.length > 0 && (
        <ul className="text-xs text-slate-400 space-y-1">
          {backups.map(b => (
            <li key={b}>📁 {b}</li>
          ))}
        </ul>
      )}
      {backups.length === 0 && (
        <p className="text-xs text-slate-500">バックアップなし</p>
      )}
    </div>
  )
}
