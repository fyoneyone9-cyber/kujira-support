import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function GET() {
  const supabase = await createClient()
  const { data, error } = await supabase
    .from('purchase_orders')
    .select('*')
    .order('created_at', { ascending: false })

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data)
}

export async function POST(req: NextRequest) {
  const supabase = await createClient()
  const body = await req.json()
  const { items, ...order } = body

  const { data: orderData, error: orderError } = await supabase
    .from('purchase_orders')
    .insert(order)
    .select()
    .single()

  if (orderError) return NextResponse.json({ error: orderError.message }, { status: 500 })

  if (items && items.length > 0) {
    const itemsWithOrderId = items.map((item: Record<string, unknown>, idx: number) => ({
      ...item,
      order_id: orderData.id,
      sort_order: idx,
    }))
    const { error: itemsError } = await supabase.from('purchase_order_items').insert(itemsWithOrderId)
    if (itemsError) return NextResponse.json({ error: itemsError.message }, { status: 500 })
  }

  return NextResponse.json(orderData, { status: 201 })
}
