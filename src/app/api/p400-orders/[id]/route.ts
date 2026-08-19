import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()
  const { data, error } = await supabase.from('p400_orders').select('*').eq('id', id).single()
  if (error) return NextResponse.json({ error: error.message }, { status: 404 })
  return NextResponse.json(data)
}

export async function PATCH(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()
  const body = await request.json()

  // Recalculate amounts if qty fields changed
  const items = [
    { qty: body.qty_p400 ?? undefined, price: 49800 },
    { qty: body.qty_setup_credit ?? undefined, price: 6000 },
    { qty: body.qty_setup_emoney ?? undefined, price: 10000 },
    { qty: body.qty_setup_qr ?? undefined, price: 6000 },
    { qty: body.qty_cable ?? undefined, price: 4800 },
  ]
  const hasQty = items.some(i => i.qty !== undefined)
  if (hasQty) {
    // fetch existing to fill missing qtys
    const { data: existing } = await supabase.from('p400_orders').select('*').eq('id', id).single()
    const merged = { ...existing, ...body }
    const subtotal = [
      (merged.qty_p400 || 0) * 49800,
      (merged.qty_setup_credit || 0) * 6000,
      (merged.qty_setup_emoney || 0) * 10000,
      (merged.qty_setup_qr || 0) * 6000,
      (merged.qty_cable || 0) * 4800,
    ].reduce((a, b) => a + b, 0)
    const tax = Math.floor(subtotal * 0.1)
    body.subtotal = subtotal
    body.tax = tax
    body.total = subtotal + tax
  }

  body.updated_at = new Date().toISOString()
  const { data, error } = await supabase.from('p400_orders').update(body).eq('id', id).select().single()
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data)
}

export async function DELETE(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()
  const { error } = await supabase.from('p400_orders').delete().eq('id', id)
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ success: true })
}
