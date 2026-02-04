'use client'

import { useState, useRef, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, ChevronDown, Zap, Image as ImageIcon, Palette, Clock, DollarSign, Home, Sparkles, X, Loader2, Layers, Eraser, Download } from 'lucide-react'
import SegmentableImage from '@/components/SegmentableImage'
import { BlurFade } from '@/components/magicui/blur-fade'
import { useStudioStore, DesignImage as StoreDesignImage } from '@/lib/stores/studio'

import { NumberTicker } from '@/components/magicui/number-ticker'
import { Marquee } from '@/components/magicui/marquee'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const testimonials = [
  { name: '张设计师', role: '独立设计师', quote: '出图速度太快了，以前一张效果图要等2天，现在78秒！' },
  { name: '李总', role: '房产开发商', quote: '成本降低了90%，品质丝毫不减，强烈推荐。' },
  { name: '王经理', role: '装修公司', quote: '客户转化率提升40%，毛胚房秒变精装效果图太有说服力。' },
  { name: '陈工', role: '建筑师', quote: '风格多样，侘寂风太美了，完全符合高端客户需求。' },
]

const KoiFish = ({ className = '' }: { className?: string }) => (
  <svg viewBox="0 0 200 160" className={className} fill="none" stroke="currentColor" strokeWidth="1.2">
    <path d="M40 80 Q60 40 100 35 Q140 30 160 50 Q180 70 170 90 Q160 110 130 115 Q100 120 70 110 Q40 100 40 80 Z" />
    <path d="M160 50 Q175 35 185 40 Q195 50 180 60 Q170 65 160 55" />
    <path d="M160 50 Q170 60 175 75 Q178 85 170 90" />
    <circle cx="70" cy="70" r="6" fill="currentColor" />
    <circle cx="72" cy="68" r="2" fill="white" />
    <path d="M90 55 Q100 45 115 50" strokeDasharray="3 3" />
    <path d="M90 95 Q105 105 120 100" strokeDasharray="3 3" />
    <path d="M55 75 Q65 70 75 75 Q85 80 75 85 Q65 88 55 82 Q50 78 55 75" />
    <path d="M100 60 Q110 55 120 60 Q125 65 120 70 Q110 75 100 70 Q95 65 100 60" />
    <path d="M130 75 Q140 70 148 78 Q150 85 145 90 Q135 95 128 88 Q125 82 130 75" />
  </svg>
)

const Monkey = ({ className = '' }: { className?: string }) => (
  <svg viewBox="0 0 80 120" className={className} fill="none" stroke="currentColor" strokeWidth="1">
    <circle cx="40" cy="30" r="18" />
    <circle cx="32" cy="26" r="3" fill="currentColor" />
    <circle cx="48" cy="26" r="3" fill="currentColor" />
    <ellipse cx="40" cy="35" rx="6" ry="4" />
    <path d="M20 25 Q15 20 18 15 Q25 12 28 18" />
    <path d="M60 25 Q65 20 62 15 Q55 12 52 18" />
    <path d="M40 48 L40 70" />
    <path d="M40 55 Q25 50 15 60" />
    <path d="M40 55 Q55 50 65 45" />
    <path d="M40 70 Q35 90 30 110" />
    <path d="M40 70 Q45 90 50 100" />
    <path d="M50 100 Q55 105 60 100 Q58 95 50 100" />
  </svg>
)

const BuildingIcon = ({ className = '' }: { className?: string }) => (
  <svg viewBox="0 0 50 60" className={className} fill="none" stroke="currentColor" strokeWidth="1.2">
    <rect x="5" y="15" width="40" height="40" rx="1" />
    <path d="M5 15 L25 5 L45 15" />
    <rect x="12" y="22" width="8" height="10" rx="0.5" />
    <rect x="30" y="22" width="8" height="10" rx="0.5" />
    <rect x="12" y="38" width="8" height="10" rx="0.5" />
    <rect x="30" y="38" width="8" height="10" rx="0.5" />
    <circle cx="25" cy="10" r="2" />
  </svg>
)

