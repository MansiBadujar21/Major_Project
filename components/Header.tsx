'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Bot, Sparkles, Shield, LogOut, User, ChevronDown } from 'lucide-react'
import toast from 'react-hot-toast'
import { createPortal } from 'react-dom'

interface UserInfo {
  emp_id: number
  full_name: string
  email: string
  designation: string
  department: string
}

export default function Header() {
  const router = useRouter()
  const [user, setUser] = useState<UserInfo | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [showUserMenu, setShowUserMenu] = useState(false)

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('/api/auth/me', {
          credentials: 'include'
        })
        
        if (response.ok) {
          const data = await response.json()
          setUser(data.user)
        } else {
          // Don't redirect here - let the main page handle authentication
          // Just set user to null and let the main page redirect
          setUser(null)
        }
      } catch (error) {
        console.error('Error fetching user info:', error)
        // Don't redirect here - let the main page handle authentication
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    fetchUserInfo()
  }, [router])

  // Handle keyboard events to close dropdown
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && showUserMenu) {
        setShowUserMenu(false)
      }
    }

    if (showUserMenu) {
      document.addEventListener('keydown', handleKeyDown)
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [showUserMenu])

  // Handle global click events to close dropdown
  useEffect(() => {
    const handleGlobalClick = (event: MouseEvent) => {
      if (showUserMenu) {
        // Check if click is outside the user menu container
        const userMenuContainer = document.querySelector('[data-user-menu]')
        if (userMenuContainer && !userMenuContainer.contains(event.target as Node)) {
          console.log('🔍 Header - Global click outside detected, closing dropdown')
          setShowUserMenu(false)
        }
      }
    }

    if (showUserMenu) {
      document.addEventListener('click', handleGlobalClick)
    }

    return () => {
      document.removeEventListener('click', handleGlobalClick)
    }
  }, [showUserMenu])

  // Cleanup effect for portal
  useEffect(() => {
    return () => {
      // Ensure dropdown is closed when component unmounts
      if (showUserMenu) {
        setShowUserMenu(false)
      }
    }
  }, [showUserMenu])

  const handleLogout = async () => {
    try {
      console.log('🔍 Header - Starting logout process...')
      
      const response = await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'include'
      })

      if (response.ok) {
        console.log('✅ Header - Logout successful')
        toast.success('Logged out successfully')
        // Clear user state immediately
        setUser(null)
        // Add a small delay to ensure logout completes, then redirect to login page
        console.log('✅ Header - Logout complete, redirecting to login...')
        setTimeout(() => {
          // Use hard redirect to ensure it works
          window.location.href = '/login'
        }, 500)
      } else {
        console.log('❌ Header - Logout failed')
        toast.error('Failed to logout')
      }
    } catch (error) {
      console.error('❌ Header - Error during logout:', error)
      toast.error('Network error during logout')
    }
  }

  if (isLoading) {
    return (
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50"
      >
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Reliance Jio Infotech Solutions
                </h1>
                <p className="text-sm text-gray-600 flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  AI-Powered HR Assistant
                </p>
              </div>
            </div>
            <div className="animate-pulse bg-gray-200 h-8 w-32 rounded"></div>
          </div>
        </div>
      </motion.header>
    )
  }

  return (
    <motion.header 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50"
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.div 
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="flex items-center gap-3"
          >
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <motion.div
                animate={{ 
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 1, 0.5]
                }}
                transition={{ 
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
                className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center"
              >
                <div className="w-2 h-2 bg-white rounded-full" />
              </motion.div>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Reliance Jio Infotech Solutions
              </h1>
              <p className="text-sm text-gray-600 flex items-center gap-1">
                <Sparkles className="w-3 h-3" />
                AI-Powered HR Assistant
              </p>
            </div>
          </motion.div>

          {/* User Menu */}
          {user && (
            <div className="relative" data-user-menu>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  setShowUserMenu(!showUserMenu)
                }}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
              >
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
                <div className="hidden md:block text-left">
                  <p className="text-sm font-medium text-gray-900">{user.full_name}</p>
                  <p className="text-xs text-gray-600">{user.designation}</p>
                </div>
                <ChevronDown className={`w-4 h-4 text-gray-600 transition-transform ${showUserMenu ? 'rotate-180' : ''}`} />
              </button>

              {/* Dropdown Menu */}
              {showUserMenu && (
                <>
                  {/* Click outside overlay using portal */}
                  {typeof window !== 'undefined' && createPortal(
                    <div 
                      className="fixed inset-0 z-40 bg-transparent" 
                      onClick={() => {
                        console.log('🔍 Header - Portal overlay clicked, closing dropdown')
                        setShowUserMenu(false)
                      }}
                      style={{ 
                        top: 0, 
                        left: 0, 
                        right: 0, 
                        bottom: 0,
                        width: '100vw',
                        height: '100vh'
                      }}
                    />,
                    document.body
                  )}
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
                    onClick={(e) => {
                      e.stopPropagation()
                      console.log('🔍 Header - Dropdown clicked, keeping open')
                    }}
                  >
                    <div className="px-4 py-3 border-b border-gray-100">
                      <p className="text-sm font-medium text-gray-900">{user.full_name}</p>
                      <p className="text-xs text-gray-600">{user.email}</p>
                      <p className="text-xs text-gray-500">{user.department} • {user.designation}</p>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleLogout()
                      }}
                      className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    >
                      <LogOut className="w-4 h-4" />
                      Logout
                    </button>
                  </motion.div>
                </>
              )}
            </div>
          )}

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </motion.header>
  )
}
