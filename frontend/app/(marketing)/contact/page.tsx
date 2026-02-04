'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Send, Mail, MessageCircle, ArrowRight } from 'lucide-react'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    email: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsSubmitting(false)
    setSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-brand-cream pt-20">
      {/* Hero */}
      <section className="py-24 px-6 bg-brand-charcoal relative overflow-hidden">
        {/* 装饰背景 */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-brand-terracotta rounded-full blur-3xl" />
          <div className="absolute bottom-10 right-20 w-96 h-96 bg-brand-terracotta rounded-full blur-3xl" />
        </div>
        
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="w-16 h-16 bg-brand-terracotta/20 rounded-2xl flex items-center justify-center mx-auto mb-8">
              <MessageCircle className="w-8 h-8 text-brand-terracotta" />
            </div>
            <h1 className="text-4xl md:text-5xl font-serif font-bold text-white mb-6">
              联系我们
            </h1>
            <p className="text-xl text-white/60 leading-relaxed max-w-xl mx-auto">
              有问题、建议或者只是想打个招呼？<br />我们很乐意听到你的声音。
            </p>
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-5 gap-12">
            {/* Left - Email */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="md:col-span-2"
            >
              <div className="sticky top-32">
                <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">
                  直接发邮件
                </h2>
                <div className="bg-white rounded-2xl p-6 shadow-sm border border-brand-charcoal/5">
                  <div className="w-12 h-12 bg-brand-terracotta/10 rounded-xl flex items-center justify-center mb-4">
                    <Mail className="w-6 h-6 text-brand-terracotta" />
                  </div>
                  <a 
                    href="mailto:cancansauce@gmail.com" 
                    className="text-lg font-medium text-brand-charcoal hover:text-brand-terracotta transition-colors flex items-center gap-2 group"
                  >
                    cancansauce@gmail.com
                    <ArrowRight className="w-4 h-4 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                  </a>
                  <p className="text-brand-charcoal/50 text-sm mt-3 leading-relaxed">
                    产品问题、功能建议、<br />合作咨询都可以发到这里
                  </p>
                </div>
              </div>
            </motion.div>

            {/* Right - Form */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="md:col-span-3"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">
                或者在这里留言
              </h2>
              <div className="bg-white rounded-2xl p-8 shadow-sm border border-brand-charcoal/5">
                {submitted ? (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center py-12"
                  >
                    <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                      <Send className="w-10 h-10 text-green-600" />
                    </div>
                    <h3 className="text-2xl font-serif font-bold text-brand-charcoal mb-3">
                      消息已发送 ✨
                    </h3>
                    <p className="text-brand-charcoal/60">
                      感谢你的留言，我们会尽快回复！
                    </p>
                  </motion.div>
                ) : (
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-brand-charcoal mb-2">
                        你的邮箱
                      </label>
                      <input
                        type="email"
                        required
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        className="w-full px-4 py-3.5 bg-brand-cream/30 rounded-xl border border-brand-charcoal/10 focus:outline-none focus:ring-2 focus:ring-brand-terracotta/50 focus:border-transparent transition-all"
                        placeholder="方便我们回复你"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-brand-charcoal mb-2">
                        想说什么
                      </label>
                      <textarea
                        required
                        rows={5}
                        value={formData.message}
                        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                        className="w-full px-4 py-3.5 bg-brand-cream/30 rounded-xl border border-brand-charcoal/10 focus:outline-none focus:ring-2 focus:ring-brand-terracotta/50 focus:border-transparent resize-none transition-all"
                        placeholder="问题、建议、或者只是打个招呼..."
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full py-4 bg-brand-charcoal text-white font-medium rounded-xl hover:bg-brand-terracotta transition-all disabled:opacity-50 flex items-center justify-center gap-2 group"
                    >
                      {isSubmitting ? (
                        '发送中...'
                      ) : (
                        <>
                          发送消息
                          <Send className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </>
                      )}
                    </button>
                  </form>
                )}
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  )
}
