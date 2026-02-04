'use client'

import { motion } from 'framer-motion'
import { 
  Sofa, Bed, UtensilsCrossed, CookingPot, 
  Bath, BookOpen, Sun, DoorOpen 
} from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import { ROOM_TYPES } from '@/lib/constants/rooms'

const iconMap: Record<string, React.ElementType> = {
  Sofa,
  Bed,
  UtensilsCrossed,
  CookingPot,
  Bath,
  BookOpen,
  Sun,
  DoorOpen,
}

interface RoomTypeSelectorProps {
  value: string
  onChange: (roomId: string) => void
  className?: string
}

export function RoomTypeSelector({ value, onChange, className }: RoomTypeSelectorProps) {
  return (
    <div className={cn("space-y-3", className)}>
      <label className="text-sm font-medium text-stone-700">房间类型</label>
      <div className="grid grid-cols-4 gap-2">
        {ROOM_TYPES.map((room) => {
          const Icon = iconMap[room.icon] || Sofa
          const isSelected = value === room.id
          
          return (
            <motion.button
              key={room.id}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onChange(room.id)}
              className={cn(
                "flex flex-col items-center gap-2 p-3 rounded-xl border-2 transition-all",
                isSelected
                  ? "border-stone-800 bg-stone-800 text-white"
                  : "border-stone-200 hover:border-stone-300 bg-white text-stone-600 hover:text-stone-800"
              )}
            >
              <Icon className="w-5 h-5" />
              <span className="text-xs font-medium">{room.name}</span>
            </motion.button>
          )
        })}
      </div>
    </div>
  )
}
