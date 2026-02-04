'use client'

import React, { useState, useRef, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Loader2, Layers, X, RotateCcw, Sparkles } from 'lucide-react'

interface SegmentedObject {
  label: string
  label_zh: string
  mask_url: string  // 彩色 mask（用于可视化）
  inpaint_mask_url?: string  // 黑白 mask URL（用于 inpaint）
  inpaint_mask_base64?: string  // 黑白 mask base64（直接传递给 API）
  bbox: number[]
  confidence: number
}

interface SegmentableImageProps {
  imageUrl: string
  imageBase64?: string  // 用于 API 调用
  cachedSegments?: SegmentedObject[]  // 缓存的识别结果
  onSegmentSelect?: (segment: SegmentedObject, maskUrl: string) => void
  onSegmentsLoaded?: (segments: SegmentedObject[]) => void  // 识别完成回调
  onPointClick?: (x: number, y: number) => void
  className?: string
}

export default function SegmentableImage({
  imageUrl,
  imageBase64,
  cachedSegments,
  onSegmentSelect,
  onSegmentsLoaded,
  onPointClick,
  className = ''
}: SegmentableImageProps) {
  const [segments, setSegments] = useState<SegmentedObject[]>([])
  const [selectedSegments, setSelectedSegments] = useState<SegmentedObject[]>([])  // 支持多选
  const [isLoading, setIsLoading] = useState(false)
  const [isSegmented, setIsSegmented] = useState(false)
  
  // 如果有缓存的识别结果，直接使用
  useEffect(() => {
    if (cachedSegments && cachedSegments.length > 0) {
      console.log('[SegmentableImage] 使用缓存的识别结果:', cachedSegments.length, '个物体')
      setSegments(cachedSegments)
      setIsSegmented(true)
      // 保留已选择的物品（如果仍在缓存中）
      setSelectedSegments(prev => {
        const cachedKeys = new Set(cachedSegments.map(s => `${s.label}-${s.bbox?.join(',')}`))
        return prev.filter(s => cachedKeys.has(`${s.label}-${s.bbox?.join(',')}`))
      })
    } else {
      // 切换到新图片时重置状态
      console.log('[SegmentableImage] 无缓存，重置状态')
      setSegments([])
      setSelectedSegments([])
      setIsSegmented(false)
    }
  }, [cachedSegments, imageUrl])
  const [hoveredSegment, setHoveredSegment] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loadingProgress, setLoadingProgress] = useState(0)
  const [loadingStage, setLoadingStage] = useState('')
  
  const containerRef = useRef<HTMLDivElement>(null)
  const imageRef = useRef<HTMLImageElement>(null)

  // 自动分割图片
  const segmentImage = useCallback(async () => {
    if (!imageUrl || isLoading) return
    
    setIsLoading(true)
    setError(null)
    setLoadingProgress(0)
    setLoadingStage('正在加载模型...')
    
    // 模拟进度动画 - 持续增长不卡住
    const progressInterval = setInterval(() => {
      setLoadingProgress(prev => {
        if (prev < 30) {
          setLoadingStage('正在准备智能识别...')
          return prev + 3
        } else if (prev < 60) {
          setLoadingStage('正在分析图片内容...')
          return prev + 2
        } else if (prev < 85) {
          setLoadingStage('正在识别家具物品...')
          return prev + 1
        } else if (prev < 98) {
          setLoadingStage('即将完成...')
          return prev + 0.3
        }
        return Math.min(prev + 0.1, 99) // 最多到99%，等待API返回
      })
    }, 200)
    
    try {
      // 使用 base64 或公开 URL
      const requestBody = imageBase64 
        ? { image_base64: imageBase64 }
        : { image_url: imageUrl }
      
      const response = await fetch('/api/segment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      })
      
      const data = await response.json()
      
      clearInterval(progressInterval)
      console.log('分割API返回:', data.success, '物体数:', data.objects?.length)
      
      if (data.success && data.objects) {
        setLoadingProgress(100)
        setLoadingStage(`识别完成！发现 ${data.objects.length} 个物品`)
        await new Promise(r => setTimeout(r, 500)) // 短暂显示完成状态
        console.log('设置segments:', data.objects.length, '个物体')
        setSegments(data.objects)
        setIsSegmented(true)
        // 回调通知父组件缓存结果
        onSegmentsLoaded?.(data.objects)
      } else {
        setError(data.error || '分割服务暂不可用')
      }
    } catch (err) {
      clearInterval(progressInterval)
      setError('识别服务暂时不可用')
      console.error('Segment error:', err)
    } finally {
      setIsLoading(false)
      setLoadingProgress(0)
    }
  }, [imageUrl, imageBase64, isLoading])

  // 选择/取消选择分割区域 - 支持多选
  const handleSegmentClick = (segment: SegmentedObject) => {
    const segmentKey = `${segment.label}-${segment.bbox?.join(',')}`
    const isAlreadySelected = selectedSegments.some(
      s => `${s.label}-${s.bbox?.join(',')}` === segmentKey
    )
    
    if (isAlreadySelected) {
      // 取消选择
      setSelectedSegments(prev => prev.filter(
        s => `${s.label}-${s.bbox?.join(',')}` !== segmentKey
      ))
    } else {
      // 添加选择
      setSelectedSegments(prev => [...prev, segment])
    }
    onSegmentSelect?.(segment, segment.mask_url)
  }

  // 重置
  const handleReset = () => {
    setSegments([])
    setSelectedSegments([])
    setIsSegmented(false)
    setError(null)
  }

  return (
    <div className={`relative flex items-center justify-center ${className}`} ref={containerRef}>
      {/* 工具栏 */}
      <div className="absolute top-3 left-3 z-20 flex items-center gap-2">
        {!isSegmented ? (
          <button
            onClick={segmentImage}
            disabled={isLoading}
            className="flex items-center gap-2 px-3 py-2 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg text-sm font-medium text-gray-700 hover:bg-white transition-all disabled:opacity-50"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Layers className="w-4 h-4" />
            )}
            {isLoading ? '分析中...' : '识别家具'}
          </button>
        ) : (
          <button
            onClick={handleReset}
            className="flex items-center gap-1.5 px-3 py-2 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg text-sm font-medium text-gray-600 hover:bg-white transition-all"
          >
            <RotateCcw className="w-4 h-4" />
            重新识别
          </button>
        )}
      </div>

      {/* 图片容器 */}
      <div className="relative overflow-hidden rounded-xl">
        <img
          ref={imageRef}
          src={imageUrl}
          alt=""
          className="w-full h-full object-contain"
        />
        
        {/* Mask 蒙版叠加层 - 只显示选中或悬停的 */}
        <AnimatePresence>
          {isSegmented && segments.map((segment, index) => {
            const segmentKey = `${segment.label}-${segment.bbox?.join(',')}`
            const isSelected = selectedSegments.some(s => `${s.label}-${s.bbox?.join(',')}` === segmentKey)
            const isHovered = hoveredSegment === `${segment.label}-${index}`
            const shouldShow = isSelected || isHovered
            
            return (
            <motion.div
              key={`${segment.label}-${index}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 pointer-events-none"
            >
              {/* 彩色半透明 mask - 悬停/选中时显示 */}
              {segment.mask_url && (
                <>
                  {/* 显示的 mask 图片 */}
                  <img
                    src={segment.mask_url}
                    alt=""
                    className="absolute inset-0 w-full h-full object-contain pointer-events-none"
                    style={{
                      opacity: shouldShow ? 0.7 : 0,
                      transition: 'opacity 0.15s ease-out',
                    }}
                  />
                  {/* 透明的可点击区域 - 基于 bbox */}
                  {segment.bbox?.length === 4 && (
                    <div
                      className="absolute cursor-pointer pointer-events-auto"
                      style={{
                        left: `${(segment.bbox[0] / (imageRef.current?.naturalWidth || 1)) * 100}%`,
                        top: `${(segment.bbox[1] / (imageRef.current?.naturalHeight || 1)) * 100}%`,
                        width: `${((segment.bbox[2] - segment.bbox[0]) / (imageRef.current?.naturalWidth || 1)) * 100}%`,
                        height: `${((segment.bbox[3] - segment.bbox[1]) / (imageRef.current?.naturalHeight || 1)) * 100}%`,
                      }}
                      onClick={(e) => {
                        e.stopPropagation()
                        handleSegmentClick(segment)
                      }}
                      onMouseEnter={() => setHoveredSegment(`${segment.label}-${index}`)}
                      onMouseLeave={() => setHoveredSegment(null)}
                    />
                  )}
                </>
              )}
              {/* 如果没有 mask_url，使用 bbox 区域 */}
              {!segment.mask_url && segment.bbox?.length === 4 && (
                <div
                  className={`absolute cursor-pointer pointer-events-auto transition-all ${
                    isSelected ? 'bg-brand-terracotta/30'
                    : isHovered ? 'bg-blue-400/20'
                    : 'bg-transparent'
                  }`}
                  style={{
                    left: `${(segment.bbox[0] / (imageRef.current?.naturalWidth || 1)) * 100}%`,
                    top: `${(segment.bbox[1] / (imageRef.current?.naturalHeight || 1)) * 100}%`,
                    width: `${((segment.bbox[2] - segment.bbox[0]) / (imageRef.current?.naturalWidth || 1)) * 100}%`,
                    height: `${((segment.bbox[3] - segment.bbox[1]) / (imageRef.current?.naturalHeight || 1)) * 100}%`,
                  }}
                  onClick={(e) => {
                    e.stopPropagation()
                    handleSegmentClick(segment)
                  }}
                  onMouseEnter={() => setHoveredSegment(`${segment.label}-${index}`)}
                  onMouseLeave={() => setHoveredSegment(null)}
                />
              )}
            </motion.div>
          )
          })}
        </AnimatePresence>

        {/* 加载遮罩 - 不确定进度动画 */}
        {isLoading && (
          <div className="absolute inset-0 bg-gradient-to-b from-black/40 to-black/60 backdrop-blur-sm flex items-center justify-center">
            <div className="bg-white/95 rounded-2xl px-8 py-6 shadow-2xl max-w-xs w-full mx-4">
              {/* 顶部图标和标题 */}
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-terracotta to-orange-400 flex items-center justify-center animate-pulse">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-gray-800">AI 智能识别</h3>
                  <p className="text-xs text-gray-500">正在分析您的图片</p>
                </div>
              </div>
              
              {/* 不确定进度条 - 来回滑动动画 */}
              <div className="mb-3">
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden relative">
                  <div 
                    className="absolute h-full w-1/3 bg-gradient-to-r from-transparent via-brand-terracotta to-transparent rounded-full"
                    style={{ 
                      animation: 'indeterminate 1.5s ease-in-out infinite'
                    }}
                  />
                </div>
              </div>
              
              {/* 状态文字 */}
              <p className="text-xs text-gray-600 text-center">{loadingStage}</p>
              
              {/* 底部提示 */}
              <p className="mt-4 text-[10px] text-gray-400 text-center">
                首次识别可能需要稍长时间，请耐心等待
              </p>
            </div>
          </div>
        )}
      </div>

      {/* 已选家具栏目 - 支持多选 */}
      <AnimatePresence>
        {selectedSegments.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute -bottom-16 left-4 right-4 bg-white/95 backdrop-blur rounded-xl shadow-xl p-3 z-30"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-gray-600">已选择 {selectedSegments.length} 个物品</span>
              <button
                onClick={(e) => { e.stopPropagation(); setSelectedSegments([]); }}
                className="text-xs text-gray-400 hover:text-brand-terracotta"
              >
                清空
              </button>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {selectedSegments.map((seg, idx) => (
                <div 
                  key={`selected-${idx}`}
                  className="flex items-center gap-1 px-2 py-1 bg-brand-terracotta/10 text-brand-terracotta rounded-full text-xs"
                >
                  <span>{seg.label_zh}</span>
                  <button
                    onClick={(e) => { 
                      e.stopPropagation()
                      const segKey = `${seg.label}-${seg.bbox?.join(',')}`
                      setSelectedSegments(prev => prev.filter(s => `${s.label}-${s.bbox?.join(',')}` !== segKey))
                    }}
                    className="hover:bg-brand-terracotta/20 rounded-full p-0.5"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 错误提示 */}
      {error && (
        <div className="absolute bottom-4 left-4 right-4 bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-600">
          {error}
        </div>
      )}
    </div>
  )
}
