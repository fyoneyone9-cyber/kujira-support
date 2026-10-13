import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'

// GET: 一覧取得（アラート対象も含む）
export async function GET(req: NextRequest) {
  const supabase = await createClient()
  const { searchParams } = new URL(req.url)
  const mode = searchParams.get('mode') // 'alert' = 未納品のみ、納品予定日が近い順

  let query = supabase
    .from('delivery_items')
    .select('*')
    .order('delivery_due_date', { ascending: true })

  if (mode === 'alert') {
    query = query.eq('status', 'active')
  }

  const { data, error } = await query
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ items: data })
}

// PATCH: ステータス更新（確認済みにする等）
export async function PATCH(req: NextRequest) {
  const supabase = await createClient()
  const body = await req.json()
  const { id, ...updates } = body
  if (!id) return NextResponse.json({ error: 'id required' }, { status: 400 })
  const { data, error } = await supabase
    .from('delivery_items')
    .update(updates)
    .eq('id', id)
    .select()
    .single()
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ item: data })
}
