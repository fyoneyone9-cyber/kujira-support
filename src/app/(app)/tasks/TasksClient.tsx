'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type Task = {
  id: string
  title: string
  description: string | null
  due_at: string | null
  done: boolean
  created_at: string
}

export default function TasksClient() {
  const supabase = createClient()
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [dueAt, setDueAt] = useState('')
  const [loading, setLoading] = useState(true)
  const [notifGranted, setNotifGranted] = useState(false)

  useEffect(() => {
    fetchTasks()
    if ('Notification' in window) {
      if (Notification.permission === 'granted') setNotifGranted(true)
    }
    const interval = setInterval(checkAlarms, 60000)
    return () => clearInterval(interval)
  }, [])

  const fetchTasks = async () => {
    const { data } = await supabase
      .from('tasks')
      .select('*')
      .eq('done', false)
      .order('due_at', { ascending: true, nullsFirst: false })
    setTasks(data || [])
    setLoading(false)
  }

  const requestNotif = async () => {
    const perm = await Notification.requestPermission()
    setNotifGranted(perm === 'granted')
  }

  const checkAlarms = async () => {
    if (Notification.permission !== 'granted') return
    const { data } = await supabase.from('tasks').select('*').eq('done', false)
    const now = new Date()
    for (const task of data || []) {
      if (!task.due_at) continue
      const due = new Date(task.due_at)
      const diff = (due.getTime() - now.getTime()) / 60000
      if (diff > 29 && diff <= 30) {
        new Notification(`⏰ 30分前: ${task.title}`, { body: due.toLocaleString('ja-JP'), icon: '/favicon.ico' })
      }
      if (diff > 9 && diff <= 10) {
        new Notification(`🔔 10分前: ${task.title}`, { body: due.toLocaleString('ja-JP'), icon: '/favicon.ico' })
      }
    }
  }

  const addTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return
    await supabase.from('tasks').insert({ title: title.trim(), description: description.trim() || null, due_at: dueAt || null })
    setTitle(''); setDescription(''); setDueAt('')
    fetchTasks()
  }

  const toggleDone = async (id: string) => {
    await supabase.from('tasks').update({ done: true }).eq('id', id)
    setTasks(prev => prev.filter(t => t.id !== id))
  }

  const deleteTask = async (id: string) => {
    await supabase.from('tasks').delete().eq('id', id)
    setTasks(prev => prev.filter(t => t.id !== id))
  }

  const isUrgent = (due_at: string | null) => {
    if (!due_at) return false
    const diff = (new Date(due_at).getTime() - Date.now()) / 60000
    return diff <= 30 && diff > 0
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">✅ タスク管理</h1>
        {!notifGranted && 'Notification' in window && (
          <button onClick={requestNotif} className="text-xs px-4 py-2 bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/40 text-yellow-300 rounded-xl transition-colors">
            🔔 通知を有効にする
          </button>
        )}
        {notifGranted && <span className="text-xs text-green-400">🔔 通知ON</span>}
      </div>

      <form onSubmit={addTask} className="bg-slate-800 rounded-2xl border border-slate-700 p-5 mb-6">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">タスクを追加</h2>
        <div className="space-y-3">
          <input type="text" value={title} onChange={e => setTitle(e.target.value)} placeholder="タスク名" required className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="メモ（任意）" rows={2} className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none" />
          <div className="flex gap-3">
            <input type="datetime-local" value={dueAt} onChange={e => setDueAt(e.target.value)} className="flex-1 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <button type="submit" className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-xl transition-colors">追加</button>
          </div>
        </div>
      </form>

      <div className="space-y-3">
        {loading && <p className="text-slate-400 text-sm">読み込み中...</p>}
        {!loading && tasks.length === 0 && (
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-10 text-center">
            <p className="text-slate-500 text-sm">タスクがありません</p>
          </div>
        )}
        {tasks.map(task => (
          <div key={task.id} className={`bg-slate-800 rounded-2xl border p-4 flex items-start gap-4 ${isUrgent(task.due_at) ? 'border-yellow-500/60 bg-yellow-500/5' : 'border-slate-700'}`}>
            <button onClick={() => toggleDone(task.id)} className="mt-0.5 w-5 h-5 rounded-full border-2 border-slate-500 hover:border-green-400 flex-shrink-0 transition-colors" />
            <div className="flex-1 min-w-0">
              <p className="text-white font-medium text-sm">{task.title}</p>
              {task.description && <p className="text-slate-400 text-xs mt-1 whitespace-pre-wrap">{task.description}</p>}
              {task.due_at && (
                <p className={`text-xs mt-1.5 ${isUrgent(task.due_at) ? 'text-yellow-400 font-semibold' : 'text-slate-500'}`}>
                  {isUrgent(task.due_at) ? '⚠️ ' : '📅 '}
                  {new Date(task.due_at).toLocaleString('ja-JP', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                </p>
              )}
            </div>
            <button onClick={() => deleteTask(task.id)} className="text-slate-600 hover:text-red-400 transition-colors text-sm flex-shrink-0">🗑</button>
          </div>
        ))}
      </div>
    </div>
  )
}
