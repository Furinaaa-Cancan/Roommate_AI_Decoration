"use client"

import { motion } from "framer-motion"

export const GreekMeander = ({ className = "" }: { className?: string }) => (
  <svg viewBox="0 0 400 20" className={className} fill="none" stroke="currentColor" strokeWidth="1">
    {[0, 40, 80, 120, 160, 200, 240, 280, 320, 360].map((x, i) => (
      <path key={i} d={`M${x} 2 L${x+5} 2 L${x+5} 8 L${x+15} 8 L${x+15} 14 L${x+10} 14 L${x+10} 8 L${x} 8 Z`} />
    ))}
  </svg>
)

export const CorinthianColumn = ({ className = "", side = "left" }: { className?: string; side?: "left" | "right" }) => (
  <svg viewBox="0 0 60 600" className={className} fill="none" stroke="currentColor" strokeWidth="0.5">
    <rect x="10" y="20" width="40" height="8" rx="1" />
    <rect x="14" y="28" width="32" height="4" />
    <path d="M18 32 C18 32 12 40 18 48 C24 40 18 32 18 32" />
    <path d="M30 32 C30 32 24 40 30 48 C36 40 30 32 30 32" />
    <path d="M42 32 C42 32 36 40 42 48 C48 40 42 32 42 32" />
    <rect x="14" y="48" width="32" height="3" />
    {Array.from({ length: 20 }).map((_, i) => (
      <g key={i}>
        <path d={`M18 ${55 + i*26} L18 ${78 + i*26}`} />
        <path d={`M26 ${55 + i*26} L26 ${78 + i*26}`} strokeDasharray="2 3" />
        <path d={`M30 ${55 + i*26} L30 ${78 + i*26}`} />
        <path d={`M34 ${55 + i*26} L34 ${78 + i*26}`} strokeDasharray="2 3" />
        <path d={`M42 ${55 + i*26} L42 ${78 + i*26}`} />
      </g>
    ))}
    <rect x="14" y="575" width="32" height="4" />
    <rect x="10" y="579" width="40" height="10" rx="1" />
  </svg>
)

export const ClassicArch = ({ className = "" }: { className?: string }) => (
  <svg viewBox="0 0 300 400" className={className} fill="none" stroke="currentColor" strokeWidth="0.8">
    <path d="M50 120 L50 350 Q50 380 150 380 Q250 380 250 350 L250 120" />
    <path d="M60 120 L60 345 Q60 370 150 370 Q240 370 240 345 L240 120" />
    <path d="M70 120 L70 340 Q70 360 150 360 Q230 360 230 340 L230 120" />
    <circle cx="150" cy="220" r="50" />
    <circle cx="150" cy="220" r="42" />
    <circle cx="150" cy="220" r="30" />
    <path d="M120 220 L180 220 M150 190 L150 250" />
    <path d="M130 200 L170 240 M170 200 L130 240" strokeDasharray="2 2" />
    <path d="M140 125 L150 105 L160 125 Z" />
    <rect x="135" y="125" width="30" height="10" />
    <path d="M30 100 L150 60 L270 100 L30 100" />
    <path d="M50 98 L150 65 L250 98" />
    <circle cx="150" cy="82" r="8" />
  </svg>
)

export const FloatingParticles = ({ count = 20 }: { count?: number }) => (
  <div className="absolute inset-0 overflow-hidden pointer-events-none">
    {Array.from({ length: count }).map((_, i) => (
      <motion.div
        key={i}
        className="absolute w-1 h-1 bg-brand-terracotta/20 rounded-full"
        style={{
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
        }}
        animate={{
          y: [0, -30, 0],
          opacity: [0.2, 0.6, 0.2],
          scale: [1, 1.5, 1],
        }}
        transition={{
          duration: 4 + Math.random() * 4,
          repeat: Infinity,
          delay: Math.random() * 4,
          ease: "easeInOut",
        }}
      />
    ))}
  </div>
)

export const VitruvianBackground = ({ className = "" }: { className?: string }) => (
  <motion.div
    className={`absolute inset-0 pointer-events-none ${className}`}
    animate={{
      rotate: [0, 0.5, -0.5, 0],
      scale: [1, 1.02, 1],
    }}
    transition={{
      duration: 20,
      repeat: Infinity,
      ease: "easeInOut",
    }}
    style={{
      backgroundImage: `url("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg/800px-Da_Vinci_Vitruve_Luc_Viatour.jpg")`,
      backgroundSize: "contain",
      backgroundRepeat: "no-repeat",
      backgroundPosition: "center",
      opacity: 0.06,
      filter: "sepia(20%) contrast(1.1)",
    }}
  />
)

export const CreationBackground = ({ className = "" }: { className?: string }) => (
  <motion.div
    className={`absolute inset-0 pointer-events-none ${className}`}
    animate={{
      scale: [1, 1.03, 1],
      x: [0, 5, -5, 0],
    }}
    transition={{
      duration: 25,
      repeat: Infinity,
      ease: "easeInOut",
    }}
    style={{
      backgroundImage: `url("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Michelangelo_-_Creation_of_Adam_%28cropped%29.jpg/1280px-Michelangelo_-_Creation_of_Adam_%28cropped%29.jpg")`,
      backgroundSize: "cover",
      backgroundPosition: "center",
      opacity: 0.12,
      filter: "sepia(15%) contrast(1.1) brightness(1.05)",
    }}
  />
)

export const staggerContainer = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
}

export const staggerItem = {
  hidden: { opacity: 0, y: 30 },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 12,
    },
  },
}

export const fadeInUp = {
  hidden: { opacity: 0, y: 40 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.8,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
}

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.6,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
}

export const slideInLeft = {
  hidden: { opacity: 0, x: -60 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.8,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
}

export const slideInRight = {
  hidden: { opacity: 0, x: 60 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.8,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
}
