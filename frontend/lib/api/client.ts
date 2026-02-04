const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface GenerateRequest {
  image: string
  roomType: string
  style: string
  quality: '1K' | '2K' | '4K'
}

export interface GenerateResponse {
  success: boolean
  taskId?: string
  images?: string[]
  cost?: number
  elapsedSeconds?: number
  error?: string
}

export async function generateImage(request: GenerateRequest): Promise<GenerateResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : '生成失败，请重试',
    }
  }
}

export async function uploadImage(file: File): Promise<{ url: string } | { error: string }> {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : '上传失败',
    }
  }
}

export function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = reader.result as string
      resolve(result)
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}
