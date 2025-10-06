'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Mail, Lock, Eye, EyeOff, ArrowLeft, RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'

interface LoginResponse {
  success: boolean
  message: string
  token?: string
}

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [otp, setOtp] = useState('')
  const [isOtpSent, setIsOtpSent] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [countdown, setCountdown] = useState(0)
  const [hasCheckedAuth, setHasCheckedAuth] = useState(false)

  // Check if user is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      // Prevent multiple checks
      if (hasCheckedAuth) {
        return
      }

      try {
        console.log('🔍 Login page - Checking if already authenticated...')
        const response = await fetch('/api/auth/me', {
          credentials: 'include'
        })
        
        if (response.ok) {
          console.log('✅ Login page - Already authenticated, redirecting to main page...')
          setHasCheckedAuth(true)
          router.push('/')
        } else {
          console.log('❌ Login page - Not authenticated, staying on login page')
          setHasCheckedAuth(true)
        }
      } catch (error) {
        console.error('❌ Login page - Error checking authentication:', error)
        setHasCheckedAuth(true)
        // User not authenticated, stay on login page
      }
    }
    
    // Add a small delay to prevent race conditions with logout
    const timer = setTimeout(() => {
      checkAuth()
    }, 100)
    
    return () => clearTimeout(timer)
  }, [router, hasCheckedAuth])

  // Countdown timer for OTP expiry
  useEffect(() => {
    let interval: NodeJS.Timeout
    if (countdown > 0) {
      interval = setInterval(() => {
        setCountdown((prev) => prev - 1)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [countdown])

  const handleSendOtp = async () => {
    if (!email) {
      toast.error('Please enter your email address')
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/api/auth/send-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      })

      const data: LoginResponse = await response.json()

      if (response.ok) {
        setIsOtpSent(true)
        setCountdown(300) // 5 minutes
        toast.success(data.message)
      } else {
        toast.error(data.message || 'Failed to send OTP')
      }
    } catch (error) {
      toast.error('Network error. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleVerifyOtp = async () => {
    if (!otp) {
      toast.error('Please enter the OTP')
      return
    }

    setIsLoading(true)
    try {
      console.log('🔍 Login page - Verifying OTP...')
      console.log('🔍 Login page - Email:', email, 'OTP:', otp)
      
      const response = await fetch('/api/auth/verify-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, otp }),
        credentials: 'include'
      })

      const data: LoginResponse = await response.json()
      console.log('🔍 Login page - OTP verification response:', response.status, data)

      if (response.ok) {
        console.log('✅ Login page - OTP verification successful')
        console.log('✅ Login page - Cookies after verification:', document.cookie)
        toast.success('Login successful!')
        
        // Add a longer delay to ensure cookie is properly set and backend processes the request
        setTimeout(() => {
          console.log('🔍 Login page - Redirecting to main page...')
          // Force a hard redirect to ensure the page reloads completely
          window.location.href = '/'
        }, 1000)
      } else {
        console.log('❌ Login page - OTP verification failed')
        toast.error(data.message || 'Invalid OTP')
      }
    } catch (error) {
      console.error('❌ Login page - Error during OTP verification:', error)
      toast.error('Network error. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleResendOtp = async () => {
    console.log('🔍 Login page - Starting resend OTP process...')
    console.log('🔍 Login page - Email:', email)
    
    setIsLoading(true)
    try {
      const response = await fetch('/api/auth/resend-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      })

      const data: LoginResponse = await response.json()
      console.log('🔍 Login page - Resend OTP response:', response.status, data)

      if (response.ok) {
        console.log('✅ Login page - Resend OTP successful')
        setCountdown(300) // 5 minutes
        toast.success(data.message)
      } else {
        console.log('❌ Login page - Resend OTP failed')
        toast.error(data.message || 'Failed to resend OTP')
      }
    } catch (error) {
      console.error('❌ Login page - Error during resend OTP:', error)
      toast.error('Network error. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  // Handle Enter key for email input
  const handleEmailKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && email && !isLoading) {
      e.preventDefault()
      handleSendOtp()
    }
  }

  // Handle Enter key for OTP input
  const handleOtpKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && otp && otp.length === 6 && !isLoading) {
      e.preventDefault()
      handleVerifyOtp()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <Lock className="w-8 h-8 text-white" />
          </motion.div>
                     <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
           <p className="text-gray-600">Sign in to access Reliance Jio Infotech Solutions</p>
        </div>

        {/* Login Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100"
        >
          {!isOtpSent ? (
            // Email Input Step
            <form onSubmit={(e) => {
              e.preventDefault()
              if (email && !isLoading) {
                handleSendOtp()
              }
            }} className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    onKeyDown={handleEmailKeyDown}
                    placeholder="Enter your email address"
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    disabled={isLoading}
                    required
                  />
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  Only authorized employees can access this system
                </p>
              </div>

              <button
                type="submit"
                disabled={isLoading || !email}
                className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:from-blue-600 hover:to-indigo-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Sending OTP...
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <span>Send OTP</span>
                    <span className="ml-2 text-xs opacity-75">(or press Enter)</span>
                  </div>
                )}
              </button>
            </form>
          ) : (
            // OTP Verification Step
            <form onSubmit={(e) => {
              e.preventDefault()
              if (otp && otp.length === 6 && !isLoading) {
                handleVerifyOtp()
              }
            }} className="space-y-6">
              <div className="text-center">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Mail className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Check Your Email</h3>
                <p className="text-sm text-gray-600 mb-2">
                  We've sent a 6-digit OTP to <span className="font-medium">{email}</span>
                </p>
                {countdown > 0 && (
                  <p className="text-xs text-red-600">
                    OTP expires in {formatTime(countdown)}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="otp" className="block text-sm font-medium text-gray-700 mb-2">
                  Enter OTP
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    id="otp"
                    type={showPassword ? "text" : "password"}
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    onKeyDown={handleOtpKeyDown}
                    placeholder="Enter 6-digit OTP"
                    maxLength={6}
                    className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-center text-lg tracking-widest"
                    disabled={isLoading}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                <button
                  type="submit"
                  disabled={isLoading || !otp || otp.length !== 6}
                  className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:from-blue-600 hover:to-indigo-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Verifying...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center">
                      <span>Verify OTP</span>
                      <span className="ml-2 text-xs opacity-75">(or press Enter)</span>
                    </div>
                  )}
                </button>

                <button
                  type="button"
                  onClick={() => setIsOtpSent(false)}
                  className="w-full flex items-center justify-center text-gray-600 hover:text-gray-800 transition-colors duration-200"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back to Email
                </button>

                {countdown === 0 && (
                  <button
                    type="button"
                    onClick={handleResendOtp}
                    disabled={isLoading}
                    className="w-full flex items-center justify-center text-blue-600 hover:text-blue-700 transition-colors duration-200 disabled:opacity-50"
                  >
                    <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                    Resend OTP
                  </button>
                )}
              </div>
            </form>
          )}
        </motion.div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center mt-6"
        >
                     <p className="text-sm text-gray-500">
             © 2025 Reliance Jio Infotech Solutions. All rights reserved.
           </p>
        </motion.div>
      </motion.div>
    </div>
  )
}
