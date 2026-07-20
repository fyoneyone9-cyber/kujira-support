import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json()
    if (!email || !password) {
      return NextResponse.json({ error: 'メールとパスワードは必須です' }, { status: 400 })
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    )

    const { data, error } = await supabase.auth.admin.createUser({
      email,
      password,
      email_confirm: true,
    })

    if (error) {
      const msg = error.message.includes('already') ? 'このメールアドレスは既に登録されています' : error.message
      return NextResponse.json({ error: msg }, { status: 400 })
    }

    return NextResponse.json({ id: data.user.id, email: data.user.email })
  } catch {
    return NextResponse.json({ error: 'サーバーエラー' }, { status: 500 })
  }
}
