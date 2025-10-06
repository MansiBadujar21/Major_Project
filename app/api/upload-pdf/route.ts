import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json(
        { 
          success: false,
          error: 'No file provided',
          jobId: null,
          fileName: null,
          fileSize: 0,
          status: 'error',
          message: 'No file uploaded'
        },
        { status: 400 }
      )
    }

    if (file.type !== 'application/pdf') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Only PDF files are allowed',
          jobId: null,
          fileName: file.name,
          fileSize: file.size,
          status: 'error',
          message: 'Invalid file type'
        },
        { status: 400 }
      )
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB limit
      return NextResponse.json(
        { 
          success: false,
          error: 'File size exceeds 50MB limit',
          jobId: null,
          fileName: file.name,
          fileSize: file.size,
          status: 'error',
          message: 'File too large'
        },
        { status: 400 }
      )
    }

    // Forward the file to the FastAPI backend using async Gemini endpoint
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    
    const backendFormData = new FormData()
    backendFormData.append('file', file)

    // Start async processing
    const response = await fetch(`${backendUrl}/gemini/upload-gemini-async`, {
      method: 'POST',
      body: backendFormData,
    })

    if (!response.ok) {
      const errorData = await response.text()
      console.error('Backend upload error:', errorData)
      
      // Try to parse error as JSON for better error messages
      let errorMessage = 'Backend upload failed'
      try {
        const errorJson = JSON.parse(errorData)
        errorMessage = errorJson.detail || errorJson.error || errorMessage
      } catch {
        errorMessage = `${errorMessage}: ${errorData}`
      }
      
      return NextResponse.json(
        { 
          success: false,
          error: errorMessage,
          jobId: null,
          fileName: file.name,
          fileSize: file.size,
          status: 'error',
          message: 'Upload failed'
        },
        { status: response.status }
      )
    }

    const result = await response.json()
    
    // Validate backend response
    if (!result || typeof result !== 'object' || !result.job_id) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Invalid response from backend - missing job ID',
          jobId: null,
          fileName: file.name,
          fileSize: file.size,
          status: 'error',
          message: 'Invalid backend response'
        },
        { status: 500 }
      )
    }
    
    // Return job ID for status tracking
    return NextResponse.json({
      success: true,
      jobId: result.job_id,
      fileName: file.name,
      fileSize: file.size,
      status: 'processing',
      message: 'PDF processing started'
    })

  } catch (error) {
    console.error('PDF upload error:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        success: false,
        error: `Failed to upload PDF: ${errorMessage}`,
        jobId: null,
        fileName: null,
        fileSize: 0,
        status: 'error',
        message: 'Upload failed'
      },
      { status: 500 }
    )
  }
}
