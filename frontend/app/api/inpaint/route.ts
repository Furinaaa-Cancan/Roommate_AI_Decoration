import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BACKEND_URL}/api/v1/inpaint`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    
    const data = await response.json()
    
    // 处理后端返回的错误状态码
    if (!response.ok) {
      return NextResponse.json({
        success: false,
        error: data.detail || data.error || '后端服务错误'
      })
    }
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Inpaint API error:', error)
    return NextResponse.json(
      { success: false, error: '局部重绘服务暂不可用' },
      { status: 500 }
    )
  }
}
