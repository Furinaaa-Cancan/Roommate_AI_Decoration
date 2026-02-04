'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import { ArrowLeft, Filter, X, Download, ZoomIn, Heart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils/cn'
import { DESIGN_STYLES } from '@/lib/constants/styles'
import { ROOM_TYPES } from '@/lib/constants/rooms'

// Mock data for gallery
const mockGalleryItems = [
  {
    id: '1',
    imageUrl: 'https://file2.aitohumanize.com/file/4228ee00ad7040908b83e6dd9157db69.png',
    style: 'wabi_sabi',
    roomType: 'living_room',
    likes: 128,
    createdAt: '2026-01-15',
  },
  {
    id: '2',
    imageUrl: '/images/showcase/cream-bedroom.jpg',
    style: 'cream_style',
    roomType: 'bedroom',
    likes: 96,
    createdAt: '2026-01-14',
  },
  {
    id: '3',
    imageUrl: '/images/showcase/modern-kitchen.jpg',
    style: 'modern_luxury',
    roomType: 'kitchen',
    likes: 84,
    createdAt: '2026-01-13',
  },
  {
    id: '4',
    imageUrl: '/images/showcase/chinese-study.jpg',
    style: 'modern_chinese',
    roomType: 'study',
    likes: 72,
    createdAt: '2026-01-12',
  },
  {
    id: '5',
    imageUrl: '/images/showcase/nordic-dining.jpg',
    style: 'scandinavian',
    roomType: 'dining_room',
    likes: 65,
    createdAt: '2026-01-11',
  },
  {
    id: '6',
    imageUrl: '/images/showcase/industrial-loft.jpg',
    style: 'industrial',
    roomType: 'living_room',
    likes: 58,
    createdAt: '2026-01-10',
  },
]

