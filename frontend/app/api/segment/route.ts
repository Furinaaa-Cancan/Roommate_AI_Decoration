import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BACKEND_URL}/api/v1/segment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    
    const data = await response.json()
    
    // 保持 mask_url 为相对路径，通过 Next.js rewrites 代理访问
    if (data.objects) {
      data.objects = data.objects.map((obj: any) => ({
        ...obj,
        mask_url: obj.mask_url || ''
      }))
    }
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Segment API error:', error)
    return NextResponse.json(
      { success: false, error: '分割服务暂不可用' },
      { status: 500 }
    )
  }
}
