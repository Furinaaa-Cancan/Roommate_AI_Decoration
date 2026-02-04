"use client"

import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { useEffect, useState, useRef } from "react"
import { motion } from "framer-motion"
import { 
  ArrowLeft,
  User,
  Mail,
  Bell,
  Shield,
  Save,
  Check,
  Camera,
  Upload
} from "lucide-react"
import {
  VitruvianBackground,
  GreekMeander,
  FloatingParticles,
  staggerContainer,
  staggerItem,
} from "@/components/shared/ClassicDecorations"

export default function SettingsPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [isSaving, setIsSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [notifications, setNotifications] = useState(true)
  const [avatar, setAvatar] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login?callbackUrl=/settings")
    }
  }, [status, router])

  useEffect(() => {
    if (session?.user) {
      setName(session.user.name || "")
      setEmail(session.user.email || "")
      setAvatar(session.user.image || null)
    }
  }, [session])

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

  const handleSave = async () => {
    if (!session?.user) return
    
    setIsSaving(true)
    try {
      const userId = (session.user as any).id
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/auth/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          name: name,
          avatar: avatar,
        }),
      })
      
      if (response.ok) {
        setSaved(true)
        setTimeout(() => {
          setSaved(false)
          window.location.reload()
        }, 1000)
      } else {
        console.error('保存失败')
      }
    } catch (error) {
      console.error('保存错误:', error)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="min-h-screen bg-brand-cream relative overflow-hidden">
      {/* 古典艺术背景 */}
      <VitruvianBackground className="opacity-[0.04]" />
      <FloatingParticles count={10} />
      
      {/* 左侧装饰条 */}
      <div className="hidden lg:flex fixed left-0 top-0 h-full w-12 bg-brand-cream/80 backdrop-blur-sm border-r border-brand-charcoal/10 items-center justify-center z-40">
        <span className="text-[10px] tracking-[0.3em] text-brand-charcoal/40 transform -rotate-90 whitespace-nowrap uppercase font-serif">
          Settings
        </span>
      </div>

      {/* 顶部导航 */}
      <header className="sticky top-0 z-50 bg-brand-cream/80 backdrop-blur-xl border-b border-brand-charcoal/10">
        <div className="max-w-3xl mx-auto px-6 lg:pl-16 h-16 flex items-center justify-between">
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
            账号设置
          </motion.h1>
          <div className="w-16" />
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 lg:pl-16 py-12 relative z-10">
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="show"
          className="space-y-8"
        >
          {/* 希腊回纹装饰 */}
          <div className="text-brand-charcoal/10">
            <GreekMeander className="w-full h-4" />
          </div>

          {/* 基本信息 */}
          <motion.section variants={staggerItem} className="bg-white/60 backdrop-blur-sm rounded-2xl border border-brand-charcoal/5 p-8">
            <div className="flex items-center gap-3 mb-6">
              <User className="h-5 w-5 text-brand-terracotta" />
              <h2 className="font-serif text-lg text-brand-charcoal">基本信息</h2>
            </div>
            
            <div className="flex flex-col md:flex-row items-start gap-8">
              {/* 头像 */}
              <div className="relative group">
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="relative"
                >
                  {avatar ? (
                    <img
                      src={avatar}
                      alt=""
                      className="h-28 w-28 rounded-2xl object-cover border-2 border-brand-charcoal/10"
                    />
                  ) : (
                    <div className="h-28 w-28 rounded-2xl bg-brand-charcoal/5 flex items-center justify-center border-2 border-brand-charcoal/10">
                      <User className="h-12 w-12 text-brand-charcoal/30" />
                    </div>
                  )}
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="absolute inset-0 rounded-2xl bg-brand-charcoal/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center cursor-pointer"
                    disabled={isUploading}
                  >
                    {isUploading ? (
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full"
                      />
                    ) : (
                      <Camera className="h-6 w-6 text-white" />
                    )}
                  </button>
                </motion.div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={async (e) => {
                    const file = e.target.files?.[0]
                    if (file) {
                      setIsUploading(true)
                      const reader = new FileReader()
                      reader.onload = (event) => {
                        setAvatar(event.target?.result as string)
                        setIsUploading(false)
                      }
                      reader.readAsDataURL(file)
                    }
                  }}
                />
              </div>
              
              {/* 信息表单 */}
              <div className="flex-1 space-y-6 w-full">
                <div>
                  <p className="text-sm text-brand-charcoal/50 mb-2">个人头像</p>
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    disabled={isUploading}
                    className="inline-flex items-center gap-2 px-4 py-2 border border-brand-charcoal/20 text-brand-charcoal/70 hover:bg-brand-charcoal hover:text-white rounded-lg transition-all text-sm"
                  >
                    <Upload className="h-4 w-4" />
                    上传头像
                  </button>
                </div>
                
                <div>
                  <label className="text-sm text-brand-charcoal/50 mb-2 block">昵称</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="您的昵称"
                    className="w-full px-4 py-3 bg-brand-charcoal/5 border border-brand-charcoal/10 rounded-xl text-brand-charcoal placeholder:text-brand-charcoal/30 focus:outline-none focus:border-brand-terracotta/50 transition-colors"
                  />
                </div>
              </div>
            </div>
          </motion.section>

          {/* 邮箱 */}
          <motion.section variants={staggerItem} className="bg-white/60 backdrop-blur-sm rounded-2xl border border-brand-charcoal/5 p-8">
            <div className="flex items-center gap-3 mb-6">
              <Mail className="h-5 w-5 text-brand-terracotta" />
              <h2 className="font-serif text-lg text-brand-charcoal">邮箱地址</h2>
            </div>
            
            <div>
              <label className="text-sm text-brand-charcoal/50 mb-2 block">邮箱</label>
              <input
                type="email"
                value={email}
                disabled
                className="w-full px-4 py-3 bg-brand-charcoal/5 border border-brand-charcoal/10 rounded-xl text-brand-charcoal/50 cursor-not-allowed"
              />
              <p className="text-xs text-brand-charcoal/40 mt-2">邮箱地址来自 Google 账号，无法修改</p>
            </div>
          </motion.section>

          {/* 通知设置 */}
          <motion.section variants={staggerItem} className="bg-white/60 backdrop-blur-sm rounded-2xl border border-brand-charcoal/5 p-8">
            <div className="flex items-center gap-3 mb-6">
              <Bell className="h-5 w-5 text-brand-terracotta" />
              <h2 className="font-serif text-lg text-brand-charcoal">通知设置</h2>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-brand-charcoal">邮件通知</p>
                <p className="text-sm text-brand-charcoal/50">接收产品更新和促销信息</p>
              </div>
              <button
                onClick={() => setNotifications(!notifications)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  notifications 
                    ? "bg-brand-terracotta text-white" 
                    : "bg-brand-charcoal/5 text-brand-charcoal/60 hover:bg-brand-charcoal/10"
                }`}
              >
                {notifications ? "已开启" : "已关闭"}
              </button>
            </div>
          </motion.section>

          {/* 账号安全 */}
          <motion.section variants={staggerItem} className="bg-white/60 backdrop-blur-sm rounded-2xl border border-brand-charcoal/5 p-8">
            <div className="flex items-center gap-3 mb-6">
              <Shield className="h-5 w-5 text-brand-terracotta" />
              <h2 className="font-serif text-lg text-brand-charcoal">账号安全</h2>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-brand-charcoal">登录方式</p>
                <p className="text-sm text-brand-charcoal/50">Google 账号登录</p>
              </div>
              <div className="flex items-center gap-2 text-emerald-600">
                <Check className="h-4 w-4" />
                <span className="text-sm font-medium">已绑定</span>
              </div>
            </div>
          </motion.section>

          {/* 希腊回纹装饰 */}
          <div className="text-brand-charcoal/10">
            <GreekMeander className="w-full h-4" />
          </div>

          {/* 保存按钮 */}
          <motion.div variants={staggerItem}>
            <button
              onClick={handleSave}
              disabled={isSaving}
              className={`w-full py-4 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
                saved 
                  ? "bg-emerald-500 text-white" 
                  : "bg-brand-charcoal text-white hover:bg-brand-terracotta"
              }`}
            >
              {isSaving ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                  />
                  保存中...
                </>
              ) : saved ? (
                <>
                  <Check className="h-5 w-5" />
                  已保存
                </>
              ) : (
                <>
                  <Save className="h-5 w-5" />
                  保存设置
                </>
              )}
            </button>
          </motion.div>
        </motion.div>
      </main>
    </div>
  )
}
