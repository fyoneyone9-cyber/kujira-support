import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function POST(req: NextRequest) {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.json({ error: 'unauthorized' }, { status: 401 })

  const { title, description, due_at } = await req.json()
  if (!due_at) return NextResponse.json({ error: 'due_at required' }, { status: 400 })

  const { data: tokenData } = await supabase
    .from('google_tokens')
    .select('access_token')
    .eq('user_id', user.id)
    .single()

  if (!tokenData?.access_token) return NextResponse.json({ error: 'not_connected' }, { status: 401 })

  const start = new Date(due_at)
  const end = new Date(start.getTime() + 60 * 60 * 1000) // 1時間後

  const event = {
    summary: title,
    description: description || '',
    start: { dateTime: start.toISOString(), timeZone: 'Asia/Tokyo' },
    end: { dateTime: end.toISOString(), timeZone: 'Asia/Tokyo' },
    reminders: {
      useDefault: false,
      overrides: [
        { method: 'popup', minutes: 30 },
        { method: 'popup', minutes: 10 },
      ],
    },
  }

  const res = await fetch('https://www.googleapis.com/calendar/v3/calendars/primary/events', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${tokenData.access_token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(event),
  })

  const data = await res.json()
  if (!res.ok) return NextResponse.json({ error: data }, { status: 500 })
  return NextResponse.json({ eventId: data.id })
}

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
