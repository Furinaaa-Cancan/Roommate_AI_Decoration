'use client'

import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'
import Link from 'next/link'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-brand-cream pt-20">
      {/* Hero */}
      <section className="py-24 px-6 bg-gradient-to-b from-brand-charcoal to-brand-charcoal/95">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-5xl font-serif font-bold text-white mb-8 leading-tight">
              关于 Roommate AI
            </h1>
            <p className="text-xl text-white/70 leading-relaxed max-w-3xl mx-auto">
              我们正在用 AI 技术，让室内设计变得更简单。
            </p>
          </motion.div>
        </div>
      </section>

      {/* What we do */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-serif font-bold text-brand-charcoal mb-8">我们在做什么</h2>
            <div className="prose prose-lg max-w-none text-brand-charcoal/70">
              <p>
                Roommate AI 是一个 AI 室内设计工具。上传一张毛胚房或现有空间的照片，
                AI 会帮你生成装修效果图。
              </p>
              <p>
                我们希望解决的问题是：在装修之前，很难直观地看到装修后的效果。
                传统效果图需要找设计师，又贵又慢。我们想让这件事变得简单。
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Current Stage */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-serif font-bold text-brand-charcoal mb-8">当前阶段</h2>
            <div className="bg-brand-cream rounded-2xl p-6">
              <p className="text-brand-charcoal/70 leading-relaxed">
                我们目前处于<strong className="text-brand-charcoal">早期开发阶段</strong>，
                正在不断完善产品功能和提升生成效果。如果你在使用过程中遇到问题或有建议，
                欢迎随时<Link href="/contact" className="text-brand-terracotta hover:underline">联系我们</Link>。
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">
              试试看？
            </h2>
            <p className="text-brand-charcoal/60 mb-8">
              上传一张照片，看看 AI 能生成什么效果
            </p>
            <Link
              href="/"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-brand-charcoal text-white font-medium rounded-full hover:bg-brand-terracotta transition-colors"
            >
              开始体验
              <ArrowRight className="w-4 h-4" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
