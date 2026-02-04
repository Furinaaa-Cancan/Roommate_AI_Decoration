"use client"

import { useSession } from "next-auth/react"
import { useRouter, useSearchParams } from "next/navigation"
import { useEffect, useState, Suspense, useCallback } from "react"
import { motion } from "framer-motion"
import { ArrowLeft, Check, Clock, Shield, Copy, AlertCircle } from "lucide-react"
import Link from "next/link"

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface OrderData {
  order_no: string
  product_name: string
  base_amount: number
  pay_amount: number
  price_code: string
  pay_method: string
  qrcode_url: string
  expire_at: string
  expire_seconds: number
  status?: string
  reject_reason?: string
}

function CheckoutContent() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const searchParams = useSearchParams()
  
  const type = searchParams.get("type")
  const planId = searchParams.get("plan")
  const existingOrderNo = searchParams.get("order")
  
  const [paymentMethod, setPaymentMethod] = useState<"wechat" | "alipay">("wechat")
  const [orderData, setOrderData] = useState<OrderData | null>(null)
  const [orderStatus, setOrderStatus] = useState<"loading" | "pending" | "submitted" | "rejected" | "error">("loading")
  const [countdown, setCountdown] = useState(0)
  const [transactionId, setTransactionId] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const userId = (session?.user as any)?.id

  // 创建订单
  const createOrder = useCallback(async () => {
    // 调试日志
    console.log('createOrder called:', { userId, type, planId, paymentMethod })
    
    if (!userId) {
      setError('用户未登录或用户ID无效，请重新登录')
      setOrderStatus('error')
      return
    }
    if (!type || !planId) {
      setError('缺少商品信息')
      setOrderStatus('error')
      return
    }
    
    try {
      const res = await fetch(`${API_URL}/api/v1/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          product_type: type,
          product_id: planId,
          pay_method: paymentMethod
        })
      })
      
      const data = await res.json()
      console.log('Order API response:', data)
      
      if (!res.ok) {
        setError(data.detail || '创建订单失败')
        setOrderStatus('error')
        return
      }
      
      setOrderData(data.data)
      setCountdown(data.data.expire_seconds)
      setOrderStatus('pending')
    } catch (err) {
      console.error('Order API error:', err)
      setError('网络错误，请稍后重试')
      setOrderStatus('error')
    }
  }, [userId, type, planId, paymentMethod])

  // 获取现有订单
  const fetchOrder = useCallback(async (orderNo: string) => {
    if (!userId) return
    
    try {
      const res = await fetch(`${API_URL}/api/v1/orders/${orderNo}?user_id=${userId}`)
      const data = await res.json()
      
      if (!res.ok) {
        setError(data.detail || '订单不存在')
        setOrderStatus('error')
        return
      }
      
      setOrderData(data.data)
      setCountdown(data.data.expire_seconds)
      
      if (data.data.status === 'submitted') {
        setOrderStatus('submitted')
      } else if (data.data.status === 'rejected') {
        setOrderStatus('rejected')
      } else {
        setOrderStatus('pending')
      }
    } catch (err) {
      setError('网络错误')
      setOrderStatus('error')
    }
  }, [userId])

  // 提交订单
  const handleSubmitOrder = async () => {
    if (!orderData) return
    
    setIsSubmitting(true)
    setError(null)
    
    try {
      const res = await fetch(`${API_URL}/api/v1/orders/${orderData.order_no}/submit?user_id=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transaction_id: transactionId || null })
      })
      
      const data = await res.json()
      
      if (!res.ok) {
        setError(data.detail)
        setIsSubmitting(false)
        return
      }
      
      setOrderStatus('submitted')
    } catch (err) {
      setError('提交失败，请重试')
    }
    
    setIsSubmitting(false)
  }

  const copyText = (text: string) => {
    navigator.clipboard.writeText(text)
    alert('已复制')
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  // 初始化订单
  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login?callbackUrl=/billing")
      return
    }
    
    if (status === "authenticated" && userId) {
      if (existingOrderNo) {
        fetchOrder(existingOrderNo)
      } else if (type && planId) {
        createOrder()
      }
    }
  }, [status, userId, existingOrderNo, type, planId, createOrder, fetchOrder])

  // 倒计时
  useEffect(() => {
    if (countdown <= 0 || orderStatus !== 'pending') return
    
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(timer)
          setError('订单已过期，请重新下单')
          return 0
        }
        return prev - 1
      })
    }, 1000)
    
    return () => clearInterval(timer)
  }, [countdown, orderStatus])

  // 条件渲染放在Hooks之后
  if (status === "loading" || !session) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-brand-cream">
        <div className="w-8 h-8 border border-brand-charcoal/10 border-t-brand-charcoal/40 rounded-full animate-spin" />
      </div>
    )
  }

  // 加载中
  if (orderStatus === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-brand-cream">
        <div className="text-center">
          <div className="w-8 h-8 border border-brand-charcoal/10 border-t-brand-charcoal/40 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-brand-charcoal/50">正在创建订单...</p>
        </div>
      </div>
    )
  }

  // 错误页面
  if (orderStatus === "error") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-brand-cream p-6">
        <div className="text-center max-w-md">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="w-8 h-8 text-red-500" />
          </div>
          <p className="text-brand-charcoal/70 mb-6">{error}</p>
          <Link href="/billing" className="inline-block px-6 py-3 bg-brand-charcoal text-white rounded-xl">
            返回定价页面
          </Link>
        </div>
      </div>
    )
  }

  // 订单已提交页面
  if (orderStatus === "submitted") {
    return (
      <div className="min-h-screen bg-brand-cream flex items-center justify-center p-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white rounded-2xl p-10 text-center max-w-md w-full shadow-xl"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-20 h-20 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-6"
          >
            <Clock className="w-10 h-10 text-amber-600" />
          </motion.div>
          <h1 className="text-2xl font-serif text-brand-charcoal mb-2">订单已提交</h1>
          <p className="text-brand-charcoal/50 mb-4">
            我们将在确认收款后为您开通服务
          </p>
          <div className="bg-brand-cream rounded-xl p-4 mb-6 text-left">
            <p className="text-sm text-brand-charcoal/60 mb-2">订单号</p>
            <p className="font-mono text-brand-charcoal">{orderData?.order_no}</p>
          </div>
          <p className="text-xs text-brand-charcoal/40 mb-6">
            通常在1-24小时内处理完成，如有问题请联系客服
          </p>
          <div className="space-y-3">
            <Link
              href="/profile"
              className="block w-full py-3 bg-brand-charcoal text-white rounded-xl font-medium hover:bg-brand-charcoal/90 transition-colors"
            >
              查看个人中心
            </Link>
            <Link
              href="/billing"
              className="block w-full py-3 bg-brand-charcoal/5 text-brand-charcoal rounded-xl font-medium hover:bg-brand-charcoal/10 transition-colors"
            >
              返回定价页面
            </Link>
          </div>
        </motion.div>
      </div>
    )
  }

  // 订单被驳回页面
  if (orderStatus === "rejected") {
    return (
      <div className="min-h-screen bg-brand-cream flex items-center justify-center p-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white rounded-2xl p-10 text-center max-w-md w-full shadow-xl"
        >
          <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <AlertCircle className="w-10 h-10 text-orange-500" />
          </div>
          <h1 className="text-2xl font-serif text-brand-charcoal mb-2">订单需要重新提交</h1>
          <p className="text-brand-charcoal/50 mb-4">
            {orderData?.reject_reason || '请重新确认支付信息'}
          </p>
          <button
            onClick={() => setOrderStatus('pending')}
            className="w-full py-3 bg-brand-terracotta text-white rounded-xl font-medium hover:bg-brand-terracotta/90 transition-colors"
          >
            重新提交
          </button>
        </motion.div>
      </div>
    )
  }

  if (!orderData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-brand-cream">
        <div className="text-center">
          <p className="text-brand-charcoal/50 mb-4">订单信息无效</p>
          <Link href="/billing" className="text-brand-terracotta hover:underline">
            返回定价页面
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-brand-cream relative overflow-hidden">
      {/* 古典建筑名画背景 - Canaletto 威尼斯风景 */}
      <div 
        className="fixed inset-0 pointer-events-none"
        style={{
          backgroundImage: `url("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Canaletto_-_The_Grand_Canal_and_the_Church_of_the_Salute.jpg/2560px-Canaletto_-_The_Grand_Canal_and_the_Church_of_the_Salute.jpg")`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: 0.06,
          filter: 'sepia(30%) contrast(1.1)'
        }}
      />
      
      {/* 顶部导航 */}
      <header className="sticky top-0 z-50 bg-brand-cream/90 backdrop-blur-sm border-b border-brand-charcoal/5">
        <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
          <button 
            onClick={() => router.back()}
            className="flex items-center gap-2 text-brand-charcoal/50 hover:text-brand-charcoal transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            <span className="text-sm">返回</span>
          </button>
          <div className="flex items-center gap-2 text-brand-charcoal/50">
            <Shield className="h-4 w-4" />
            <span className="text-sm">安全支付</span>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12 relative z-10">
        {/* 倒计时提示 */}
        {countdown > 0 && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8 p-4 bg-amber-50/80 backdrop-blur-sm border border-amber-200/50 rounded-2xl flex items-center justify-between shadow-sm"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center">
                <Clock className="w-5 h-5 text-amber-600" />
              </div>
              <span className="text-amber-800">订单将在 <strong className="text-amber-900">{formatTime(countdown)}</strong> 后过期</span>
            </div>
          </motion.div>
        )}

        {/* 错误提示 */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-500" />
            <span className="text-red-700">{error}</span>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-10">
          {/* 左侧 - 订单信息 */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h1 className="text-2xl font-serif text-brand-charcoal mb-8">确认订单</h1>
            
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 mb-6 shadow-sm border border-brand-charcoal/5">
              <div className="flex justify-between items-start mb-6 pb-6 border-b border-brand-charcoal/10">
                <div>
                  <p className="text-xs text-brand-charcoal/40 uppercase tracking-wider mb-1">
                    {type === "membership" ? "会员套餐" : "积分包"}
                  </p>
                  <h2 className="text-xl font-medium text-brand-charcoal">
                    {orderData.product_name}
                  </h2>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-light text-brand-charcoal">
                    ¥{orderData.base_amount}
                  </p>
                  {type === "membership" && (
                    <p className="text-sm text-brand-charcoal/40">/月</p>
                  )}
                </div>
              </div>
              
              <div className="space-y-3 text-sm">
                <div className="flex justify-between pt-3 border-t border-brand-charcoal/10">
                  <span className="font-medium text-brand-charcoal">应付金额</span>
                  <span className="text-xl font-medium text-brand-terracotta">¥{orderData.pay_amount}</span>
                </div>
              </div>
            </div>

            {/* 支付方式选择 */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-sm border border-brand-charcoal/5">
              <h3 className="font-medium text-brand-charcoal mb-4">支付方式</h3>
              <div className="space-y-3">
                <button
                  onClick={() => setPaymentMethod("wechat")}
                  className={`w-full flex items-center gap-4 p-4 rounded-xl border-2 transition-all ${
                    paymentMethod === "wechat"
                      ? "border-green-500 bg-green-50/50"
                      : "border-brand-charcoal/10 hover:border-brand-charcoal/20 bg-white/50"
                  }`}
                >
                  <div className="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center">
                    <svg viewBox="0 0 24 24" className="w-6 h-6 text-white" fill="currentColor">
                      <path d="M9.5 4C5.36 4 2 6.69 2 10c0 1.89 1.08 3.56 2.78 4.66l-.7 2.1 2.47-1.25c.73.25 1.52.42 2.35.47-.15-.47-.23-.96-.23-1.48C8.67 11.46 11.84 9 15.75 9c.44 0 .87.04 1.29.1C16.36 6.19 13.26 4 9.5 4zm-2.87 4.5a.88.88 0 110-1.75.88.88 0 010 1.75zm4.62 0a.88.88 0 110-1.75.88.88 0 010 1.75zM22 14.5c0-2.73-2.89-4.96-6.42-4.96S9.17 11.77 9.17 14.5s2.89 4.96 6.41 4.96c.7 0 1.38-.09 2.01-.26l1.94.99-.55-1.65C20.92 17.62 22 16.17 22 14.5zm-8.27-.56a.72.72 0 110-1.44.72.72 0 010 1.44zm3.68 0a.72.72 0 110-1.44.72.72 0 010 1.44z"/>
                    </svg>
                  </div>
                  <span className="font-medium text-brand-charcoal">微信支付</span>
                  {paymentMethod === "wechat" && <Check className="w-5 h-5 text-green-500 ml-auto" />}
                </button>
                
                <button
                  onClick={() => setPaymentMethod("alipay")}
                  className={`w-full flex items-center gap-4 p-4 rounded-xl border-2 transition-all ${
                    paymentMethod === "alipay"
                      ? "border-blue-500 bg-blue-50/50"
                      : "border-brand-charcoal/10 hover:border-brand-charcoal/20 bg-white/50"
                  }`}
                >
                  <div className="w-10 h-10 bg-blue-500 rounded-xl flex items-center justify-center">
                    <svg viewBox="0 0 24 24" className="w-6 h-6 text-white" fill="currentColor">
                      <path d="M21.5 13.5c-.34-.54-1.17-1.04-2.43-1.52a42.4 42.4 0 00-3.57-1.18c.53-1.2.9-2.48 1.06-3.72h-2.36v-1.5h2.93V4.5h-2.93V2.5h-1.88v2h-2.94v1.08h2.94v1.5H9.38v1.5h5.56c-.14.87-.42 1.77-.82 2.63-1.24-.26-2.4-.44-3.4-.44-2.54 0-4.22 1.06-4.22 2.83 0 1.68 1.46 2.85 3.7 2.85 1.72 0 3.38-.7 4.68-1.97.87.38 2.57 1.13 4.37 2.03v1.97c0 .92-.76 1.52-1.75 1.52H5.5c-.99 0-1.75-.6-1.75-1.52V5c0-.92.76-1.5 1.75-1.5h13c.99 0 1.75.58 1.75 1.5v8.5h1.5V5c0-1.66-1.34-3-3.25-3H5.5C3.59 2 2.25 3.34 2.25 5v14c0 1.66 1.34 3 3.25 3h13c1.91 0 3.25-1.34 3.25-3v-3.5c0-.78-.35-1.53-1-2zm-11.78 2.45c-1.42 0-2.13-.53-2.13-1.33 0-.87.88-1.35 2.34-1.35.82 0 1.74.15 2.7.42-.93 1.42-2.03 2.26-2.91 2.26z"/>
                    </svg>
                  </div>
                  <span className="font-medium text-brand-charcoal">支付宝</span>
                  {paymentMethod === "alipay" && <Check className="w-5 h-5 text-blue-500 ml-auto" />}
                </button>
              </div>
            </div>
          </motion.div>

          {/* 右侧 - 收款码和提交表单 */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex flex-col"
          >
            {/* 收款二维码 */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 text-center mb-6 shadow-sm border border-brand-charcoal/5">
              <h3 className="font-medium text-brand-charcoal mb-4">
                请使用{paymentMethod === "wechat" ? "微信" : "支付宝"}扫码支付
              </h3>
              
              {/* 二维码图片区域 */}
              <div className={`w-52 h-52 mx-auto rounded-2xl overflow-hidden mb-4 ${
                paymentMethod === "wechat" ? "bg-green-50" : "bg-blue-50"
              }`}>
                {/* 收款码图片 - 请将图片放到 /public/payment/ 目录 */}
                <img
                  src={paymentMethod === "wechat" ? "/payment/wechat.jpg" : "/payment/alipay.jpg"}
                  alt={paymentMethod === "wechat" ? "微信收款码" : "支付宝收款码"}
                  className="w-full h-full object-contain"
                  onError={(e) => {
                    // 图片加载失败时显示提示
                    const target = e.target as HTMLImageElement
                    target.style.display = 'none'
                    const fallback = target.nextElementSibling as HTMLElement
                    if (fallback) fallback.style.display = 'flex'
                  }}
                />
                {/* 图片加载失败时的备用显示 */}
                <div className="qr-fallback w-full h-full items-center justify-center text-center p-4" style={{display: 'none'}}>
                  <div>
                    <div className={`w-12 h-12 mx-auto mb-3 rounded-xl flex items-center justify-center ${
                      paymentMethod === "wechat" ? "bg-green-500" : "bg-blue-500"
                    }`}>
                      <img 
                        src={paymentMethod === "wechat" 
                          ? "https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico"
                          : "https://t.alipayobjects.com/images/T1HHFgXXVeXXXXXXXX.png"
                        } 
                        alt="" 
                        className="w-8 h-8"
                      />
                    </div>
                    <p className="text-xs text-brand-charcoal/50">
                      收款码未配置
                    </p>
                  </div>
                </div>
              </div>
              
              {/* 支付金额 */}
              <div className="pt-4 border-t border-brand-charcoal/10">
                <p className="text-brand-charcoal/50 text-sm">支付金额</p>
                <p className="text-4xl font-bold text-brand-terracotta mt-1">
                  ¥{orderData.pay_amount}
                </p>
                <p className="text-xs text-brand-charcoal/50 mt-2">
                  付款时请备注订单号
                </p>
              </div>
            </div>

            {/* 订单信息和提交表单 */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-sm border border-brand-charcoal/5">
              <h3 className="font-medium text-brand-charcoal mb-4">订单信息</h3>
              
              {/* 订单号 */}
              <div className="mb-4">
                <label className="block text-sm text-brand-charcoal/60 mb-2">订单号</label>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-brand-cream rounded-xl px-4 py-3 font-mono text-sm text-brand-charcoal">
                    {orderData.order_no}
                  </div>
                  <button
                    onClick={() => copyText(orderData.order_no)}
                    className="p-3 bg-brand-cream hover:bg-brand-charcoal/10 rounded-xl transition-colors"
                    title="复制订单号"
                  >
                    <Copy className="w-4 h-4 text-brand-charcoal/60" />
                  </button>
                </div>
              </div>
              
              {/* 交易单号输入（可选） */}
              <div className="mb-6">
                <label className="block text-sm text-brand-charcoal/60 mb-2">
                  支付交易单号 <span className="text-brand-charcoal/30">(可选)</span>
                </label>
                <input
                  type="text"
                  value={transactionId}
                  onChange={(e) => setTransactionId(e.target.value)}
                  placeholder="支付完成后可填写交易单号"
                  className="w-full bg-brand-cream rounded-xl px-4 py-3 text-sm text-brand-charcoal placeholder:text-brand-charcoal/30 focus:outline-none focus:ring-2 focus:ring-brand-terracotta/50"
                />
                <p className="text-xs text-brand-charcoal/40 mt-2">
                  填写交易单号可加快审核速度
                </p>
              </div>
              
              {/* 提交按钮 */}
              <button
                onClick={handleSubmitOrder}
                disabled={isSubmitting}
                className={`w-full py-3.5 rounded-xl font-medium transition-all duration-300 ${
                  isSubmitting
                    ? "bg-brand-charcoal/10 text-brand-charcoal/30 cursor-not-allowed"
                    : "bg-brand-terracotta text-white hover:bg-brand-terracotta/90"
                }`}
              >
                {isSubmitting ? "提交中..." : "我已支付，提交订单"}
              </button>
            </div>
            
            {/* 提示信息 */}
            <div className="mt-4 text-center text-xs text-brand-charcoal/40 space-y-1">
              <p>提交后我们将在1-24小时内确认并开通服务</p>
              <p>如有问题请联系客服</p>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  )
}

export default function CheckoutPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-brand-cream">
        <div className="w-8 h-8 border border-brand-charcoal/10 border-t-brand-charcoal/40 rounded-full animate-spin" />
      </div>
    }>
      <CheckoutContent />
    </Suspense>
  )
}
