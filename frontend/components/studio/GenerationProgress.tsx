'use client'

import { motion } from 'framer-motion'
import { Loader2, CheckCircle, XCircle } from 'lucide-react'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils/cn'

interface GenerationProgressProps {
  status: 'idle' | 'uploading' | 'generating' | 'success' | 'error'
  progress: number
  message?: string
  className?: string
}

export function GenerationProgress({ 
  status, 
  progress, 
  message,
  className 
}: GenerationProgressProps) {
  if (status === 'idle') return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "p-4 rounded-xl border",
        status === 'success' && "bg-green-50 border-green-200",
        status === 'error' && "bg-red-50 border-red-200",
        (status === 'uploading' || status === 'generating') && "bg-stone-50 border-stone-200",
        className
      )}
    >
      <div className="flex items-center gap-3">
        {status === 'uploading' || status === 'generating' ? (
          <Loader2 className="w-5 h-5 text-stone-600 animate-spin" />
        ) : status === 'success' ? (
          <CheckCircle className="w-5 h-5 text-green-600" />
        ) : (
          <XCircle className="w-5 h-5 text-red-600" />
        )}
        
        <div className="flex-1">
          <p className={cn(
            "text-sm font-medium",
            status === 'success' && "text-green-800",
            status === 'error' && "text-red-800",
            (status === 'uploading' || status === 'generating') && "text-stone-800"
          )}>
            {status === 'uploading' && '上传中...'}
            {status === 'generating' && 'AI渲染中...'}
            {status === 'success' && '生成完成！'}
            {status === 'error' && '生成失败'}
          </p>
          {message && (
            <p className="text-xs text-stone-500 mt-0.5">{message}</p>
          )}
        </div>

        {(status === 'uploading' || status === 'generating') && (
          <span className="text-sm font-medium text-stone-600">
            {Math.round(progress)}%
          </span>
        )}
      </div>

      {(status === 'uploading' || status === 'generating') && (
        <Progress value={progress} className="mt-3" />
      )}
    </motion.div>
  )
}
