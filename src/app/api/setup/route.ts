import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  const results: string[] = []

  // manualsテーブル作成
  const { error: e1 } = await supabase.rpc('exec_migration', {
    sql: `CREATE TABLE IF NOT EXISTS manuals (
      id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
      title text NOT NULL,
      category text,
      content text,
      created_by uuid,
      created_at timestamptz DEFAULT now(),
      updated_at timestamptz DEFAULT now()
    )`
  })

  if (e1) {
    // rpcがない場合はテーブルに直接INSERT/SELECTで確認
    const { error: checkErr } = await supabase.from('manuals').select('id').limit(1)
    if (checkErr?.code === 'PGRST205') {
      results.push('ERROR: manuals table not found. Please run SQL migration manually.')
      results.push('Go to: https://supabase.com/dashboard/project/fjkpdejyusnttbhdmyxt/sql/new')
      results.push('Run the SQL from: supabase/migrations/001_initial.sql')
    } else {
      results.push('manuals table already exists ✓')
    }
  } else {
    results.push('manuals table created ✓')
  }

  return NextResponse.json({ results, message: 'Setup check complete' })
}
