'use client'

import { useEffect, useState } from 'react'

interface P400Order {
  id: string
  order_no: string
  order_date: string
  store_name: string
  store_address?: string
  store_tel?: string
  store_manager?: string
  general_manager?: string
  delivery_place?: string
  payment_terms?: string
  notes?: string
  qty_p400: number
  qty_setup_credit: number
  qty_setup_emoney: number
  qty_setup_qr: number
  qty_cable: number
  subtotal: number
  tax: number
  total: number
  status: string
}

const STATUS_LABELS: Record<string, { label: string; color: string }> = {
  draft: { label: '下書き', color: 'bg-slate-600 text-slate-200' },
  sent: { label: '送付済', color: 'bg-blue-600 text-white' },
  delivered: { label: '納品済', color: 'bg-green-600 text-white' },
  cancelled: { label: 'キャンセル', color: 'bg-red-600 text-white' },
}

const ITEMS = [
  { key: 'qty_p400', label: 'Verifone P400', price: 49800 },
  { key: 'qty_setup_credit', label: 'セットアップ用（クレジット・電子マネー）', price: 6000 },
  { key: 'qty_setup_emoney', label: 'セットアップ用（電子マネー）', price: 10000 },
  { key: 'qty_setup_qr', label: 'セットアップ用（QRコード）', price: 6000 },
  { key: 'qty_cable', label: 'RS-232Cケーブル(1m)', price: 4800 },
] as const

type QtyKey = typeof ITEMS[number]['key']

const defaultForm = () => ({
  order_date: new Date().toISOString().slice(0, 10),
  store_name: '',
  store_address: '',
  store_tel: '',
  store_manager: '',
  general_manager: '',
  delivery_place: '',
  payment_terms: '別途請求',
  notes: '',
  qty_p400: 0,
  qty_setup_credit: 0,
  qty_setup_emoney: 0,
  qty_setup_qr: 0,
  qty_cable: 0,
})

