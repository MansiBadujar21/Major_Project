import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // Get the session token from cookies
    const sessionToken = request.cookies.get('session_token')
    
    console.log('🔍 Auth/me - Checking authentication...')
    console.log('🔍 Auth/me - Session token found:', !!sessionToken)
    
    if (!sessionToken) {
      console.log('❌ Auth/me - No session token found')
      return NextResponse.json(
        { success: false, message: 'Not authenticated' },
        { status: 401 }
      )
    }
    
    // Forward request to backend
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    console.log('🔍 Auth/me - Forwarding to backend:', `${backendUrl}/auth/me`)
    
    const response = await fetch(`${backendUrl}/auth/me`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': `session_token=${sessionToken.value}`
      }
    })

    const data = await response.json()
    console.log('🔍 Auth/me - Backend response:', response.status, data)

    if (response.ok) {
      console.log('✅ Auth/me - Authentication successful')
      return NextResponse.json(data)
    } else {
      console.log('❌ Auth/me - Authentication failed:', data)
      return NextResponse.json(
        { success: false, message: data.detail || 'Not authenticated' },
        { status: response.status }
      )
    }
  } catch (error) {
    console.error('❌ Auth/me - Error getting user info:', error)
    return NextResponse.json(
      { success: false, message: 'Internal server error' },
      { status: 500 }
    )
  }
}
