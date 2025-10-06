import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    console.log('🔍 Logout - Starting logout process...')
    
    // Create response with cleared cookies immediately
    const nextResponse = NextResponse.json({ 
      success: true, 
      message: 'Logged out successfully' 
    })
    
    // Clear the session cookie with multiple approaches to ensure it's cleared
    console.log('🔍 Logout - Clearing session cookie...')
    nextResponse.cookies.set('session_token', '', {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 0, // Expire immediately
      path: '/', // Ensure it's cleared from all paths
    })
    
    // Also try to delete the cookie
    nextResponse.cookies.delete('session_token')
    
    console.log('✅ Logout - Cookie cleared successfully')
    
    // Try to notify backend about logout (but don't wait for it)
    try {
      const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
      fetch(`${backendUrl}/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      }).catch(error => {
        console.log('⚠️ Logout - Backend notification failed (non-critical):', error)
      })
    } catch (backendError) {
      console.log('⚠️ Logout - Backend notification failed (non-critical):', backendError)
    }
    
    return nextResponse
  } catch (error) {
    console.error('❌ Logout - Error during logout:', error)
    
    // Even if there's an error, clear the cookie
    const nextResponse = NextResponse.json(
      { success: true, message: 'Logged out successfully' },
      { status: 200 }
    )
    
    // Clear the session cookie
    console.log('🔍 Logout - Clearing session cookie (fallback)...')
    nextResponse.cookies.set('session_token', '', {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 0,
      path: '/',
    })
    
    nextResponse.cookies.delete('session_token')
    
    console.log('✅ Logout - Cookie cleared successfully (fallback)')
    
    return nextResponse
  }
}
