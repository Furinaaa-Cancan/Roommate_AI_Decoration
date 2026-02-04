import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type GenerationStatus = 'idle' | 'uploading' | 'generating' | 'success' | 'error'

export interface DesignImage {
  id: string
  url: string
  base64?: string
  type: 'original' | 'generated'
  style?: string
  name?: string
}

export interface SegmentInfo {
  label: string
  label_zh: string
  mask_url: string
  inpaint_mask_url?: string
  inpaint_mask_base64?: string
  bbox: number[]
  confidence: number
}

interface StudioState {
  // Image
  originalFile: File | null
  originalPreview: string | null
  generatedImages: string[]
  
  // 工作台状态（持久化）
  workImages: DesignImage[]
  selectedImageId: string | null
  segmentsCache: Record<string, SegmentInfo[]>
  selectedSegmentIds: string[]
  selectedStyle: number
  editMode: 'full' | 'segment'
  prompt: string
  
  // Settings
  roomType: string
  style: string
  quality: '1K' | '2K' | '4K'
  
  // Generation
  status: GenerationStatus
  progress: number
  error: string | null
  
  // Actions
  setOriginalImage: (file: File, preview: string) => void
  clearOriginalImage: () => void
  setRoomType: (roomType: string) => void
  setStyle: (style: string) => void
  setQuality: (quality: '1K' | '2K' | '4K') => void
  setStatus: (status: GenerationStatus) => void
  setProgress: (progress: number) => void
  setError: (error: string | null) => void
  addGeneratedImage: (url: string) => void
  clearGeneratedImages: () => void
  reset: () => void
  
  // 工作台Actions
  setWorkImages: (images: DesignImage[]) => void
  addWorkImage: (image: DesignImage) => void
  setSelectedImageId: (id: string | null) => void
  setSegmentsCache: (imageId: string, segments: SegmentInfo[]) => void
  setSelectedSegmentIds: (ids: string[]) => void
  setSelectedStyle: (index: number) => void
  setEditMode: (mode: 'full' | 'segment') => void
  setPrompt: (prompt: string) => void
}

const initialState = {
  originalFile: null,
  originalPreview: null,
  generatedImages: [],
  roomType: 'living_room',
  style: 'wabi_sabi',
  quality: '4K' as const,
  status: 'idle' as const,
  progress: 0,
  error: null,
  // 工作台初始状态
  workImages: [] as DesignImage[],
  selectedImageId: null as string | null,
  segmentsCache: {} as Record<string, SegmentInfo[]>,
  selectedSegmentIds: [] as string[],
  selectedStyle: 0,
  editMode: 'full' as const,
  prompt: '',
}

export const useStudioStore = create<StudioState>()(
  persist(
    (set) => ({
      ...initialState,
  
      setOriginalImage: (file, preview) => set({ 
    originalFile: file, 
    originalPreview: preview,
    generatedImages: [],
    status: 'idle',
    error: null,
  }),
  
  clearOriginalImage: () => set({ 
    originalFile: null, 
    originalPreview: null,
    generatedImages: [],
    status: 'idle',
  }),
  
  setRoomType: (roomType) => set({ roomType }),
  setStyle: (style) => set({ style }),
  setQuality: (quality) => set({ quality }),
  setStatus: (status) => set({ status }),
  setProgress: (progress) => set({ progress }),
  setError: (error) => set({ error, status: error ? 'error' : 'idle' }),
  
  addGeneratedImage: (url) => set((state) => ({ 
    generatedImages: [...state.generatedImages, url],
    status: 'success',
  })),
  
  clearGeneratedImages: () => set({ generatedImages: [], status: 'idle' }),
  
  reset: () => set(initialState),
  
  // 工作台Actions
  setWorkImages: (images) => set({ workImages: images }),
  addWorkImage: (image) => set((state) => ({ 
    workImages: [...state.workImages, image],
    selectedImageId: image.id
  })),
  setSelectedImageId: (id) => set({ selectedImageId: id }),
  setSegmentsCache: (imageId, segments) => set((state) => ({
    segmentsCache: { ...state.segmentsCache, [imageId]: segments }
  })),
  setSelectedSegmentIds: (ids) => set({ selectedSegmentIds: ids }),
  setSelectedStyle: (index) => set({ selectedStyle: index }),
  setEditMode: (mode) => set({ editMode: mode }),
  setPrompt: (prompt) => set({ prompt }),
    }),
    {
      name: 'studio-storage',
      partialize: (state) => ({
        // 不存储base64数据，避免超出localStorage配额
        // 不存储blob URL（刷新后会失效），只保留生成的远程URL图片
        workImages: state.workImages
          .filter(img => !img.url.startsWith('blob:'))  // 排除blob URL
          .map(img => ({
            ...img,
            base64: undefined  // 排除base64
          })),
        selectedImageId: state.selectedImageId,
        // 不存储segmentsCache中的inpaint_mask_base64
        segmentsCache: Object.fromEntries(
          Object.entries(state.segmentsCache).map(([k, v]) => [
            k,
            v.map(seg => ({ ...seg, inpaint_mask_base64: undefined }))
          ])
        ),
        selectedStyle: state.selectedStyle,
        editMode: state.editMode,
        prompt: state.prompt,
      }),
    }
  )
)
