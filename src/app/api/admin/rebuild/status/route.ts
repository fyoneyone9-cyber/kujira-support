import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export const runtime = 'nodejs'

// 「更新を反映」ボタンの進捗確認用。rebuild_log.txt の中身を返す。
export async function GET() {
  const logPath = path.join(process.cwd(), 'rebuild_log.txt')
  if (!fs.existsSync(logPath)) {
    return NextResponse.json({ log: null, done: false, success: null })
  }
  const log = fs.readFileSync(logPath, 'utf-8')
  const done = log.includes('Build finished with exit code')
  const success = log.includes('Build succeeded')
  const failed = log.includes('Build FAILED')
  return NextResponse.json({ log, done: done || failed, success: success && !failed })
}
