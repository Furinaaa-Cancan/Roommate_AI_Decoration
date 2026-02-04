'use client'

import { cn } from '@/lib/utils/cn'
import { motion } from 'framer-motion'

interface BentoGridProps {
  children: React.ReactNode
  className?: string
}

export function BentoGrid({ children, className }: BentoGridProps) {
  return (
    <div className={cn(
      "grid grid-cols-1 md:grid-cols-3 gap-4 max-w-7xl mx-auto",
      className
    )}>
      {children}
    </div>
  )
}

interface BentoCardProps {
  title: string
  description?: string
  icon?: React.ReactNode
  children?: React.ReactNode
  className?: string
  backgroundImage?: string
  span?: 'default' | 'wide' | 'tall' | 'large'
}

const spanClasses = {
  default: '',
  wide: 'md:col-span-2',
  tall: 'md:row-span-2',
  large: 'md:col-span-2 md:row-span-2',
}

export function BentoCard({ 
  title, 
  description, 
  icon, 
  children, 
  className,
  backgroundImage,
  span = 'default'
}: BentoCardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      transition={{ duration: 0.2 }}
      className={cn(
        "group relative overflow-hidden rounded-2xl border border-stone-200 bg-white p-6",
        "hover:shadow-xl hover:border-stone-300 transition-shadow duration-300",
        spanClasses[span],
        className
      )}
    >
      {backgroundImage && (
        <div 
          className="absolute inset-0 opacity-10 group-hover:opacity-20 transition-opacity"
          style={{ 
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
        />
      )}
      
      <div className="relative z-10">
        {icon && (
          <div className="mb-4 w-12 h-12 rounded-xl bg-stone-100 flex items-center justify-center text-stone-600 group-hover:bg-stone-800 group-hover:text-white transition-colors">
            {icon}
          </div>
        )}
        
        <h3 className="text-lg font-semibold text-stone-900 mb-2">{title}</h3>
        
        {description && (
          <p className="text-sm text-stone-600 leading-relaxed">{description}</p>
        )}
        
        {children}
      </div>

      {/* Gradient overlay on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-stone-900/0 to-stone-900/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
    </motion.div>
  )
}
