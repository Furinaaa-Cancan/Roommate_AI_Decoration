'use client'

import React, { useState, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Upload, Image as ImageIcon, Sparkles, ArrowRight, Loader2, 
  X, Download, Trash2, ChevronRight, Layers, MousePointer2,
  Paintbrush, RotateCcw, Settings, Zap, Grid3X3
} from 'lucide-react'
import SegmentableImage from './SegmentableImage'

interface DesignImage {
  id: string
  url: string
  base64?: string
  type: 'original' | 'generated'
  style?: string
  name: string
}

interface SegmentedObject {
  label: string
  label_zh: string
  mask_url: string
  bbox: number[]
  confidence: number
}

const designStyles = [
  { id: 'nanobanana', name: '奶油暖阳', color: 'from-amber-400 to-orange-400' },
  { id: 'modern', name: '现代简约', color: 'from-gray-400 to-slate-500' },
  { id: 'nordic', name: '北欧清新', color: 'from-sky-400 to-blue-400' },
  { id: 'wabi_sabi', name: '侘寂美学', color: 'from-stone-400 to-neutral-500' },
  { id: 'new_chinese', name: '新中式', color: 'from-red-400 to-rose-500' },
  { id: 'luxury', name: '轻奢格调', color: 'from-yellow-400 to-amber-500' },
  { id: 'industrial', name: '工业风', color: 'from-zinc-400 to-gray-600' },
  { id: 'japanese', name: '日式禅意', color: 'from-green-400 to-emerald-500' },
]

// 文件转 base64
async function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = error => reject(error)
  })
}

