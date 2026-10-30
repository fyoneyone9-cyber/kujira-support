// [GAS_SOURCE_V1 2026-10-29]
// Apps Script に貼り付けるコードを「テキストとして」返す。
//
// これまで /docs/hearing-gas-dialog.html を直接開かせていたが、
// ブラウザが HTML として解釈してしまい「動かない」と混乱を招いた。
// ここは text/plain で返し、コピー専用であることを明確にする。
import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs/promises'
import path from 'path'

export const runtime = 'nodejs'

const FILES: Record<string, string> = {
  code: 'hearing-gas.js',
  dialog: 'hearing-gas-dialog.html',
  // [KOUTEI_GAS_V1 2026-10-29] 工程管理表のスプレッドシート版
  'koutei': 'koutei-gas.js',
  'koutei-dialog': 'koutei-gas-dialog.html',
}

export async function GET(req: NextRequest) {
  const kind = req.nextUrl.searchParams.get('f') || 'code'
  const name = FILES[kind]
  if (!name) return new NextResponse('unknown file', { status: 400 })

  const p = path.join(process.cwd(), 'public', 'docs', name)
  const body = await fs.readFile(p, 'utf8').catch(() => null)
  if (body === null) return new NextResponse('not found', { status: 404 })

  return new NextResponse(body, {
    status: 200,
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  })
}
