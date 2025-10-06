/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost'],
  },
  async rewrites() {
    return [
      {
        source: '/api/chat/:path*',
        destination: 'http://localhost:8000/chat/:path*',
      },
      {
        source: '/api/documents/:path*',
        destination: 'http://localhost:8000/documents/:path*',
      },
      {
        source: '/api/certificates/:path*',
        destination: 'http://localhost:8000/certificates/:path*',
      },
      {
        source: '/api/gemini/:path*',
        destination: 'http://localhost:8000/gemini/:path*',
      },
      {
        source: '/api/advanced-qa/:path*',
        destination: 'http://localhost:8000/advanced-qa/:path*',
      },
    ];
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
