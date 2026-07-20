import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'KUJIRA Support System',
  description: '導入支援サポートシステム',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className="bg-slate-900 text-slate-100 min-h-screen">
        {children}
      </body>
    </html>
  )
}
