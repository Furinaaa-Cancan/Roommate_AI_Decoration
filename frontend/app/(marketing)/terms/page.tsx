'use client'

import { motion } from 'framer-motion'
import { Info } from 'lucide-react'
import Link from 'next/link'

export default function TermsPage() {
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
              服务条款
            </h1>
            <p className="text-white/40 text-sm">最后更新：2026年1月20日</p>
          </motion.div>
        </div>
      </section>

      {/* Quick Nav */}
      <section className="py-6 px-6 bg-white border-b border-brand-charcoal/5 sticky top-20 z-40">
        <div className="max-w-3xl mx-auto">
          <div className="flex flex-wrap gap-3 text-sm">
            <a href="#accept" className="text-brand-charcoal/60 hover:text-brand-terracotta">接受条款</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#service" className="text-brand-charcoal/60 hover:text-brand-terracotta">服务说明</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#account" className="text-brand-charcoal/60 hover:text-brand-terracotta">账户</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#rules" className="text-brand-charcoal/60 hover:text-brand-terracotta">使用规范</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#ip" className="text-brand-charcoal/60 hover:text-brand-terracotta">知识产权</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#payment" className="text-brand-charcoal/60 hover:text-brand-terracotta">付费</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#disclaimer" className="text-brand-charcoal/60 hover:text-brand-terracotta">免责</a>
            <span className="text-brand-charcoal/20">·</span>
            <a href="#law" className="text-brand-charcoal/60 hover:text-brand-terracotta">法律</a>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-12 px-6">
        <div className="max-w-3xl mx-auto">
          <div className="prose prose-stone max-w-none">
            
            {/* 接受条款 */}
            <motion.div
              id="accept"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">1. 接受条款</h2>
              <p className="text-brand-charcoal/70 mb-4">
                欢迎使用 Roommate AI（以下简称"本服务"）。
              </p>
              <p className="text-brand-charcoal/70 mb-4">
                使用本服务前，请仔细阅读以下条款。注册账户、使用任何功能或支付服务费用，即表示您已阅读、理解并同意受本条款约束。
              </p>
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
                <p className="text-amber-800 text-sm">
                  <strong>如果您不同意本条款的任何内容，请勿使用本服务。</strong>
                </p>
              </div>
            </motion.div>

            {/* 服务说明 */}
            <motion.div
              id="service"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">2. 服务说明</h2>
              <p className="text-brand-charcoal/70 mb-4">
                Roommate AI 是一个基于人工智能的室内设计效果图生成平台。您可以上传毛胚房或现有空间的照片，
                AI 将生成相应的装修效果图。
              </p>
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">服务内容</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>AI 效果图生成（多种设计风格）</li>
                <li>局部区域修改和替换</li>
                <li>高清图片导出（最高 4K 分辨率）</li>
                <li>生成历史记录保存</li>
              </ul>
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">服务可用性</h3>
              <p className="text-brand-charcoal/70">
                我们致力于提供稳定的服务，但不保证 100% 的正常运行时间。我们可能因系统维护、升级或不可抗力因素暂停服务。
                计划内的维护会提前在平台公告。
              </p>
            </motion.div>

            {/* 账户 */}
            <motion.div
              id="account"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">3. 账户</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">注册要求</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>您必须年满 18 周岁，或在监护人同意下使用本服务</li>
                <li>注册时需提供真实、准确的信息</li>
                <li>每人仅限注册一个账户</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">账户安全</h3>
              <p className="text-brand-charcoal/70 mb-4">
                您有责任保护您的账户安全。请勿与他人共享密码或转让账户。
                如发现账户被盗用，请立即联系 <a href="mailto:cancansauce@gmail.com" className="text-brand-terracotta">cancansauce@gmail.com</a>。
              </p>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">账户终止</h3>
              <p className="text-brand-charcoal/70 mb-2">我们可能在以下情况下终止或暂停您的账户：</p>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>违反本服务条款</li>
                <li>存在欺诈、滥用或非法行为</li>
                <li>账户超过 24 个月未活跃</li>
              </ul>
              <p className="text-brand-charcoal/70 mt-4">
                账户终止后，您有权申请导出您的数据（违规终止除外）。未使用的付费服务将按比例退款。
              </p>
            </motion.div>

            {/* 使用规范 */}
            <motion.div
              id="rules"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">4. 使用规范</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">允许的使用</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>个人装修设计参考</li>
                <li>商业项目设计展示（需购买专业版或企业版）</li>
                <li>房产营销展示（需购买企业版）</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">禁止行为</h3>
              <p className="text-brand-charcoal/70 mb-2">您同意不会：</p>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>上传违法、淫秽、暴力或侵权内容</li>
                <li>上传包含他人隐私信息的照片</li>
                <li>尝试破解、逆向工程或攻击本服务</li>
                <li>使用自动化工具批量访问（API 用户除外）</li>
                <li>转售、分发或二次许可本服务</li>
                <li>将服务用于任何违法目的</li>
              </ul>

              <div className="bg-red-50 border border-red-200 rounded-xl p-4 mt-6">
                <p className="text-red-800 text-sm">
                  <strong>警告：</strong>违反上述规定可能导致账户立即终止，且不予退款。严重违规将报告执法机关。
                </p>
              </div>
            </motion.div>

            {/* 知识产权 */}
            <motion.div
              id="ip"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">5. 知识产权</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">您上传的内容</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>您上传的原始照片，版权归您所有</li>
                <li>您保证您有权上传这些内容，且不侵犯第三方权利</li>
                <li>您授予我们处理这些内容以提供服务的许可</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">AI 生成的内容</h3>
              <div className="bg-white rounded-xl p-6 mt-4">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-brand-charcoal/10">
                      <th className="text-left py-3 text-brand-charcoal font-semibold">套餐</th>
                      <th className="text-left py-3 text-brand-charcoal font-semibold">使用权限</th>
                    </tr>
                  </thead>
                  <tbody className="text-brand-charcoal/70">
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">免费版 / 个人版</td>
                      <td className="py-3">仅限个人非商业用途</td>
                    </tr>
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">专业版</td>
                      <td className="py-3">可用于商业项目展示</td>
                    </tr>
                    <tr>
                      <td className="py-3">企业版</td>
                      <td className="py-3">完整商业使用权，可用于营销</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">平台内容</h3>
              <p className="text-brand-charcoal/70">
                Roommate AI 的技术、算法、界面设计、商标、Logo 及其他内容均受知识产权法保护。
                未经书面许可，不得复制、修改、分发或创建衍生作品。
              </p>
            </motion.div>

            {/* 付费 */}
            <motion.div
              id="payment"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">6. 付费服务</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">订阅服务</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>订阅按月或按年计费，价格以购买页面显示为准</li>
                <li>除非您在当前周期结束前取消，订阅将自动续期</li>
                <li>取消后，当前周期内的服务仍可使用</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">积分</h3>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>积分用于消费 AI 生成服务</li>
                <li>积分有效期为购买后 12 个月</li>
                <li>积分不可转让或兑换现金</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">退款政策</h3>
              <div className="bg-white rounded-xl p-6 mt-4">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-brand-charcoal/10">
                      <th className="text-left py-3 text-brand-charcoal font-semibold">类型</th>
                      <th className="text-left py-3 text-brand-charcoal font-semibold">退款政策</th>
                    </tr>
                  </thead>
                  <tbody className="text-brand-charcoal/70">
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">订阅（首次）</td>
                      <td className="py-3">7 天内可申请全额退款</td>
                    </tr>
                    <tr className="border-b border-brand-charcoal/5">
                      <td className="py-3">订阅（续费）</td>
                      <td className="py-3">不支持退款，可取消下次续费</td>
                    </tr>
                    <tr>
                      <td className="py-3">积分充值</td>
                      <td className="py-3">充值后不支持退款</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">价格变更</h3>
              <p className="text-brand-charcoal/70">
                我们可能调整服务价格。价格变更将提前 30 天通知。变更不影响当前订阅周期。
              </p>
            </motion.div>

            {/* 免责声明 */}
            <motion.div
              id="disclaimer"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">7. 免责声明与责任限制</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">服务性质</h3>
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-4">
                <p className="text-amber-800 text-sm">
                  <strong>重要提示：</strong>AI 生成的效果图仅供参考，不构成专业室内设计建议。
                  实际装修施工请咨询持证设计师和装修公司。
                </p>
              </div>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">按现状提供 (As-Is)</h3>
              <p className="text-brand-charcoal/70 mb-4">
                本服务按"现状"和"可用状态"提供。我们不作任何明示或暗示的保证，包括但不限于：
              </p>
              <ul className="text-brand-charcoal/70 space-y-2">
                <li>生成效果图的准确性、完整性或适用性</li>
                <li>服务不会中断或无错误</li>
                <li>服务满足您的特定需求</li>
              </ul>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">责任上限</h3>
              <p className="text-brand-charcoal/70 mb-4">
                在法律允许的最大范围内，我们对因使用或无法使用本服务而产生的任何直接、间接、附带、
                特殊或惩罚性损害不承担责任。
              </p>
              <p className="text-brand-charcoal/70">
                <strong className="text-brand-charcoal">我们的最大累计责任不超过您在过去 12 个月内向我们支付的服务费用总额。</strong>
              </p>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">不可抗力</h3>
              <p className="text-brand-charcoal/70">
                对于因自然灾害、战争、政府行为、网络攻击、供应商故障等不可抗力因素导致的服务中断或损失，我们不承担责任。
              </p>
            </motion.div>

            {/* 法律 */}
            <motion.div
              id="law"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="mb-12 scroll-mt-32"
            >
              <h2 className="text-2xl font-serif font-bold text-brand-charcoal mb-6">8. 适用法律与争议解决</h2>
              
              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">适用法律</h3>
              <p className="text-brand-charcoal/70 mb-4">
                本条款受<strong className="text-brand-charcoal">中华人民共和国法律</strong>管辖并依其解释，不考虑法律冲突原则。
              </p>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">争议解决</h3>
              <p className="text-brand-charcoal/70 mb-4">
                如发生争议，双方应首先友好协商解决。
              </p>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">条款变更</h3>
              <p className="text-brand-charcoal/70 mb-4">
                我们可能不时修改本条款。重大变更将通过邮件和平台公告提前 30 天通知。
                继续使用服务即表示您接受修改后的条款。
              </p>

              <h3 className="text-lg font-semibold text-brand-charcoal mt-6 mb-3">语言</h3>
              <p className="text-brand-charcoal/70">
                本条款以中文为准。如有翻译版本与中文版本不一致，以中文版本为准。
              </p>
            </motion.div>

            {/* 联系 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="bg-brand-charcoal rounded-xl p-6 text-center"
            >
              <h3 className="text-lg font-semibold text-white mb-4">联系我们</h3>
              <p className="text-white/70 mb-4">如有任何关于本条款的问题，请联系：</p>
              <a href="mailto:cancansauce@gmail.com" className="text-brand-terracotta hover:underline">cancansauce@gmail.com</a>
            </motion.div>

          </div>
        </div>
      </section>
    </div>
  )
}
