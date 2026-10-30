import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

export const runtime = 'nodejs'

// 「更新を反映」ボタン用API。
// next build を実行し、成功したら現在のサーバープロセスを終了する。
// start_production.bat の再起動ループが自動的に新しいビルドで next start を立ち上げ直す。
// ビルド自体には数十秒かかるため、このAPIはすぐ202を返し、処理はバックグラウンドの
// 別プロセス（rebuild_and_restart.bat）に任せる。
export async function POST() {
  const projectDir = path.resolve(process.cwd())
  const batPath = path.join(projectDir, 'rebuild_and_restart.bat')

  const child = spawn('cmd.exe', ['/c', batPath], {
    cwd: projectDir,
    detached: true,
    stdio: 'ignore',
    windowsHide: true,
  })
  child.unref()

  return NextResponse.json({
    ok: true,
    message: 'ビルドと再起動を開始しました。完了まで1〜2分ほどかかります。完了後、サーバーが一瞬落ちて自動的に再起動します。',
  }, { status: 202 })
}
