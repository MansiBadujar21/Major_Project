import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { summary_data, original_filename } = body

    if (!summary_data || typeof summary_data !== 'object') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Summary data is required and must be a valid object'
        },
        { status: 400 }
      )
    }

    // Validate original filename
    const filename = original_filename || 'document.pdf'
    if (typeof filename !== 'string' || filename.trim().length === 0) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Original filename must be a valid string'
        },
        { status: 400 }
      )
    }

    // Forward the request to the FastAPI backend
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    
    const response = await fetch(`${backendUrl}/gemini/download-summary-pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        summary_data,
        original_filename: filename.trim()
      }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('PDF generation failed:', response.status, errorText)
      
      // Try to parse error as JSON for better error messages
      let errorMessage = 'PDF generation failed'
      try {
        const errorJson = JSON.parse(errorText)
        errorMessage = errorJson.detail || errorJson.error || errorMessage
      } catch {
        errorMessage = `${errorMessage}: ${errorText}`
      }
      
      return NextResponse.json(
        { 
          success: false,
          error: errorMessage
        },
        { status: response.status }
      )
    }

    // Return the PDF blob
    const pdfBlob = await response.blob()
    
    // Validate PDF blob
    if (!pdfBlob || pdfBlob.size === 0) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Generated PDF is empty or invalid'
        },
        { status: 500 }
      )
    }
    
    return new NextResponse(pdfBlob, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${filename.replace('.pdf', '') || 'document'}_summary.pdf"`,
      },
    })

  } catch (error) {
    console.error('PDF download error:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        success: false,
        error: `Failed to generate PDF summary: ${errorMessage}`
      },
      { status: 500 }
    )
  }
}
