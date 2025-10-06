import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { jobId } = body

    if (!jobId || typeof jobId !== 'string' || jobId.trim().length === 0) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Job ID is required and must be a non-empty string',
          status: 'error',
          progress: 0,
          message: 'Invalid job ID'
        },
        { status: 400 }
      )
    }

    // Check status from the FastAPI backend
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    
    const response = await fetch(`${backendUrl}/gemini/status/${jobId.trim()}`, {
      method: 'GET',
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Status check failed:', response.status, errorText)
      
      // Try to parse error as JSON for better error messages
      let errorMessage = 'Status check failed'
      try {
        const errorJson = JSON.parse(errorText)
        errorMessage = errorJson.detail || errorJson.error || errorMessage
      } catch {
        errorMessage = `${errorMessage}: ${errorText}`
      }
      
      return NextResponse.json(
        { 
          success: false,
          error: errorMessage,
          status: 'error',
          progress: 0,
          message: 'Status check failed'
        },
        { status: response.status }
      )
    }

    const status = await response.json()
    
    // Validate backend response
    if (!status || typeof status !== 'object') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Invalid response format from backend',
          status: 'error',
          progress: 0,
          message: 'Invalid backend response'
        },
        { status: 500 }
      )
    }
    
    return NextResponse.json({
      success: true,
      ...status
    })

  } catch (error) {
    console.error('Status check error:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        success: false,
        error: `Failed to check status: ${errorMessage}`,
        status: 'error',
        progress: 0,
        message: 'Status check failed'
      },
      { status: 500 }
    )
  }
}
