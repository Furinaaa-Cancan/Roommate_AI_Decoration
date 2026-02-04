import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    
    const response = await fetch(`${BACKEND_URL}/api/v1/upload`, {
      method: 'POST',
      body: formData,
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      return NextResponse.json({
        success: false,
        error: data.detail || '上传失败'
      }, { status: response.status })
    }
    
    // 将后端返回的完整URL转换为相对路径，通过Next.js代理访问
    if (data.image_url) {
      data.image_url = data.image_url.replace(/^https?:\/\/[^/]+/, '')
    }
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Upload API error:', error)
    return NextResponse.json(
      { success: false, error: '图片上传服务暂不可用' },
      { status: 500 }
    )
  }
}
