'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion'
import { Menu, X as XIcon, ArrowRight, Github, User } from 'lucide-react'
import { useState } from 'react'
import { useSession } from 'next-auth/react'
import { cn } from '@/lib/utils/cn'

const navItems = [
  { href: '/', label: '首页' },
  { href: '/billing', label: '定价' },
]

export function Header() {
  const pathname = usePathname()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { data: session } = useSession()

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-brand-cream/95 backdrop-blur-md border-b border-brand-charcoal/5">
      <nav className="max-w-7xl mx-auto px-6 lg:px-10 h-20 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <span className="font-serif font-bold text-2xl text-brand-charcoal tracking-tight">
            Roommate
          </span>
          <span className="text-xs text-brand-terracotta font-medium tracking-wider uppercase mt-1">
            AI
          </span>
        </Link>

        {/* Desktop Nav - 居中 */}
        <div className="hidden md:flex items-center gap-8 absolute left-1/2 -translate-x-1/2">
          {navItems.map((item) => {
            const isActive = pathname === item.href || 
              (item.href !== '/' && pathname.startsWith(item.href))
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative text-sm font-medium transition-colors py-2",
                  isActive 
                    ? "text-brand-terracotta" 
                    : "text-brand-charcoal/70 hover:text-brand-charcoal"
                )}
              >
                {item.label}
                {isActive && (
                  <motion.div
                    layoutId="nav-underline"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-terracotta"
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  />
                )}
              </Link>
            )
          })}
        </div>

        {/* CTA */}
        <div className="hidden md:flex items-center gap-5">
          {/* 社交图标 */}
          <div className="flex items-center gap-3 pr-5 border-r border-brand-charcoal/10">
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="p-2 text-brand-charcoal/50 hover:text-brand-charcoal transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
            <a 
              href="https://x.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="p-2 text-brand-charcoal/50 hover:text-brand-charcoal transition-colors"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>
          </div>
          
          {session ? (
            <Link 
              href="/profile" 
              className="inline-flex items-center gap-2 text-sm font-medium text-brand-charcoal/70 hover:text-brand-charcoal transition-colors"
            >
              {session.user?.image ? (
                <img src={session.user.image} alt="" className="w-6 h-6 rounded-full" />
              ) : (
                <User className="w-5 h-5" />
              )}
              {session.user?.name || '个人中心'}
            </Link>
          ) : (
            <Link 
              href="/login" 
              className="text-sm font-medium text-brand-charcoal/70 hover:text-brand-charcoal transition-colors"
            >
              登录
            </Link>
          )}
          <Link 
            href={session ? "/profile" : "/login"} 
            className="inline-flex items-center gap-2 bg-brand-charcoal text-white px-5 py-2.5 text-sm font-medium hover:bg-brand-terracotta transition-colors"
          >
            开始体验
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden p-2 hover:bg-brand-charcoal/5 rounded-lg transition-colors"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? (
            <XIcon className="w-6 h-6 text-brand-charcoal" />
          ) : (
            <Menu className="w-6 h-6 text-brand-charcoal" />
          )}
        </button>
      </nav>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="md:hidden bg-brand-cream border-b border-brand-charcoal/10 px-6 py-6"
        >
          <div className="space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    "block px-4 py-3 text-base font-medium transition-colors",
                    isActive
                      ? "text-brand-terracotta"
                      : "text-brand-charcoal/70 hover:text-brand-charcoal"
                  )}
                >
                  {item.label}
                </Link>
              )
            })}
          </div>
          <div className="mt-6 pt-6 border-t border-brand-charcoal/10 space-y-3">
            {session ? (
              <Link 
                href="/profile" 
                className="block text-center text-brand-charcoal px-4 py-3 text-sm font-medium"
              >
                个人中心
              </Link>
            ) : (
              <Link 
                href="/login" 
                className="block text-center text-brand-charcoal px-4 py-3 text-sm font-medium"
              >
                登录
              </Link>
            )}
            <Link 
              href={session ? "/profile" : "/login"} 
              className="block text-center bg-brand-charcoal text-white px-4 py-3 text-sm font-medium"
            >
              开始体验
            </Link>
          </div>
        </motion.div>
      )}
    </header>
  )
}
