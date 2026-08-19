'use client'

import { useEffect, useState } from 'react'

type PurchaseOrderItem = {
  id?: string
  description: string
  sub_description: string
  quantity: number
  unit: string
  unit_price: number
  amount: number
}

type PurchaseOrder = {
  id: string
  order_no: string
  order_date: string
  delivery_date: string
  vendor_name: string
  payment_terms: string
  delivery_place: string
  status: string
  notes: string
  subtotal: number
  tax: number
  total: number
}

const STATUS_LABELS: Record<string, string> = {
  draft: '下書き',
  sent: '送付済',
  delivered: '納品済',
  cancelled: 'キャンセル',
}

const STATUS_COLORS: Record<string, string> = {
  draft: 'bg-slate-600 text-slate-200',
  sent: 'bg-blue-600 text-blue-100',
  delivered: 'bg-green-600 text-green-100',
  cancelled: 'bg-red-600 text-red-100',
}

const today = new Date().toISOString().split('T')[0]

const emptyItem = (): PurchaseOrderItem => ({
  description: '',
  sub_description: '',
  quantity: 1,
  unit: '台',
  unit_price: 0,
  amount: 0,
})

export default function PurchaseOrdersPage() {
  const [orders, setOrders] = useState<PurchaseOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)

  // フォーム状態
  const [orderDate, setOrderDate] = useState(today)
  const [deliveryDate, setDeliveryDate] = useState('')
  const [vendorName, setVendorName] = useState('日本コムネックス')
  const [paymentTerms, setPaymentTerms] = useState('請求書払い')
  const [deliveryPlace, setDeliveryPlace] = useState('大阪府大阪市西区靭本町　本社')
  const [notes, setNotes] = useState('')
  const [items, setItems] = useState<PurchaseOrderItem[]>([emptyItem()])
  const [saving, setSaving] = useState(false)

  const fetchOrders = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/purchase-orders')
      const data = await res.json()
      setOrders(Array.isArray(data) ? data : [])
    } catch {
      setOrders([])
    }
    setLoading(false)
  }

  useEffect(() => { fetchOrders() }, [])

  // リアルタイム計算
  const subtotal = items.reduce((s, i) => s + i.quantity * i.unit_price, 0)
  const tax = Math.floor(subtotal * 0.1)
  const total = subtotal + tax

  const updateItem = (idx: number, field: keyof PurchaseOrderItem, value: string | number) => {
    setItems(prev => {
      const next = [...prev]
      const item = { ...next[idx], [field]: value }
      item.amount = item.quantity * item.unit_price
      next[idx] = item
      return next
    })
  }

  const addPreset = (description: string, unit_price: number) => {
    setItems(prev => [...prev, { description, sub_description: '', quantity: 1, unit: '台', unit_price, amount: unit_price }])
  }

  const generateOrderNo = () => {
    const now = new Date()
    return `PO-${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}-${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}`
  }

  const handleSubmit = async () => {
    setSaving(true)
    const orderNo = generateOrderNo()
    const payload = {
      order_no: orderNo,
      order_date: orderDate,
      delivery_date: deliveryDate,
      vendor_name: vendorName,
      payment_terms: paymentTerms,
      delivery_place: deliveryPlace,
      notes,
      subtotal,
      tax,
      total,
      items: items.map((item, idx) => ({ ...item, amount: item.quantity * item.unit_price, sort_order: idx })),
    }
    const res = await fetch('/api/purchase-orders', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    if (res.ok) {
      setShowForm(false)
      setItems([emptyItem()])
      setDeliveryDate('')
      setNotes('')
      await fetchOrders()
    }
    setSaving(false)
  }

  const handleStatusChange = async (id: string, status: string) => {
    await fetch(`/api/purchase-orders/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status }) })
    await fetchOrders()
  }

  const handleDelete = async (id: string) => {
    if (!confirm('この発注書を削除しますか？')) return
    await fetch(`/api/purchase-orders/${id}`, { method: 'DELETE' })
    await fetchOrders()
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">発注書管理</h1>
        <button
          onClick={() => setShowForm(v => !v)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          {showForm ? '閉じる' : '+ 新規作成'}
        </button>
      </div>

      {/* 新規作成フォーム */}
      {showForm && (
        <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6 space-y-4">
          <h2 className="text-lg font-semibold text-white">新規発注書</h2>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-slate-400">発注日</label>
              <input type="date" value={orderDate} onChange={e => setOrderDate(e.target.value)}
                className="w-full mt-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="text-sm text-slate-400">納期</label>
              <input type="text" value={deliveryDate} onChange={e => setDeliveryDate(e.target.value)} placeholder="例: 2024年3月末"
                className="w-full mt-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="text-sm text-slate-400">仕入先名</label>
              <input type="text" value={vendorName} onChange={e => setVendorName(e.target.value)}
                className="w-full mt-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div>
              <label className="text-sm text-slate-400">支払条件</label>
              <input type="text" value={paymentTerms} onChange={e => setPaymentTerms(e.target.value)}
                className="w-full mt-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div className="col-span-2">
              <label className="text-sm text-slate-400">入荷場所</label>
              <input type="text" value={deliveryPlace} onChange={e => setDeliveryPlace(e.target.value)}
                className="w-full mt-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
            <div className="col-span-2">
              <label className="text-sm text-slate-400">備考</label>
              <textarea value={notes} onChange={e => setNotes(e.target.value)} rows={2}
                className="w-full mt-1 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm" />
            </div>
          </div>

          {/* プリセット */}
          <div className="flex gap-2 flex-wrap">
            <span className="text-sm text-slate-400 self-center">プリセット:</span>
            <button onClick={() => addPreset('PayCube本体', 370000)}
              className="bg-slate-600 hover:bg-slate-500 text-white text-xs px-3 py-1 rounded-lg">
              PayCube本体 ¥370,000
            </button>
            <button onClick={() => addPreset('電源アダプター', 2000)}
              className="bg-slate-600 hover:bg-slate-500 text-white text-xs px-3 py-1 rounded-lg">
              電源アダプター ¥2,000
            </button>
          </div>

          {/* 品目テーブル */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-slate-400 text-xs">
                  <th className="text-left pb-2">品名</th>
                  <th className="text-left pb-2">補足</th>
                  <th className="text-right pb-2 w-16">数量</th>
                  <th className="text-left pb-2 w-16">単位</th>
                  <th className="text-right pb-2 w-24">単価</th>
                  <th className="text-right pb-2 w-24">金額</th>
                  <th className="pb-2 w-8"></th>
                </tr>
              </thead>
              <tbody className="space-y-2">
                {items.map((item, idx) => (
                  <tr key={idx} className="gap-2">
                    <td className="pr-2">
                      <input type="text" value={item.description} onChange={e => updateItem(idx, 'description', e.target.value)}
                        className="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-white" />
                    </td>
                    <td className="pr-2">
                      <input type="text" value={item.sub_description} onChange={e => updateItem(idx, 'sub_description', e.target.value)}
                        className="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-white" />
                    </td>
                    <td className="pr-2">
                      <input type="number" value={item.quantity} min={1} onChange={e => updateItem(idx, 'quantity', Number(e.target.value))}
                        className="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-white text-right" />
                    </td>
                    <td className="pr-2">
                      <input type="text" value={item.unit} onChange={e => updateItem(idx, 'unit', e.target.value)}
                        className="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-white" />
                    </td>
                    <td className="pr-2">
                      <input type="number" value={item.unit_price} min={0} onChange={e => updateItem(idx, 'unit_price', Number(e.target.value))}
                        className="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-white text-right" />
                    </td>
                    <td className="pr-2 text-right text-slate-300">
                      ¥{(item.quantity * item.unit_price).toLocaleString()}
                    </td>
                    <td>
                      <button onClick={() => setItems(prev => prev.filter((_, i) => i !== idx))}
                        className="text-red-400 hover:text-red-300 text-lg leading-none">×</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <button onClick={() => setItems(prev => [...prev, emptyItem()])}
            className="text-sm text-blue-400 hover:text-blue-300">+ 行を追加</button>

          {/* 合計 */}
          <div className="border-t border-slate-700 pt-4 space-y-1 text-sm text-right">
            <div className="text-slate-400">小計: <span className="text-white">¥{subtotal.toLocaleString()}</span></div>
            <div className="text-slate-400">消費税(10%): <span className="text-white">¥{tax.toLocaleString()}</span></div>
            <div className="text-white font-bold text-base">合計(税込): ¥{total.toLocaleString()}</div>
          </div>

          <button onClick={handleSubmit} disabled={saving}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white py-2 rounded-lg font-medium transition-colors">
            {saving ? '保存中...' : '発注書を作成'}
          </button>
        </div>
      )}

      {/* 一覧テーブル */}
      <div className="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-400">読み込み中...</div>
        ) : orders.length === 0 ? (
          <div className="p-8 text-center text-slate-400">発注書がありません</div>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-slate-700/50">
              <tr className="text-slate-400 text-xs">
                <th className="text-left px-4 py-3">発注番号</th>
                <th className="text-left px-4 py-3">発注日</th>
                <th className="text-left px-4 py-3">仕入先</th>
                <th className="text-right px-4 py-3">合計金額</th>
                <th className="text-center px-4 py-3">ステータス</th>
                <th className="text-center px-4 py-3">操作</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id} className="border-t border-slate-700 hover:bg-slate-700/30">
                  <td className="px-4 py-3 text-white font-mono">{order.order_no}</td>
                  <td className="px-4 py-3 text-slate-300">{order.order_date}</td>
                  <td className="px-4 py-3 text-slate-300">{order.vendor_name}</td>
                  <td className="px-4 py-3 text-right text-white">¥{order.total.toLocaleString()}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_COLORS[order.status] || STATUS_COLORS.draft}`}>
                      {STATUS_LABELS[order.status] || order.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-center gap-2">
                      <a href={`/api/purchase-orders/${order.id}/excel`}
                        className="bg-green-700 hover:bg-green-600 text-white text-xs px-2 py-1 rounded transition-colors">
                        Excel
                      </a>
                      <select value={order.status} onChange={e => handleStatusChange(order.id, e.target.value)}
                        className="bg-slate-700 border border-slate-600 text-white text-xs rounded px-2 py-1">
                        <option value="draft">下書き</option>
                        <option value="sent">送付済</option>
                        <option value="delivered">納品済</option>
                        <option value="cancelled">キャンセル</option>
                      </select>
                      <button onClick={() => handleDelete(order.id)}
                        className="bg-red-700 hover:bg-red-600 text-white text-xs px-2 py-1 rounded transition-colors">
                        削除
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
