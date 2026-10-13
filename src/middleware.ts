import { NextResponse, type NextRequest } from 'next/server'

export const runtime = 'nodejs'

export async function middleware(request: NextRequest) {
  // ローカル開発用: 認証スキップ
  return NextResponse.next()
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
