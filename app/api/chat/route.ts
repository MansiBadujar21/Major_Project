import { NextRequest, NextResponse } from 'next/server'

// Simple configuration - like HTML version
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json()
    const { message } = body

    // Basic validation - like HTML version
    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Message is required',
          response: 'Please provide a message to chat with.'
        },
        { status: 400 }
      )
    }

    // Simple fetch to backend - exactly like HTML version's handleQAMessage
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message })
    })

    if (!response.ok) {
      throw new Error(`QA API error: ${response.statusText}`)
    }

    const data = await response.json()

    return NextResponse.json({
      success: true,
      response: data.response || '',
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('QA Error:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        success: false,
        error: errorMessage,
        response: `❌ Sorry, I encountered an error processing your question: ${errorMessage}\n\nPlease try again or contact support if the issue persists.`
      },
      { status: 500 }
    )
  }
}
