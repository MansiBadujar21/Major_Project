'use client'

import { motion } from 'framer-motion'
import { Loader2, FileText, Download, CheckCircle } from 'lucide-react'

interface LoadingSpinnerProps {
  message?: string
  type?: 'default' | 'document' | 'download' | 'success'
  size?: 'sm' | 'md' | 'lg'
  showProgress?: boolean
  progress?: number
}

export default function LoadingSpinner({
  message = 'Loading...',
  type = 'default',
  size = 'md',
  showProgress = false,
  progress = 0
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  }

  const iconSizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  }

  const getIcon = () => {
    switch (type) {
      case 'document':
        return <FileText className={iconSizeClasses[size]} />
      case 'download':
        return <Download className={iconSizeClasses[size]} />
      case 'success':
        return <CheckCircle className={iconSizeClasses[size]} />
      default:
        return <Loader2 className={iconSizeClasses[size]} />
    }
  }

  const getColorClasses = () => {
    switch (type) {
      case 'success':
        return 'text-green-600 bg-green-100'
      case 'document':
        return 'text-blue-600 bg-blue-100'
      case 'download':
        return 'text-purple-600 bg-purple-100'
      default:
        return 'text-blue-600 bg-blue-100'
    }
  }

  return (
    <div className="flex flex-col items-center justify-center p-6">
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className={`inline-flex items-center justify-center ${sizeClasses[size]} rounded-full ${getColorClasses()} mb-4`}
      >
        <motion.div
          animate={type === 'default' ? { rotate: 360 } : {}}
          transition={type === 'default' ? { duration: 1, repeat: Infinity, ease: 'linear' } : {}}
        >
          {getIcon()}
        </motion.div>
      </motion.div>

      {message && (
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-gray-600 text-center font-medium"
        >
          {message}
        </motion.p>
      )}

      {showProgress && (
        <div className="w-full max-w-xs mt-4">
          <div className="bg-gray-200 rounded-full h-2">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
              className="bg-blue-600 h-2 rounded-full"
            />
          </div>
          <p className="text-sm text-gray-500 text-center mt-2">
            {Math.round(progress)}% complete
          </p>
        </div>
      )}
    </div>
  )
}

// Specialized loading components for common use cases
export function DocumentLoadingSpinner({ message = 'Generating document...' }: { message?: string }) {
  return (
    <LoadingSpinner
      type="document"
      message={message}
      size="lg"
    />
  )
}

export function DownloadLoadingSpinner({ message = 'Preparing download...' }: { message?: string }) {
  return (
    <LoadingSpinner
      type="download"
      message={message}
      size="md"
    />
  )
}

export function SuccessSpinner({ message = 'Success!' }: { message?: string }) {
  return (
    <LoadingSpinner
      type="success"
      message={message}
      size="md"
    />
  )
}

export function ProgressSpinner({ 
  message = 'Processing...', 
  progress = 0 
}: { 
  message?: string
  progress: number 
}) {
  return (
    <LoadingSpinner
      type="default"
      message={message}
      size="lg"
      showProgress={true}
      progress={progress}
    />
  )
}
