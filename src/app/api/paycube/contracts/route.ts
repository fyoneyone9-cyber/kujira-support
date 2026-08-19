import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'

// GET: 一覧取得（アラート対象も含む）
export async function GET(req: NextRequest) {
  const supabase = createClient()
  const { searchParams } = new URL(req.url)
  const mode = searchParams.get('mode') // 'alert' = 2ヶ月以内のみ

  const today = new Date()
  const twoMonthsLater = new Date(today)
  twoMonthsLater.setMonth(twoMonthsLater.getMonth() + 2)

  let query = supabase
    .from('paycube_contracts')
    .select('*')
    .neq('status', 'expired')
    .neq('status', 'renewed')
    .order('end_date', { ascending: true })

  if (mode === 'alert') {
    query = query
      .lte('end_date', twoMonthsLater.toISOString().split('T')[0])
      .gte('end_date', today.toISOString().split('T')[0])
  } else if (mode === 'review') {
    query = query.eq('status', 'needs_review')
  }

  const { data, error } = await query
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ contracts: data })
}

// POST: 新規登録
export async function POST(req: NextRequest) {
  const supabase = createClient()
  const body = await req.json()
  const { data, error } = await supabase
    .from('paycube_contracts')
    .insert(body)
    .select()
    .single()
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ contract: data })
}

// PATCH: ステータス更新
export async function PATCH(req: NextRequest) {
  const supabase = createClient()
  const body = await req.json()
  const { id, ...updates } = body
  if (!id) return NextResponse.json({ error: 'id required' }, { status: 400 })
  const { data, error } = await supabase
    .from('paycube_contracts')
    .update(updates)
    .eq('id', id)
    .select()
    .single()
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ contract: data })
}
