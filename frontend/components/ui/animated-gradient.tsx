'use client'

import { cn } from '@/lib/utils/cn'

interface AnimatedGradientProps {
  children: React.ReactNode
  className?: string
}

export function AnimatedGradient({ children, className }: AnimatedGradientProps) {
  return (
    <div className={cn("relative group", className)}>
      <div className="absolute -inset-0.5 bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 rounded-xl blur opacity-30 group-hover:opacity-60 transition duration-1000 group-hover:duration-200 animate-gradient-xy" />
      <div className="relative">{children}</div>
    </div>
  )
}

interface GradientTextProps {
  children: React.ReactNode
  className?: string
  from?: string
  via?: string
  to?: string
}

export function GradientText({ 
  children, 
  className,
  from = "from-stone-900",
  via = "via-stone-600", 
  to = "to-stone-400"
}: GradientTextProps) {
  return (
    <span className={cn(
      "bg-gradient-to-r bg-clip-text text-transparent",
      from, via, to,
      className
    )}>
      {children}
    </span>
  )
}

interface ShimmerButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  shimmerColor?: string
  shimmerSize?: string
  borderRadius?: string
  shimmerDuration?: string
  background?: string
  children: React.ReactNode
}

export function ShimmerButton({
  shimmerColor = "#ffffff",
  shimmerSize = "0.1em",
  borderRadius = "0.75rem",
  shimmerDuration = "2s",
  background = "linear-gradient(110deg,#1c1917,45%,#292524,55%,#1c1917)",
  className,
  children,
  ...props
}: ShimmerButtonProps) {
  return (
    <button
      style={{
        "--shimmer-color": shimmerColor,
        "--shimmer-size": shimmerSize,
        "--border-radius": borderRadius,
        "--shimmer-duration": shimmerDuration,
        "--background": background,
      } as React.CSSProperties}
      className={cn(
        "group relative overflow-hidden whitespace-nowrap px-6 py-3 text-white",
        "[background:var(--background)]",
        "rounded-[var(--border-radius)]",
        "transition-all duration-300 hover:scale-105 hover:shadow-[0_0_40px_8px_rgba(0,0,0,0.1)]",
        className
      )}
      {...props}
    >
      <div className="absolute inset-0 overflow-hidden rounded-[var(--border-radius)]">
        <div className="absolute inset-[-100%] animate-[shimmer_var(--shimmer-duration)_linear_infinite] bg-gradient-to-r from-transparent via-[var(--shimmer-color)]/10 to-transparent" />
      </div>
      <span className="relative z-10 flex items-center justify-center gap-2 font-medium">
        {children}
      </span>
    </button>
  )
}
