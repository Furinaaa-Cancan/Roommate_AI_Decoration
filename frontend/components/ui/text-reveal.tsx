'use client'

import { useRef } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import { cn } from '@/lib/utils/cn'

interface TextRevealProps {
  text: string
  className?: string
}

export function TextReveal({ text, className }: TextRevealProps) {
  const targetRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: targetRef,
    offset: ['start 0.9', 'start 0.25'],
  })

  const words = text.split(' ')

  return (
    <div ref={targetRef} className={cn('relative', className)}>
      <p className="flex flex-wrap text-2xl md:text-4xl lg:text-5xl font-bold text-stone-900/20">
        {words.map((word, i) => {
          const start = i / words.length
          const end = start + 1 / words.length
          return (
            <Word key={i} progress={scrollYProgress} range={[start, end]}>
              {word}
            </Word>
          )
        })}
      </p>
    </div>
  )
}

interface WordProps {
  children: string
  progress: any
  range: [number, number]
}

function Word({ children, progress, range }: WordProps) {
  const opacity = useTransform(progress, range, [0.2, 1])
  const color = useTransform(
    progress,
    range,
    ['rgb(28 25 23 / 0.2)', 'rgb(28 25 23 / 1)']
  )

  return (
    <motion.span
      style={{ opacity, color }}
      className="mr-3 mt-3"
    >
      {children}
    </motion.span>
  )
}

interface TypewriterProps {
  text: string
  className?: string
  speed?: number
}

export function Typewriter({ text, className, speed = 50 }: TypewriterProps) {
  return (
    <motion.span className={cn('inline-block', className)}>
      {text.split('').map((char, i) => (
        <motion.span
          key={i}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: i * (speed / 1000) }}
        >
          {char}
        </motion.span>
      ))}
    </motion.span>
  )
}

interface CountUpProps {
  end: number
  duration?: number
  suffix?: string
  prefix?: string
  className?: string
}

export function CountUp({ 
  end, 
  duration = 2, 
  suffix = '', 
  prefix = '',
  className 
}: CountUpProps) {
  return (
    <motion.span
      className={cn('tabular-nums', className)}
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
    >
      {prefix}
      <motion.span
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
      >
        {end.toLocaleString()}
      </motion.span>
      {suffix}
    </motion.span>
  )
}
