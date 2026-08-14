import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export const runtime = 'nodejs'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

// テーブル作成（初回のみ）
async function ensureTable() {
  await supabase.rpc('exec_sql', {
    sql: `
      CREATE TABLE IF NOT EXISTS teleapo_memos (
        id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
        content text NOT NULL,
        category text NOT NULL DEFAULT 'other',
        created_at timestamptz DEFAULT now()
      );
    `
  }).catch(() => null) // rpcがなければ無視
}

export async function GET() {
  const { data, error } = await supabase
    .from('teleapo_memos')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(100)

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ memos: data })
}

export async function POST(request: Request) {
  const { content, category } = await request.json()
  if (!content?.trim()) return NextResponse.json({ error: 'content required' }, { status: 400 })

  const { data, error } = await supabase
    .from('teleapo_memos')
    .insert({ content: content.trim(), category: category ?? 'other' })
    .select()
    .single()

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ memo: data })
}

export async function DELETE(request: Request) {
  const { id } = await request.json()
  if (!id) return NextResponse.json({ error: 'id required' }, { status: 400 })

  const { error } = await supabase.from('teleapo_memos').delete().eq('id', id)
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ ok: true })
}
