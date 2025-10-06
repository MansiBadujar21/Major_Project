'use client'

import { useState, useCallback, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, FileText, Download, Loader2, X, CheckCircle } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import toast from 'react-hot-toast'

interface UploadedFile {
  id: string
  name: string
  size: number
  status: 'uploading' | 'processing' | 'completed' | 'error'
  summary?: any
  downloadUrl?: string
  jobId?: string
  progress?: number
  message?: string
}

export default function PDFUploader() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isProcessing, setIsProcessing] = useState(false)

  // Status checking intervals
  const statusIntervals = new Map<string, NodeJS.Timeout>()

  // Cleanup intervals on unmount
  useEffect(() => {
    return () => {
      statusIntervals.forEach(interval => clearInterval(interval))
    }
  }, [])

  const checkJobStatus = useCallback(async (fileId: string, jobId: string) => {
    try {
      const response = await fetch('/api/process-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ jobId }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        console.error('Status check failed:', errorData)
        
        const errorMessage = errorData.error || 'Status check failed'
        throw new Error(errorMessage)
      }

      const status = await response.json()

      // Validate status response
      if (!status.success) {
        throw new Error(status.error || 'Status check failed')
      }

      setUploadedFiles(prev => 
        prev.map(f => f.id === fileId ? {
          ...f,
          progress: status.progress || 0,
          message: status.message || 'Processing...'
        } : f)
      )

      if (status.status === 'completed') {
        // Clear interval
        const interval = statusIntervals.get(fileId)
        if (interval) {
          clearInterval(interval)
          statusIntervals.delete(fileId)
        }

        // Update file status
        setUploadedFiles(prev => 
          prev.map(f => f.id === fileId ? {
            ...f,
            status: 'completed',
            summary: status.result,
            progress: 100,
            message: 'Processing completed'
          } : f)
        )

        toast.success('PDF processing completed!')
      } else if (status.status === 'failed') {
        // Clear interval
        const interval = statusIntervals.get(fileId)
        if (interval) {
          clearInterval(interval)
          statusIntervals.delete(fileId)
        }

        // Update file status
        setUploadedFiles(prev => 
          prev.map(f => f.id === fileId ? {
            ...f,
            status: 'error',
            message: status.error || 'Processing failed'
          } : f)
        )

        toast.error(`Processing failed: ${status.error || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Status check error:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
      
      // Update file status on error
      setUploadedFiles(prev => 
        prev.map(f => f.id === fileId ? {
          ...f,
          status: 'error',
          message: errorMessage
        } : f)
      )
    }
  }, [statusIntervals])

  const startStatusChecking = useCallback((fileId: string, jobId: string) => {
    const interval = setInterval(() => checkJobStatus(fileId, jobId), 2000)
    statusIntervals.set(fileId, interval)
  }, [checkJobStatus, statusIntervals])

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      if (file.type !== 'application/pdf') {
        toast.error(`${file.name} is not a PDF file`)
        continue
      }

      if (file.size > 50 * 1024 * 1024) { // 50MB limit
        toast.error(`${file.name} is too large. Maximum size is 50MB`)
        continue
      }

      const fileId = Date.now().toString()
      const newFile: UploadedFile = {
        id: fileId,
        name: file.name,
        size: file.size,
        status: 'uploading'
      }

      setUploadedFiles(prev => [...prev, newFile])

      try {
        // Upload file and start async processing
        const formData = new FormData()
        formData.append('file', file)

        const uploadResponse = await fetch('/api/upload-pdf', {
          method: 'POST',
          body: formData,
        })

        if (!uploadResponse.ok) {
          const errorData = await uploadResponse.json()
          console.error('Upload response error:', errorData)
          
          const errorMessage = errorData.error || `Upload failed: ${uploadResponse.status}`
          throw new Error(errorMessage)
        }

        const uploadData = await uploadResponse.json()

        // Validate upload response
        if (!uploadData.success) {
          throw new Error(uploadData.error || 'Upload failed')
        }

        // Update status to processing and start status checking
        setUploadedFiles(prev => 
          prev.map(f => f.id === fileId ? {
            ...f,
            status: 'processing',
            jobId: uploadData.jobId,
            progress: 0,
            message: 'Starting PDF analysis...'
          } : f)
        )

        // Start status checking
        startStatusChecking(fileId, uploadData.jobId)

        toast.success(`${file.name} uploaded and processing started!`)

      } catch (error) {
        console.error('Error processing file:', error)
        const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
        
        setUploadedFiles(prev => 
          prev.map(f => f.id === fileId ? { 
            ...f, 
            status: 'error',
            message: errorMessage
          } : f)
        )
        toast.error(`Failed to process ${file.name}: ${errorMessage}`)
      }
    }
  }, [startStatusChecking])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true
  })

  const removeFile = (fileId: string) => {
    // Clear status checking interval if exists
    const interval = statusIntervals.get(fileId)
    if (interval) {
      clearInterval(interval)
      statusIntervals.delete(fileId)
    }
    
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const downloadSummary = async (file: UploadedFile) => {
    if (!file.summary) return

    try {
      // Call backend to generate PDF summary
      const response = await fetch('/api/download-summary-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          summary_data: file.summary,
          original_filename: file.name
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate PDF summary')
      }

      // Download the PDF
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${file.name.replace('.pdf', '')}_summary.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      toast.success('Summary PDF downloaded successfully!')
    } catch (error) {
      console.error('Error downloading summary:', error)
      toast.error('Failed to download summary PDF')
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-semibold">PDF Summarization</h2>
              <p className="text-purple-100 text-sm">Upload large PDFs and get intelligent summaries with AI processing</p>
            </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="p-6">
          <div
            {...getRootProps()}
            className={`
              border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200
              ${isDragActive 
                ? 'border-purple-500 bg-purple-50' 
                : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
              }
            `}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-lg font-medium text-gray-900 mb-2">
              {isDragActive ? 'Drop PDF files here' : 'Drop your PDF files here'}
            </p>
            <p className="text-gray-600 mb-4">
              Supports files up to 50MB | Large documents (30+ pages) supported
            </p>
            <p className="text-sm text-gray-500">
              Powered by advanced AI for superior accuracy
            </p>
          </div>

          {/* File List */}
          {uploadedFiles.length > 0 && (
            <div className="mt-6 space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Uploaded Files</h3>
              {uploadedFiles.map((file) => (
                <motion.div
                  key={file.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-gray-50 rounded-lg p-4 border border-gray-200"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <FileText className="w-5 h-5 text-gray-600" />
                      <div>
                        <p className="font-medium text-gray-900">{file.name}</p>
                        <p className="text-sm text-gray-600">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {file.status === 'uploading' && (
                        <div className="flex items-center gap-2 text-blue-600">
                          <Loader2 className="w-4 h-4 animate-spin" />
                          <span className="text-sm">Uploading...</span>
                        </div>
                      )}
                      {file.status === 'processing' && (
                        <div className="flex items-center gap-2 text-purple-600">
                          <Loader2 className="w-4 h-4 animate-spin" />
                          <span className="text-sm">
                            {file.progress ? `${file.progress}%` : 'Processing...'}
                          </span>
                        </div>
                      )}
                      {file.status === 'completed' && (
                        <div className="flex items-center gap-2 text-green-600">
                          <CheckCircle className="w-4 h-4" />
                          <span className="text-sm">Completed</span>
                        </div>
                      )}
                      {file.status === 'error' && (
                        <div className="flex items-center gap-2 text-red-600">
                          <X className="w-4 h-4" />
                          <span className="text-sm">Error</span>
                        </div>
                      )}
                      <button
                        onClick={() => removeFile(file.id)}
                        className="text-gray-400 hover:text-red-500 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {/* Progress Bar for Processing */}
                  {file.status === 'processing' && file.progress !== undefined && (
                    <div className="mb-3">
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>{file.message || 'Processing...'}</span>
                        <span>{file.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${file.progress}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {/* Summary Display */}
                  {file.status === 'completed' && file.summary && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="mt-4 p-4 bg-white rounded-lg border border-gray-200"
                    >
                      <h4 className="font-semibold text-gray-900 mb-3">AI Summary</h4>
                      
                      {/* Executive Summary */}
                      {file.summary.executive_summary && (
                        <div className="mb-4">
                          <h5 className="font-medium text-gray-800 mb-2">Executive Summary</h5>
                          <p className="text-gray-700 text-sm leading-relaxed">
                            {file.summary.executive_summary}
                          </p>
                        </div>
                      )}

                      {/* Key Points */}
                      {file.summary.key_points && file.summary.key_points.length > 0 && (
                        <div className="mb-4">
                          <h5 className="font-medium text-gray-800 mb-2">Key Points</h5>
                          <ul className="list-disc list-inside space-y-1 text-gray-700 text-sm">
                            {file.summary.key_points.map((point: string, index: number) => (
                              <li key={index}>{point}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Keywords */}
                      {file.summary.keywords && file.summary.keywords.length > 0 && (
                        <div className="mb-4">
                          <h5 className="font-medium text-gray-800 mb-2">Key Topics</h5>
                          <div className="flex flex-wrap gap-2">
                            {file.summary.keywords.slice(0, 10).map((keyword: string, index: number) => (
                              <span
                                key={index}
                                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                              >
                                {keyword}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Tables */}
                      {file.summary.tables && file.summary.tables.length > 0 && (
                        <div className="mb-4">
                          <h5 className="font-medium text-gray-800 mb-2">Tables Found ({file.summary.tables.length})</h5>
                          {file.summary.tables.map((table: any, index: number) => (
                            <div key={index} className="mb-3 p-3 bg-gray-50 rounded-lg">
                              <h6 className="font-medium text-gray-700 mb-1">
                                Table {table.id}: {table.title}
                              </h6>
                              <p className="text-sm text-gray-600 mb-2">{table.dimensions}</p>
                              <div className="overflow-x-auto">
                                <div 
                                  className="text-sm"
                                  dangerouslySetInnerHTML={{ __html: table.markdown.replace(/\n/g, '<br/>') }}
                                />
                              </div>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Actions */}
                      <div className="flex gap-3 mt-4">
                        <button
                          onClick={() => downloadSummary(file)}
                          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                        >
                          <Download className="w-4 h-4" />
                          Download Summary PDF
                        </button>
                      </div>
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
