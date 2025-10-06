import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Get the pathname of the request
  const path = request.nextUrl.pathname

  // Define public paths that don't require authentication
  const publicPaths = ['/login']
  
  // Check if the current path is public
  const isPublicPath = publicPaths.some(publicPath => path === publicPath)
  
  // Allow specific API auth routes (but not /me which requires authentication)
  const isAuthApiPath = path.startsWith('/api/auth/') && !path.endsWith('/me')

  // Get the session token from cookies
  const sessionToken = request.cookies.get('session_token')

  console.log('🔍 Middleware - Path:', path, 'Session token:', sessionToken ? 'Found' : 'Not found')
  
  // If the path is public or auth API, allow access
  if (isPublicPath || isAuthApiPath) {
    console.log('✅ Middleware - Allowing access to public/auth path:', path)
    return NextResponse.next()
  }

  // If no session token and trying to access protected route, redirect to login
  if (!sessionToken) {
    console.log('❌ Middleware - No session token, redirecting to login')
    const loginUrl = new URL('/login', request.url)
    return NextResponse.redirect(loginUrl)
  }

  // If session token exists, allow access to protected routes
  console.log('✅ Middleware - Session token found, allowing access to:', path)
  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
