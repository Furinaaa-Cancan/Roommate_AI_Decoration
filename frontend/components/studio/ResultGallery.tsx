'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Download, ZoomIn, X, ArrowLeftRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils/cn'

interface ResultGalleryProps {
  originalImage?: string | null
  generatedImages: string[]
  className?: string
}

export function ResultGallery({ 
  originalImage, 
  generatedImages,
  className 
}: ResultGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [showComparison, setShowComparison] = useState(false)
  const [comparisonPosition, setComparisonPosition] = useState(50)

  const handleDownload = async (url: string, filename: string) => {
    try {
      const response = await fetch(url)
      const blob = await response.blob()
      const downloadUrl = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = downloadUrl
      a.download = filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(downloadUrl)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  if (generatedImages.length === 0) {
    return (
      <div className={cn(
        "aspect-[4/3] rounded-xl bg-stone-100 flex items-center justify-center",
        className
      )}>
        <div className="text-center text-stone-400">
          <ZoomIn className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p className="text-sm">生成结果将在此显示</p>
        </div>
      </div>
    )
  }

  return (
    <>
      <div className={cn("space-y-4", className)}>
        {/* Main Preview */}
        <div className="relative aspect-[4/3] rounded-xl overflow-hidden bg-stone-100 group">
          <img
            src={generatedImages[0]}
            alt="生成结果"
            className="w-full h-full object-cover"
          />
          
          {/* Action Buttons */}
          <div className="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            {originalImage && (
              <Button
                size="icon"
                variant="secondary"
                className="bg-white/90 hover:bg-white"
                onClick={() => setShowComparison(true)}
              >
                <ArrowLeftRight className="w-4 h-4" />
              </Button>
            )}
            <Button
              size="icon"
              variant="secondary"
              className="bg-white/90 hover:bg-white"
              onClick={() => setSelectedImage(generatedImages[0])}
            >
              <ZoomIn className="w-4 h-4" />
            </Button>
            <Button
              size="icon"
              variant="secondary"
              className="bg-white/90 hover:bg-white"
              onClick={() => handleDownload(generatedImages[0], 'nanobanana-design-4k.png')}
            >
              <Download className="w-4 h-4" />
            </Button>
          </div>

          {/* 4K Badge */}
          <div className="absolute bottom-3 left-3 px-2 py-1 bg-black/60 rounded text-xs text-white font-medium">
            4K 超清
          </div>
        </div>

        {/* Thumbnails */}
        {generatedImages.length > 1 && (
          <div className="flex gap-2 overflow-x-auto pb-2">
            {generatedImages.map((img, i) => (
              <button
                key={i}
                onClick={() => setSelectedImage(img)}
                className="flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 border-stone-200 hover:border-stone-400 transition-colors"
              >
                <img src={img} alt={`结果 ${i + 1}`} className="w-full h-full object-cover" />
              </button>
            ))}
          </div>
        )}
      </div>

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
            <motion.img
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              src={selectedImage}
              alt="放大预览"
              className="max-w-full max-h-full object-contain rounded-lg"
              onClick={(e) => e.stopPropagation()}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Comparison Modal */}
      <AnimatePresence>
        {showComparison && originalImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
            onClick={() => setShowComparison(false)}
          >
            <button
              className="absolute top-4 right-4 p-2 text-white/70 hover:text-white"
              onClick={() => setShowComparison(false)}
            >
              <X className="w-6 h-6" />
            </button>
            
            <div 
              className="relative max-w-4xl w-full aspect-[4/3] rounded-lg overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              {/* After Image (Full) */}
              <img
                src={generatedImages[0]}
                alt="渲染后"
                className="absolute inset-0 w-full h-full object-cover"
              />
              
              {/* Before Image (Clipped) */}
              <div
                className="absolute inset-0 overflow-hidden"
                style={{ width: `${comparisonPosition}%` }}
              >
                <img
                  src={originalImage}
                  alt="原图"
                  className="absolute inset-0 w-full h-full object-cover"
                  style={{ width: `${100 / (comparisonPosition / 100)}%` }}
                />
              </div>
              
              {/* Slider */}
              <div
                className="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize"
                style={{ left: `${comparisonPosition}%` }}
              >
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-lg">
                  <ArrowLeftRight className="w-5 h-5 text-stone-600" />
                </div>
              </div>

              {/* Labels */}
              <div className="absolute top-4 left-4 px-3 py-1 bg-black/60 rounded text-sm text-white">
                原图
              </div>
              <div className="absolute top-4 right-4 px-3 py-1 bg-black/60 rounded text-sm text-white">
                AI渲染
              </div>
              
              {/* Range Input */}
              <input
                type="range"
                min="0"
                max="100"
                value={comparisonPosition}
                onChange={(e) => setComparisonPosition(Number(e.target.value))}
                className="absolute bottom-4 left-1/2 -translate-x-1/2 w-1/2 opacity-0 cursor-ew-resize"
                style={{ height: '100%', top: 0 }}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
