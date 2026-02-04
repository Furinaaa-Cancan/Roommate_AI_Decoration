import Link from 'next/link'

const footerLinks = {
  product: [
    { label: '工作台', href: '/' },
    { label: '作品展', href: '/gallery' },
    { label: '定价', href: '/pricing' },
  ],
  company: [
    { label: '关于我们', href: '/about' },
    { label: '联系我们', href: '/contact' },
  ],
  legal: [
    { label: '隐私政策', href: '/privacy' },
    { label: '服务条款', href: '/terms' },
  ],
}

export function Footer() {
  return (
    <footer className="bg-brand-charcoal text-white/60">
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid md:grid-cols-4 gap-12">
          {/* Brand */}
          <div className="md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <span className="font-serif font-bold text-2xl text-white tracking-tight">
                Roommate
              </span>
              <span className="text-xs text-brand-terracotta font-medium tracking-wider uppercase mt-1">
                AI
              </span>
            </Link>
            <p className="text-sm text-white/50 leading-relaxed">
              AI驱动的室内设计平台，将毛胚房一键转化为精装效果图。
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="text-white font-medium mb-4">产品</h4>
            <ul className="space-y-3">
              {footerLinks.product.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm hover:text-white transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-white font-medium mb-4">公司</h4>
            <ul className="space-y-3">
              {footerLinks.company.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm hover:text-white transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-white font-medium mb-4">法律</h4>
            <ul className="space-y-3">
              {footerLinks.legal.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm hover:text-white transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-white/40">
            © 2026 Roommate AI. All rights reserved.
          </p>
          <p className="text-sm text-white/40">
            Made with AI for designers
          </p>
        </div>
      </div>
    </footer>
  )
}
