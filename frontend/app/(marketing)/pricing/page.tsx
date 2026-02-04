'use client'

import { motion } from 'framer-motion'
import { Check, Sparkles, Zap, Building2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { cn } from '@/lib/utils/cn'

const plans = [
  {
    id: 'free',
    name: '免费体验',
    description: '适合个人用户试用',
    price: '0',
    unit: '元',
    period: '',
    icon: Sparkles,
    features: [
      '每月 5 张免费额度',
      '1K 分辨率',
      '基础风格选择',
      '72小时有效期',
    ],
    cta: '免费开始',
    popular: false,
  },
  {
    id: 'pro',
    name: '专业版',
    description: '适合设计师和小团队',
    price: '99',
    unit: '元',
    period: '/月',
    icon: Zap,
    features: [
      '每月 200 张额度',
      '4K 超清分辨率',
      '全部 10+ 设计风格',
      '优先处理队列',
      '批量处理',
      'API 接口访问',
    ],
    cta: '立即订阅',
    popular: true,
  },
  {
    id: 'enterprise',
    name: '企业版',
    description: '适合房企和装修公司',
    price: '联系我们',
    unit: '',
    period: '',
    icon: Building2,
    features: [
      '无限生成额度',
      '4K/8K 分辨率',
      '自定义风格训练',
      '专属技术支持',
      '私有化部署',
      'SLA 保障',
    ],
    cta: '联系销售',
    popular: false,
  },
]

const faqs = [
  {
    q: '生成一张图需要多长时间？',
    a: '4K 分辨率的图片通常在 60-90 秒内完成，1K 分辨率约 20-30 秒。',
  },
  {
    q: '支持哪些图片格式？',
    a: '支持 JPG、PNG、WEBP 格式，建议上传分辨率不低于 1920x1080 的清晰照片。',
  },
  {
    q: '额度用完了怎么办？',
    a: '可以随时升级套餐或购买额外额度包。企业用户可申请无限额度。',
  },
  {
    q: '生成的图片版权归谁？',
    a: '您拥有所有生成图片的完整商业使用权，可用于营销、展示等任何用途。',
  },
]

export default function PricingPage() {
  return (
    <main className="pt-24 pb-20">
      {/* Header */}
      <section className="max-w-4xl mx-auto px-6 text-center mb-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl md:text-5xl font-bold text-stone-900 mb-4">
            简单透明的定价
          </h1>
          <p className="text-xl text-stone-600">
            按需选择，随时升级，无隐藏费用
          </p>
        </motion.div>
      </section>

      {/* Pricing Cards */}
      <section className="max-w-6xl mx-auto px-6 mb-20">
        <div className="grid md:grid-cols-3 gap-8">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className={cn(
                "relative h-full",
                plan.popular && "border-stone-800 shadow-xl"
              )}>
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-stone-800 text-white text-xs font-medium rounded-full">
                    最受欢迎
                  </div>
                )}
                
                <CardHeader className="text-center pb-2">
                  <div className={cn(
                    "w-12 h-12 mx-auto mb-4 rounded-xl flex items-center justify-center",
                    plan.popular ? "bg-stone-800 text-white" : "bg-stone-100 text-stone-600"
                  )}>
                    <plan.icon className="w-6 h-6" />
                  </div>
                  <CardTitle className="text-xl">{plan.name}</CardTitle>
                  <CardDescription>{plan.description}</CardDescription>
                </CardHeader>

                <CardContent className="space-y-6">
                  <div className="text-center">
                    <span className="text-4xl font-bold text-stone-900">{plan.price}</span>
                    <span className="text-stone-500">{plan.unit}{plan.period}</span>
                  </div>

                  <ul className="space-y-3">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-center gap-3 text-sm">
                        <Check className="w-4 h-4 text-green-600 flex-shrink-0" />
                        <span className="text-stone-700">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <Button 
                    className="w-full" 
                    variant={plan.popular ? "default" : "outline"}
                    size="lg"
                  >
                    {plan.cta}
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Pay Per Use */}
      <section className="max-w-4xl mx-auto px-6 mb-20">
        <Card className="bg-stone-50 border-stone-200">
          <CardContent className="p-8">
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
              <div>
                <h3 className="text-xl font-semibold text-stone-900 mb-2">
                  按量付费
                </h3>
                <p className="text-stone-600">
                  不想订阅？也可以按张付费，灵活使用
                </p>
              </div>
              <div className="flex items-center gap-8">
                <div className="text-center">
                  <p className="text-2xl font-bold text-stone-900">¥0.18</p>
                  <p className="text-sm text-stone-500">1K 分辨率/张</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-stone-900">¥0.38</p>
                  <p className="text-sm text-stone-500">4K 分辨率/张</p>
                </div>
                <Button variant="outline">购买额度包</Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* FAQ */}
      <section className="max-w-4xl mx-auto px-6">
        <h2 className="text-2xl font-bold text-stone-900 text-center mb-10">
          常见问题
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          {faqs.map((faq, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              viewport={{ once: true }}
              className="p-6 bg-white rounded-xl border border-stone-200"
            >
              <h4 className="font-medium text-stone-900 mb-2">{faq.q}</h4>
              <p className="text-sm text-stone-600">{faq.a}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </main>
  )
}
