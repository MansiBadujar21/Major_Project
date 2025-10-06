import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, otp } = body

    console.log('🔍 Verify OTP - Starting verification for email:', email)

    if (!email || !otp) {
      console.log('❌ Verify OTP - Missing email or OTP')
      return NextResponse.json(
        { success: false, message: 'Email and OTP are required' },
        { status: 400 }
      )
    }

    // Forward request to backend
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    console.log('🔍 Verify OTP - Forwarding to backend:', `${backendUrl}/auth/verify-otp`)
    
    const response = await fetch(`${backendUrl}/auth/verify-otp`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, otp }),
    })

    const data = await response.json()
    console.log('🔍 Verify OTP - Backend response:', response.status, data)

    if (response.ok) {
      // Create response with cookies
      const nextResponse = NextResponse.json(data)
      
      // Set the session cookie from backend response
      if (data.token) {
        console.log('✅ Verify OTP - Setting session cookie')
        nextResponse.cookies.set('session_token', data.token, {
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production',
          sameSite: 'lax',
          maxAge: 86400, // 24 hours
          path: '/', // Ensure cookie is available on all paths
        })
      } else {
        console.log('⚠️ Verify OTP - No token in response')
      }
      
      console.log('✅ Verify OTP - Verification successful')
      return nextResponse
    } else {
      console.log('❌ Verify OTP - Verification failed:', data)
      return NextResponse.json(
        { success: false, message: data.detail || 'Invalid OTP' },
        { status: response.status }
      )
    }
  } catch (error) {
    console.error('❌ Verify OTP - Error during verification:', error)
    return NextResponse.json(
      { success: false, message: 'Internal server error' },
      { status: 500 }
    )
  }
}