export default function DesignStudio() {
  // 状态
  const [images, setImages] = useState<DesignImage[]>([])
  const [selectedImage, setSelectedImage] = useState<DesignImage | null>(null)
  const [selectedStyle, setSelectedStyle] = useState(0)
  const [selectedSegment, setSelectedSegment] = useState<SegmentedObject | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatingProgress, setGeneratingProgress] = useState(0)
  const [activeTab, setActiveTab] = useState<'style' | 'segment'>('style')
  const [prompt, setPrompt] = useState('')
  
  const fileInputRef = useRef<HTMLInputElement>(null)

  // 处理图片上传
  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const url = URL.createObjectURL(file)
      const base64 = await fileToBase64(file)
      const newImage: DesignImage = {
        id: Date.now().toString(),
        url,
        base64,
        type: 'original',
        name: file.name
      }
      setImages(prev => [...prev, newImage])
      setSelectedImage(newImage)
    }
  }

  // 处理拖拽上传
  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file)
      const base64 = await fileToBase64(file)
      const newImage: DesignImage = {
        id: Date.now().toString(),
        url,
        base64,
        type: 'original',
        name: file.name
      }
      setImages(prev => [...prev, newImage])
      setSelectedImage(newImage)
    }
  }

  // 生成效果图
  const handleGenerate = async () => {
    const originalImage = images.find(img => img.type === 'original')
    if (!originalImage?.base64) return

    setIsGenerating(true)
    setGeneratingProgress(0)

    const progressInterval = setInterval(() => {
      setGeneratingProgress(prev => prev >= 90 ? prev : prev + Math.random() * 10)
    }, 500)

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image: originalImage.base64,
          style: designStyles[selectedStyle].id,
          prompt: prompt,
        }),
      })

      const result = await response.json()
      clearInterval(progressInterval)
      setGeneratingProgress(100)

      if (result.success && result.images?.length > 0) {
        const generatedImage: DesignImage = {
          id: Date.now().toString(),
          url: result.images[0],
          type: 'generated',
          style: designStyles[selectedStyle].name,
          name: `${designStyles[selectedStyle].name}_效果图.jpg`
        }
        setImages(prev => [...prev, generatedImage])
        setSelectedImage(generatedImage)
      } else {
        alert(`生成失败: ${result.error || '未知错误'}`)
      }
    } catch (error) {
      clearInterval(progressInterval)
      alert('网络错误，请检查后端服务')
    } finally {
      setIsGenerating(false)
      setGeneratingProgress(0)
    }
  }

  // 删除图片
  const handleDeleteImage = (id: string) => {
    setImages(prev => prev.filter(img => img.id !== id))
    if (selectedImage?.id === id) {
      setSelectedImage(images.length > 1 ? images[images.length - 2] : null)
    }
  }

  // 处理分割选择
  const handleSegmentSelect = (segment: SegmentedObject, maskUrl: string) => {
    setSelectedSegment(segment)
    console.log('Selected segment:', segment, 'Mask:', maskUrl)
  }

  const hasOriginalImage = images.some(img => img.type === 'original')

  return (
    <div className="h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
      {/* 隐藏的文件输入 */}
      <input 
        type="file" 
        ref={fileInputRef}
        onChange={handleImageUpload}
        accept="image/*"
        className="hidden"
      />

      {/* 顶部导航 */}
      <header className="h-14 px-4 flex items-center justify-between bg-white border-b border-gray-200 shrink-0">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-terracotta to-orange-500 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-gray-900">Roommate Studio</span>
          </div>
          <div className="h-6 w-px bg-gray-200" />
          <span className="text-sm text-gray-500">AI 室内设计工作台</span>
        </div>

        <div className="flex items-center gap-3">
          {images.length > 0 && (
            <span className="text-xs text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full">
              {images.length} 张图片
            </span>
          )}
          <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <Settings className="w-5 h-5 text-gray-500" />
          </button>
        </div>
      </header>

      {/* 主内容区 */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* 左侧 - 图库面板 */}
        <aside className="w-20 bg-white border-r border-gray-200 flex flex-col shrink-0">
          <div className="p-3 border-b border-gray-100">
            <p className="text-[10px] font-medium text-gray-400 text-center uppercase tracking-wider">图库</p>
          </div>
          
          <div className="flex-1 overflow-y-auto p-2 space-y-2">
            {/* 上传按钮 */}
            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full aspect-square rounded-xl bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-dashed border-gray-200 flex items-center justify-center hover:border-brand-terracotta hover:from-orange-50 hover:to-amber-50 transition-all group"
            >
              <Upload className="w-5 h-5 text-gray-300 group-hover:text-brand-terracotta transition-colors" />
            </button>

            {/* 图片列表 */}
            {images.map((img) => (
              <div
                key={img.id}
                onClick={() => setSelectedImage(img)}
                className={`relative aspect-square rounded-xl overflow-hidden cursor-pointer transition-all group ${
                  selectedImage?.id === img.id
                    ? 'ring-2 ring-brand-terracotta ring-offset-2'
                    : 'hover:ring-2 hover:ring-gray-300'
                }`}
              >
                <img src={img.url} alt="" className="w-full h-full object-cover" />
                
                {/* 类型标识 */}
                <div className={`absolute bottom-0 inset-x-0 py-0.5 text-center text-[8px] font-medium ${
                  img.type === 'generated' 
                    ? 'bg-brand-terracotta text-white' 
                    : 'bg-gray-900/70 text-white'
                }`}>
                  {img.type === 'generated' ? '效果图' : '原图'}
                </div>

                {/* 删除按钮 */}
                <button
                  onClick={(e) => { e.stopPropagation(); handleDeleteImage(img.id) }}
                  className="absolute top-1 right-1 w-5 h-5 bg-black/50 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-500"
                >
                  <X className="w-3 h-3 text-white" />
                </button>
              </div>
            ))}
          </div>
        </aside>

        {/* 中间 - 画布区 */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* 工具栏 */}
          <div className="h-12 px-4 flex items-center justify-between bg-white border-b border-gray-100 shrink-0">
            <div className="flex items-center gap-1">
              <button
                onClick={() => setActiveTab('style')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                  activeTab === 'style'
                    ? 'bg-brand-terracotta text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Sparkles className="w-4 h-4" />
                整体风格
              </button>
              <button
                onClick={() => setActiveTab('segment')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                  activeTab === 'segment'
                    ? 'bg-brand-terracotta text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Layers className="w-4 h-4" />
                局部替换
              </button>
            </div>

            <div className="flex items-center gap-2">
              {selectedImage && (
                <button className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-all">
                  <Download className="w-4 h-4" />
                  导出
                </button>
              )}
            </div>
          </div>

          {/* 画布 */}
          <div className="flex-1 p-6 overflow-hidden">
            <div
              className="w-full h-full bg-white rounded-2xl shadow-sm border border-gray-200 flex items-center justify-center overflow-hidden relative"
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
            >
              {/* 生成中遮罩 */}
              <AnimatePresence>
                {isGenerating && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="absolute inset-0 bg-white/95 backdrop-blur-sm flex flex-col items-center justify-center z-20"
                  >
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-terracotta to-orange-500 flex items-center justify-center mb-4 shadow-lg">
                      <Loader2 className="w-8 h-8 text-white animate-spin" />
                    </div>
                    <p className="text-lg font-medium text-gray-900 mb-2">
                      正在生成 {designStyles[selectedStyle].name} 效果图
                    </p>
                    <div className="w-64 h-2 bg-gray-100 rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-gradient-to-r from-brand-terracotta to-orange-400"
                        initial={{ width: 0 }}
                        animate={{ width: `${generatingProgress}%` }}
                      />
                    </div>
                    <p className="text-sm text-gray-500 mt-2">{Math.round(generatingProgress)}%</p>
                  </motion.div>
                )}
              </AnimatePresence>

              {selectedImage ? (
                activeTab === 'segment' ? (
                  <SegmentableImage
                    imageUrl={selectedImage.url}
                    imageBase64={selectedImage.base64}
                    onSegmentSelect={handleSegmentSelect}
                    className="w-full h-full"
                  />
                ) : (
                  <div className="w-full h-full p-4">
                    <img
                      src={selectedImage.url}
                      alt=""
                      className="w-full h-full object-contain rounded-xl"
                    />
                    {/* 图片信息 */}
                    <div className="absolute bottom-6 left-6 right-6 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className={`px-3 py-1.5 rounded-full text-xs font-medium ${
                          selectedImage.type === 'generated'
                            ? 'bg-brand-terracotta text-white'
                            : 'bg-gray-900/80 text-white'
                        }`}>
                          {selectedImage.type === 'generated' ? `${selectedImage.style} · AI生成` : '毛坯原图'}
                        </span>
                      </div>
                      <span className="text-xs text-gray-500 bg-white/90 backdrop-blur px-3 py-1.5 rounded-full">
                        {selectedImage.name}
                      </span>
                    </div>
                  </div>
                )
              ) : (
                <div
                  onClick={() => fileInputRef.current?.click()}
                  className="text-center cursor-pointer group p-8"
                >
                  <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-gray-50 to-gray-100 group-hover:from-orange-50 group-hover:to-amber-50 flex items-center justify-center mx-auto mb-6 transition-all border-2 border-dashed border-gray-200 group-hover:border-brand-terracotta">
                    <ImageIcon className="w-10 h-10 text-gray-300 group-hover:text-brand-terracotta transition-colors" />
                  </div>
                  <p className="text-lg font-medium text-gray-700 mb-2">上传毛坯房照片</p>
                  <p className="text-sm text-gray-400 mb-6">点击或拖拽图片到此处</p>
                  <div className="flex items-center justify-center gap-3">
                    <button className="px-5 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-xl hover:bg-brand-terracotta transition-colors">
                      选择文件
                    </button>
                    <button
                      onClick={(e) => e.stopPropagation()}
                      className="px-5 py-2.5 bg-gray-100 text-gray-700 text-sm font-medium rounded-xl hover:bg-gray-200 transition-colors"
                    >
                      使用示例
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>

        {/* 右侧 - 控制面板 */}
        <aside className="w-80 bg-white border-l border-gray-200 flex flex-col shrink-0">
          {/* AI 助手 */}
          <div className="p-4 border-b border-gray-100">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-terracotta to-orange-500 flex items-center justify-center shadow-sm">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-900">AI 设计助手</p>
                <p className="text-xs text-gray-500">
                  {hasOriginalImage ? '已就绪，选择风格开始生成' : '请先上传毛坯房照片'}
                </p>
              </div>
            </div>
          </div>

          {activeTab === 'style' ? (
            <>
              {/* 风格选择 */}
              <div className="p-4 border-b border-gray-100">
                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">设计风格</p>
                <div className="grid grid-cols-2 gap-2">
                  {designStyles.map((style, i) => (
                    <button
                      key={style.id}
                      onClick={() => setSelectedStyle(i)}
                      className={`relative p-3 rounded-xl text-left transition-all ${
                        selectedStyle === i
                          ? 'bg-gradient-to-br ' + style.color + ' text-white shadow-md'
                          : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <span className="text-sm font-medium">{style.name}</span>
                      {selectedStyle === i && (
                        <motion.div
                          layoutId="selected-style"
                          className="absolute top-2 right-2 w-2 h-2 bg-white rounded-full"
                        />
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* 效果描述 */}
              <div className="p-4 flex-1">
                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">效果描述（可选）</p>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="描述你想要的效果，如：明亮的客厅，落地窗，木质地板..."
                  rows={4}
                  className="w-full p-3 text-sm text-gray-700 placeholder:text-gray-400 bg-gray-50 rounded-xl border border-gray-200 focus:outline-none focus:border-brand-terracotta focus:ring-1 focus:ring-brand-terracotta/20 resize-none transition-all"
                />
              </div>
            </>
          ) : (
            /* 局部替换面板 */
            <div className="p-4 flex-1">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">局部替换</p>
              
              {selectedSegment ? (
                <div className="space-y-4">
                  <div className="p-3 bg-brand-terracotta/10 rounded-xl">
                    <p className="text-sm font-medium text-brand-terracotta mb-1">
                      已选择: {selectedSegment.label_zh}
                    </p>
                    <p className="text-xs text-gray-500">选择替换风格后点击替换</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2">
                    {['现代简约', '北欧风', '轻奢', '日式', '工业风', '新中式'].map((style) => (
                      <button
                        key={style}
                        className="p-2.5 text-sm font-medium bg-gray-50 hover:bg-brand-terracotta hover:text-white rounded-xl transition-all"
                      >
                        {style}
                      </button>
                    ))}
                  </div>
                  
                  <button className="w-full py-3 bg-brand-terracotta text-white font-medium rounded-xl hover:bg-gray-900 transition-colors">
                    替换选中区域
                  </button>
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="w-16 h-16 rounded-2xl bg-gray-100 flex items-center justify-center mx-auto mb-4">
                    <MousePointer2 className="w-8 h-8 text-gray-300" />
                  </div>
                  <p className="text-sm text-gray-500 mb-2">点击图片中的家具</p>
                  <p className="text-xs text-gray-400">或使用"识别家具"自动检测</p>
                </div>
              )}
            </div>
          )}

          {/* 生成按钮 */}
          <div className="p-4 border-t border-gray-100">
            <button
              onClick={handleGenerate}
              disabled={!hasOriginalImage || isGenerating}
              className="w-full py-3.5 bg-gradient-to-r from-gray-900 to-gray-800 text-white font-semibold rounded-xl hover:from-brand-terracotta hover:to-orange-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-gray-900/20"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  生成中...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  {activeTab === 'style' ? '生成效果图' : '替换选中区域'}
                </>
              )}
            </button>
            
            <div className="flex items-center justify-center gap-4 mt-3 text-xs text-gray-400">
              <span>约 30 秒</span>
              <span>•</span>
              <span>4K 输出</span>
              <span>•</span>
              <span>首张免费</span>
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}
