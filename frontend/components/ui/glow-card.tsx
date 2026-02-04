'use client'

import { useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils/cn'

interface GlowCardProps {
  children: React.ReactNode
  className?: string
  glowColor?: string
}

export function GlowCard({ 
  children, 
  className,
  glowColor = 'rgba(245, 158, 11, 0.4)' 
}: GlowCardProps) {
  const divRef = useRef<HTMLDivElement>(null)
  const [position, setPosition] = useState({ x: 0, y: 0 })
  const [isHovered, setIsHovered] = useState(false)

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!divRef.current) return
    const rect = divRef.current.getBoundingClientRect()
    setPosition({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    })
  }

  return (
    <motion.div
      ref={divRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={{ y: -4 }}
      className={cn(
        'relative overflow-hidden rounded-2xl border border-stone-200 bg-white p-6',
        'transition-shadow duration-300',
        isHovered && 'shadow-2xl',
        className
      )}
    >
      {/* Glow effect */}
      <div
        className="pointer-events-none absolute -inset-px transition-opacity duration-300"
        style={{
          opacity: isHovered ? 1 : 0,
          background: `radial-gradient(400px circle at ${position.x}px ${position.y}px, ${glowColor}, transparent 50%)`,
        }}
      />
      
      {/* Border glow */}
      <div
        className="pointer-events-none absolute inset-0 rounded-2xl transition-opacity duration-300"
        style={{
          opacity: isHovered ? 1 : 0,
          background: `radial-gradient(400px circle at ${position.x}px ${position.y}px, ${glowColor}, transparent 50%)`,
          mask: 'linear-gradient(black, black) content-box, linear-gradient(black, black)',
          maskComposite: 'xor',
          WebkitMaskComposite: 'xor',
          padding: '1px',
        }}
      />

      <div className="relative z-10">{children}</div>
    </motion.div>
  )
}

interface FloatingCardProps {
  children: React.ReactNode
  className?: string
  delay?: number
}

export function FloatingCard({ children, className, delay = 0 }: FloatingCardProps) {
  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay, duration: 0.5, ease: 'easeOut' }}
      whileHover={{ y: -8, scale: 1.02 }}
      className={cn(
        'rounded-2xl border border-stone-200 bg-white p-6 shadow-lg',
        'hover:shadow-2xl transition-shadow duration-300',
        className
      )}
    >
      {children}
    </motion.div>
  )
}