const ClassicArchBg = ({ className = '' }: { className?: string }) => (
  <svg viewBox="0 0 400 700" className={className} fill="none" stroke="currentColor" strokeWidth="0.4">
    {/* 顶部希腊回纹边框 */}
    <g>
      {[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380].map((x, i) => (
        <path key={`greek-${i}`} d={`M${x} 5 L${x+5} 5 L${x+5} 10 L${x+15} 10 L${x+15} 15 L${x+10} 15 L${x+10} 10 L${x} 10 Z`} />
      ))}
    </g>
    
    {/* 左侧精细科林斯柱 */}
    <g>
      <rect x="15" y="35" width="30" height="6" rx="1" />
      <rect x="18" y="41" width="24" height="3" />
      <path d="M20 44 C20 44 15 50 20 55 C25 50 20 44 20 44" />
      <path d="M30 44 C30 44 25 50 30 55 C35 50 30 44 30 44" />
      <path d="M40 44 C40 44 35 50 40 55 C45 50 40 44 40 44" />
      <rect x="18" y="55" width="24" height="2" />
      {[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19].map((i) => (
        <g key={`col-l-${i}`}>
          <path d={`M20 ${60 + i*25} L20 ${85 + i*25}`} />
          <path d={`M25 ${60 + i*25} L25 ${85 + i*25}`} strokeDasharray="2 3" />
          <path d={`M30 ${60 + i*25} L30 ${85 + i*25}`} />
          <path d={`M35 ${60 + i*25} L35 ${85 + i*25}`} strokeDasharray="2 3" />
          <path d={`M40 ${60 + i*25} L40 ${85 + i*25}`} />
        </g>
      ))}
      <rect x="18" y="560" width="24" height="3" />
      <rect x="15" y="563" width="30" height="8" rx="1" />
    </g>
    
    {/* 右侧精细科林斯柱 */}
    <g>
      <rect x="355" y="35" width="30" height="6" rx="1" />
      <rect x="358" y="41" width="24" height="3" />
      <path d="M360 44 C360 44 355 50 360 55 C365 50 360 44 360 44" />
      <path d="M370 44 C370 44 365 50 370 55 C375 50 370 44 370 44" />
      <path d="M380 44 C380 44 375 50 380 55 C385 50 380 44 380 44" />
      <rect x="358" y="55" width="24" height="2" />
      {[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19].map((i) => (
        <g key={`col-r-${i}`}>
          <path d={`M360 ${60 + i*25} L360 ${85 + i*25}`} />
          <path d={`M365 ${60 + i*25} L365 ${85 + i*25}`} strokeDasharray="2 3" />
          <path d={`M370 ${60 + i*25} L370 ${85 + i*25}`} />
          <path d={`M375 ${60 + i*25} L375 ${85 + i*25}`} strokeDasharray="2 3" />
          <path d={`M380 ${60 + i*25} L380 ${85 + i*25}`} />
        </g>
      ))}
      <rect x="358" y="560" width="24" height="3" />
      <rect x="355" y="563" width="30" height="8" rx="1" />
    </g>
    
    {/* 中央大拱门 */}
    <path d="M100 180 L100 400 Q100 480 200 480 Q300 480 300 400 L300 180" />
    <path d="M110 180 L110 395 Q110 470 200 470 Q290 470 290 395 L290 180" />
    <path d="M120 180 L120 390 Q120 460 200 460 Q280 460 280 390 L280 180" />
    
    {/* 拱门内装饰 */}
    <circle cx="200" cy="280" r="40" />
    <circle cx="200" cy="280" r="35" />
    <circle cx="200" cy="280" r="25" />
    <path d="M175 280 L225 280 M200 255 L200 305" />
    <path d="M180 260 L220 300 M220 260 L180 300" strokeDasharray="2 2" />
    
    {/* 拱门顶部装饰石 */}
    <path d="M190 185 L200 170 L210 185 Z" />
    <rect x="185" y="185" width="30" height="8" />
    
    {/* 顶部三角楣饰 */}
    <path d="M60 30 L200 0 L340 30 L60 30" />
    <path d="M80 28 L200 5 L320 28" />
    <circle cx="200" cy="18" r="6" />
    
    {/* 左侧藤蔓装饰 */}
    <g>
      <path d="M55 100 Q65 120 55 140 Q45 160 55 180 Q65 200 55 220 Q45 240 55 260" strokeDasharray="1 2" />
      {[100, 140, 180, 220].map((y, i) => (
        <g key={`vine-l-${i}`}>
          <ellipse cx={i % 2 === 0 ? 62 : 48} cy={y + 10} rx="8" ry="4" transform={`rotate(${i % 2 === 0 ? -30 : 30} ${i % 2 === 0 ? 62 : 48} ${y + 10})`} />
          <ellipse cx={i % 2 === 0 ? 48 : 62} cy={y + 25} rx="8" ry="4" transform={`rotate(${i % 2 === 0 ? 30 : -30} ${i % 2 === 0 ? 48 : 62} ${y + 25})`} />
        </g>
      ))}
    </g>
    
    {/* 右侧藤蔓装饰 */}
    <g>
      <path d="M345 100 Q335 120 345 140 Q355 160 345 180 Q335 200 345 220 Q355 240 345 260" strokeDasharray="1 2" />
      {[100, 140, 180, 220].map((y, i) => (
        <g key={`vine-r-${i}`}>
          <ellipse cx={i % 2 === 0 ? 338 : 352} cy={y + 10} rx="8" ry="4" transform={`rotate(${i % 2 === 0 ? 30 : -30} ${i % 2 === 0 ? 338 : 352} ${y + 10})`} />
          <ellipse cx={i % 2 === 0 ? 352 : 338} cy={y + 25} rx="8" ry="4" transform={`rotate(${i % 2 === 0 ? -30 : 30} ${i % 2 === 0 ? 352 : 338} ${y + 25})`} />
        </g>
      ))}
    </g>
    
    {/* 四角花纹medallion */}
    <g>
      <circle cx="75" cy="100" r="18" />
      <circle cx="75" cy="100" r="14" />
      <circle cx="75" cy="100" r="8" />
      {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => (
        <path key={`medal-l-${i}`} d={`M${75 + 10*Math.cos(angle*Math.PI/180)} ${100 + 10*Math.sin(angle*Math.PI/180)} L${75 + 16*Math.cos(angle*Math.PI/180)} ${100 + 16*Math.sin(angle*Math.PI/180)}`} />
      ))}
    </g>
    <g>
      <circle cx="325" cy="100" r="18" />
      <circle cx="325" cy="100" r="14" />
      <circle cx="325" cy="100" r="8" />
      {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => (
        <path key={`medal-r-${i}`} d={`M${325 + 10*Math.cos(angle*Math.PI/180)} ${100 + 10*Math.sin(angle*Math.PI/180)} L${325 + 16*Math.cos(angle*Math.PI/180)} ${100 + 16*Math.sin(angle*Math.PI/180)}`} />
      ))}
    </g>
    
    {/* 底部浮雕装饰带 */}
    <rect x="50" y="580" width="300" height="3" />
    <rect x="50" y="590" width="300" height="2" />
    {[60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((x, i) => (
      <g key={`relief-${i}`}>
        <rect x={x} y="595" width="20" height="25" rx="2" />
        <path d={`M${x+10} 600 L${x+10} 615`} />
        <circle cx={x+10} cy="605" r="3" />
      </g>
    ))}
    
    {/* 底部齿状装饰 */}
    {[50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330].map((x, i) => (
      <rect key={`dent-${i}`} x={x} y="625" width="12" height="8" />
    ))}
    
    {/* 角落装饰花纹 */}
    <g>
      <path d="M60 640 Q70 650 60 660 Q50 650 60 640" />
      <path d="M60 650 Q75 640 80 655 Q75 670 60 660" />
      <path d="M60 650 Q45 640 40 655 Q45 670 60 660" />
    </g>
    <g>
      <path d="M340 640 Q350 650 340 660 Q330 650 340 640" />
      <path d="M340 650 Q355 640 360 655 Q355 670 340 660" />
      <path d="M340 650 Q325 640 320 655 Q325 670 340 660" />
    </g>
    
    {/* 额外装饰 - 小窗格 */}
    <rect x="70" y="300" width="25" height="40" rx="2" />
    <path d="M82.5 300 L82.5 340 M70 320 L95 320" />
    <rect x="305" y="300" width="25" height="40" rx="2" />
    <path d="M317.5 300 L317.5 340 M305 320 L330 320" />
    
    {/* 橄榄枝环绕 */}
    <path d="M140 520 Q170 510 200 520 Q230 530 260 520" />
    <path d="M145 525 Q170 515 200 525 Q230 535 255 525" />
    {[150, 170, 190, 210, 230, 250].map((x, i) => (
      <ellipse key={`olive-${i}`} cx={x} cy={i % 2 === 0 ? 515 : 530} rx="6" ry="3" transform={`rotate(${i % 2 === 0 ? -20 : 20} ${x} ${i % 2 === 0 ? 515 : 530})`} />
    ))}
    <circle cx="200" cy="522" r="4" fill="currentColor" fillOpacity="0.3" />
  </svg>
)

const ClassicPattern = ({ className = '' }: { className?: string }) => (
  <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="0.4">
    {/* 外边框 */}
    <rect x="5" y="5" width="90" height="90" />
    <rect x="8" y="8" width="84" height="84" />
    <rect x="12" y="12" width="76" height="76" />
    
    {/* 中央圆形装饰 */}
    <circle cx="50" cy="50" r="30" />
    <circle cx="50" cy="50" r="26" />
    <circle cx="50" cy="50" r="20" />
    <circle cx="50" cy="50" r="14" />
    <circle cx="50" cy="50" r="8" />
    
    {/* 十字和对角线 */}
    <path d="M50 20 L50 80 M20 50 L80 50" />
    <path d="M28 28 L72 72 M72 28 L28 72" strokeDasharray="2 3" />
    
    {/* 放射线 */}
    {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((angle, i) => (
      <path key={`ray-${i}`} d={`M${50 + 22*Math.cos(angle*Math.PI/180)} ${50 + 22*Math.sin(angle*Math.PI/180)} L${50 + 28*Math.cos(angle*Math.PI/180)} ${50 + 28*Math.sin(angle*Math.PI/180)}`} />
    ))}
    
    {/* 四角花纹 */}
    <g>
      <circle cx="18" cy="18" r="8" />
      <circle cx="18" cy="18" r="5" />
      <path d="M18 10 L18 26 M10 18 L26 18" />
    </g>
    <g>
      <circle cx="82" cy="18" r="8" />
      <circle cx="82" cy="18" r="5" />
      <path d="M82 10 L82 26 M74 18 L90 18" />
    </g>
    <g>
      <circle cx="18" cy="82" r="8" />
      <circle cx="18" cy="82" r="5" />
      <path d="M18 74 L18 90 M10 82 L26 82" />
    </g>
    <g>
      <circle cx="82" cy="82" r="8" />
      <circle cx="82" cy="82" r="5" />
      <path d="M82 74 L82 90 M74 82 L90 82" />
    </g>
    
    {/* 边缘小装饰 */}
    <circle cx="50" cy="8" r="3" />
    <circle cx="50" cy="92" r="3" />
    <circle cx="8" cy="50" r="3" />
    <circle cx="92" cy="50" r="3" />
  </svg>
)

