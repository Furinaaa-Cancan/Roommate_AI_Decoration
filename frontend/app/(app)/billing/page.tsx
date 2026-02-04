"use client"

import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { Check, ArrowLeft } from "lucide-react"
import Link from "next/link"
import { staggerContainer, staggerItem } from "@/components/shared/ClassicDecorations"

const membershipPlans = [
  {
    id: "free",
    name: "免费版",
    nameEn: "FREE",
    price: 0,
    credits: 5,
    period: "永久",
    features: ["5次免费体验", "4K分辨率", "基础风格"],
    popular: false,
  },
  {
    id: "personal",
    name: "个人版",
    nameEn: "PERSONAL",
    price: 39,
    credits: 50,
    period: "月",
    features: ["每月50次生成", "4K超清输出", "全部风格", "历史记录保存"],
    popular: true,
  },
  {
    id: "designer",
    name: "设计师版",
    nameEn: "DESIGNER",
    price: 99,
    credits: 200,
    period: "月",
    features: ["每月200次生成", "4K超清输出", "批量生成", "优先队列", "专属客服"],
    popular: false,
  },
  {
    id: "enterprise",
    name: "企业版",
    nameEn: "ENTERPRISE",
    price: 299,
    credits: 800,
    period: "月",
    features: ["每月800次生成", "API访问", "团队协作", "定制风格", "专属客户经理"],
    popular: false,
  },
]

const creditPacks = [
  { id: "pack_10", credits: 10, price: 9.9, label: "" },
  { id: "pack_40", credits: 40, price: 29, label: "超值" },
  { id: "pack_100", credits: 100, price: 59, label: "热销" },
  { id: "pack_400", credits: 400, price: 199, label: "最划算" },
]

