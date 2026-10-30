import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export const runtime = 'nodejs'

// 「更新を反映」ボタンの押し忘れ検知用API。
// .next/BUILD_ID のファイル更新時刻（＝最後にビルドが完了した時刻）と、
// srcディレクトリ内の最新ソース更新時刻を比較し、ビルド後にソースが編集されていたら
// 「未反映の変更がある」と判定する。
function getLatestMtime(dir: string): number {
  let latest = 0
  let entries: fs.Dirent[]
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true })
  } catch {
    return latest
  }
  for (const entry of entries) {
    if (entry.name === 'node_modules' || entry.name === '.next' || entry.name.startsWith('.')) continue
    const fullPath = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      latest = Math.max(latest, getLatestMtime(fullPath))
    } else if (/\.(tsx?|css)$/.test(entry.name)) {
      try {
        const stat = fs.statSync(fullPath)
        latest = Math.max(latest, stat.mtimeMs)
      } catch {
        // noop
      }
    }
  }
  return latest
}

export async function GET() {
  const projectDir = process.cwd()
  const buildIdPath = path.join(projectDir, '.next', 'BUILD_ID')

  let buildTime: number | null = null
  try {
    const stat = fs.statSync(buildIdPath)
    buildTime = stat.mtimeMs
  } catch {
    return NextResponse.json({ buildTime: null, latestSourceTime: null, isStale: null })
  }

  const srcDir = path.join(projectDir, 'src')
  const latestSourceTime = getLatestMtime(srcDir)

  const isStale = latestSourceTime > buildTime

  return NextResponse.json({
    buildTime: new Date(buildTime).toISOString(),
    latestSourceTime: latestSourceTime ? new Date(latestSourceTime).toISOString() : null,
    isStale,
  })
}
