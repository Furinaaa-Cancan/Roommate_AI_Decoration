'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, X } from 'lucide-react'

const galleryItems = [
  {
    id: 1,
    before: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800',
    after: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800',
    style: '现代简约',
    room: '客厅'
  },
  {
    id: 2,
    before: 'https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=800',
    after: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800',
    style: '北欧风',
    room: '卧室'
  },
  {
    id: 3,
    before: 'https://images.unsplash.com/photo-1560185127-6ed189bf02f4?w=800',
    after: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800',
    style: '侘寂风',
    room: '书房'
  },
  {
    id: 4,
    before: 'https://images.unsplash.com/photo-1560448075-cbc16bb4af8e?w=800',
    after: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',
    style: '轻奢',
    room: '餐厅'
  },
  {
    id: 5,
    before: 'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=800',
    after: 'https://images.unsplash.com/photo-1600573472550-8090b5e0745e?w=800',
    style: '日式',
    room: '客厅'
  },
  {
    id: 6,
    before: 'https://images.unsplash.com/photo-1560449752-3fd4bdbe7df0?w=800',
    after: 'https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800',
    style: '工业风',
    room: '工作室'
  },
]

export default function GalleryPage() {
  const [selectedItem, setSelectedItem] = useState<typeof galleryItems[0] | null>(null)
  const [showBefore, setShowBefore] = useState(false)

  return (
    <div className="min-h-screen bg-brand-cream pt-20">
      {/* Hero */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-5xl font-serif font-bold text-brand-charcoal mb-6">
              作品展示
            </h1>
            <p className="text-lg text-brand-charcoal/60 leading-relaxed max-w-2xl mx-auto">
              浏览由 Roommate AI 生成的精美室内设计效果图，感受AI的设计魔力。
            </p>
          </motion.div>
        </div>
      </section>

      {/* Gallery Grid */}
      <section className="py-16 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {galleryItems.map((item, i) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: i * 0.1 }}
                viewport={{ once: true }}
                onClick={() => setSelectedItem(item)}
                className="group cursor-pointer"
              >
                <div className="relative aspect-[4/3] rounded-2xl overflow-hidden bg-white">
                  <img
                    src={item.after}
                    alt={item.style}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                  <div className="absolute bottom-0 left-0 right-0 p-4 translate-y-full group-hover:translate-y-0 transition-transform">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-1 bg-brand-terracotta text-white text-xs rounded-full">
                        {item.style}
                      </span>
                      <span className="px-2 py-1 bg-white/20 text-white text-xs rounded-full backdrop-blur">
                        {item.room}
                      </span>
                    </div>
                  </div>
                  <div className="absolute top-3 right-3">
                    <div className="w-8 h-8 bg-brand-terracotta rounded-full flex items-center justify-center">
                      <Sparkles className="w-4 h-4 text-white" />
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Lightbox */}
      {selectedItem && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-6"
          onClick={() => setSelectedItem(null)}
        >
          <button
            onClick={() => setSelectedItem(null)}
            className="absolute top-6 right-6 w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-white/20 transition-colors"
          >
            <X className="w-5 h-5 text-white" />
          </button>
          <div className="max-w-5xl w-full" onClick={(e) => e.stopPropagation()}>
            <div className="relative aspect-[16/10] rounded-2xl overflow-hidden">
              <img
                src={showBefore ? selectedItem.before : selectedItem.after}
                alt=""
                className="w-full h-full object-cover"
              />
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                <button
                  onClick={() => setShowBefore(false)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    !showBefore ? 'bg-brand-terracotta text-white' : 'bg-white/20 text-white hover:bg-white/30'
                  }`}
                >
                  效果图
                </button>
                <button
                  onClick={() => setShowBefore(true)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    showBefore ? 'bg-brand-terracotta text-white' : 'bg-white/20 text-white hover:bg-white/30'
                  }`}
                >
                  原图
                </button>
              </div>
            </div>
            <div className="mt-4 text-center">
              <span className="text-white/60 text-sm">{selectedItem.room} · {selectedItem.style}</span>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}
