import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email } = body

    console.log('🔍 Resend OTP - Starting resend process for email:', email)

    if (!email) {
      console.log('❌ Resend OTP - Missing email')
      return NextResponse.json(
        { success: false, message: 'Email is required' },
        { status: 400 }
      )
    }

    // Forward request to backend
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    console.log('🔍 Resend OTP - Forwarding to backend:', `${backendUrl}/auth/resend-otp`)
    
    const response = await fetch(`${backendUrl}/auth/resend-otp`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    })

    const data = await response.json()
    console.log('🔍 Resend OTP - Backend response:', response.status, data)

    if (response.ok) {
      console.log('✅ Resend OTP - Resend successful')
      return NextResponse.json(data)
    } else {
      console.log('❌ Resend OTP - Resend failed:', data)
      return NextResponse.json(
        { success: false, message: data.detail || 'Failed to resend OTP' },
        { status: response.status }
      )
    }
  } catch (error) {
    console.error('❌ Resend OTP - Error during resend:', error)
    return NextResponse.json(
      { success: false, message: 'Internal server error' },
      { status: 500 }
    )
  }
}
