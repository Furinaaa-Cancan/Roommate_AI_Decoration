export interface GenerateRequest {
  image: string | File
  roomType: string
  style: string
  quality: '1K' | '2K' | '4K'
  customPrompt?: string
}

export interface GenerateResponse {
  success: boolean
  taskId: string
  images: string[]
  cost: number
  elapsedSeconds: number
  error?: string
}

export interface TaskProgress {
  id: string
  progress: number
  status: 'running' | 'succeeded' | 'failed'
  results: Array<{ url: string }>
  error?: string
}

export interface Project {
  id: string
  name: string
  createdAt: string
  updatedAt: string
  images: ProjectImage[]
}

export interface ProjectImage {
  id: string
  originalUrl: string
  generatedUrl: string
  style: string
  roomType: string
  quality: string
  createdAt: string
}