export default function P400OrdersPage() {
  const [orders, setOrders] = useState<P400Order[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(defaultForm())
  const [submitting, setSubmitting] = useState(false)

  const subtotal = ITEMS.reduce((sum, item) => sum + (form[item.key] || 0) * item.price, 0)
  const tax = Math.floor(subtotal * 0.1)
  const total = subtotal + tax

  const fetchOrders = async () => {
    const res = await fetch('/api/p400-orders')
    const data = await res.json()
    setOrders(data)
    setLoading(false)
  }

  useEffect(() => { fetchOrders() }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    await fetch('/api/p400-orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    setForm(defaultForm())
    setShowForm(false)
    setSubmitting(false)
    fetchOrders()
  }

  const handleStatusChange = async (id: string, status: string) => {
    await fetch(`/api/p400-orders/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    })
    fetchOrders()
  }

  const handleDelete = async (id: string) => {
    if (!confirm('削除しますか？')) return
    await fetch(`/api/p400-orders/${id}`, { method: 'DELETE' })
    fetchOrders()
  }

  const handleExcel = (id: string) => {
    window.open(`/api/p400-orders/${id}/excel`, '_blank')
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">P400注文書</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-medium transition-colors"
        >
          {showForm ? '✕ 閉じる' : '＋ 新規作成'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-slate-800 rounded-2xl border border-slate-700 p-6 space-y-4">
          <h2 className="text-lg font-bold text-white">新規注文書作成</h2>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">注文日 *</label>
              <input type="date" required value={form.order_date}
                onChange={e => setForm({ ...form, order_date: e.target.value })}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">対象店舗名 *</label>
              <input type="text" required value={form.store_name}
                onChange={e => setForm({ ...form, store_name: e.target.value })}
                placeholder="店舗名"
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">住所</label>
              <input type="text" value={form.store_address}
                onChange={e => setForm({ ...form, store_address: e.target.value })}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">電話番号</label>
              <input type="text" value={form.store_tel}
                onChange={e => setForm({ ...form, store_tel: e.target.value })}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">担当者名</label>
              <input type="text" value={form.store_manager}
                onChange={e => setForm({ ...form, store_manager: e.target.value })}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">総括担当者名</label>
              <input type="text" value={form.general_manager}
                onChange={e => setForm({ ...form, general_manager: e.target.value })}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">入荷場所</label>
              <input type="text" value={form.delivery_place}
                onChange={e => setForm({ ...form, delivery_place: e.target.value })}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">支払条件</label>
              <input type="text" value={form.payment_terms}
                onChange={e => setForm({ ...form, payment_terms: e.target.value })}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
          </div>

          <div>
            <label className="block text-xs text-slate-400 mb-1">備考</label>
            <textarea value={form.notes} rows={2}
              onChange={e => setForm({ ...form, notes: e.target.value })}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
          </div>

          {/* Items */}
          <div>
            <h3 className="text-sm font-medium text-slate-300 mb-2">品目数量</h3>
            <div className="space-y-2">
              {ITEMS.map(item => (
                <div key={item.key} className="flex items-center gap-4">
                  <span className="text-sm text-slate-300 w-64">{item.label}</span>
                  <span className="text-xs text-slate-400 w-24">{item.price.toLocaleString()}円</span>
                  <input
                    type="number" min={0}
                    value={form[item.key]}
                    onChange={e => setForm({ ...form, [item.key]: parseInt(e.target.value) || 0 })}
                    className="w-20 bg-slate-700 border border-slate-600 rounded-lg px-3 py-1 text-white text-sm text-center"
                  />
                  <span className="text-sm text-slate-400">
                    = {((form[item.key] || 0) * item.price).toLocaleString()}円
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Totals */}
          <div className="bg-slate-700/50 rounded-xl p-4 text-sm space-y-1">
            <div className="flex justify-between text-slate-300">
              <span>小計</span><span>{subtotal.toLocaleString()}円</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span>消費税(10%)</span><span>{tax.toLocaleString()}円</span>
            </div>
            <div className="flex justify-between text-white font-bold border-t border-slate-600 pt-1">
              <span>合計(税込)</span><span>{total.toLocaleString()}円</span>
            </div>
          </div>

          <div className="flex justify-end gap-3">
            <button type="button" onClick={() => setShowForm(false)}
              className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-xl text-sm transition-colors">
              キャンセル
            </button>
            <button type="submit" disabled={submitting}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-medium transition-colors disabled:opacity-50">
              {submitting ? '作成中...' : '作成'}
            </button>
          </div>
        </form>
      )}

      {/* List */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700 text-slate-400 text-xs">
              <th className="px-4 py-3 text-left">注文番号</th>
              <th className="px-4 py-3 text-left">注文日</th>
              <th className="px-4 py-3 text-left">対象店舗</th>
              <th className="px-4 py-3 text-right">合計</th>
              <th className="px-4 py-3 text-center">ステータス</th>
              <th className="px-4 py-3 text-center">操作</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="px-4 py-8 text-center text-slate-400">読み込み中...</td></tr>
            ) : orders.length === 0 ? (
              <tr><td colSpan={6} className="px-4 py-8 text-center text-slate-400">注文書がありません</td></tr>
            ) : orders.map(order => {
              const st = STATUS_LABELS[order.status] || STATUS_LABELS.draft
              return (
                <tr key={order.id} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                  <td className="px-4 py-3 text-white font-mono text-xs">{order.order_no}</td>
                  <td className="px-4 py-3 text-slate-300">{order.order_date}</td>
                  <td className="px-4 py-3 text-slate-300">{order.store_name}</td>
                  <td className="px-4 py-3 text-right text-white">{order.total.toLocaleString()}円</td>
                  <td className="px-4 py-3 text-center">
                    <select
                      value={order.status}
                      onChange={e => handleStatusChange(order.id, e.target.value)}
                      className={`text-xs px-2 py-1 rounded-full font-medium cursor-pointer border-0 ${st.color}`}
                    >
                      <option value="draft">下書き</option>
                      <option value="sent">送付済</option>
                      <option value="delivered">納品済</option>
                      <option value="cancelled">キャンセル</option>
                    </select>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <button
                        onClick={() => handleExcel(order.id)}
                        className="px-2 py-1 bg-green-700 hover:bg-green-600 text-white rounded-lg text-xs transition-colors"
                      >
                        📥 Excel
                      </button>
                      <button
                        onClick={() => handleDelete(order.id)}
                        className="px-2 py-1 bg-red-800 hover:bg-red-700 text-white rounded-lg text-xs transition-colors"
                      >
                        🗑
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
