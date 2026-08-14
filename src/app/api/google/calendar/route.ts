import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function GET() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.json({ error: 'unauthorized' }, { status: 401 })

  const { data: tokenData } = await supabase
    .from('google_tokens')
    .select('access_token')
    .eq('user_id', user.id)
    .single()

  if (!tokenData?.access_token) return NextResponse.json({ error: 'not_connected' }, { status: 401 })

  const now = new Date()
  const timeMin = now.toISOString()
  const timeMax = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString()

  const res = await fetch(
    `https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=${timeMin}&timeMax=${timeMax}&singleEvents=true&orderBy=startTime&maxResults=10`,
    { headers: { Authorization: `Bearer ${tokenData.access_token}` } }
  )

  const data = await res.json()
  return NextResponse.json({ events: data.items || [] })
}
