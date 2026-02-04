import type { Metadata } from 'next'
import './globals.css'
import { AuthProvider } from '@/lib/auth-provider'

export const metadata: Metadata = {
  title: 'NanoBanana AI | 顶级室内设计AI平台',
  description: '将毛胚房一键转化为精装效果图，4K超清，78秒出图，支持侘寂、奶油风、新中式等10+顶级设计风格',
  keywords: ['室内设计', 'AI设计', '毛胚房', '效果图', '装修设计', '4K渲染'],
  authors: [{ name: 'NanoBanana AI' }],
  openGraph: {
    title: 'NanoBanana AI | 顶级室内设计AI平台',
    description: '将毛胚房一键转化为精装效果图',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className="font-sans antialiased">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
