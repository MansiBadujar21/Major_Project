import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { documentType, documentName, formData } = body

    if (!documentType || !documentName || !formData) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Missing required fields: documentType, documentName, and formData are required',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 400 }
      )
    }

    // Validate document type
    if (typeof documentType !== 'string' || documentType.trim().length === 0) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Document type must be a valid string',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 400 }
      )
    }

    // Validate document name
    if (typeof documentName !== 'string' || documentName.trim().length === 0) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Document name must be a valid string',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 400 }
      )
    }

    // Validate form data
    if (!formData || typeof formData !== 'object') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Form data must be a valid object',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 400 }
      )
    }

    // Map frontend field names to backend expected names
    const details = {
      // Employee fields (mapped to backend expected names)
      employeeName: formData.employeeName || '',
      employeeId: formData.employeeId || '',
      designation: formData.designation || '',
      department: formData.department || '',
      joiningDate: formData.joiningDate || '',
      // Document-specific fields
      relievingDate: formData.relievingDate || '',
      salaryAmount: formData.salaryAmount || '',
      appointmentDate: formData.appointmentDate || '',
      promotionDate: formData.promotionDate || '',
      newDesignation: formData.newDesignation || '',
      nocPurpose: formData.nocPurpose || '',
      effectiveDate: formData.effectiveDate || '',
      signingDate: formData.signingDate || '',
      reason: formData.reason || '',
      destination: formData.destination || '',
      purpose: formData.purpose || '',
      duration: formData.duration || '',
      travelDate: formData.travelDate || ''
    }

    console.log('Original formData:', formData)  // Debug log
    console.log('Mapped details:', details)  // Debug log

    // Submit document request to backend
    const requestBody = {
      document_type: documentType,
      document_name: documentName,
      user_id: 'anonymous',
      details: JSON.stringify(details)
    }
    
    console.log('Sending request to backend:', requestBody)  // Debug log
    console.log('Details JSON string:', JSON.stringify(details))  // Debug log
    
    let submitResponse: Response
    try {
      submitResponse = await fetch(`${process.env.BACKEND_URL || 'http://localhost:8000'}/document-requests/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      })

      if (!submitResponse.ok) {
        const errorData = await submitResponse.text()
        console.error('Backend submission error:', errorData)
        
        // Try to parse error as JSON for better error messages
        let errorMessage = `Failed to submit document request: ${submitResponse.status}`
        try {
          const errorJson = JSON.parse(errorData)
          errorMessage = errorJson.detail || errorJson.error || errorMessage
        } catch {
          errorMessage = `${errorMessage}: ${errorData}`
        }
        
        return NextResponse.json(
          { 
            success: false,
            error: errorMessage,
            downloadUrl: null,
            previewUrl: null,
            requestId: null
          },
          { status: submitResponse.status }
        )
      }
    } catch (fetchError) {
      console.error('Network error during document submission:', fetchError)
      return NextResponse.json(
        { 
          success: false,
          error: 'Network error: Unable to connect to document generation service',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 503 }
      )
    }

    const submitData = await submitResponse.json()
    console.log('Submit response:', submitData)  // Debug log
    
    // Validate submit response
    if (!submitData || typeof submitData !== 'object') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Invalid response format from backend',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 500 }
      )
    }
    
    const requestId = submitData.request_id  // Changed from submitData.id to submitData.request_id
    
    if (!requestId) {
      console.error('No request_id in response:', submitData)
      return NextResponse.json(
        { 
          success: false,
          error: 'Invalid response from backend - missing request ID',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 500 }
      )
    }

    // Check if the request was successful
    if (submitData.status === 'error') {
      return NextResponse.json(
        { 
          success: false,
          error: submitData.message || 'Document generation failed',
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: 500 }
      )
    }

    // Fetch the generated PDF
    const downloadResponse = await fetch(`${process.env.BACKEND_URL || 'http://localhost:8000'}/document-requests/download/${requestId}`)

    if (!downloadResponse.ok) {
      const errorText = await downloadResponse.text()
      console.error('Download response error:', downloadResponse.status, errorText)
      
      // Try to parse error as JSON for better error messages
      let errorMessage = `Failed to download generated document: ${downloadResponse.status}`
      try {
        const errorJson = JSON.parse(errorText)
        errorMessage = errorJson.detail || errorJson.error || errorMessage
      } catch {
        errorMessage = `${errorMessage}: ${errorText}`
      }
      
      return NextResponse.json(
        { 
          success: false,
          error: errorMessage,
          downloadUrl: null,
          previewUrl: null,
          requestId: null
        },
        { status: downloadResponse.status }
      )
    }

    console.log('Download response successful, status:', downloadResponse.status)
    console.log('Download response headers:', Object.fromEntries(downloadResponse.headers.entries()))

    // Return separate URLs for download and preview
    const downloadUrl = `${process.env.BACKEND_URL || 'http://localhost:8000'}/document-requests/download/${requestId}`
    const previewUrl = `${process.env.BACKEND_URL || 'http://localhost:8000'}/document-requests/preview/${requestId}`

    console.log('Generated download URL:', downloadUrl)
    console.log('Generated preview URL:', previewUrl)

    return NextResponse.json({
      success: true,
      downloadUrl,
      previewUrl,
      requestId
    })

  } catch (error) {
    console.error('Error generating document:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        success: false,
        error: `Internal server error: ${errorMessage}`,
        downloadUrl: null,
        previewUrl: null,
        requestId: null
      },
      { status: 500 }
    )
  }
}
