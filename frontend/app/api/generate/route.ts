import { NextRequest, NextResponse } from 'next/server'
import https from 'https'

// 禁用SSL证书验证（开发环境）
const agent = new https.Agent({
  rejectUnauthorized: false
})

// Nano Banana API 配置
const GRSAI_API_URL = 'https://grsai.dakka.com.cn/v1/draw/nano-banana'
const GRSAI_API_KEY = process.env.GRSAI_API_KEY || ''

// 风格提示词映射
const stylePromptMap: Record<string, string> = {
  '现代简约': 'Modern minimalist interior design, clean lines, neutral colors, simple furniture, open space, natural light, high quality, 4K, photorealistic',
  '北欧风': 'Scandinavian interior design, bright airy space, white walls, light wood floors, cozy textiles, plants, hygge atmosphere, high quality, 4K, photorealistic',
  '侘寂风': 'Wabi-sabi interior design, Japanese aesthetics, natural materials, earth tones, handcrafted items, minimal furniture, zen atmosphere, high quality, 4K, photorealistic',
  '新中式': 'Modern Chinese interior design, traditional elements with contemporary twist, dark wood, subtle patterns, elegant decoration, high quality, 4K, photorealistic',
  '轻奢': 'Light luxury interior design, elegant and sophisticated, marble surfaces, gold accents, velvet textures, crystal lighting, high quality, 4K, photorealistic',
  '工业风': 'Industrial interior design, exposed brick walls, metal pipes, concrete floors, Edison bulbs, urban loft style, high quality, 4K, photorealistic',
  '日式': 'Japanese interior design, tatami mats, shoji screens, natural wood, zen garden elements, minimalist, peaceful atmosphere, high quality, 4K, photorealistic',
  '法式': 'French interior design, elegant moldings, chandelier, parquet floors, classic furniture, romantic atmosphere, high quality, 4K, photorealistic',
  // 新设计页面风格
  'wabi_sabi': 'Wabi-sabi interior design, Japanese aesthetics, natural materials, earth tones, handcrafted items, minimal furniture, zen atmosphere, high quality, 4K, photorealistic',
  'cream_style': 'Cream style interior design, soft warm tones, creamy white, cozy and elegant, natural textures, high quality, 4K, photorealistic',
  'modern_luxury': 'Modern luxury interior design, elegant and sophisticated, marble surfaces, gold accents, velvet textures, crystal lighting, high quality, 4K, photorealistic',
  'modern_chinese': 'Modern Chinese interior design, traditional elements with contemporary twist, dark wood, subtle patterns, elegant decoration, high quality, 4K, photorealistic',
  'scandinavian': 'Scandinavian interior design, bright airy space, white walls, light wood floors, cozy textiles, plants, hygge atmosphere, high quality, 4K, photorealistic',
  'industrial': 'Industrial interior design, exposed brick walls, metal pipes, concrete floors, Edison bulbs, urban loft style, high quality, 4K, photorealistic',
  'french_vintage': 'French vintage interior design, elegant moldings, chandelier, parquet floors, classic furniture, romantic atmosphere, high quality, 4K, photorealistic',
  'japanese': 'Japanese interior design, tatami mats, shoji screens, natural wood, zen garden elements, minimalist, peaceful atmosphere, high quality, 4K, photorealistic',
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { image, image_url, style, quality, room_type, user_id } = body

    const imageData = image || image_url
    if (!imageData) {
      return NextResponse.json(
        { success: false, error: '请上传图片' },
        { status: 400 }
      )
    }

    if (!GRSAI_API_KEY) {
      return NextResponse.json(
        { success: false, error: 'API密钥未配置，请在.env.local中设置GRSAI_API_KEY' },
        { status: 500 }
      )
    }

    // 构建提示词
    const basePrompt = stylePromptMap[style] || stylePromptMap['现代简约']
    const prompt = `Transform this room into ${style} style. ${basePrompt}`

    // 统一使用 nano-banana-pro 模型
    const model = 'nano-banana-pro'
    const imageSize = quality || '4K'

    console.log('=== Nano Banana API 请求 ===')
    console.log('Model:', model)
    console.log('Style:', style)
    console.log('ImageSize:', imageSize)
    console.log('Prompt:', prompt)

    // 调用 Nano Banana API
    const response = await fetch(GRSAI_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GRSAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: model,
        prompt: prompt,
        urls: [imageData], // Base64图片
        imageSize: imageSize,
        aspectRatio: 'auto',
        shutProgress: true, // 关闭进度，直接返回结果
      }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('API响应错误:', response.status, errorText)
      throw new Error(`API错误: ${response.status}`)
    }

    // 处理流式响应
    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    let result = ''

    if (reader) {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        result += decoder.decode(value, { stream: true })
      }
    }

    console.log('API原始响应:', result)

    // 解析SSE格式响应
    const lines = result.split('\n').filter(line => line.trim())
    let finalData = null

    for (const line of lines) {
      try {
        // 处理SSE格式：去掉 "data: " 前缀
        let jsonStr = line
        if (line.startsWith('data: ')) {
          jsonStr = line.substring(6)
        } else if (line.startsWith('data:')) {
          jsonStr = line.substring(5)
        }
        
        const data = JSON.parse(jsonStr)
        console.log('解析的数据:', data)
        
        if (data.status === 'succeeded' && data.results) {
          finalData = data
          break
        }
        // 保存最新的数据
        finalData = data
      } catch (e) {
        // 跳过无法解析的行
        console.log('跳过无法解析的行:', line)
      }
    }

    console.log('最终数据:', finalData)

    if (finalData && finalData.status === 'succeeded' && finalData.results?.length > 0) {
      const imageUrls = finalData.results.map((r: any) => r.url)
      console.log('返回图片URL:', imageUrls)
      return NextResponse.json({
        success: true,
        images: imageUrls,
        content: finalData.results[0]?.content || '',
      })
    } else if (finalData?.status === 'failed') {
      const errorMsg = finalData.error || finalData.failure_reason || '生成失败'
      // 返回更友好的错误信息
      return NextResponse.json({
        success: false,
        error: errorMsg.includes('timeout') ? 'AI服务繁忙，请稍后重试' : errorMsg
      })
    } else {
      return NextResponse.json({
        success: false,
        error: '未获取到生成结果，请重试'
      })
    }

  } catch (error) {
    console.error('Generate API error:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : '生成失败，请重试' 
      },
      { status: 500 }
    )
  }
}