// 设计风格配置（包含提示词模板）
const designStylesConfig = [
  {
    name: '现代简约',
    prompt: 'Modern minimalist interior, clean lines, neutral colors, simple furniture, open space, natural light',
    negativePrompt: 'cluttered, ornate, traditional, busy patterns',
  },
  {
    name: '北欧风',
    prompt: 'Scandinavian interior, bright airy, white walls, light wood, cozy textiles, plants, hygge',
    negativePrompt: 'dark colors, heavy furniture, ornate details',
  },
  {
    name: '侘寂风',
    prompt: 'Wabi-sabi interior, Japanese aesthetics, natural materials, earth tones, minimal, zen',
    negativePrompt: 'bright colors, modern tech, plastic materials',
  },
  {
    name: '新中式',
    prompt: 'Modern Chinese interior, traditional elements, dark wood, subtle patterns, elegant',
    negativePrompt: 'western style, industrial, colorful',
  },
  {
    name: '轻奢',
    prompt: 'Light luxury interior, elegant, marble, gold accents, velvet, crystal lighting',
    negativePrompt: 'cheap materials, industrial, rustic',
  },
  {
    name: '工业风',
    prompt: 'Industrial interior, exposed brick, metal pipes, concrete, Edison bulbs, urban loft',
    negativePrompt: 'traditional, ornate, soft textures',
  },
  {
    name: '日式',
    prompt: 'Japanese interior, tatami, shoji screens, natural wood, zen, minimalist, peaceful',
    negativePrompt: 'western furniture, bright colors, cluttered',
  },
  {
    name: '法式',
    prompt: 'French interior, elegant moldings, chandelier, parquet floors, romantic, luxurious',
    negativePrompt: 'modern, industrial, minimal',
  },
]

// 设计风格名称列表
const designStyles = designStylesConfig.map(s => s.name)

// 示例毛坯房图片（仅用于演示）
const sampleOriginalImage = 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=1200&q=80'

// 图片类型
interface DesignImage {
  id: string
  url: string
  base64?: string // 用于API调用的base64数据
  type: 'original' | 'generated'
  style?: string
  name?: string
  segments?: any[] // 缓存的家具识别结果
}

// 将File转换为base64
const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = error => reject(error)
  })
}

// 将图片URL转换为base64
const urlToBase64 = async (url: string): Promise<string> => {
  // 将后端完整URL转换为相对路径，通过Next.js代理访问避免CORS
  let fetchUrl = url
  if (url.includes('localhost:8000') || url.includes('127.0.0.1:8000')) {
    fetchUrl = url.replace(/https?:\/\/(localhost|127\.0\.0\.1):8000/, '')
  }
  const response = await fetch(fetchUrl)
  const blob = await response.blob()
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(blob)
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = error => reject(error)
  })
}

