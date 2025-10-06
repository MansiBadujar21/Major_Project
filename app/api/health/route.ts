import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    
    // Test backend connectivity
    const response = await fetch(`${backendUrl}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      return NextResponse.json(
        { 
          status: 'error',
          message: 'Backend is not responding properly',
          backend_status: response.status,
          backend_url: backendUrl
        },
        { status: 503 }
      )
    }

    const backendData = await response.json()
    
    return NextResponse.json({
      status: 'ok',
      message: 'All systems operational',
      backend_status: 'ok',
      backend_url: backendUrl,
      backend_data: backendData
    })

  } catch (error) {
    console.error('Health check error:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        status: 'error',
        message: 'Health check failed',
        error: errorMessage,
        backend_url: process.env.BACKEND_URL || 'http://localhost:8000'
      },
      { status: 500 }
    )
  }
}
