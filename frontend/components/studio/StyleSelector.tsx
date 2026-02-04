'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import { DESIGN_STYLES } from '@/lib/constants/styles'

interface StyleSelectorProps {
  value: string
  onChange: (styleId: string) => void
  className?: string
}

export function StyleSelector({ value, onChange, className }: StyleSelectorProps) {
  return (
    <div className={cn("space-y-3", className)}>
      <label className="text-sm font-medium text-stone-700">选择风格</label>
      <div className="grid grid-cols-2 gap-3">
        {DESIGN_STYLES.map((style) => (
          <motion.button
            key={style.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onChange(style.id)}
            className={cn(
              "relative p-4 rounded-xl border-2 text-left transition-all",
              value === style.id
                ? "border-stone-800 bg-stone-50"
                : "border-stone-200 hover:border-stone-300 bg-white"
            )}
          >
            {value === style.id && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="absolute top-2 right-2 w-5 h-5 bg-stone-800 rounded-full flex items-center justify-center"
              >
                <Check className="w-3 h-3 text-white" />
              </motion.div>
            )}
            <div className="flex items-center gap-3 mb-2">
              <div className="flex gap-1">
                {style.colors.map((color, i) => (
                  <div
                    key={i}
                    className="w-4 h-4 rounded-full border border-stone-200"
                    style={{ backgroundColor: color }}
                  />
                ))}
              </div>
            </div>
            <p className="font-medium text-stone-800">{style.name}</p>
            <p className="text-xs text-stone-500 mt-0.5">{style.nameEn}</p>
          </motion.button>
        ))}
      </div>
    </div>
  )
}
