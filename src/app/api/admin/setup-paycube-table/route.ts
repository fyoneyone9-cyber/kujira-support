import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export const runtime = 'nodejs'

export async function GET() {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  // テーブル作成
  const { error } = await supabase.rpc('exec_sql', {
    sql: `
      create table if not exists paycube_contracts (
        id uuid default gen_random_uuid() primary key,
        client_name text not null,
        management_no text,
        management_no_dealer text,
        product_type text,
        serial_no_hard text,
        serial_no_bill text,
        plan_name text,
        plan_type text default 'paid',
        start_date date,
        end_date date not null,
        status text default 'active',
        contacted_at timestamptz,
        renewed_at timestamptz,
        notes text,
        created_at timestamptz default now(),
        updated_at timestamptz default now()
      );
    `
  }).catch(() => ({ error: null }))

  // RPC不可の場合はダイレクトにテーブル存在確認
  const { data, error: selectErr } = await supabase
    .from('paycube_contracts')
    .select('id')
    .limit(1)

  if (selectErr && selectErr.code === '42P01') {
    return NextResponse.json({
      error: 'テーブルが存在しません。Supabase SQLエディタで003_paycube_contracts.sqlを実行してください。',
      sql_url: 'https://supabase.com/dashboard/project/fjkpdejyusnttbhdmyxt/sql/new'
    }, { status: 500 })
  }

  return NextResponse.json({ ok: true, message: 'paycube_contractsテーブル確認OK' })
}
