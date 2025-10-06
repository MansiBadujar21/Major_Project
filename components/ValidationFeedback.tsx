'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, AlertCircle, XCircle, Info, AlertTriangle } from 'lucide-react'

interface ValidationFeedbackProps {
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  details?: string[]
  show?: boolean
  onClose?: () => void
  autoHide?: boolean
  duration?: number
}

export default function ValidationFeedback({
  type,
  message,
  details,
  show = true,
  onClose,
  autoHide = false,
  duration = 5000
}: ValidationFeedbackProps) {
  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5" />
      case 'error':
        return <XCircle className="w-5 h-5" />
      case 'warning':
        return <AlertTriangle className="w-5 h-5" />
      case 'info':
        return <Info className="w-5 h-5" />
    }
  }

  const getColorClasses = () => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200 text-green-800'
      case 'error':
        return 'bg-red-50 border-red-200 text-red-800'
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800'
      case 'info':
        return 'bg-blue-50 border-blue-200 text-blue-800'
    }
  }

  const getIconColorClasses = () => {
    switch (type) {
      case 'success':
        return 'text-green-600'
      case 'error':
        return 'text-red-600'
      case 'warning':
        return 'text-yellow-600'
      case 'info':
        return 'text-blue-600'
    }
  }

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 0, y: -20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.95 }}
          transition={{ duration: 0.2 }}
          className={`border rounded-lg p-4 ${getColorClasses()}`}
        >
          <div className="flex items-start gap-3">
            <div className={`flex-shrink-0 ${getIconColorClasses()}`}>
              {getIcon()}
            </div>
            
            <div className="flex-1 min-w-0">
              <p className="font-medium">{message}</p>
              
              {details && details.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {details.map((detail, index) => (
                    <li key={index} className="text-sm opacity-90">
                      • {detail}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {onClose && (
              <button
                onClick={onClose}
                className="flex-shrink-0 opacity-60 hover:opacity-100 transition-opacity"
              >
                <XCircle className="w-4 h-4" />
              </button>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

// Specialized validation components for common use cases
export function SuccessFeedback({ message, details }: { message: string; details?: string[] }) {
  return (
    <ValidationFeedback
      type="success"
      message={message}
      details={details}
    />
  )
}

export function ErrorFeedback({ message, details }: { message: string; details?: string[] }) {
  return (
    <ValidationFeedback
      type="error"
      message={message}
      details={details}
    />
  )
}

export function WarningFeedback({ message, details }: { message: string; details?: string[] }) {
  return (
    <ValidationFeedback
      type="warning"
      message={message}
      details={details}
    />
  )
}

export function InfoFeedback({ message, details }: { message: string; details?: string[] }) {
  return (
    <ValidationFeedback
      type="info"
      message={message}
      details={details}
    />
  )
}

// Toast-style feedback for temporary messages
export function ToastFeedback({
  type,
  message,
  onClose,
  duration = 5000
}: {
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  onClose: () => void
  duration?: number
}) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 300 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 300 }}
      transition={{ duration: 0.3 }}
      className="fixed top-4 right-4 z-50 max-w-sm"
    >
      <ValidationFeedback
        type={type}
        message={message}
        show={true}
        onClose={onClose}
        autoHide={true}
        duration={duration}
      />
    </motion.div>
  )
}