export default function GalleryPage() {
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null)
  const [selectedRoom, setSelectedRoom] = useState<string | null>(null)
  const [selectedImage, setSelectedImage] = useState<typeof mockGalleryItems[0] | null>(null)
  const [showFilters, setShowFilters] = useState(false)

  const filteredItems = mockGalleryItems.filter((item) => {
    if (selectedStyle && item.style !== selectedStyle) return false
    if (selectedRoom && item.roomType !== selectedRoom) return false
    return true
  })

  const getStyleName = (id: string) => 
    DESIGN_STYLES.find(s => s.id === id)?.name || id

  const getRoomName = (id: string) => 
    ROOM_TYPES.find(r => r.id === id)?.name || id

  return (
    <div className="min-h-screen bg-stone-50">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-stone-200">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/" className="p-2 hover:bg-stone-100 rounded-lg transition-colors">
              <ArrowLeft className="w-5 h-5 text-stone-600" />
            </Link>
            <h1 className="font-semibold text-stone-800">作品展廊</h1>
          </div>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowFilters(!showFilters)}
            className={cn(showFilters && "bg-stone-100")}
          >
            <Filter className="w-4 h-4 mr-2" />
            筛选
            {(selectedStyle || selectedRoom) && (
              <span className="ml-2 px-1.5 py-0.5 bg-stone-800 text-white text-xs rounded">
                {[selectedStyle, selectedRoom].filter(Boolean).length}
              </span>
            )}
          </Button>
        </div>

        {/* Filter Panel */}
        <AnimatePresence>
          {showFilters && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden border-t border-stone-100"
            >
              <div className="max-w-7xl mx-auto px-6 py-4 space-y-4">
                {/* Style Filter */}
                <div>
                  <label className="text-sm font-medium text-stone-600 mb-2 block">风格</label>
                  <div className="flex flex-wrap gap-2">
                    {DESIGN_STYLES.map((style) => (
                      <button
                        key={style.id}
                        onClick={() => setSelectedStyle(
                          selectedStyle === style.id ? null : style.id
                        )}
                        className={cn(
                          "px-3 py-1.5 text-sm rounded-full border transition-colors",
                          selectedStyle === style.id
                            ? "bg-stone-800 text-white border-stone-800"
                            : "border-stone-300 hover:border-stone-400"
                        )}
                      >
                        {style.name}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Room Filter */}
                <div>
                  <label className="text-sm font-medium text-stone-600 mb-2 block">房间</label>
                  <div className="flex flex-wrap gap-2">
                    {ROOM_TYPES.map((room) => (
                      <button
                        key={room.id}
                        onClick={() => setSelectedRoom(
                          selectedRoom === room.id ? null : room.id
                        )}
                        className={cn(
                          "px-3 py-1.5 text-sm rounded-full border transition-colors",
                          selectedRoom === room.id
                            ? "bg-stone-800 text-white border-stone-800"
                            : "border-stone-300 hover:border-stone-400"
                        )}
                      >
                        {room.name}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Clear Filters */}
                {(selectedStyle || selectedRoom) && (
                  <button
                    onClick={() => {
                      setSelectedStyle(null)
                      setSelectedRoom(null)
                    }}
                    className="text-sm text-stone-500 hover:text-stone-700"
                  >
                    清除筛选
                  </button>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* Gallery Grid */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="columns-1 sm:columns-2 lg:columns-3 gap-4 space-y-4">
          {filteredItems.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="break-inside-avoid"
            >
              <div 
                className="group relative bg-white rounded-xl overflow-hidden border border-stone-200 hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedImage(item)}
              >
                <div className="aspect-[4/3] bg-stone-100">
                  <img
                    src={item.imageUrl}
                    alt={`${getStyleName(item.style)} ${getRoomName(item.roomType)}`}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect fill="%23e7e5e4" width="400" height="300"/><text fill="%2378716c" x="50%" y="50%" text-anchor="middle" dy=".3em" font-family="system-ui" font-size="14">示例图片</text></svg>'
                    }}
                  />
                </div>

                {/* Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="absolute bottom-0 left-0 right-0 p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-white font-medium">{getStyleName(item.style)}</p>
                        <p className="text-white/70 text-sm">{getRoomName(item.roomType)}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <button className="p-2 bg-white/20 hover:bg-white/30 rounded-full text-white transition-colors">
                          <Heart className="w-4 h-4" />
                        </button>
                        <button className="p-2 bg-white/20 hover:bg-white/30 rounded-full text-white transition-colors">
                          <ZoomIn className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Tags */}
                <div className="absolute top-3 left-3 flex gap-2">
                  <span className="px-2 py-1 bg-white/90 backdrop-blur-sm rounded text-xs font-medium text-stone-700">
                    {getStyleName(item.style)}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {filteredItems.length === 0 && (
          <div className="text-center py-20">
            <p className="text-stone-500">暂无符合条件的作品</p>
            <button
              onClick={() => {
                setSelectedStyle(null)
                setSelectedRoom(null)
              }}
              className="mt-4 text-stone-700 underline"
            >
              清除筛选
            </button>
          </div>
        )}
      </main>

      {/* Lightbox */}
      <AnimatePresence>
        {selectedImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
            onClick={() => setSelectedImage(null)}
          >
            <button
              className="absolute top-4 right-4 p-2 text-white/70 hover:text-white"
              onClick={() => setSelectedImage(null)}
            >
              <X className="w-6 h-6" />
            </button>

            <div className="max-w-5xl w-full" onClick={(e) => e.stopPropagation()}>
              <motion.img
                initial={{ scale: 0.9 }}
                animate={{ scale: 1 }}
                src={selectedImage.imageUrl}
                alt="放大预览"
                className="w-full rounded-lg"
              />
              <div className="mt-4 flex items-center justify-between text-white">
                <div>
                  <p className="font-medium text-lg">
                    {getStyleName(selectedImage.style)} · {getRoomName(selectedImage.roomType)}
                  </p>
                  <p className="text-white/60 text-sm">
                    {selectedImage.likes} 人喜欢
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button variant="secondary" size="sm">
                    <Heart className="w-4 h-4 mr-2" />
                    喜欢
                  </Button>
                  <Button size="sm">
                    <Download className="w-4 h-4 mr-2" />
                    下载
                  </Button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
