'use client'

import { useRef } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, Play, Check } from 'lucide-react'
import { ShimmerButton } from '@/components/magicui/shimmer-button'
import { BlurFade } from '@/components/magicui/blur-fade'
import { NumberTicker } from '@/components/magicui/number-ticker'

const stats = [
  { value: 78, suffix: '秒', label: '平均出图时间' },
  { value: 0.18, suffix: '元', label: '每张成本', prefix: '¥' },
  { value: 4, suffix: 'K', label: '超清分辨率' },
  { value: 10, suffix: '+', label: '设计风格' },
]

const styles = [
  { name: '侘寂极简', en: 'Wabi-Sabi', image: '/images/styles/wabi-sabi.jpg' },
  { name: '奶油法式', en: 'Cream French', image: '/images/styles/cream.jpg' },
  { name: '现代轻奢', en: 'Modern Luxury', image: '/images/styles/luxury.jpg' },
  { name: '新中式', en: 'Neo Chinese', image: '/images/styles/chinese.jpg' },
]

const features = [
  { title: '毛胚房秒变精装', desc: '上传一张毛胚房照片，AI自动识别空间结构，智能生成精装效果图' },
  { title: '商业级4K品质', desc: '采用专业级渲染引擎，输出4K超清图片，细节纤毫毕现' },
  { title: '10+顶级设计风格', desc: '侘寂、奶油风、新中式、北欧等主流风格，一键切换' },
]