export default function BillingPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)
  const [selectedPack, setSelectedPack] = useState<string | null>(null)

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login?callbackUrl=/billing")
    }
  }, [status, router])

  if (status === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#FAFAF8]">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="w-8 h-8 border border-black/10 border-t-black/40 rounded-full animate-spin" />
        </motion.div>
      </div>
    )
  }

  if (!session) return null

  const currentMembership = (session.user as any)?.membership_type ?? "free"
  const currentCredits = (session.user as any)?.credits ?? 0

  const handleSubscribe = (planId: string) => {
    setSelectedPlan(planId)
    router.push(`/checkout?type=membership&plan=${planId}`)
  }

  const handleBuyCredits = (packId: string) => {
    setSelectedPack(packId)
    router.push(`/checkout?type=credits&plan=${packId}`)
  }

  return (
    <div className="min-h-screen bg-brand-cream relative overflow-hidden">
      {/* 古典建筑名画背景 - Raphael 雅典学院 */}
      <div 
        className="fixed inset-0 pointer-events-none"
        style={{
          backgroundImage: `url("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg/2560px-%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg")`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: 0.07,
          filter: 'sepia(15%) contrast(1.1)'
        }}
      />
      
      {/* 顶部导航 */}
      <header className="sticky top-0 z-50 bg-brand-cream/90 backdrop-blur-sm border-b border-brand-charcoal/5">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <button 
            onClick={() => router.push('/')}
            className="flex items-center gap-2 text-brand-charcoal/50 hover:text-brand-charcoal transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            <span className="text-sm">返回首页</span>
          </button>
          <Link href="/profile" className="text-sm text-brand-charcoal/50 hover:text-brand-charcoal transition-colors">
            个人中心
          </Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-20 relative z-10">
        
        {/* Hero */}
        <motion.section
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-xs tracking-[0.4em] text-brand-charcoal/40 uppercase mb-4"
          >
            Membership & Pricing
          </motion.p>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-4xl md:text-5xl lg:text-6xl font-serif text-brand-charcoal mb-4 tracking-tight"
          >
            选择适合您的方案
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-brand-charcoal/50 text-lg max-w-xl mx-auto"
          >
            开启专业级 AI 设计之旅
          </motion.p>
          
          {/* 当前状态 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="inline-flex items-center gap-5 mt-10 px-6 py-3 bg-white/60 backdrop-blur-sm rounded-full border border-brand-charcoal/10"
          >
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-brand-terracotta" />
              <span className="text-brand-charcoal font-medium">
                {membershipPlans.find(p => p.id === currentMembership)?.name}
              </span>
            </div>
            <span className="w-px h-4 bg-brand-charcoal/10" />
            <span className="text-brand-charcoal">
              <span className="text-xl font-semibold">{currentCredits}</span>
              <span className="text-brand-charcoal/50 text-sm ml-1">次可用</span>
            </span>
          </motion.div>
        </motion.section>

        {/* 会员套餐 */}
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mb-20"
        >
          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            animate="show"
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5"
          >
            {membershipPlans.map((plan) => (
              <motion.div
                key={plan.id}
                variants={staggerItem}
                whileHover={{ y: -8, transition: { duration: 0.3 } }}
                className={`relative bg-white rounded-2xl p-6 transition-all duration-300 ${
                  plan.popular 
                    ? "ring-2 ring-brand-terracotta shadow-xl shadow-brand-terracotta/10" 
                    : "ring-1 ring-brand-charcoal/10 hover:ring-brand-charcoal/20 hover:shadow-lg"
                }`}
              >
                {/* 推荐标签 */}
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-brand-terracotta text-white text-[10px] tracking-[0.15em] uppercase px-4 py-1.5 rounded-full font-medium">
                    推荐
                  </div>
                )}
                
                <div className={plan.popular ? "pt-3" : ""}>
                  {/* 名称 */}
                  <p className="text-[10px] text-brand-charcoal/40 tracking-[0.25em] uppercase mb-1">{plan.nameEn}</p>
                  <h3 className="font-serif text-xl text-brand-charcoal mb-6">{plan.name}</h3>
                  
                  {/* 价格 */}
                  <div className="mb-6">
                    {plan.price === 0 ? (
                      <span className="text-4xl font-light text-brand-charcoal">免费</span>
                    ) : (
                      <div className="flex items-baseline">
                        <span className="text-brand-charcoal/40 mr-1">¥</span>
                        <span className="text-4xl font-light text-brand-charcoal">{plan.price}</span>
                        <span className="text-brand-charcoal/40 text-sm ml-1">/月</span>
                      </div>
                    )}
                    <p className="text-sm text-brand-charcoal/50 mt-2">{plan.credits} 次生成/月</p>
                  </div>
                  
                  {/* 功能 */}
                  <ul className="space-y-3 mb-8 pb-6 border-b border-brand-charcoal/10">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-3 text-sm text-brand-charcoal/70">
                        <Check className="h-4 w-4 text-brand-terracotta shrink-0 mt-0.5" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  
                  {/* 按钮 */}
                  <button
                    onClick={() => handleSubscribe(plan.id)}
                    disabled={currentMembership === plan.id || plan.id === "free"}
                    className={`w-full py-3.5 rounded-xl text-sm font-medium transition-all duration-300 ${
                      currentMembership === plan.id
                        ? "bg-brand-charcoal/5 text-brand-charcoal/30 cursor-default"
                        : plan.id === "free"
                          ? "bg-brand-charcoal/5 text-brand-charcoal/30 cursor-default"
                          : plan.popular
                            ? "bg-brand-terracotta text-white hover:bg-brand-terracotta/90"
                            : "bg-brand-charcoal text-white hover:bg-brand-charcoal/90"
                    }`}
                  >
                    {currentMembership === plan.id ? "当前方案" : plan.id === "free" ? "免费使用" : "选择此方案"}
                  </button>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </motion.section>

        {/* 分隔线 */}
        <div className="flex items-center gap-8 mb-16">
          <div className="flex-1 h-px bg-brand-charcoal/10" />
          <span className="text-xs tracking-[0.3em] text-brand-charcoal/30 uppercase">积分充值</span>
          <div className="flex-1 h-px bg-brand-charcoal/10" />
        </div>

        {/* 积分充值 */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mb-20"
        >
          <div className="text-center mb-10">
            <h2 className="text-2xl font-serif text-brand-charcoal mb-2">按需购买</h2>
            <p className="text-brand-charcoal/50">一次购买，永久有效</p>
          </div>
          
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {creditPacks.map((pack, index) => (
              <motion.div
                key={pack.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 + index * 0.08 }}
                whileHover={{ y: -6, transition: { duration: 0.25 } }}
                onClick={() => setSelectedPack(pack.id)}
                className={`relative cursor-pointer bg-white rounded-2xl p-6 text-center transition-all duration-300 ${
                  selectedPack === pack.id 
                    ? "ring-2 ring-brand-terracotta shadow-lg" 
                    : "ring-1 ring-brand-charcoal/10 hover:ring-brand-charcoal/20 hover:shadow-md"
                }`}
              >
                {/* 标签 */}
                {pack.label && (
                  <span className="absolute -top-2.5 left-1/2 -translate-x-1/2 bg-brand-terracotta text-white text-[9px] tracking-[0.1em] uppercase px-3 py-1 rounded-full font-medium">
                    {pack.label}
                  </span>
                )}
                
                <div className={pack.label ? "pt-2" : ""}>
                  <div className="text-4xl font-light text-brand-charcoal mb-1">{pack.credits}</div>
                  <div className="text-[11px] text-brand-charcoal/40 uppercase tracking-wider mb-4">次生成</div>
                  <div className="text-xl text-brand-charcoal mb-4">¥{pack.price}</div>
                  
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleBuyCredits(pack.id)
                    }}
                    className="w-full py-3 bg-brand-charcoal/5 hover:bg-brand-charcoal hover:text-white text-brand-charcoal text-sm rounded-xl transition-all duration-300"
                  >
                    购买
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* 说明 */}
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="max-w-2xl mx-auto text-center"
        >
          <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 ring-1 ring-brand-charcoal/5">
            <h3 className="text-sm font-medium text-brand-charcoal/60 mb-4 tracking-wide">使用说明</h3>
            <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 text-sm text-brand-charcoal/50">
              <span>每次渲染消耗 1 积分</span>
              <span>充值积分永久有效</span>
              <span>会员积分每月重置</span>
              <span>如需发票请联系客服</span>
            </div>
          </div>
        </motion.section>
      </main>
    </div>
  )
}
