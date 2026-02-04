'use client'

import { cn } from '@/lib/utils/cn'

interface MarqueeProps {
  children: React.ReactNode
  className?: string
  reverse?: boolean
  pauseOnHover?: boolean
  speed?: 'slow' | 'normal' | 'fast'
}

const speedMap = {
  slow: '60s',
  normal: '40s',
  fast: '20s',
}

export function Marquee({
  children,
  className,
  reverse = false,
  pauseOnHover = true,
  speed = 'normal',
}: MarqueeProps) {
  return (
    <div
      className={cn(
        'group flex overflow-hidden [--gap:1rem] gap-[var(--gap)]',
        className
      )}
    >
      {Array.from({ length: 2 }).map((_, i) => (
        <div
          key={i}
          className={cn(
            'flex shrink-0 justify-around gap-[var(--gap)]',
            'animate-marquee',
            reverse && 'animate-marquee-reverse',
            pauseOnHover && 'group-hover:[animation-play-state:paused]'
          )}
          style={{
            animationDuration: speedMap[speed],
          }}
        >
          {children}
        </div>
      ))}
    </div>
  )
}

interface TestimonialCardProps {
  quote: string
  author: string
  role: string
  avatar?: string
  className?: string
}

export function TestimonialCard({
  quote,
  author,
  role,
  avatar,
  className,
}: TestimonialCardProps) {
  return (
    <div
      className={cn(
        'relative w-80 rounded-2xl border border-stone-200 bg-white p-6',
        'hover:shadow-lg transition-shadow duration-300',
        className
      )}
    >
      <p className="text-stone-600 text-sm leading-relaxed mb-4">"{quote}"</p>
      <div className="flex items-center gap-3">
        {avatar ? (
          <img src={avatar} alt={author} className="w-10 h-10 rounded-full" />
        ) : (
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-stone-300 to-stone-400" />
        )}
        <div>
          <p className="font-medium text-stone-900 text-sm">{author}</p>
          <p className="text-stone-500 text-xs">{role}</p>
        </div>
      </div>
    </div>
  )
}
