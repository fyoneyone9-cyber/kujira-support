import { NextResponse } from 'next/server'
import { execSync } from 'child_process'
import fs from 'fs'
import path from 'path'

const BACKUP_BASE = 'C:\\GensparkClaw\\kujira-backup'
const SOURCE = 'C:\\GensparkClaw\\kujira-support'
const MAX_GENERATIONS = 3

export async function POST() {
  try {
    // バックアップフォルダ作成
    if (!fs.existsSync(BACKUP_BASE)) {
      fs.mkdirSync(BACKUP_BASE, { recursive: true })
    }

    // タイムスタンプフォルダ名
    const now = new Date()
    const ts = now.toISOString().replace(/[:.]/g, '-').slice(0, 19)
    const destDir = path.join(BACKUP_BASE, ts)

    // robocopyでコピー（node_modules/.nextを除外）
    // robocopyは成功時も1,2,3を返すためspawnSyncで制御
    try {
      execSync(
        `robocopy "${SOURCE}" "${destDir}" /E /XD node_modules .next .git /NFL /NDL /NJH /NJS`,
        { stdio: 'pipe' }
      )
    } catch (robocopyErr: any) {
      // robocopyの終了コード8未満は成功（1=ファイルコピー済み、3=コピー+削除等）
      if (robocopyErr.status >= 8) throw robocopyErr
    }

    // 3世代超えたら古いのを削除
    const dirs = fs.readdirSync(BACKUP_BASE)
      .filter(d => fs.statSync(path.join(BACKUP_BASE, d)).isDirectory())
      .map(d => ({ name: d, time: fs.statSync(path.join(BACKUP_BASE, d)).mtime }))
      .sort((a, b) => a.time.getTime() - b.time.getTime())

    const deleted: string[] = []
    while (dirs.length > MAX_GENERATIONS) {
      const old = dirs.shift()!
      fs.rmSync(path.join(BACKUP_BASE, old.name), { recursive: true, force: true })
      deleted.push(old.name)
    }

    // 残存世代一覧
    const remaining = fs.readdirSync(BACKUP_BASE)
      .filter(d => fs.statSync(path.join(BACKUP_BASE, d)).isDirectory())
      .sort()

    return NextResponse.json({
      ok: true,
      backup: ts,
      deleted,
      remaining,
    })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: e.message }, { status: 500 })
  }
}

export async function GET() {
  try {
    if (!fs.existsSync(BACKUP_BASE)) {
      return NextResponse.json({ backups: [] })
    }
    const backups = fs.readdirSync(BACKUP_BASE).sort().reverse()
    return NextResponse.json({ backups })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: e.message }, { status: 500 })
  }
}
