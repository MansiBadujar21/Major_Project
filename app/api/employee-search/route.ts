import { NextRequest, NextResponse } from 'next/server'

// Simple configuration - like HTML version
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json()
    const { query } = body

    // Basic validation - like HTML version
    if (!query || typeof query !== 'string') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Query is required',
          suggestions: [],
          count: 0
        },
        { status: 400 }
      )
    }

    // Simple fetch to backend - exactly like HTML version's searchEmployees
    const response = await fetch(`${BACKEND_URL}/certificates/employee-suggestions/${encodeURIComponent(query)}`)
    
    if (!response.ok) {
      throw new Error(`Employee search error: ${response.statusText}`)
    }

    const data = await response.json()

    return NextResponse.json({
      success: data.success || false,
      suggestions: data.suggestions || [],
      count: data.count || 0,
      error: data.error || undefined,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('Employee search error:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        success: false,
        error: errorMessage,
        suggestions: [],
        count: 0
      },
      { status: 500 }
    )
  }
}
