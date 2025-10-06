'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Send, 
  Upload, 
  FileText, 
  MessageCircle, 
  Download, 
  Eye, 
  Copy,
  Sparkles,
  Shield,
  Zap,
  Users,
  FileCheck,
  Bot,
  ChevronDown,
  ChevronUp
} from 'lucide-react'
import toast from 'react-hot-toast'
import ChatInterface from '@/components/ChatInterface'
import DocumentForm from '@/components/DocumentForm'
import PDFUploader from '@/components/PDFUploader'
import ModeSelector from '@/components/ModeSelector'
import Header from '@/components/Header'
import ErrorBoundary from '@/components/ErrorBoundary'
import { cn } from '@/lib/utils'
import { Message, ChatSession, TeamMember } from '@/lib/types'

export default function Home() {
  const router = useRouter()
  const [currentMode, setCurrentMode] = useState<'chat' | 'pdf' | 'documents'>('chat')
  const [showFeatures, setShowFeatures] = useState(false)
  const [isClient, setIsClient] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [hasRedirected, setHasRedirected] = useState(false)
  const mainContainerRef = useRef<HTMLDivElement>(null)
  const interfaceSectionRef = useRef<HTMLDivElement>(null)

  // Chat state - lifted up to persist across mode switches
  const [chatMessages, setChatMessages] = useState<Message[]>([])
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([])
  const [currentSessionId, setCurrentSessionId] = useState<string>('')

  // Handle authentication check
  useEffect(() => {
    const checkAuth = async () => {
      try {
        console.log('🔍 Main page - Checking authentication...')
        console.log('🔍 Main page - Current URL:', window.location.href)
        
        const response = await fetch('/api/auth/me', {
          credentials: 'include'
        })
        
        console.log('🔍 Main page - Auth response status:', response.status)
        
        if (response.ok) {
          const data = await response.json()
          console.log('✅ Main page - Authentication successful:', data)
          setIsAuthenticated(true)
          // Reset redirect flag when authentication is successful
          setHasRedirected(false)
        } else {
          const data = await response.json()
          console.log('❌ Main page - Authentication failed:', data)
          
          // If we were previously authenticated but now we're not, this is likely a logout
          if (isAuthenticated) {
            console.log('🔄 Main page - Logout detected, redirecting to login...')
            setIsAuthenticated(false)
            setHasRedirected(false)
            // Force a redirect to login
            router.push('/login')
            return
          }
          
          // Only redirect if we haven't already and we're not already on login page
          if (!hasRedirected && window.location.pathname !== '/login') {
            console.log('❌ Main page - Redirecting to login...')
            setHasRedirected(true)
            router.push('/login')
            return
          }
        }
      } catch (error) {
        console.error('❌ Main page - Error checking authentication:', error)
        
        // If we were previously authenticated but now we're not, this is likely a logout
        if (isAuthenticated) {
          console.log('🔄 Main page - Logout detected (error), redirecting to login...')
          setIsAuthenticated(false)
          setHasRedirected(false)
          // Force a redirect to login
          router.push('/login')
          return
        }
        
        // Only redirect if we haven't already and we're not already on login page
        if (!hasRedirected && window.location.pathname !== '/login') {
          console.log('❌ Main page - Redirecting to login due to error...')
          setHasRedirected(true)
          router.push('/login')
          return
        }
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [router, hasRedirected, isAuthenticated])

  // Handle hydration and ensure page starts at top
  useEffect(() => {
    setIsClient(true)
    
    // Ensure page scrolls to top on load/reload
    window.scrollTo(0, 0)
  }, [])

  // Handle scrolling when mode changes (triggered by feature card clicks)
  const [shouldScrollToInterface, setShouldScrollToInterface] = useState(false)
  
  useEffect(() => {
    if (shouldScrollToInterface) {
      setTimeout(() => {
        if (interfaceSectionRef.current) {
          interfaceSectionRef.current.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
          })
        }
        setShouldScrollToInterface(false)
      }, 100)
    }
  }, [currentMode, shouldScrollToInterface])

  // Handle feature card clicks
  const handleFeatureClick = (featureTitle: string) => {
    let targetMode: 'chat' | 'pdf' | 'documents' = 'chat'
    
    // Map feature titles to modes
    if (featureTitle.includes('Q&A') || featureTitle.includes('Chat')) {
      targetMode = 'chat'
    } else if (featureTitle.includes('PDF') || featureTitle.includes('Summarization')) {
      targetMode = 'pdf'
    } else if (featureTitle.includes('Document') || featureTitle.includes('Request')) {
      targetMode = 'documents'
    }
    
    console.log('Feature clicked:', featureTitle, 'Target mode:', targetMode)
    
    // Set the mode and trigger scroll
    setCurrentMode(targetMode)
    setShouldScrollToInterface(true)
  }

  const features = [
    {
      icon: <MessageCircle className="w-6 h-6" />,
      title: "HR Q&A Chat",
      description: "Ask questions about company policies, benefits, and procedures with semantic search and AI assistance"
    },
    {
      icon: <FileText className="w-6 h-6" />,
      title: "PDF Summarization",
      description: "Upload large PDFs (30+ pages) with tables and get comprehensive summaries with advanced AI processing"
    },
    {
      icon: <FileCheck className="w-6 h-6" />,
      title: "Document Requests",
      description: "Request any of 16 official document types through chat with form-based data collection"
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Enhanced Security",
      description: "Digital signatures and verification elements"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Real-time Processing",
      description: "Handles large PDFs up to 50MB with intelligent chunking and progress tracking"
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: "Employee Validation",
      description: "Seamless employee data validation against records with form-based requests"
    }
  ]

  const teamMembers: TeamMember[] = [
    {
      name: "Devyani Suresh Deore",
      role: "Brand Manager",
      department: "Marketing",
      skills: ["Frontend", "UI/UX", "Project Management"]
    },
    {
      name: "Ashwini Anil Nikumbh",
      role: "Account Executive", 
      department: "Finance",
      skills: ["Backend", "Database", "API Development"]
    },
    {
      name: "Khushbu Arun Jain",
      role: "HR Specialist",
      department: "Human Resources", 
      skills: ["AI Integration", "Business Logic", "Testing"]
    },
    {
      name: "Mansi Anil Badgujar",
      role: "Software Engineer",
      department: "IT",
      skills: ["Full Stack", "DevOps", "System Architecture"]
    }
  ]

  // Don't render until client-side hydration and authentication are complete
  if (!isClient || isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated && hasRedirected) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header />
      
      <main ref={mainContainerRef} className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-full mb-6"
          >
            <Sparkles className="w-5 h-5" />
            <span className="font-semibold">AI-Powered HR Assistant</span>
          </motion.div>
          
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Welcome to{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Reliance Jio
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Your intelligent companion for HR Q&A, document processing, and official document requests. 
            Powered by advanced AI for superior accuracy and efficiency.
          </p>

          {/* Features Toggle */}
          <div className="mb-8">
            <button
              onClick={() => setShowFeatures(!showFeatures)}
              className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium transition-colors"
            >
              {showFeatures ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
              {showFeatures ? 'Hide Features' : 'View Key Features'}
            </button>
          </div>

          {/* Features Grid */}
          <AnimatePresence>
            {showFeatures && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12"
              >
                {features.map((feature, index) => {
                  // Determine if this feature is currently active
                  const isActive = 
                    (feature.title.includes('Q&A') || feature.title.includes('Chat')) && currentMode === 'chat' ||
                    (feature.title.includes('PDF') || feature.title.includes('Summarization')) && currentMode === 'pdf' ||
                    (feature.title.includes('Document') || feature.title.includes('Request')) && currentMode === 'documents'
                  
                  return (
                    <motion.div
                      key={feature.title}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={cn(
                        "card-clickable",
                        isActive && "ring-2 ring-blue-500 bg-blue-50/50 border-blue-300"
                      )}
                      onClick={() => handleFeatureClick(feature.title)}
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <div className={cn(
                          "p-2 rounded-lg",
                          isActive ? "bg-blue-200 text-blue-700" : "bg-blue-100 text-blue-600"
                        )}>
                          {feature.icon}
                        </div>
                        <h3 className="font-semibold text-gray-900">{feature.title}</h3>
                      </div>
                      <p className="text-gray-600 text-sm">{feature.description}</p>
                    </motion.div>
                  )
                })}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Mode Selector */}
        <ModeSelector 
          currentMode={currentMode} 
          onModeChange={setCurrentMode}
          onModeChangeWithScroll={(mode) => {
            setCurrentMode(mode)
            setShouldScrollToInterface(true)
          }}
        />

        {/* Main Interface */}
        <ErrorBoundary>
          <motion.div
            key={currentMode}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="mt-8"
            ref={interfaceSectionRef}
          >
            {currentMode === 'chat' && (
              <ChatInterface 
                messages={chatMessages}
                setMessages={setChatMessages}
                chatSessions={chatSessions}
                setChatSessions={setChatSessions}
                currentSessionId={currentSessionId}
                setCurrentSessionId={setCurrentSessionId}
              />
            )}
            {currentMode === 'pdf' && <PDFUploader />}
            {currentMode === 'documents' && <DocumentForm />}
          </motion.div>
        </ErrorBoundary>
      </main>

      {/* Team Section */}
      <section className="bg-gradient-to-r from-blue-50 to-purple-50 py-16 mt-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Meet Our Development Team
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              This AI-powered HR Assistant was built by talented students as their college major project. 
              Each team member contributed their expertise to create this innovative solution.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member: TeamMember, index: number) => (
              <motion.div
                key={member.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-6 text-center group"
              >
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center text-white text-2xl font-bold group-hover:scale-110 transition-transform duration-300">
                  {member.name.split(' ').map((n: string) => n[0]).join('')}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{member.name}</h3>
                <p className="text-blue-600 font-medium mb-1">{member.role}</p>
                <p className="text-gray-600 text-sm mb-3">{member.department}</p>
                <div className="flex justify-center space-x-2">
                  {member.skills.map((skill: string, skillIndex: number) => (
                    <span
                      key={skillIndex}
                      className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.5 }}
            className="text-center mt-12"
          >
            <div className="inline-flex items-center gap-2 bg-gradient-to-r from-green-600 to-blue-600 text-white px-6 py-3 rounded-full">
              <Sparkles className="w-5 h-5" />
              <span className="font-semibold">College Major Project</span>
            </div>
            <p className="text-gray-600 mt-4 max-w-2xl mx-auto">
              This project demonstrates the power of modern web technologies, AI integration, 
              and collaborative development in creating real-world solutions for enterprise needs.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Bot className="w-6 h-6 text-blue-400" />
            <span className="text-xl font-semibold">Reliance Jio Infotech Solutions</span>
          </div>
          <p className="text-gray-400">
            Advanced AI-Powered Document Processing & HR Q&A System
          </p>
          <p className="text-gray-500 text-sm mt-2">
            © 2025 Reliance Jio Infotech Solutions. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}
