'use client'

import { motion } from 'framer-motion'
import { Shield, Info } from 'lucide-react'
import Link from 'next/link'

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-brand-cream pt-20">
      {/* Hero */}
      <section className="py-20 px-6 bg-gradient-to-b from-brand-charcoal to-brand-charcoal/95">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-5xl font-serif font-bold text-white mb-6">
              隐私政策
            </h1>
            <p className="text-white/40 text-sm">最后更新：2026年1月20日</p>
          </motion.div>
        </div>
      </section>

      {/* Plain Language Summary - 人话版摘要 */}
      <section className="py-12 px-6 bg-brand-terracotta/10 border-b border-brand-terracotta/20">
        <div className="max-w-3xl mx-auto">
          <div className="flex gap-4">
            <Info className="w-6 h-6 text-brand-terracotta flex-shrink-0 mt-1" />
            <div>
              <h2 className="font-semibold text-brand-charcoal mb-2">简单来说</h2>
              <p className="text-brand-charcoal/70 leading-relaxed">
                我们只收集提供服务必需的信息。你上传的照片只用于生成效果图，不会用于其他目的。
                我们不会把你的数据卖给任何人。你可以随时删除你的账户和所有数据。
                如果有任何疑问，发邮件给 <a href="mailto:cancansauce@gmail.com" className="text-brand-terracotta">cancansauce@gmail.com</a>，我们会尽快回复。
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Nav */}
      <section className="py-6 px-6 bg-white border-b border-brand-charcoal/5 sticky top-20 z-40">
        <div className="max-w-3xl mx-auto">
          <div className="flex flex-wrap gap-3 text-sm">
            <a href="#collect" className="text-brand-charcoal/60 hover:text-brand-terracotta">收集什么</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#use" className="text-brand-charcoal/60 hover:text-brand-terracotta">怎么用</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#share" className="text-brand-charcoal/60 hover:text-brand-terracotta">第三方</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#rights" className="text-brand-charcoal/60 hover:text-brand-terracotta">你的权利</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#cookie" className="text-brand-charcoal/60 hover:text-brand-terracotta">Cookie</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#contact" className="text-brand-charcoal/60 hover:text-brand-terracotta">联系我们</a>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-12 px-6">
        <div className="max-w-3xl mx-auto">
          <div className="prose prose-stone max-w-none">
            
            {/* 1. 收集什么 */}
            <motion.div
              id="collect"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">1. 我们收集什么信息</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">账户信息</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>邮箱地址（用于登录和通知）</li>
                <li>密码（加密存储，我们无法看到明文）</li>
                <li>头像和昵称（可选，你可以不填）</li>
                <li>第三方登录信息（如使用 Google 登录）</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">你上传的内容</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>原始照片：你上传的毛胚房图片</li>
                <li>生成结果：AI 生成的效果图</li>
                <li>这些内容只用于提供服务，不会用于训练 AI 模型</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">自动收集的信息</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>IP 地址（用于安全防护和区域识别）</li>
                <li>浏览器和设备信息（用于适配和问题排查）</li>
                <li>使用日志（你用了哪些功能、停留时长等）</li>
                <li>Cookie 和类似技术（见下方 Cookie 政策）</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">支付信息</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>订单记录（订单号、购买时间、金额）</li>
                <li>我们<strong>不存储</strong>你的银行卡号或支付密码</li>
                <li>支付由支付宝/微信支付/Stripe 处理</li>
              </ul>
            </motion.div>

            {/* 2. 怎么用 */}
            <motion.div
              id="use"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">2. 我们如何使用这些信息</h2>
              
              <div className="bg-white rounded-xl p-6 mb-6">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-brand-charcoal/10">
                      <th className="text-left py-3 text-brand-charcoal font-semibold">信息类型</th>
                      <th className="text-left py-3 text-brand-charcoal font-semibold">用途</th>
                    </tr>
                  </thead>
                  <tbody className="text-brand-charcoal/70">
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">邮箱</td>
                      <td className="py-3">登录验证、发送账单、重要通知</td>
                    </tr>
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">上传的照片</td>
                      <td className="py-3">生成效果图（处理完成后可删除）</td>
                    </tr>
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">使用日志</td>
                      <td className="py-3">改进产品、排查问题</td>
                    </tr>
                    <tr>
                      <td className="py-3">IP 地址</td>
                      <td className="py-3">安全防护、防止滥用</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <p className="text-brand-charcoal/70">
                <strong className="text-brand-charcoal">我们不会：</strong>
                将你的照片用于 AI 训练、出售你的个人信息、向你发送垃圾邮件（营销邮件可以退订）。
              </p>
            </motion.div>

            {/* 3. 第三方 */}
            <motion.div
              id="share"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">3. 我们与谁共享信息</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">服务提供商</h3>
              <p className="text-brand-charcoal/70 mb-4">我们使用第三方服务来运营平台（如云服务、支付处理等）。这些服务提供商只能在提供服务所必需的范围内访问你的数据。</p>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">法律要求</h3>
              <p className="text-brand-charcoal/70">
                如果法律要求（如法院传票、政府调查），我们可能被迫披露你的信息。
                这种情况下，我们会在法律允许的范围内通知你。
              </p>

              <div className="bg-green-50 border border-green-200 rounded-xl p-4 mt-6">
                <p className="text-green-800 text-sm">
                  <strong>我们承诺：</strong>绝不出售你的个人信息给广告商或数据经纪商。
                </p>
              </div>
            </motion.div>

            {/* 4. 你的权利 */}
            <motion.div
              id="rights"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">4. 你的权利</h2>
              
              <p className="text-brand-charcoal/70 mb-6">
                根据《个人信息保护法》和其他适用法律，你有以下权利：
              </p>

              <div className="space-y-4">
                <div className="bg-white rounded-xl p-5">
                  <h4 className="font-semibold text-brand-charcoal mb-2">查看和下载你的数据</h4>
                  <p className="text-brand-charcoal/60 text-sm">在账户设置中，你可以查看和导出你的所有数据。</p>
                </div>
                <div className="bg-white rounded-xl p-5">
                  <h4 className="font-semibold text-brand-charcoal mb-2">更正信息</h4>
                  <p className="text-brand-charcoal/60 text-sm">你可以随时在账户设置中修改你的个人信息。</p>
                </div>
                <div className="bg-white rounded-xl p-5">
                  <h4 className="font-semibold text-brand-charcoal mb-2">删除账户</h4>
                  <p className="text-brand-charcoal/60 text-sm">你可以在账户设置中申请删除账户。删除后，你的所有数据将在 30 天内永久清除。</p>
                </div>
                <div className="bg-white rounded-xl p-5">
                  <h4 className="font-semibold text-brand-charcoal mb-2">撤回同意</h4>
                  <p className="text-brand-charcoal/60 text-sm">你可以随时退订营销邮件，或在 Cookie 设置中关闭非必要 Cookie。</p>
                </div>
              </div>

              <p className="text-brand-charcoal/70 mt-6">
                如需行使这些权利或有任何疑问，请联系 <a href="mailto:cancansauce@gmail.com" className="text-brand-terracotta">cancansauce@gmail.com</a>。
                我们会尽快回复。
              </p>
            </motion.div>

            {/* 5. Cookie */}
            <motion.div
              id="cookie"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">5. Cookie 政策</h2>
              
              <p className="text-brand-charcoal/70 mb-4">
                我们使用 Cookie 和类似技术来记住你的登录状态、保存偏好设置、分析网站使用情况。
              </p>

              <div className="bg-white rounded-xl p-6">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-brand-charcoal/10">
                      <th className="text-left py-3 text-brand-charcoal font-semibold">类型</th>
                      <th className="text-left py-3 text-brand-charcoal font-semibold">用途</th>
                      <th className="text-left py-3 text-brand-charcoal font-semibold">可否关闭</th>
                    </tr>
                  </thead>
                  <tbody className="text-brand-charcoal/70">
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">必要 Cookie</td>
                      <td className="py-3">登录、安全、基本功能</td>
                      <td className="py-3">否</td>
                    </tr>
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">功能 Cookie</td>
                      <td className="py-3">记住偏好设置</td>
                      <td className="py-3">是</td>
                    </tr>
                    <tr>
                      <td className="py-3">分析 Cookie</td>
                      <td className="py-3">了解用户如何使用网站</td>
                      <td className="py-3">是</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <p className="text-brand-charcoal/70 mt-4">
                你可以通过浏览器设置管理或删除 Cookie。但关闭必要 Cookie 可能导致部分功能无法使用。
              </p>
            </motion.div>

            {/* 6. 联系我们 */}
            <motion.div
              id="contact"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">6. 联系我们</h2>
              
              <div className="bg-brand-charcoal rounded-xl p-6 text-center">
                <p className="text-white/70 mb-4">
                  如果你对本隐私政策有任何疑问，请联系我们：
                </p>
                <a href="mailto:cancansauce@gmail.com" className="text-brand-terracotta hover:underline">cancansauce@gmail.com</a>
              </div>
            </motion.div>

            {/* 变更通知 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="border-t border-brand-charcoal/10 pt-8"
            >
              <h2 className="text-lg font-semibold text-brand-charcoal mb-4">政策变更</h2>
              <p className="text-brand-charcoal/70 text-sm">
                我们可能会不时更新本隐私政策。重大变更时，我们会通过邮件或站内通知提前告知你。
                建议你定期查看本页面了解最新政策。本政策顶部的"最后更新"日期表示最近一次修改时间。
              </p>
            </motion.div>

          </div>
        </div>
      </section>
    </div>
  )
}
