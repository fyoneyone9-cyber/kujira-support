import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()
  const { data, error } = await supabase
    .from('p400_orders')
    .select('*')
    .order('created_at', { ascending: false })
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data)
}

export async function POST(request: Request) {
  const supabase = await createClient()
  const body = await request.json()

  const items = [
    { qty: body.qty_p400 || 0, price: 49800 },
    { qty: body.qty_setup_credit || 0, price: 6000 },
    { qty: body.qty_setup_emoney || 0, price: 10000 },
    { qty: body.qty_setup_qr || 0, price: 6000 },
    { qty: body.qty_cable || 0, price: 4800 },
  ]
  const subtotal = items.reduce((sum, i) => sum + i.qty * i.price, 0)
  const tax = Math.floor(subtotal * 0.1)
  const total = subtotal + tax

  // Generate order_no
  const today = new Date()
  const dateStr = today.toISOString().slice(0, 10).replace(/-/g, '')
  const { count } = await supabase.from('p400_orders').select('*', { count: 'exact', head: true })
  const seq = String((count || 0) + 1).padStart(4, '0')
  const order_no = `P400-${dateStr}-${seq}`

  const { data, error } = await supabase
    .from('p400_orders')
    .insert({ ...body, order_no, subtotal, tax, total })
    .select()
    .single()

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data, { status: 201 })
}