export default function HomePage() {
  const containerRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end start'],
  })
  
  const y = useTransform(scrollYProgress, [0, 1], ['0%', '50%'])
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])

  return (
    <main className="bg-[#fafafa]">
      {/* Hero - Apple Style Full Screen */}
      <section ref={containerRef} className="relative min-h-screen flex flex-col justify-center overflow-hidden">
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-b from-white via-stone-50 to-stone-100" />
        
        {/* Content */}
        <motion.div style={{ y, opacity }} className="relative z-10 max-w-6xl mx-auto px-6 pt-32 pb-20">
          <div className="text-center">
            {/* Eyebrow */}
            <BlurFade delay={0.1} inView>
              <p className="text-sm font-medium tracking-widest text-stone-500 uppercase mb-6">
                AI Interior Design
              </p>
            </BlurFade>

            {/* Headline - Apple Style Large Typography */}
            <BlurFade delay={0.2} inView>
              <h1 className="text-[clamp(3rem,8vw,7rem)] font-bold text-stone-900 leading-[0.95] tracking-tight mb-8">
                将毛胚房
                <br />
                <span className="bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 bg-clip-text text-transparent">
                  一键变精装
                </span>
              </h1>
            </BlurFade>

            {/* Subheadline */}
            <BlurFade delay={0.3} inView>
              <p className="text-xl md:text-2xl text-stone-600 max-w-2xl mx-auto mb-12 leading-relaxed">
                78秒出图，4K超清，¥0.18/张
                <br className="hidden md:block" />
                专为房地产开发商、室内设计师打造
              </p>
            </BlurFade>

            {/* CTA Buttons */}
            <BlurFade delay={0.4} inView>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link href="/studio">
                  <ShimmerButton className="h-14 px-8">
                    <span className="text-base font-medium">开始设计</span>
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </ShimmerButton>
                </Link>
                <button className="group flex items-center gap-3 h-14 px-6 text-stone-700 hover:text-stone-900 transition-colors">
                  <div className="w-12 h-12 rounded-full bg-stone-900 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Play className="w-5 h-5 text-white ml-0.5" fill="white" />
                  </div>
                  <span className="font-medium">观看演示</span>
                </button>
              </div>
            </BlurFade>
          </div>
        </motion.div>

        {/* Hero Image - Floating Card */}
        <BlurFade delay={0.6} inView>
          <div className="relative z-10 max-w-5xl mx-auto px-6 -mt-8">
            <div className="relative rounded-3xl overflow-hidden shadow-2xl shadow-stone-900/10">
              <div className="aspect-[16/9] bg-stone-200">
                <img 
                  src="https://file2.aitohumanize.com/file/4228ee00ad7040908b83e6dd9157db69.png"
                  alt="AI室内设计效果图"
                  className="w-full h-full object-cover"
                />
              </div>
              {/* Floating Label */}
              <div className="absolute bottom-6 left-6 px-4 py-2 bg-white/90 backdrop-blur-sm rounded-full text-sm font-medium text-stone-700">
                侘寂风格 · 客厅 · 4K
              </div>
            </div>
          </div>
        </BlurFade>

        {/* Scroll Indicator */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
        >
          <div className="w-6 h-10 rounded-full border-2 border-stone-300 flex justify-center pt-2">
            <motion.div 
              animate={{ y: [0, 8, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="w-1.5 h-1.5 bg-stone-400 rounded-full"
            />
          </div>
        </motion.div>
      </section>

      {/* Stats Section - Clean Grid */}
      <section className="py-24 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-4">
            {stats.map((stat, i) => (
              <BlurFade key={i} delay={0.1 * i} inView>
                <div className="text-center">
                  <p className="text-4xl md:text-5xl font-bold text-stone-900 mb-2">
                    {stat.prefix}
                    <NumberTicker value={stat.value} decimalPlaces={stat.value < 1 ? 2 : 0} />
                    {stat.suffix}
                  </p>
                  <p className="text-sm text-stone-500">{stat.label}</p>
                </div>
              </BlurFade>
            ))}
          </div>
        </div>
      </section>

      {/* Features - Large Cards */}
      <section className="py-32 bg-[#fafafa]">
        <div className="max-w-6xl mx-auto px-6">
          <BlurFade inView>
            <p className="text-sm font-medium tracking-widest text-stone-500 uppercase text-center mb-4">
              Why NanoBanana
            </p>
            <h2 className="text-4xl md:text-5xl font-bold text-stone-900 text-center mb-20">
              为什么选择我们
            </h2>
          </BlurFade>

          <div className="space-y-8">
            {features.map((feature, i) => (
              <BlurFade key={i} delay={0.1 * i} inView>
                <div className="group relative bg-white rounded-3xl p-8 md:p-12 hover:shadow-xl transition-shadow duration-500">
                  <div className="flex flex-col md:flex-row md:items-center gap-6">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-stone-100 to-stone-200 flex items-center justify-center text-3xl font-bold text-stone-400 group-hover:from-amber-100 group-hover:to-orange-100 group-hover:text-amber-600 transition-all duration-500">
                      {String(i + 1).padStart(2, '0')}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-stone-900 mb-2">{feature.title}</h3>
                      <p className="text-lg text-stone-600">{feature.desc}</p>
                    </div>
                    <ArrowRight className="w-6 h-6 text-stone-300 group-hover:text-stone-600 group-hover:translate-x-2 transition-all" />
                  </div>
                </div>
              </BlurFade>
            ))}
          </div>
        </div>
      </section>

      {/* Styles Showcase - Horizontal Scroll Look */}
      <section className="py-32 bg-stone-900 text-white overflow-hidden">
        <div className="max-w-6xl mx-auto px-6">
          <BlurFade inView>
            <p className="text-sm font-medium tracking-widest text-stone-500 uppercase text-center mb-4">
              Design Styles
            </p>
            <h2 className="text-4xl md:text-5xl font-bold text-center mb-6">
              10+ 顶级设计风格
            </h2>
            <p className="text-lg text-stone-400 text-center max-w-2xl mx-auto mb-16">
              从侘寂极简到现代轻奢，覆盖主流审美需求
            </p>
          </BlurFade>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {styles.map((style, i) => (
              <BlurFade key={i} delay={0.1 * i} inView>
                <div className="group relative aspect-[3/4] rounded-2xl overflow-hidden cursor-pointer">
                  <div className="absolute inset-0 bg-gradient-to-br from-stone-700 to-stone-800" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                  <div className="absolute bottom-0 left-0 right-0 p-6">
                    <p className="text-xs text-stone-400 uppercase tracking-wider mb-1">{style.en}</p>
                    <p className="text-xl font-bold">{style.name}</p>
                  </div>
                  {/* Hover Effect */}
                  <div className="absolute inset-0 bg-amber-500/20 opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </BlurFade>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link href="/gallery" className="inline-flex items-center gap-2 text-stone-400 hover:text-white transition-colors">
              <span>查看全部风格</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Pricing Preview */}
      <section className="py-32 bg-white">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <BlurFade inView>
            <p className="text-sm font-medium tracking-widest text-stone-500 uppercase mb-4">
              Simple Pricing
            </p>
            <h2 className="text-4xl md:text-5xl font-bold text-stone-900 mb-6">
              透明定价，按量付费
            </h2>
            <p className="text-lg text-stone-600 mb-12">
              首张免费体验，无需绑定信用卡
            </p>
          </BlurFade>

          <BlurFade delay={0.2} inView>
            <div className="inline-block bg-stone-50 rounded-3xl p-8 md:p-12">
              <div className="flex items-baseline justify-center gap-2 mb-4">
                <span className="text-6xl md:text-7xl font-bold text-stone-900">¥0.18</span>
                <span className="text-xl text-stone-500">/张</span>
              </div>
              <p className="text-stone-600 mb-8">4K超清分辨率</p>
              <ul className="text-left space-y-3 mb-8">
                {['4K超清输出', '10+设计风格', '78秒极速出图', '商用授权'].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-stone-700">
                    <Check className="w-5 h-5 text-green-500" />
                    {item}
                  </li>
                ))}
              </ul>
              <Link href="/studio">
                <button className="w-full h-14 bg-stone-900 text-white font-medium rounded-xl hover:bg-stone-800 transition-colors">
                  免费体验
                </button>
              </Link>
            </div>
          </BlurFade>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-32 bg-stone-900">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <BlurFade inView>
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
              开始你的设计之旅
            </h2>
            <p className="text-xl text-stone-400 mb-12">
              加入 10,000+ 设计师和开发商的选择
            </p>
            <Link href="/studio">
              <ShimmerButton className="h-16 px-12">
                <span className="text-lg font-medium">立即开始</span>
                <ArrowRight className="w-5 h-5 ml-2" />
              </ShimmerButton>
            </Link>
          </BlurFade>
        </div>
      </section>
    </main>
  )
}
