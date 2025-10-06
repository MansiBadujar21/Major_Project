'use client'

import { motion } from 'framer-motion'
import { MessageCircle, FileText, FileCheck } from 'lucide-react'

interface ModeSelectorProps {
  currentMode: 'chat' | 'pdf' | 'documents'
  onModeChange: (mode: 'chat' | 'pdf' | 'documents') => void
  onModeChangeWithScroll?: (mode: 'chat' | 'pdf' | 'documents') => void
}

const modes = [
  {
    id: 'chat' as const,
    name: 'HR Q&A Chat',
    description: 'Ask questions about policies and procedures',
    icon: MessageCircle,
    color: 'from-blue-500 to-blue-600'
  },
  {
    id: 'pdf' as const,
    name: 'PDF Summarization',
    description: 'Upload and summarize large PDF documents',
    icon: FileText,
    color: 'from-purple-500 to-purple-600'
  },
  {
    id: 'documents' as const,
    name: 'Document Requests',
    description: 'Generate official HR documents',
    icon: FileCheck,
    color: 'from-green-500 to-green-600'
  }
]

export default function ModeSelector({ currentMode, onModeChange, onModeChangeWithScroll }: ModeSelectorProps) {
  return (
    <div className="flex flex-col sm:flex-row gap-4 justify-center" data-mode-selector>
      {modes.map((mode) => {
        const Icon = mode.icon
        const isActive = currentMode === mode.id
        
        return (
          <motion.button
            key={mode.id}
            onClick={() => {
              onModeChange(mode.id)
              if (onModeChangeWithScroll) {
                onModeChangeWithScroll(mode.id)
              }
            }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`
              relative p-6 rounded-xl border-2 transition-all duration-300 cursor-pointer
              ${isActive 
                ? `bg-gradient-to-r ${mode.color} text-white border-transparent shadow-lg` 
                : 'bg-white text-gray-700 border-gray-200 hover:border-gray-300 hover:shadow-md'
              }
            `}
          >
            {isActive && (
              <motion.div
                layoutId="activeMode"
                className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent rounded-xl"
                initial={false}
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
              />
            )}
            
            <div className="relative z-10 flex flex-col items-center text-center">
              <div className={`
                p-3 rounded-lg mb-3 transition-colors
                ${isActive ? 'bg-white/20' : 'bg-gray-100'}
              `}>
                <Icon className={`w-6 h-6 ${isActive ? 'text-white' : 'text-gray-600'}`} />
              </div>
              
              <h3 className={`font-semibold mb-1 ${isActive ? 'text-white' : 'text-gray-900'}`}>
                {mode.name}
              </h3>
              
              <p className={`text-sm ${isActive ? 'text-white/90' : 'text-gray-600'}`}>
                {mode.description}
              </p>
            </div>
          </motion.button>
        )
      })}
    </div>
  )
}
