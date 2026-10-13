import Sidebar from '@/components/Sidebar'
import GlobalAlertBar from '@/components/GlobalAlertBar'

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <GlobalAlertBar />
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  )
}
