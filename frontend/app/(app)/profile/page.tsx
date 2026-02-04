"use client"

import { useSession, signOut } from "next-auth/react"
import { useRouter } from "next/navigation"
import { useEffect } from "react"
import { motion } from "framer-motion"
import { 
  User, 
  Mail, 
  CreditCard, 
  LogOut, 
  Settings,
  Sparkles,
  Zap,
  ArrowLeft,
  ChevronRight,
  Image as ImageIcon,
  Clock,
  Gift,
  ArrowRight,
  Crown
} from "lucide-react"
import Link from "next/link"
import {
  VitruvianBackground,
  CreationBackground,
  GreekMeander,
  FloatingParticles,
  staggerContainer,
  staggerItem,
} from "@/components/shared/ClassicDecorations"

export default function ProfilePage() {
  const { data: session, status } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login")
    }
  }, [status, router])

  if (status === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-brand-cream relative overflow-hidden">
        <VitruvianBackground />
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative z-10"
        >
          <div className="w-20 h-20 border-2 border-brand-charcoal/10 rounded-full flex items-center justify-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
              className="w-16 h-16 border-t-2 border-brand-terracotta rounded-full"
            />
          </div>
        </motion.div>
      </div>
    )
  }

  if (!session) return null

  const user = session.user
  const credits = (user as any)?.credits ?? 5
  const membershipType = (user as any)?.membership_type ?? "free"

  const membershipLabels: Record<string, string> = {
    free: "免费版",
    personal: "个人版",
    designer: "设计师版",
    enterprise: "企业版",
  }

  const quickActions = [
    { icon: Sparkles, label: "开始设计", desc: "毛胚房秒变精装", href: "/" },
    { icon: CreditCard, label: "充值中心", desc: "购买积分或会员", href: "/billing" },
    { icon: Settings, label: "账号设置", desc: "管理个人信息", href: "/settings" },
    { icon: Gift, label: "邀请有礼", desc: "邀请好友赚积分", href: "#" },
  ]

  return (
    <div className="min-h-screen bg-brand-cream relative overflow-hidden">
      {/* 古典艺术背景 */}
      <CreationBackground className="opacity-[0.08]" />
      <FloatingParticles count={15} />
      
      {/* 左侧装饰条 */}
      <div className="hidden lg:flex fixed left-0 top-0 h-full w-12 bg-brand-cream/80 backdrop-blur-sm border-r border-brand-charcoal/10 items-center justify-center z-40">
        <span className="text-[10px] tracking-[0.3em] text-brand-charcoal/40 transform -rotate-90 whitespace-nowrap uppercase font-serif">
          Personal Center
        </span>
      </div>

      {/* 顶部导航 */}
      <header className="sticky top-0 z-50 bg-brand-cream/80 backdrop-blur-xl border-b border-brand-charcoal/10">
        <div className="max-w-5xl mx-auto px-6 lg:pl-16 h-16 flex items-center justify-between">
          <button 
            onClick={() => router.back()}
            className="flex items-center gap-2 text-brand-charcoal/60 hover:text-brand-charcoal transition-colors group"
          >
            <ArrowLeft className="h-4 w-4 group-hover:-translate-x-1 transition-transform" />
            <span className="text-sm font-serif tracking-wide">返回</span>
          </button>
          <motion.h1 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="font-serif text-lg text-brand-charcoal tracking-wider"
          >
            个人中心
          </motion.h1>
          <motion.button 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={() => signOut({ callbackUrl: "/" })}
            className="flex items-center gap-2 text-brand-charcoal/40 hover:text-brand-terracotta transition-colors"
          >
            <LogOut className="h-4 w-4" />
          </motion.button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 lg:pl-16 py-12 relative z-10">
        {/* 用户信息卡片 - 古典风格 */}
        <motion.section
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.25, 0.46, 0.45, 0.94] }}
          className="relative mb-16"
        >
          {/* 希腊回纹装饰 */}
          <div className="absolute -top-4 left-0 right-0 text-brand-charcoal/10">
            <GreekMeander className="w-full h-6" />
          </div>
          
          <div className="pt-12 flex flex-col md:flex-row items-start gap-8">
            {/* 头像 */}
            <motion.div
              whileHover={{ scale: 1.03 }}
              transition={{ type: "spring", stiffness: 300 }}
              className="relative"
            >
              {user?.image ? (
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-br from-brand-terracotta/20 to-transparent rounded-2xl blur-xl" />
                  <img
                    src={user.image}
                    alt={user.name || ""}
                    className="relative h-28 w-28 md:h-36 md:w-36 rounded-2xl object-cover border-2 border-brand-charcoal/10 shadow-xl"
                  />
                </div>
              ) : (
                <div className="h-28 w-28 md:h-36 md:w-36 rounded-2xl bg-gradient-to-br from-brand-charcoal/5 to-brand-charcoal/10 flex items-center justify-center border-2 border-brand-charcoal/10">
                  <User className="h-14 w-14 text-brand-charcoal/30" />
                </div>
              )}
            </motion.div>

            {/* 用户信息 */}
            <div className="flex-1 space-y-4">
              <div>
                <motion.h2 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 }}
                  className="font-serif text-3xl md:text-4xl text-brand-charcoal tracking-tight"
                >
                  {user?.name || "用户"}
                </motion.h2>
                <motion.p 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="text-brand-charcoal/50 flex items-center gap-2 mt-2 text-sm"
                >
                  <Mail className="h-4 w-4" />
                  {user?.email}
                </motion.p>
              </div>
              
              {/* 会员徽章 */}
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="flex items-center gap-4"
              >
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-brand-charcoal/5 border border-brand-charcoal/10 rounded-full">
                  <Crown className="h-4 w-4 text-brand-terracotta" />
                  <span className="text-sm font-medium text-brand-charcoal">
                    {membershipLabels[membershipType]}
                  </span>
                </div>
                {membershipType === "free" && (
                  <Link 
                    href="/billing"
                    className="text-sm text-brand-terracotta hover:underline"
                  >
                    升级会员 →
                  </Link>
                )}
              </motion.div>
            </div>

            {/* 右侧操作 */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Link
                href="/settings"
                className="hidden md:inline-flex items-center gap-2 px-5 py-2.5 border border-brand-charcoal/20 text-brand-charcoal/70 hover:bg-brand-charcoal hover:text-white rounded-lg transition-all text-sm"
              >
                <Settings className="h-4 w-4" />
                编辑资料
              </Link>
            </motion.div>
          </div>
          
          {/* 希腊回纹装饰 */}
          <div className="absolute -bottom-4 left-0 right-0 text-brand-charcoal/10">
            <GreekMeander className="w-full h-6" />
          </div>
        </motion.section>

        {/* 数据统计 */}
        <motion.section
          variants={staggerContainer}
          initial="hidden"
          animate="show"
          className="grid grid-cols-3 gap-6 mb-16"
        >
          {[
            { label: "剩余积分", value: credits, unit: "次", icon: Zap },
            { label: "设计作品", value: 0, unit: "件", icon: ImageIcon },
            { label: "使用天数", value: 1, unit: "天", icon: Clock },
          ].map((stat) => (
            <motion.div
              key={stat.label}
              variants={staggerItem}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-brand-charcoal/5 hover:border-brand-charcoal/20 transition-all group"
            >
              <stat.icon className="h-5 w-5 text-brand-terracotta mb-3 group-hover:scale-110 transition-transform" />
              <div className="flex items-baseline gap-1">
                <span className="font-serif text-3xl text-brand-charcoal">{stat.value}</span>
                <span className="text-sm text-brand-charcoal/50">{stat.unit}</span>
              </div>
              <p className="text-xs text-brand-charcoal/40 mt-1 uppercase tracking-wider">{stat.label}</p>
            </motion.div>
          ))}
        </motion.section>

        {/* 快捷操作 */}
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mb-16"
        >
          <h3 className="font-serif text-lg text-brand-charcoal mb-6 tracking-wide">快捷操作</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {quickActions.map((action, index) => (
              <motion.div
                key={action.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                whileHover={{ y: -4 }}
                whileTap={{ scale: 0.98 }}
              >
                <Link
                  href={action.href}
                  className="block p-6 bg-white/60 backdrop-blur-sm rounded-xl border border-brand-charcoal/5 hover:border-brand-terracotta/30 hover:shadow-lg transition-all group"
                >
                  <action.icon className="h-6 w-6 text-brand-charcoal/40 group-hover:text-brand-terracotta transition-colors mb-3" />
                  <h4 className="font-medium text-brand-charcoal mb-1">{action.label}</h4>
                  <p className="text-xs text-brand-charcoal/40">{action.desc}</p>
                </Link>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* 我的设计 */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-serif text-lg text-brand-charcoal tracking-wide">我的设计</h3>
            <Link href="#" className="text-sm text-brand-charcoal/50 hover:text-brand-charcoal flex items-center gap-1 group">
              查看全部 <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
          
          <div className="bg-white/60 backdrop-blur-sm rounded-2xl border border-brand-charcoal/5 p-16">
            <div className="flex flex-col items-center justify-center text-center">
              <motion.div
                animate={{ y: [0, -5, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                className="w-24 h-24 rounded-full bg-brand-charcoal/5 flex items-center justify-center mb-6"
              >
                <ImageIcon className="h-10 w-10 text-brand-charcoal/20" />
              </motion.div>
              <h4 className="font-serif text-xl text-brand-charcoal mb-2">还没有设计作品</h4>
              <p className="text-brand-charcoal/50 mb-8 max-w-sm text-sm">
                开始您的第一个 AI 室内设计，见证毛胚房秒变精装效果图
              </p>
              <Link
                href="/"
                className="inline-flex items-center gap-2 px-6 py-3 bg-brand-charcoal text-white rounded-lg hover:bg-brand-terracotta transition-colors text-sm font-medium"
              >
                <Sparkles className="h-4 w-4" />
                开始设计
              </Link>
            </div>
          </div>
        </motion.section>

        {/* 升级提示 */}
        {membershipType === "free" && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1 }}
            className="mt-16 relative overflow-hidden rounded-2xl bg-brand-charcoal p-8 md:p-12"
          >
            <VitruvianBackground className="opacity-10" />
            <div className="relative flex flex-col md:flex-row items-center justify-between gap-8">
              <div className="text-center md:text-left">
                <p className="text-brand-cream/60 text-sm uppercase tracking-widest mb-2">限时优惠</p>
                <h3 className="font-serif text-2xl md:text-3xl text-brand-cream mb-3">升级专业版，解锁更多功能</h3>
                <p className="text-brand-cream/60">获得无限生成次数、4K超清输出、8+设计风格</p>
              </div>
              <Link
                href="/billing"
                className="shrink-0 inline-flex items-center gap-2 px-8 py-4 bg-brand-terracotta text-white rounded-lg font-medium hover:bg-brand-terracotta/90 transition-colors"
              >
                查看套餐
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </motion.section>
        )}
      </main>
    </div>
  )
}
