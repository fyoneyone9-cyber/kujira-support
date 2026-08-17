import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export const runtime = 'nodejs'

export async function GET() {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  // テーブル存在確認のみ行う（テーブル作成はSQLエディタで実行）

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
