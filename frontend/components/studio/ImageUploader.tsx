'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, Image as ImageIcon } from 'lucide-react'
import { cn } from '@/lib/utils/cn'

interface ImageUploaderProps {
  onImageSelect: (file: File, preview: string) => void
  currentImage?: string | null
  onClear?: () => void
  className?: string
}

export function ImageUploader({ 
  onImageSelect, 
  currentImage, 
  onClear,
  className 
}: ImageUploaderProps) {
  const [isDragActive, setIsDragActive] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      const preview = URL.createObjectURL(file)
      onImageSelect(file, preview)
    }
  }, [onImageSelect])

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp']
    },
    maxFiles: 1,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
  })

  if (currentImage) {
    return (
      <div className={cn("relative group", className)}>
        <div className="aspect-[4/3] rounded-xl overflow-hidden bg-stone-100">
          <img 
            src={currentImage} 
            alt="上传的图片" 
            className="w-full h-full object-cover"
          />
        </div>
        {onClear && (
          <button
            onClick={onClear}
            className="absolute top-3 right-3 p-2 bg-black/50 hover:bg-black/70 rounded-full text-white opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <X className="w-4 h-4" />
          </button>
        )}
        <div className="absolute bottom-3 left-3 right-3">
          <div {...getRootProps()} className="cursor-pointer">
            <input {...getInputProps()} />
            <button className="w-full py-2 bg-white/90 hover:bg-white rounded-lg text-sm font-medium text-stone-700 transition-colors">
              更换图片
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div
      {...getRootProps()}
      className={cn(
        "relative aspect-[4/3] rounded-xl border-2 border-dashed transition-all cursor-pointer",
        isDragActive 
          ? "border-stone-400 bg-stone-100" 
          : "border-stone-300 hover:border-stone-400 bg-stone-50 hover:bg-stone-100",
        className
      )}
    >
      <input {...getInputProps()} />
      <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
        <div className={cn(
          "w-16 h-16 rounded-2xl flex items-center justify-center mb-4 transition-colors",
          isDragActive ? "bg-stone-200" : "bg-stone-100"
        )}>
          {isDragActive ? (
            <ImageIcon className="w-8 h-8 text-stone-500" />
          ) : (
            <Upload className="w-8 h-8 text-stone-400" />
          )}
        </div>
        <p className="text-stone-700 font-medium mb-1">
          {isDragActive ? "松开以上传" : "拖拽或点击上传"}
        </p>
        <p className="text-sm text-stone-500">
          支持 PNG、JPG、WEBP 格式
        </p>
      </div>
    </div>
  )
}
