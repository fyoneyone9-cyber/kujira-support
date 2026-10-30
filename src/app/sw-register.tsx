'use client'

import { useEffect } from 'react'

// PWA化：Service Workerを登録してホーム画面への追加（インストール）を可能にする
export default function SWRegister() {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(() => {})
    }
  }, [])
  return null
}
