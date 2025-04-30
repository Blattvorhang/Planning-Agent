import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Navbar } from '@/components/ui/navbar'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'AI Learning Planner',
  description: 'An AI-powered learning planner to help you achieve your learning goals.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
          {/* Decorative elements */}
          <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
            <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-blue-500/10 to-violet-500/10 dark:from-blue-500/5 dark:to-violet-500/5 transform rotate-12 blur-3xl" />
            <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-indigo-500/10 to-purple-500/10 dark:from-indigo-500/5 dark:to-purple-500/5 transform -rotate-12 blur-3xl" />
          </div>
          
          {/* Main content */}
          <Navbar />
          <main className="relative z-10 pt-16">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
} 