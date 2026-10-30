import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

export const runtime = 'nodejs'

// 「サーバー終了」ボタン用API。
// start_production.bat の再起動ループと watchdog.ps1 を含めて全プロセスを停止する。
// 自分自身（このリクエストを処理しているサーバープロセス）も終了するため、
// レスポンスを返した後に少し遅延してから停止用バッチを起動する。
export async function POST() {
  const projectDir = path.resolve(process.cwd())
  const batPath = path.join(projectDir, 'shutdown_all.bat')

  const child = spawn('cmd.exe', ['/c', batPath], {
    cwd: projectDir,
    detached: true,
    stdio: 'ignore',
    windowsHide: true,
  })
  child.unref()

  return NextResponse.json({
    ok: true,
    message: 'サーバーと監視プロセスを停止します。再度使うときはスタートアップのショートカット（KujiraSupportLauncher）を実行するか、PCを再起動してください。',
  })
}
