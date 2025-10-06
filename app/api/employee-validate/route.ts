import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const employeeData = body

    if (!employeeData || typeof employeeData !== 'object') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Employee data is required and must be a valid object',
          is_valid: false,
          errors: ['Invalid employee data format'],
          warnings: [],
          matched_employee: null
        },
        { status: 400 }
      )
    }

    // Validate required fields
    const requiredFields = ['employeeName', 'employeeId']
    const missingFields = requiredFields.filter(field => !employeeData[field] || employeeData[field].trim().length === 0)
    
    if (missingFields.length > 0) {
      return NextResponse.json(
        { 
          success: false,
          error: `Missing required fields: ${missingFields.join(', ')}`,
          is_valid: false,
          errors: [`Missing required fields: ${missingFields.join(', ')}`],
          warnings: [],
          matched_employee: null
        },
        { status: 400 }
      )
    }

    // Map frontend field names to backend expected names
    const mappedData = {
      full_name: employeeData.employeeName || employeeData.full_name,
      employee_code: employeeData.employeeId || employeeData.employee_code,
      designation: employeeData.designation || '',
      department: employeeData.department || '',
      joining_date: employeeData.joiningDate || employeeData.joining_date || ''
    }

    // Forward the request to the FastAPI backend
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    
    const response = await fetch(`${backendUrl}/certificates/validate-employee`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mappedData),
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Employee validation failed:', response.status, errorText)
      
      // Try to parse error as JSON for better error messages
      let errorMessage = 'Employee validation failed'
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
          is_valid: false,
          errors: [errorMessage],
          warnings: [],
          matched_employee: null
        },
        { status: response.status }
      )
    }

    const data = await response.json()
    
    // Validate backend response
    if (!data || typeof data !== 'object') {
      return NextResponse.json(
        { 
          success: false,
          error: 'Invalid response format from backend',
          is_valid: false,
          errors: ['Invalid backend response'],
          warnings: [],
          matched_employee: null
        },
        { status: 500 }
      )
    }
    
    return NextResponse.json({
      success: true,
      ...data
    })

  } catch (error) {
    console.error('Employee validation error:', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
    
    return NextResponse.json(
      { 
        success: false,
        error: `Failed to validate employee: ${errorMessage}`,
        is_valid: false,
        errors: [errorMessage],
        warnings: [],
        matched_employee: null
      },
      { status: 500 }
    )
  }
}