export default function HomePage() {
  const { data: session } = useSession()
  const userId = (session?.user as any)?.id
  
  // 从store获取持久化状态
  const {
    workImages,
    selectedImageId,
    segmentsCache,
    selectedStyle,
    editMode,
    prompt,
    setWorkImages,
    addWorkImage,
    setSelectedImageId,
    setSegmentsCache: storeSetSegmentsCache,
    setSelectedStyle,
    setEditMode,
    setPrompt,
  } = useStudioStore()
  
  // 图片加载状态
  const [loadedImages, setLoadedImages] = useState<Set<string>>(new Set())
  
  // 页面加载时清理失效的blob URL图片，并预加载所有图片
  useEffect(() => {
    console.log('[Store] 页面加载，当前workImages:', workImages.length, '张图片')
    workImages.forEach((img, i) => {
      console.log(`[Store] 图片${i + 1}: type=${img.type}, url=${img.url.substring(0, 50)}...`)
    })
    
    const validImages = workImages.filter(img => !img.url.startsWith('blob:'))
    console.log('[Store] 过滤blob后剩余:', validImages.length, '张图片')
    
    if (validImages.length !== workImages.length) {
      setWorkImages(validImages)
      if (selectedImageId && !validImages.find(img => img.id === selectedImageId)) {
        setSelectedImageId(validImages[0]?.id || null)
      }
    }
    // 预加载所有远程图片
    validImages.forEach(img => {
      if (!img.url.startsWith('blob:')) {
        const image = new Image()
        image.onload = () => setLoadedImages(prev => { const next = new Set(Array.from(prev)); next.add(img.id); return next })
        image.src = img.url
      }
    })
  }, [])
  
  // 当图片列表变化时，预加载新图片
  useEffect(() => {
    workImages.forEach(img => {
      if (!loadedImages.has(img.id) && !img.url.startsWith('blob:')) {
        const image = new Image()
        image.onload = () => setLoadedImages(prev => { const next = new Set(Array.from(prev)); next.add(img.id); return next })
        image.src = img.url
      }
    })
  }, [workImages])
  
  // 计算选中的图片（不过滤当前会话的blob URL，只在初始化时清理）
  const images = workImages
  const setImages = setWorkImages
  const selectedImage = workImages.find(img => img.id === selectedImageId) || null
  const setSelectedImage = (img: DesignImage | null) => setSelectedImageId(img?.id || null)
  
  // 临时状态（不需要持久化）
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatingProgress, setGeneratingProgress] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  // 局部替换模式
  const [selectedSegments, setSelectedSegments] = useState<any[]>([])
  const [selectedReplaceStyle, setSelectedReplaceStyle] = useState<string | null>(null)
  const [isReplacing, setIsReplacing] = useState(false)
  
  // 包装setSegmentsCache以匹配原有接口
  const setSegmentsCache = (cache: Record<string, any[]>) => {
    Object.entries(cache).forEach(([id, segments]) => {
      storeSetSegmentsCache(id, segments)
    })
  }
  
  // 局部替换风格列表
  const replaceStyles = [
    { id: 'modern', name: '现代简约', prompt: 'modern minimalist style, clean lines, neutral colors' },
    { id: 'nordic', name: '北欧风', prompt: 'scandinavian style, light wood, white and grey tones' },
    { id: 'luxury', name: '轻奢', prompt: 'luxury style, gold accents, velvet fabric, elegant' },
    { id: 'japanese', name: '日式', prompt: 'japanese style, natural materials, zen aesthetic' },
    { id: 'wabisabi', name: '侘寂风', prompt: 'wabi-sabi style, natural imperfection, earthy tones' },
    { id: 'industrial', name: '工业风', prompt: 'industrial style, exposed brick, metal accents' },
    { id: 'vintage', name: '复古', prompt: 'vintage style, antique furniture, warm colors' },
    { id: 'tropical', name: '热带', prompt: 'tropical style, plants, rattan furniture, natural light' },
  ]

  // 上传图片到服务器获取持久URL
  const uploadImageToServer = async (file: File): Promise<string | null> => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })
      
      const result = await response.json()
      if (result.success && result.url) {
        console.log('[Upload] 图片上传成功:', result.url)
        return result.url
      } else {
        console.error('[Upload] 上传失败:', result.error)
        return null
      }
    } catch (error) {
      console.error('[Upload] 上传错误:', error)
      return null
    }
  }

  // 处理图片上传
  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // 先显示临时预览
      const tempUrl = URL.createObjectURL(file)
      const base64 = await fileToBase64(file)
      const tempId = Date.now().toString()
      
      const tempImage: DesignImage = {
        id: tempId,
        url: tempUrl,
        base64,
        type: 'original',
        name: file.name
      }
      addWorkImage(tempImage)
      
      // 后台上传到服务器获取持久URL
      const persistentUrl = await uploadImageToServer(file)
      if (persistentUrl) {
        // 更新为持久URL
        setWorkImages(workImages.map(img => 
          img.id === tempId ? { ...img, url: persistentUrl } : img
        ).concat(tempImage.id === tempId ? [] : []))
        // 直接更新当前图片
        const updatedImages = [...workImages.filter(img => img.id !== tempId), {
          ...tempImage,
          url: persistentUrl
        }]
        setWorkImages(updatedImages)
      }
    }
  }

  // 处理拖拽上传
  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      // 先显示临时预览
      const tempUrl = URL.createObjectURL(file)
      const base64 = await fileToBase64(file)
      const tempId = Date.now().toString()
      
      const tempImage: DesignImage = {
        id: tempId,
        url: tempUrl,
        base64,
        type: 'original',
        name: file.name
      }
      addWorkImage(tempImage)
      
      // 后台上传到服务器获取持久URL
      const persistentUrl = await uploadImageToServer(file)
      if (persistentUrl) {
        const updatedImages = [...workImages.filter(img => img.id !== tempId), {
          ...tempImage,
          url: persistentUrl
        }]
        setWorkImages(updatedImages)
      }
    }
  }

  // 加载示例毛坯图
  const loadSampleOriginal = async () => {
    try {
      const base64 = await urlToBase64(sampleOriginalImage)
      const newImage: DesignImage = {
        id: Date.now().toString(),
        url: sampleOriginalImage,
        base64,
        type: 'original',
        name: '示例毛坯房.jpg'
      }
      addWorkImage(newImage)
    } catch (error) {
      // 如果无法获取base64（跨域），仍然添加图片但不含base64
      const newImage: DesignImage = {
        id: Date.now().toString(),
        url: sampleOriginalImage,
        type: 'original',
        name: '示例毛坯房.jpg'
      }
      addWorkImage(newImage)
      console.warn('无法获取示例图片base64，可能存在跨域问题')
    }
  }

  // 输出配置
  const outputConfig = {
    width: 3840,   // 4K宽度
    height: 2160,  // 4K高度
    quality: 'high',
    format: 'jpg',
  }

  // 构建生成请求参数（用于后续接入API）
  const buildGenerateRequest = () => {
    const originalImage = images.find(img => img.type === 'original')
    if (!originalImage) return null

    const styleConfig = designStylesConfig[selectedStyle]
    
    return {
      // 图片数据
      image: {
        url: originalImage.url,
        base64: originalImage.base64, // 用于发送给API
        name: originalImage.name,
      },
      // 风格配置
      style: {
        name: styleConfig.name,
        prompt: styleConfig.prompt,
        negativePrompt: styleConfig.negativePrompt,
      },
      // 用户输入
      userPrompt: prompt,
      // 完整提示词（风格提示词 + 用户描述）
      fullPrompt: `${styleConfig.prompt}${prompt ? ', ' + prompt : ''}`,
      fullNegativePrompt: styleConfig.negativePrompt,
      // 输出配置 - 4K分辨率
      output: {
        width: outputConfig.width,
        height: outputConfig.height,
        quality: outputConfig.quality,
        format: outputConfig.format,
        resolution: '4K',
      },
    }
  }

  // 生成效果图
  const handleGenerate = async () => {
    const originalImage = images.find(img => img.type === 'original')
    if (!originalImage) {
      alert('请先上传图片')
      return
    }
    
    // 如果没有base64，从URL重新获取
    let imageBase64 = originalImage.base64
    if (!imageBase64 && originalImage.url) {
      try {
        imageBase64 = await urlToBase64(originalImage.url)
      } catch (e) {
        console.error('获取图片base64失败:', e)
        alert('图片加载失败，请重新上传')
        return
      }
    }
    
    if (!imageBase64) {
      alert('图片数据无效，请重新上传')
      return
    }
    
    // 构建请求参数
    const requestParams = buildGenerateRequest()
    console.log('=== 生成效果图请求参数 ===')
    console.log('【图片】', { name: requestParams?.image.name, hasBase64: !!requestParams?.image.base64 })
    console.log('【风格】', requestParams?.style.name)
    console.log('【输出】', `${requestParams?.output.width}x${requestParams?.output.height}`)
    console.log('========================')
    
    setIsGenerating(true)
    setGeneratingProgress(0)
    
    // 进度模拟
    const progressInterval = setInterval(() => {
      setGeneratingProgress(prev => Math.min(90, prev + Math.random() * 10))
    }, 500)
    
    try {
      // 调用实际API
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image: imageBase64,
          roomType: 'living_room',
          style: designStyles[selectedStyle],
          quality: '4K',
        }),
      })
      
      const result = await response.json()
      console.log('API响应:', JSON.stringify(result, null, 2))
      
      clearInterval(progressInterval)
      setGeneratingProgress(100)
      
      if (result.success && result.images && result.images.length > 0) {
        // API返回成功，使用返回的图片
        const generatedImage: DesignImage = {
          id: Date.now().toString(),
          url: result.images[0], // API返回的图片URL
          type: 'generated',
          style: designStyles[selectedStyle],
          name: `${designStyles[selectedStyle]}_效果图_${Date.now()}.jpg`
        }
        console.log('✅ 生成成功，添加图片:', generatedImage)
        // 预加载图片到浏览器缓存
        const img = new Image()
        img.src = generatedImage.url
        addWorkImage(generatedImage)
        console.log('✅ 图片已添加到工作区')
        
        // 保存到用户历史记录
        if (userId) {
          console.log('[History] 保存生成记录, userId:', userId)
          fetch(`${API_URL}/api/v1/generations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              user_id: userId,
              input_image_url: selectedImage?.url || '',
              output_image_url: result.images[0],
              generation_type: 'full',
              style: designStyles[selectedStyle],
              prompt: prompt,
              processing_time: result.elapsed_seconds || 0,
              cost: result.cost || 0
            })
          })
            .then(res => res.json())
            .then(data => console.log('[History] 保存成功:', data))
            .catch(e => console.error('[History] 保存失败:', e))
        } else {
          console.warn('[History] 用户未登录，跳过保存')
        }
      } else {
        // API失败，显示错误
        console.error('生成失败:', result.error)
        alert(`生成失败: ${result.error || '未知错误'}`)
      }
    } catch (error) {
      console.error('API调用错误:', error)
      clearInterval(progressInterval)
      alert('网络错误，请检查后端服务是否启动')
    } finally {
      setIsGenerating(false)
      setGeneratingProgress(0)
    }
  }

  // 局部替换处理 - 支持多选
  const handleSegmentReplace = async () => {
    if (!selectedImage || selectedSegments.length === 0 || !selectedReplaceStyle) {
      alert('请先选择区域和替换风格')
      return
    }
    
    const styleConfig = replaceStyles.find(s => s.id === selectedReplaceStyle)
    if (!styleConfig) return
    
    setIsReplacing(true)
    setGeneratingProgress(0)
    
    // 进度模拟
    const progressInterval = setInterval(() => {
      setGeneratingProgress(prev => Math.min(90, prev + Math.random() * 12))
    }, 300)
    
    try {
      // 获取图片数据，如果没有base64则从URL获取
      let imageData = selectedImage.base64
      if (!imageData && selectedImage.url) {
        try {
          imageData = await urlToBase64(selectedImage.url)
        } catch (e) {
          console.error('获取图片base64失败:', e)
          alert('图片加载失败，请重试')
          setIsReplacing(false)
          clearInterval(progressInterval)
          return
        }
      }
      
      // 收集所有选中 segment 的 mask 和 label
      // 优先使用 inpaint_mask_base64（黑白mask），其次 inpaint_mask_url，最后 mask_url
      const maskDataList = selectedSegments.map(s => s.inpaint_mask_base64 || s.inpaint_mask_url || s.mask_url)
      const labelList = selectedSegments.map(s => s.label)
      
      console.log('[Inpaint] 选中物品:', labelList.join(', '))
      console.log('[Inpaint] mask 数量:', maskDataList.length)
      
      const response = await fetch('/api/inpaint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image_url: imageData,
          mask_url: maskDataList[0],
          mask_urls: maskDataList,
          furniture_type: labelList[0],
          furniture_types: labelList,  // 每个物品的类型，后端逐个替换
          style: styleConfig.name,
          custom_prompt: styleConfig.prompt,
        }),
      })
      
      const result = await response.json()
      console.log('NanoBanana Inpaint响应:', result)
      
      clearInterval(progressInterval)
      setGeneratingProgress(100)
      
      if (result.success && result.image_url) {
        // 添加替换后的图片
        const labelNames = selectedSegments.map(s => s.label_zh).join('+')
        const replacedImage: DesignImage = {
          id: Date.now().toString(),
          url: result.image_url,
          type: 'generated',
          style: styleConfig.name,
          name: `局部替换_${labelNames}_${styleConfig.name}_${Date.now()}.jpg`
        }
        // 预加载图片
        const img = new Image()
        img.src = replacedImage.url
        addWorkImage(replacedImage)
        
        // 保存到用户历史记录
        if (userId) {
          console.log('[History] 保存局部替换记录, userId:', userId)
          fetch(`${API_URL}/api/v1/generations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              user_id: userId,
              input_image_url: selectedImage?.url || '',
              output_image_url: result.image_url,
              generation_type: 'inpaint',
              style: styleConfig.name,
              prompt: `局部替换: ${labelNames}`,
              processing_time: result.processing_time || 0,
              cost: result.cost || 0
            })
          })
            .then(res => res.json())
            .then(data => console.log('[History] 局部替换保存成功:', data))
            .catch(e => console.error('[History] 局部替换保存失败:', e))
        } else {
          console.warn('[History] 用户未登录，跳过保存')
        }
        
        // 重置选择状态
        setSelectedSegments([])
        setSelectedReplaceStyle(null)
      } else {
        console.error('局部替换失败:', result.error)
        alert(`替换失败: ${result.error || '未知错误'}`)
      }
    } catch (error) {
      console.error('局部替换错误:', error)
      clearInterval(progressInterval)
      alert('网络错误，请检查后端服务')
    } finally {
      setIsReplacing(false)
      setGeneratingProgress(0)
    }
  }

  // 抹除选中家具
  const handleSegmentErase = async () => {
    if (!selectedImage || selectedSegments.length === 0) {
      alert('请先选择要抹除的区域')
      return
    }
    
    setIsReplacing(true)
    setGeneratingProgress(0)
    
    const progressInterval = setInterval(() => {
      setGeneratingProgress(prev => Math.min(90, prev + Math.random() * 12))
    }, 300)
    
    try {
      let imageData = selectedImage.base64
      if (!imageData && selectedImage.url) {
        try {
          imageData = await urlToBase64(selectedImage.url)
        } catch (e) {
          console.error('获取图片base64失败:', e)
          alert('图片加载失败，请重试')
          setIsReplacing(false)
          clearInterval(progressInterval)
          return
        }
      }
      
      // 优先使用 inpaint_mask_base64（黑白mask），其次 inpaint_mask_url，最后 mask_url
      const maskDataList = selectedSegments.map(s => {
        console.log('[Erase] segment:', s.label, 'inpaint_mask_base64:', !!s.inpaint_mask_base64, 'inpaint_mask_url:', s.inpaint_mask_url, 'mask_url:', s.mask_url)
        return s.inpaint_mask_base64 || s.inpaint_mask_url || s.mask_url
      }).filter(Boolean)
      const labelList = selectedSegments.map(s => s.label)
      
      console.log('[Erase] 抹除物品:', labelList.join(', '))
      console.log('[Erase] mask数据:', maskDataList.map(m => m?.substring(0, 50)))
      console.log('[Erase] Mask数量:', maskDataList.length)
      
      if (maskDataList.length === 0) {
        alert('无法获取选区mask数据，请重新识别家具')
        setIsReplacing(false)
        clearInterval(progressInterval)
        return
      }
      
      const response = await fetch('/api/inpaint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image_url: imageData,
          mask_url: maskDataList[0],
          mask_urls: maskDataList.length > 1 ? maskDataList : undefined,
          furniture_types: labelList,
          style: '抹除',
          custom_prompt: 'empty clean floor and wall, remove all furniture and objects completely, seamless background texture, natural lighting, photorealistic empty room',
        }),
      })
      
      const result = await response.json()
      clearInterval(progressInterval)
      setGeneratingProgress(100)
      
      if (result.success && result.image_url) {
        const labelNames = selectedSegments.map(s => s.label_zh).join('+')
        const erasedImage: DesignImage = {
          id: Date.now().toString(),
          url: result.image_url,
          type: 'generated',
          style: '抹除',
          name: `抹除_${labelNames}_${Date.now()}.jpg`
        }
        // 预加载图片
        const img = new Image()
        img.src = erasedImage.url
        addWorkImage(erasedImage)
        
        // 保存到用户历史记录
        if (userId) {
          console.log('[History] 保存抹除记录, userId:', userId)
          fetch(`${API_URL}/api/v1/generations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              user_id: userId,
              input_image_url: selectedImage?.url || '',
              output_image_url: result.image_url,
              generation_type: 'inpaint',
              style: '抹除',
              prompt: `抹除: ${labelNames}`,
              processing_time: result.processing_time || 0,
              cost: result.cost || 0
            })
          })
            .then(res => res.json())
            .then(data => console.log('[History] 抹除保存成功:', data))
            .catch(e => console.error('[History] 抹除保存失败:', e))
        } else {
          console.warn('[History] 用户未登录，跳过保存')
        }
        
        setSelectedSegments([])
      } else {
        console.error('抹除失败:', result.error)
        alert(`抹除失败: ${result.error || '未知错误'}`)
      }
    } catch (error) {
      console.error('抹除错误:', error)
      clearInterval(progressInterval)
      alert('网络错误，请检查后端服务')
    } finally {
      setIsReplacing(false)
      setGeneratingProgress(0)
    }
  }

  // 下载单张图片
  const handleDownloadImage = async (image: DesignImage) => {
    try {
      const response = await fetch(image.url)
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = image.name || `image_${Date.now()}.jpg`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('下载失败:', error)
      // 降级方案：直接打开链接
      window.open(image.url, '_blank')
    }
  }

  // 删除图片
  const handleDeleteImage = (id: string) => {
    const newImages = images.filter(img => img.id !== id)
    setImages(newImages)
    if (selectedImage?.id === id) {
      setSelectedImage(newImages.length > 0 ? newImages[newImages.length - 1] : null)
    }
  }

  // 导出/下载当前图片
  const handleExport = async () => {
    if (!selectedImage) return
    
    try {
      const response = await fetch(selectedImage.url)
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = selectedImage.name || `roommate_${selectedImage.type}_${Date.now()}.jpg`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      // 如果fetch失败（跨域），直接打开新窗口
      window.open(selectedImage.url, '_blank')
    }
  }

  // 清空所有图片
  const handleClearAll = () => {
    setImages([])
    setSelectedImage(null)
  }

  return (
    <main className="min-h-screen bg-brand-cream overflow-hidden">
      {/* Hero Section - 三列不规则布局 */}
      <section className="min-h-screen relative">
        {/* 左侧垂直文字装饰 - 仅Banner内显示 */}
        <div className="hidden lg:flex absolute left-0 top-0 h-full w-10 bg-brand-cream border-r border-brand-charcoal/10 items-center justify-center z-40">
          <span className="text-[10px] tracking-[0.3em] text-brand-charcoal/50 transform -rotate-90 whitespace-nowrap uppercase">
            开启您的设计之旅
          </span>
        </div>

        <div className="flex flex-col lg:flex-row min-h-screen lg:pl-10">
          {/* 左列 - Logo和主标题 */}
          <motion.div 
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="lg:w-[38.2%] bg-brand-cream px-6 lg:px-10 pt-20 lg:pt-24 pb-10 lg:pb-16 flex flex-col min-h-[60vh] lg:min-h-screen relative overflow-hidden"
          >
            {/* 古典艺术背景 - 米开朗基罗西斯廷教堂风格 - 动态 */}
            <motion.div 
              className="absolute inset-[-20px] pointer-events-none"
              animate={{ 
                scale: [1, 1.05, 1],
                x: [0, 10, -10, 0],
                y: [0, -5, 5, 0]
              }}
              transition={{ 
                duration: 20,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              style={{
                backgroundImage: `url("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Michelangelo_-_Creation_of_Adam_%28cropped%29.jpg/1280px-Michelangelo_-_Creation_of_Adam_%28cropped%29.jpg")`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                opacity: 0.25,
                filter: 'sepia(10%) contrast(1.15) brightness(1.05)'
              }}
            />
            {/* 达芬奇素描纹理叠加 - 动态 */}
            <motion.div 
              className="absolute inset-[-30px] pointer-events-none"
              animate={{ 
                rotate: [0, 1, -1, 0],
                scale: [1, 1.03, 1]
              }}
              transition={{ 
                duration: 15,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              style={{
                backgroundImage: `url("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg/800px-Da_Vinci_Vitruve_Luc_Viatour.jpg")`,
                backgroundSize: '500px',
                backgroundRepeat: 'repeat',
                backgroundPosition: 'center',
                opacity: 0.18,
                mixBlendMode: 'multiply',
                filter: 'contrast(1.2)'
              }}
            />
            {/* 装饰箭头 */}
            <div className="flex gap-0.5 mb-6">
              <ChevronDown className="w-5 h-5 text-brand-terracotta" />
              <ChevronDown className="w-5 h-5 text-brand-terracotta" />
            </div>

            {/* Logo区域 */}
            <div className="mb-6">
              <div className="flex items-start gap-2 mb-1">
                <div className="w-8 h-10 text-brand-charcoal">
                  <BuildingIcon className="w-full h-full" />
                </div>
              </div>
              <div className="font-serif text-xs tracking-[0.2em] text-brand-charcoal/60 uppercase leading-relaxed">
                Home<br/>mate<br/>
                <span className="text-brand-terracotta">AI Studio</span>
              </div>
            </div>

            {/* 主标题 - 黄金分割位置 */}
            <div className="flex-1 flex flex-col justify-start pt-[38.2%] py-8">
              <h1 className="font-serif text-4xl lg:text-5xl xl:text-6xl font-bold text-brand-charcoal leading-[1.1] tracking-tight uppercase">
                毛胚房
                <br />
                秒变
                <br />
                <span className="text-brand-terracotta">精装</span>
                <br />
                <span className="text-brand-terracotta">效果图</span>
              </h1>
            </div>

          </motion.div>

          {/* 中右区域 - Roommate大标题 */}
          <motion.div 
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:w-[61.8%] relative bg-brand-cream flex items-center justify-center"
          >
            <div className="h-[50vh] lg:h-screen flex flex-col items-center justify-center px-8 lg:px-16">
              {/* 超大标题 */}
              <h1 className="font-serif text-6xl sm:text-7xl md:text-8xl lg:text-9xl xl:text-[10rem] font-bold text-brand-charcoal tracking-tighter leading-none text-center w-full overflow-hidden">
                Roommate
              </h1>
              
              {/* 副标题 */}
              <p className="text-brand-charcoal/60 text-lg lg:text-xl mt-6 tracking-widest uppercase">
                AI Interior Design
              </p>
              
              {/* CTA按钮 */}
              <div className="flex gap-4 mt-10">
                <Link href="/studio" className="inline-flex items-center gap-2 bg-brand-terracotta text-white px-8 py-4 font-bold text-sm hover:bg-brand-charcoal transition-colors rounded-lg">
                  开始体验
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link href="#llm-section" className="inline-flex items-center gap-2 border-2 border-brand-charcoal text-brand-charcoal px-8 py-4 font-semibold text-sm hover:bg-brand-charcoal hover:text-white transition-colors rounded-lg">
                  了解更多
                </Link>
              </div>

              {/* 动态下拉箭头 */}
              <motion.div
                className="absolute bottom-12 left-1/2 -translate-x-1/2 cursor-pointer"
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                onClick={() => document.getElementById('llm-section')?.scrollIntoView({ behavior: 'smooth' })}
              >
                <div className="flex flex-col items-center gap-1 text-brand-charcoal/40 hover:text-brand-terracotta transition-colors">
                  <span className="text-xs tracking-widest uppercase">Scroll</span>
                  <ChevronDown className="w-6 h-6" />
                </div>
              </motion.div>
            </div>
          </motion.div>

        </div>
      </section>

      {/* 设计工作台 - 三栏布局 浅色主题 */}
      <section id="llm-section" className="h-[calc(100vh-80px)] bg-brand-cream flex flex-col overflow-hidden">
        {/* 隐藏的文件输入 */}
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleImageUpload}
          accept="image/*"
          className="hidden"
        />

        {/* 顶部栏 */}
        <div className="h-11 px-4 flex items-center justify-between bg-white border-b border-brand-charcoal/10 shrink-0">
          <div className="flex items-center gap-3">
            <span className="font-serif text-sm font-semibold text-brand-charcoal">Roommate</span>
            <span className="text-xs text-brand-charcoal/40">设计工作台</span>
            {images.length > 0 && (
              <span className="text-xs text-brand-terracotta bg-brand-terracotta/10 px-2 py-0.5 rounded-full">
                {images.length} 张图片
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            {images.length > 0 && (
              <button 
                onClick={handleClearAll}
                className="px-3 py-1.5 text-xs text-red-500 hover:text-red-600 hover:bg-red-50 rounded transition-all"
              >
                清空
              </button>
            )}
            <button 
              onClick={handleExport}
              className="px-3 py-1.5 text-xs text-brand-charcoal/60 hover:text-brand-charcoal hover:bg-brand-charcoal/5 rounded transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={!selectedImage}
            >
              导出图片
            </button>
          </div>
        </div>

        {/* 主内容区 - 三栏 */}
        <div className="flex-1 flex overflow-hidden">
          
          {/* 左侧 - 图片列表栏 */}
          <div className="w-20 bg-white border-r border-brand-charcoal/10 flex flex-col shrink-0">
            <div className="p-2 border-b border-brand-charcoal/10">
              <p className="text-[10px] text-brand-charcoal/40 text-center uppercase tracking-wider">图库</p>
            </div>
            <div className="flex-1 overflow-y-auto p-2 space-y-2">
              {/* 上传按钮 */}
              <div 
                onClick={() => fileInputRef.current?.click()}
                className="aspect-square rounded-lg bg-brand-cream border border-dashed border-brand-charcoal/20 flex items-center justify-center cursor-pointer hover:bg-brand-terracotta/5 hover:border-brand-terracotta/40 transition-all group"
              >
                <svg className="w-5 h-5 text-brand-charcoal/30 group-hover:text-brand-terracotta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 4v16m8-8H4" />
                </svg>
              </div>
              {/* 图片缩略图列表 */}
              {images.map((img) => (
                <div 
                  key={img.id}
                  onClick={() => setSelectedImage(img)}
                  className={`aspect-square rounded-lg overflow-hidden cursor-pointer transition-all relative group ${
                    selectedImage?.id === img.id 
                      ? 'ring-2 ring-brand-terracotta' 
                      : 'hover:ring-1 hover:ring-brand-charcoal/20'
                  }`}
                >
                  <img src={img.url} alt="" className="w-full h-full object-cover" loading="eager" />
                  {img.type === 'generated' && (
                    <div className="absolute bottom-0 left-0 right-0 bg-brand-terracotta/90 text-white text-[8px] text-center py-0.5">
                      {img.style}
                    </div>
                  )}
                  <div className="absolute top-1 right-1 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={(e) => { e.stopPropagation(); handleDownloadImage(img); }}
                      className="w-4 h-4 bg-black/50 rounded-full flex items-center justify-center hover:bg-brand-terracotta"
                    >
                      <Download className="w-2.5 h-2.5 text-white" />
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleDeleteImage(img.id); }}
                      className="w-4 h-4 bg-black/50 rounded-full flex items-center justify-center hover:bg-red-500"
                    >
                      <X className="w-3 h-3 text-white" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 中间 - 大图预览区 */}
          <motion.div 
            className="flex-1 flex items-center justify-center p-6 bg-brand-cream/50"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.4 }}
            viewport={{ once: true }}
          >
            <div 
              onClick={() => !selectedImage && !isGenerating && fileInputRef.current?.click()}
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              className={`w-full h-full max-w-5xl rounded-2xl bg-white border border-brand-charcoal/10 shadow-sm flex items-center justify-center transition-all overflow-hidden relative ${
                !selectedImage && !isGenerating ? 'cursor-pointer group hover:border-brand-terracotta/30 hover:shadow-md' : ''
              }`}
            >
              {/* 生成中遮罩 */}
              {isGenerating && (
                <div className="absolute inset-0 bg-white/90 backdrop-blur-sm flex flex-col items-center justify-center z-10">
                  <Loader2 className="w-12 h-12 text-brand-terracotta animate-spin mb-4" />
                  <p className="text-brand-charcoal font-medium mb-2">正在生成 {designStyles[selectedStyle]} 效果图...</p>
                  <div className="w-48 h-2 bg-brand-cream rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-brand-terracotta transition-all duration-300"
                      style={{ width: `${generatingProgress}%` }}
                    />
                  </div>
                  <p className="text-brand-charcoal/40 text-sm mt-2">{Math.round(generatingProgress)}%</p>
                </div>
              )}

              {selectedImage ? (
                editMode === 'segment' ? (
                  /* 局部替换模式 - 使用 SegmentableImage（支持原图和生成图） */
                  <SegmentableImage
                    imageUrl={selectedImage.url}
                    imageBase64={selectedImage.base64}
                    cachedSegments={segmentsCache[selectedImage.id]}
                    onSegmentsLoaded={(segments) => {
                      // 缓存识别结果
                      storeSetSegmentsCache(selectedImage.id, segments)
                    }}
                    onSegmentSelect={(segment, maskUrl) => {
                      // 多选模式：添加或移除
                      const segKey = `${segment.label}-${segment.bbox?.join(',')}`
                      setSelectedSegments(prev => {
                        const exists = prev.some(s => `${s.label}-${s.bbox?.join(',')}` === segKey)
                        if (exists) {
                          return prev.filter(s => `${s.label}-${s.bbox?.join(',')}` !== segKey)
                        }
                        return [...prev, segment]
                      })
                    }}
                    className="w-full h-full"
                  />
                ) : (
                  /* 普通预览模式 */
                  <div className="w-full h-full relative flex items-center justify-center">
                    {/* 加载中指示器 */}
                    {!loadedImages.has(selectedImage.id) && !selectedImage.url.startsWith('blob:') && (
                      <div className="absolute inset-0 flex items-center justify-center bg-brand-cream/50">
                        <Loader2 className="w-8 h-8 text-brand-terracotta animate-spin" />
                      </div>
                    )}
                    <img 
                      src={selectedImage.url} 
                      alt="" 
                      className="w-full h-full object-contain"
                      loading="eager"
                    />
                    {selectedImage.type === 'generated' && (
                      <div className="absolute top-4 left-4 px-3 py-1.5 bg-brand-terracotta text-white text-xs rounded-full flex items-center gap-1.5">
                        <Sparkles className="w-3 h-3" />
                        {selectedImage.style} · AI生成
                      </div>
                    )}
                    {selectedImage.type === 'original' && (
                      <div className="absolute top-4 left-4 px-3 py-1.5 bg-brand-charcoal/80 text-white text-xs rounded-full">
                        毛坯原图
                      </div>
                    )}
                    {/* 图片信息 */}
                    <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between">
                      <span className="text-xs text-brand-charcoal/60 bg-white/80 backdrop-blur px-2 py-1 rounded">
                        {selectedImage.name}
                      </span>
                      <button
                        onClick={handleExport}
                        className="text-xs text-white bg-brand-charcoal/80 hover:bg-brand-terracotta px-3 py-1.5 rounded transition-colors"
                      >
                        下载图片
                      </button>
                    </div>
                  </div>
                )
              ) : (
                <div className="text-center">
                  <div className="w-20 h-20 rounded-2xl bg-brand-cream group-hover:bg-brand-terracotta/10 flex items-center justify-center mx-auto mb-4 transition-colors">
                    <ImageIcon className="w-10 h-10 text-brand-charcoal/20 group-hover:text-brand-terracotta transition-colors" />
                  </div>
                  <p className="text-brand-charcoal/70 font-medium mb-1">上传毛坯房照片</p>
                  <p className="text-brand-charcoal/40 text-sm mb-4">点击或拖拽图片到此处</p>
                  <div className="flex items-center gap-2 justify-center">
                    <button
                      onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}
                      className="px-4 py-2 bg-brand-charcoal text-white text-xs rounded-lg hover:bg-brand-terracotta transition-colors"
                    >
                      选择文件
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); loadSampleOriginal(); }}
                      className="px-4 py-2 bg-brand-cream text-brand-charcoal text-xs rounded-lg hover:bg-brand-terracotta/10 transition-colors border border-brand-charcoal/20"
                    >
                      使用示例图片
                    </button>
                  </div>
                </div>
              )}
            </div>
          </motion.div>

          {/* 右侧 - 控制面板 */}
          <motion.div 
            className="w-72 bg-white border-l border-brand-charcoal/10 flex flex-col shrink-0"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4 }}
            viewport={{ once: true }}
          >
            {/* 模式切换 */}
            <div className="p-3 border-b border-brand-charcoal/10">
              <div className="flex gap-1 p-1 bg-brand-cream rounded-lg">
                <button
                  onClick={() => setEditMode('full')}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-md text-xs font-medium transition-all ${
                    editMode === 'full' 
                      ? 'bg-white text-brand-charcoal shadow-sm' 
                      : 'text-brand-charcoal/50 hover:text-brand-charcoal'
                  }`}
                >
                  <Sparkles className="w-3 h-3" />
                  整体风格
                </button>
                <button
                  onClick={() => setEditMode('segment')}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-md text-xs font-medium transition-all ${
                    editMode === 'segment' 
                      ? 'bg-white text-brand-charcoal shadow-sm' 
                      : 'text-brand-charcoal/50 hover:text-brand-charcoal'
                  }`}
                >
                  <Layers className="w-3 h-3" />
                  局部替换
                </button>
              </div>
            </div>

            {/* AI 提示 */}
            <div className="p-4 border-b border-brand-charcoal/10">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-6 h-6 rounded-full bg-gradient-to-br from-brand-terracotta to-orange-400 flex items-center justify-center">
                  <Sparkles className="w-3 h-3 text-white" />
                </div>
                <span className="text-xs font-medium text-brand-charcoal">AI 设计助手</span>
              </div>
              <p className="text-xs text-brand-charcoal/50 leading-relaxed">
                {editMode === 'segment' 
                  ? selectedSegments.length > 0 
                    ? `已选择 ${selectedSegments.length} 个区域，选择风格后替换`
                    : '点击图片识别家具，然后选择要替换的区域'
                  : selectedImage 
                    ? selectedImage.type === 'original' 
                      ? '已上传毛坯图，选择风格后点击生成' 
                      : '效果图已生成，可继续生成其他风格'
                    : '请先上传毛坯房照片'}
              </p>
            </div>

            {editMode === 'full' ? (
              <>
                {/* 风格选择 */}
                <div className="p-4 border-b border-brand-charcoal/10">
                  <p className="text-[10px] font-medium text-brand-charcoal/40 uppercase tracking-wider mb-3">设计风格</p>
                  <div className="grid grid-cols-2 gap-1.5">
                    {designStyles.map((style, i) => (
                      <button 
                        key={style}
                        onClick={() => setSelectedStyle(i)}
                        className={`px-2 py-2 text-xs rounded-md transition-all ${
                          selectedStyle === i 
                            ? 'bg-brand-terracotta text-white' 
                            : 'bg-brand-cream text-brand-charcoal/60 hover:bg-brand-terracotta/10 hover:text-brand-terracotta'
                        }`}
                      >
                        {style}
                      </button>
                    ))}
                  </div>
                </div>

                {/* 描述输入 */}
                <div className="p-4 flex-1">
                  <p className="text-[10px] font-medium text-brand-charcoal/40 uppercase tracking-wider mb-3">效果描述</p>
                  <textarea 
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="描述你想要的效果，如：明亮的客厅，落地窗，木质地板..."
                    rows={5}
                    className="w-full p-3 text-xs text-brand-charcoal placeholder:text-brand-charcoal/30 bg-brand-cream rounded-lg border border-brand-charcoal/10 focus:outline-none focus:border-brand-terracotta/50 resize-none"
                  />
                </div>
              </>
            ) : (
              <>
                {/* 局部替换 - 已选区域列表 */}
                <div className="p-4 border-b border-brand-charcoal/10">
                  <div className="flex items-center justify-between mb-3">
                    <p className="text-[10px] font-medium text-brand-charcoal/40 uppercase tracking-wider">
                      已选区域 ({selectedSegments.length})
                    </p>
                    {selectedSegments.length > 0 && (
                      <button
                        onClick={() => setSelectedSegments([])}
                        className="text-[10px] text-brand-charcoal/40 hover:text-brand-terracotta"
                      >
                        清空
                      </button>
                    )}
                  </div>
                  {selectedSegments.length > 0 ? (
                    <div className="space-y-1.5 max-h-32 overflow-y-auto">
                      {selectedSegments.map((seg, idx) => (
                        <div key={idx} className="p-2 bg-brand-terracotta/10 rounded-lg flex items-center justify-between">
                          <span className="text-xs font-medium text-brand-terracotta">{seg.label_zh}</span>
                          <button
                            onClick={() => {
                              const segKey = `${seg.label}-${seg.bbox?.join(',')}`
                              setSelectedSegments(prev => prev.filter(s => `${s.label}-${s.bbox?.join(',')}` !== segKey))
                            }}
                            className="p-0.5 hover:bg-brand-terracotta/20 rounded"
                          >
                            <X className="w-3 h-3 text-brand-terracotta" />
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="p-3 bg-brand-cream rounded-lg text-center">
                      <p className="text-xs text-brand-charcoal/50">
                        在左侧图片中点击"识别家具"，然后选择要替换的区域
                      </p>
                    </div>
                  )}
                </div>

                {/* 替换风格 */}
                <div className="p-4 flex-1 overflow-y-auto">
                  <p className="text-[10px] font-medium text-brand-charcoal/40 uppercase tracking-wider mb-3">
                    替换风格 {selectedReplaceStyle && <span className="text-brand-terracotta">✓</span>}
                  </p>
                  <div className="grid grid-cols-2 gap-1.5">
                    {replaceStyles.map((style) => (
                      <button 
                        key={style.id}
                        onClick={() => setSelectedReplaceStyle(style.id)}
                        disabled={selectedSegments.length === 0}
                        className={`px-2 py-2 text-xs rounded-md transition-all ${
                          selectedReplaceStyle === style.id
                            ? 'bg-brand-terracotta text-white'
                            : selectedSegments.length > 0
                            ? 'bg-brand-cream text-brand-charcoal/60 hover:bg-brand-terracotta hover:text-white'
                            : 'bg-brand-cream/50 text-brand-charcoal/30 cursor-not-allowed'
                        }`}
                      >
                        {style.name}
                      </button>
                    ))}
                  </div>
                  {selectedSegments.length === 0 && (
                    <p className="mt-2 text-[10px] text-brand-charcoal/40">请先选择要替换的区域</p>
                  )}
                </div>
              </>
            )}

            {/* 生成按钮 */}
            <div className="p-4 border-t border-brand-charcoal/10">
              {editMode === 'segment' ? (
                <div className="space-y-2">
                  <button 
                    onClick={handleSegmentReplace}
                    disabled={selectedSegments.length === 0 || !selectedReplaceStyle || isReplacing}
                    className="w-full py-3 bg-brand-charcoal text-white text-sm font-medium rounded-lg hover:bg-brand-terracotta transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isReplacing ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        处理中 {generatingProgress > 0 && `${Math.round(generatingProgress)}%`}
                      </>
                    ) : (
                      <>
                        替换选中区域
                        <ArrowRight className="w-4 h-4" />
                      </>
                    )}
                  </button>
                  <button 
                    onClick={handleSegmentErase}
                    disabled={selectedSegments.length === 0 || isReplacing}
                    className="w-full py-2.5 bg-red-500/10 text-red-600 text-sm font-medium rounded-lg hover:bg-red-500/20 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Eraser className="w-4 h-4" />
                    抹除选中区域
                  </button>
                </div>
              ) : (
                <button 
                  onClick={handleGenerate}
                  disabled={!images.some(img => img.type === 'original') || isGenerating}
                  className="w-full py-3 bg-brand-charcoal text-white text-sm font-medium rounded-lg hover:bg-brand-terracotta transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      生成中 {generatingProgress > 0 && `${Math.round(generatingProgress)}%`}
                    </>
                  ) : (
                    <>
                      生成效果图
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              )}
                          </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 bg-brand-charcoal">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <span className="font-serif text-white text-lg">Roommate AI</span>
          <p className="text-sm text-white/40">
            © 2026 Roommate AI. All rights reserved.
          </p>
        </div>
      </footer>
    </main>
  )
}
