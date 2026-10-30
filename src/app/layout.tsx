import type { Metadata, Viewport } from 'next'
import './globals.css'
import SWRegister from './sw-register'

export const metadata: Metadata = {
  title: 'KUJIRA Support System',
  description: '導入支援サポートシステム',
  icons: {
    icon: '/favicon.svg',
    apple: '/icon-192.png',
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'KUJIRA Support',
  },
}

export const viewport: Viewport = {
  themeColor: '#0f172a',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <head>
        {/* Next.js 15のストリーミングメタデータだとmanifest linkがbody末尾に出てChromeが認識しない問題を回避するため直接headに書く */}
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className="bg-slate-900 text-slate-100 min-h-screen">
        {children}
        <SWRegister />
      </body>
    </html>
  )
}
