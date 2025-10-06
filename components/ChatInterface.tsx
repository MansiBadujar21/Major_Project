'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, FileCheck, Upload, X, Building, Briefcase, FileText, CheckCircle, Sparkles, Calendar, User, DollarSign, CreditCard, Plane, Globe, Shield, Search, UserCheck, Loader2, Download, Eye, RefreshCw, QrCode, Plus, Edit, Trash2, History, Trash } from 'lucide-react'
import { Message, ChatSession } from '@/lib/types'
import toast from 'react-hot-toast'

// Compact Document Form Component for Chat
function ChatDocumentForm() {
  const [selectedDocument, setSelectedDocument] = useState<string>('')
  const [formData, setFormData] = useState<Record<string, string>>({})
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedDocument, setGeneratedDocument] = useState<{ downloadUrl: string; previewUrl: string } | null>(null)
  const [employeeSearchQuery, setEmployeeSearchQuery] = useState('')
  const [employeeSuggestions, setEmployeeSuggestions] = useState<any[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [validationResult, setValidationResult] = useState<{ isValid: boolean; errors: string[] } | null>(null)
  const [isValidating, setIsValidating] = useState(false)

  const documentTypes = [
    {
      id: "1",
      name: "Bonafide / Employment Verification Letter",
      icon: Building,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true }
      ]
    },
    {
      id: "2",
      name: "Experience Certificate",
      icon: Briefcase,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "relievingDate", label: "Relieving Date *", type: "date", required: true }
      ]
    },
    {
      id: "3",
      name: "Offer Letter Copy",
      icon: FileText,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "salaryAmount", label: "Salary Amount *", type: "text", placeholder: "e.g., 75,000 per month", required: true }
      ]
    },
    {
      id: "4",
      name: "Appointment Letter Copy",
      icon: CheckCircle,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "appointmentDate", label: "Appointment Date *", type: "date", required: true }
      ]
    },
    {
      id: "5",
      name: "Promotion Letter",
      icon: Sparkles,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "promotionDate", label: "Promotion Date *", type: "date", required: true },
        { id: "newDesignation", label: "New Designation *", type: "text", placeholder: "e.g., Senior Software Engineer", required: true }
      ]
    },
    {
      id: "6",
      name: "Relieving Letter",
      icon: Calendar,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "relievingDate", label: "Relieving Date *", type: "date", required: true }
      ]
    },
    {
      id: "7",
      name: "Salary Slips",
      icon: DollarSign,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "salaryAmount", label: "Salary Amount *", type: "text", placeholder: "e.g., 75,000 per month", required: true }
      ]
    },
    {
      id: "8",
      name: "Form 16 / Tax Documents",
      icon: FileText,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "salaryAmount", label: "Salary Amount *", type: "text", placeholder: "e.g., 75,000 per month", required: true }
      ]
    },
    {
      id: "9",
      name: "Salary Certificate",
      icon: DollarSign,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "salaryAmount", label: "Salary Amount *", type: "text", placeholder: "e.g., 75,000 per month", required: true },
        { id: "purpose", label: "Purpose *", type: "text", placeholder: "e.g., Loan application, visa", required: true }
      ]
    },
    {
      id: "10",
      name: "PF Statement / UAN details",
      icon: CreditCard,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true }
      ]
    },
    {
      id: "11",
      name: "No Objection Certificate (NOC)",
      icon: CheckCircle,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "relievingDate", label: "Relieving Date *", type: "date", required: true },
        { id: "nocPurpose", label: "NOC Purpose *", type: "text", placeholder: "e.g., Higher studies, new job", required: true },
        { id: "effectiveDate", label: "Effective Date *", type: "date", required: true }
      ]
    },
    {
      id: "12",
      name: "Non-Disclosure Agreement Copy",
      icon: Shield,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "signingDate", label: "Signing Date *", type: "date", required: true }
      ]
    },
    {
      id: "13",
      name: "ID Card Replacement",
      icon: User,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "reason", label: "Reason for Replacement *", type: "text", placeholder: "e.g., Lost, damaged, expired", required: true }
      ]
    },
    {
      id: "14",
      name: "Medical Insurance Card Copy",
      icon: CreditCard,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true }
      ]
    },
    {
      id: "15",
      name: "Business Travel Authorization Letter",
      icon: Plane,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "destination", label: "Destination *", type: "text", placeholder: "e.g., New York, USA", required: true },
        { id: "purpose", label: "Purpose *", type: "text", placeholder: "e.g., Client meeting, conference", required: true },
        { id: "duration", label: "Duration *", type: "text", placeholder: "e.g., 5 days", required: true },
        { id: "travelDate", label: "Travel Date *", type: "date", required: true }
      ]
    },
    {
      id: "16",
      name: "Visa Support Letter",
      icon: Globe,
      fields: [
        { id: "employeeName", label: "Employee Name *", type: "text", placeholder: "Enter full name as per records", required: true },
        { id: "employeeId", label: "Employee ID *", type: "text", placeholder: "Enter Employee ID", required: true },
        { id: "designation", label: "Designation *", type: "text", placeholder: "e.g., Software Engineer", required: true },
        { id: "department", label: "Department *", type: "text", placeholder: "e.g., Engineering", required: true },
        { id: "joiningDate", label: "Joining Date *", type: "date", required: true },
        { id: "destination", label: "Destination Country *", type: "text", placeholder: "e.g., USA, UK, Canada", required: true },
        { id: "purpose", label: "Purpose *", type: "text", placeholder: "e.g., Business trip, conference", required: true },
        { id: "duration", label: "Duration *", type: "text", placeholder: "e.g., 2 weeks, 1 month", required: true }
      ]
    }
  ]

  // Employee search functionality
  const searchEmployees = async (query: string) => {
    if (!query.trim()) {
      setEmployeeSuggestions([])
      return
    }

    if (query.length < 2) {
      setEmployeeSuggestions([])
      return
    }

    setIsSearching(true)
    try {
      const response = await fetch('/api/employee-search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query.trim() }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        console.error('Employee search failed:', errorData)
        
        const errorMessage = errorData.error || `Employee search failed: ${response.status}`
        throw new Error(errorMessage)
      }

      const data = await response.json()
      
      // Validate response
      if (!data.success) {
        throw new Error(data.error || 'Employee search failed')
      }
      
      if (data.suggestions && data.suggestions.length > 0) {
        setEmployeeSuggestions(data.suggestions)
      } else {
        setEmployeeSuggestions([])
        if (query.length >= 3) {
          toast('No employees found matching your search')
        }
      }
    } catch (error) {
      console.error('Employee search error:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
      toast.error(`Failed to search employees: ${errorMessage}`)
      setEmployeeSuggestions([])
    } finally {
      setIsSearching(false)
    }
  }

  const handleManualSearch = async () => {
    if (!employeeSearchQuery.trim()) {
      toast.error('Please enter a search query')
      return
    }

    if (employeeSearchQuery.length < 2) {
      toast.error('Please enter at least 2 characters to search')
      return
    }

    await searchEmployees(employeeSearchQuery)
  }

  // Convert date from DD-MM-YYYY to YYYY-MM-DD format for HTML date input
  const convertDateFormat = (dateString: string): string => {
    if (!dateString) return ''
    
    // Check if date is already in YYYY-MM-DD format
    if (/^\d{4}-\d{2}-\d{2}$/.test(dateString)) {
      return dateString
    }
    
    // Convert from DD-MM-YYYY to YYYY-MM-DD
    if (/^\d{2}-\d{2}-\d{4}$/.test(dateString)) {
      const [day, month, year] = dateString.split('-')
      return `${year}-${month}-${day}`
    }
    
    // If format is unknown, return as is
    return dateString
  }

  const fillFormWithEmployee = (employee: any) => {
    const newFormData = {
      employeeName: employee.full_name || '',
      employeeId: employee.employee_code || '',
      designation: employee.designation || '',
      department: employee.department || '',
      joiningDate: convertDateFormat(employee.joining_date || ''),
    }

    setFormData(newFormData)
    setEmployeeSuggestions([])
    setEmployeeSearchQuery('')
    setValidationResult(null)
    
    toast.success(`Form filled with details for ${employee.full_name}`)
  }

  // Validate employee data
  const validateEmployeeData = async () => {
    if (!formData.employeeId || !formData.employeeName) {
      return { isValid: false, errors: ['Employee ID and Name are required for validation'] }
    }

    setIsValidating(true)
    try {
      const response = await fetch('/api/employee-validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          employeeName: formData.employeeName,
          employeeId: formData.employeeId,
          designation: formData.designation,
          department: formData.department,
          joiningDate: formData.joiningDate,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        console.error('Validation failed:', errorData)
        
        const errorMessage = errorData.error || `Validation failed: ${response.status}`
        throw new Error(errorMessage)
      }

      const data = await response.json()
      
      // Validate response
      if (!data.success) {
        throw new Error(data.error || 'Validation failed')
      }
      
      return { isValid: data.is_valid, errors: data.errors || [] }
    } catch (error) {
      console.error('Validation error:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
      return { isValid: false, errors: [`Validation service unavailable: ${errorMessage}`] }
    } finally {
      setIsValidating(false)
    }
  }

  const handleGenerateDocument = async () => {
    if (!selectedDocument) {
      toast.error('Please select a document type first')
      return
    }

    const selectedDoc = documentTypes.find(d => d.id === selectedDocument)
    if (!selectedDoc) {
      toast.error('Invalid document type selected')
      return
    }

    // Validate required fields
    const missingFields = selectedDoc.fields
      .filter(field => field.required && !formData[field.id])
      .map(field => field.label)

    if (missingFields.length > 0) {
      toast.error(`Please fill in: ${missingFields.join(', ')}`)
      return
    }

    // Additional validation for specific fields
    if (formData.employeeId && formData.employeeId.length < 3) {
      toast.error('Employee ID must be at least 3 characters long')
      return
    }

    if (formData.employeeName && formData.employeeName.length < 2) {
      toast.error('Employee name must be at least 2 characters long')
      return
    }

    // Validate employee data if employee fields are present
    if (formData.employeeId && formData.employeeName) {
      const validation = await validateEmployeeData()
      setValidationResult(validation)
      
      if (!validation.isValid) {
        toast.error(`Employee validation failed: ${validation.errors.join(', ')}`)
        return
      }
    }

    setIsGenerating(true)
    try {
      const response = await fetch('/api/generate-document', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          documentType: selectedDocument,
          documentName: selectedDoc.name,
          formData: formData
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate document')
      }

      setGeneratedDocument({
        downloadUrl: data.downloadUrl,
        previewUrl: data.previewUrl
      })

      toast.success('Document generated successfully!')
    } catch (error) {
      console.error('Error generating document:', error)
      toast.error('Failed to generate document. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const selectedDoc = documentTypes.find(d => d.id === selectedDocument)

  return (
    <div className="space-y-4">
      {/* Document Type Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Select Document Type</label>
        <select
          value={selectedDocument}
          onChange={(e) => setSelectedDocument(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 focus:outline-none"
        >
          <option value="">Choose a document type...</option>
          {documentTypes.map((doc) => (
            <option key={doc.id} value={doc.id}>{doc.name}</option>
          ))}
        </select>
      </div>

      {/* Employee Search Section */}
      {selectedDocument && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2 text-sm">
            <Search className="w-4 h-4 text-blue-600" />
            Quick Employee Search & Auto-fill
          </h4>
          <div className="flex gap-2">
            <div className="flex-1">
              <input
                type="text"
                value={employeeSearchQuery}
                onChange={(e) => {
                  setEmployeeSearchQuery(e.target.value)
                  searchEmployees(e.target.value)
                }}
                placeholder="Search employee by name or ID..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none text-sm"
              />
            </div>
            <button
              onClick={handleManualSearch}
              disabled={isSearching}
              className="px-3 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors duration-200 flex items-center gap-1 text-sm"
            >
              {isSearching ? (
                <RefreshCw className="w-3 h-3 animate-spin" />
              ) : (
                <Search className="w-3 h-3" />
              )}
              Search
            </button>
          </div>
          
          {/* Employee Suggestions */}
          {employeeSuggestions.length > 0 && (
            <div className="mt-2 space-y-1">
              <p className="text-xs text-gray-600">Found employees:</p>
              {employeeSuggestions.map((emp, index) => (
                <div
                  key={index}
                  className="p-2 bg-white border border-gray-200 rounded cursor-pointer hover:bg-gray-50 transition-colors text-xs"
                  onClick={() => fillFormWithEmployee(emp)}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{emp.full_name}</p>
                      <p className="text-gray-600">ID: {emp.employee_code} | {emp.designation}</p>
                    </div>
                    <UserCheck className="w-3 h-3 text-green-600" />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Validation Result */}
      {validationResult && (
        <div className={`p-3 rounded-lg ${
          validationResult.isValid 
            ? 'bg-green-50 border border-green-200' 
            : 'bg-red-50 border border-red-200'
        }`}>
          <div className="flex items-center gap-2 mb-1">
            {validationResult.isValid ? (
              <CheckCircle className="w-4 h-4 text-green-600" />
            ) : (
              <UserCheck className="w-4 h-4 text-red-600" />
            )}
            <span className={`font-medium text-sm ${
              validationResult.isValid ? 'text-green-900' : 'text-red-900'
            }`}>
              Employee Validation {validationResult.isValid ? 'Passed' : 'Failed'}
            </span>
          </div>
          {validationResult.errors.length > 0 && (
            <ul className="text-xs text-red-700 space-y-1">
              {validationResult.errors.map((error, index) => (
                <li key={index}>• {error}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Dynamic Form Fields */}
      {selectedDoc && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {selectedDoc.fields.map((field) => (
            <div key={field.id}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
              <input
                type={field.type}
                value={formData[field.id] || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, [field.id]: e.target.value }))}
                placeholder={field.placeholder}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 focus:outline-none"
              />
            </div>
          ))}
        </div>
      )}

      {/* Premium Features */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-3">
        <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2 text-sm">
          <Sparkles className="w-4 h-4 text-blue-600" />
          Premium Certificate Features
        </h4>
        <div className="grid grid-cols-1 gap-2 text-xs">
          <div className="flex items-center gap-2">
            <Building className="w-3 h-3 text-blue-600" />
            <span>Professional company logo and branding</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="w-3 h-3 text-green-600" />
            <span>Digital signatures with security indicators</span>
          </div>
          <div className="flex items-center gap-2">
            <QrCode className="w-3 h-3 text-purple-600" />
            <span>QR code for instant verification</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle className="w-3 h-3 text-emerald-600" />
            <span>Digital signatures and verification</span>
          </div>
        </div>
      </div>

      {/* Generate Button */}
      <button
        onClick={handleGenerateDocument}
        disabled={!selectedDocument || isGenerating || isValidating}
        className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
      >
        {isGenerating ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Generating...
          </>
        ) : isValidating ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Validating...
          </>
        ) : (
          <>
            <FileCheck className="w-4 h-4" />
            Generate Document
          </>
        )}
      </button>

      {/* Generated Document Actions */}
      {generatedDocument && (
        <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <span className="font-medium text-green-900">Document Generated!</span>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => window.open(generatedDocument.previewUrl, '_blank')}
              className="flex items-center gap-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
            >
              <Eye className="w-3 h-3" />
              Preview
            </button>
            <button
              onClick={() => window.open(generatedDocument.downloadUrl, '_blank')}
              className="flex items-center gap-1 bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm"
            >
              <Download className="w-3 h-3" />
              Download
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

// Compact PDF Uploader Component for Chat
function ChatPDFUploader() {
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [summary, setSummary] = useState<any>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const pollingTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  // Cleanup effect to clear timeouts when component unmounts
  useEffect(() => {
    return () => {
      if (pollingTimeoutRef.current) {
        clearTimeout(pollingTimeoutRef.current)
        pollingTimeoutRef.current = null
      }
    }
  }, [])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile)
      setSummary(null)
      // Reset processing states when new file is selected
      setIsUploading(false)
      setIsGenerating(false)
      // Clear any pending polling
      if (pollingTimeoutRef.current) {
        clearTimeout(pollingTimeoutRef.current)
        pollingTimeoutRef.current = null
      }
    } else {
      toast.error('Please select a valid PDF file')
    }
  }

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a PDF file first')
      return
    }

    setIsUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to upload PDF')
      }

      const data = await response.json()
      
             if (data.success) {
         toast.success('PDF uploaded successfully! Generating summary...')
        // Don't await here to prevent state conflicts
        generateSummary(data.jobId)
       } else {
        throw new Error(data.error || 'Upload failed')
      }
    } catch (error) {
      console.error('Upload error:', error)
      toast.error('Failed to upload PDF. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

          const generateSummary = async (jobId: string) => {
    // Prevent multiple simultaneous calls
    if (isGenerating) return
    
    setIsGenerating(true)
    
    const pollSummary = async (): Promise<void> => {
    try {
       const response = await fetch('/api/process-pdf', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({ jobId }),
       })

       if (!response.ok) {
         throw new Error('Failed to generate summary')
       }

       const data = await response.json()
       
       if (data.success && data.status === 'completed' && data.result) {
         // Set the full summary result
         setSummary(data.result)
         toast.success('Summary generated successfully!')
          setIsGenerating(false)
          // Clear any pending timeout
          if (pollingTimeoutRef.current) {
            clearTimeout(pollingTimeoutRef.current)
            pollingTimeoutRef.current = null
          }
       } else if (data.status === 'processing') {
          // Job is still processing, poll again after delay
          pollingTimeoutRef.current = setTimeout(pollSummary, 2000)
       } else {
         throw new Error(data.error || 'Summary generation failed')
       }
     } catch (error) {
       console.error('Summary error:', error)
       toast.error('Failed to generate summary. Please try again.')
       setIsGenerating(false)
        // Clear any pending timeout
        if (pollingTimeoutRef.current) {
          clearTimeout(pollingTimeoutRef.current)
          pollingTimeoutRef.current = null
        }
     }
    }

    // Start polling
    pollSummary()
   }

   const downloadSummaryPDF = async (summaryData: any) => {
     try {
       // Call backend to generate PDF summary
       const response = await fetch('/api/download-summary-pdf', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({
           summary_data: summaryData,
           original_filename: file?.name || 'document'
         }),
       })

       if (!response.ok) {
         throw new Error('Failed to generate PDF summary')
       }

       // Download the PDF
       const blob = await response.blob()
       const url = URL.createObjectURL(blob)
       const a = document.createElement('a')
       a.href = url
       a.download = `${file?.name?.replace('.pdf', '') || 'document'}_summary.pdf`
       document.body.appendChild(a)
       a.click()
       window.URL.revokeObjectURL(url)
       document.body.removeChild(a)
       
       toast.success('Summary PDF downloaded successfully!')
     } catch (error) {
       console.error('Error downloading summary:', error)
       toast.error('Failed to download summary PDF')
     }
   }

  return (
    <div className="space-y-4">
      {/* File Upload */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Upload PDF Document</label>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 focus:outline-none"
        />
      </div>

      {file && (
        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-600" />
            <span className="text-sm text-blue-900">{file.name}</span>
          </div>
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={!file || isUploading || isGenerating}
        className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
      >
        {isUploading || isGenerating ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            {isUploading ? 'Uploading...' : 'Processing PDF...'}
          </>
        ) : (
          <>
            <Upload className="w-4 h-4" />
            Upload & Summarize
          </>
        )}
      </button>

             {/* Summary Display */}
       {summary && (
         <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
           <h4 className="font-medium text-purple-900 mb-3">AI Summary</h4>
           
           {/* Executive Summary */}
           {summary.executive_summary && (
             <div className="mb-4">
               <h5 className="font-medium text-purple-800 mb-2 text-sm">Executive Summary</h5>
               <p className="text-purple-700 text-sm leading-relaxed">
                 {summary.executive_summary}
               </p>
             </div>
           )}

           {/* Key Points */}
           {summary.key_points && summary.key_points.length > 0 && (
             <div className="mb-4">
               <h5 className="font-medium text-purple-800 mb-2 text-sm">Key Points</h5>
               <ul className="list-disc list-inside space-y-1 text-purple-700 text-sm">
                 {summary.key_points.map((point: string, index: number) => (
                   <li key={index}>{point}</li>
                 ))}
               </ul>
             </div>
           )}

           {/* Keywords */}
           {summary.keywords && summary.keywords.length > 0 && (
             <div className="mb-4">
               <h5 className="font-medium text-purple-800 mb-2 text-sm">Key Topics</h5>
               <div className="flex flex-wrap gap-2">
                 {summary.keywords.slice(0, 8).map((keyword: string, index: number) => (
                   <span
                     key={index}
                     className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full"
                   >
                     {keyword}
                   </span>
                 ))}
               </div>
             </div>
           )}

           {/* Tables */}
           {summary.tables && summary.tables.length > 0 && (
             <div className="mb-4">
               <h5 className="font-medium text-purple-800 mb-2 text-sm">Tables Found ({summary.tables.length})</h5>
               {summary.tables.slice(0, 2).map((table: any, index: number) => (
                 <div key={index} className="mb-3 p-3 bg-purple-100 rounded-lg">
                   <h6 className="font-medium text-purple-700 mb-1 text-sm">
                     Table {table.id}: {table.title}
                   </h6>
                   <p className="text-xs text-purple-600 mb-2">{table.dimensions}</p>
                   <div className="overflow-x-auto">
                     <div 
                       className="text-xs"
                       dangerouslySetInnerHTML={{ __html: table.markdown.replace(/\n/g, '<br/>') }}
                     />
                   </div>
                 </div>
               ))}
               {summary.tables.length > 2 && (
                 <p className="text-xs text-purple-600 italic">
                   ... and {summary.tables.length - 2} more tables
                 </p>
               )}
             </div>
           )}

           {/* Download Button */}
           <div className="flex gap-2 mt-4">
             <button
               onClick={() => downloadSummaryPDF(summary)}
               className="flex items-center gap-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
             >
               <Download className="w-3 h-3" />
               Download Summary PDF
             </button>
           </div>
         </div>
       )}
    </div>
  )
}

interface ChatInterfaceProps {
  messages: Message[]
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
  chatSessions: ChatSession[]
  setChatSessions: React.Dispatch<React.SetStateAction<ChatSession[]>>
  currentSessionId: string
  setCurrentSessionId: (sessionId: string) => void
}

export default function ChatInterface({ 
  messages, 
  setMessages, 
  chatSessions, 
  setChatSessions, 
  currentSessionId, 
  setCurrentSessionId 
}: ChatInterfaceProps) {
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isClient, setIsClient] = useState(false)
  const [showDocumentForm, setShowDocumentForm] = useState(false)
  const [showPDFUploader, setShowPDFUploader] = useState(false)
  const [editingMessageId, setEditingMessageId] = useState<string | null>(null)
  const [editingContent, setEditingContent] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [isRegenerating, setIsRegenerating] = useState(false)
  const [showChatHistory, setShowChatHistory] = useState(false)
  const messagesContainerRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Load chat sessions from localStorage on mount
  useEffect(() => {
    const savedSessions = localStorage.getItem('chatSessions')
    if (savedSessions && chatSessions.length === 0) {
      try {
        const sessions = JSON.parse(savedSessions).map((session: any) => ({
          ...session,
          createdAt: new Date(session.createdAt),
          updatedAt: new Date(session.updatedAt),
          messages: session.messages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp),
            editedAt: msg.editedAt ? new Date(msg.editedAt) : undefined
          }))
        }))
        setChatSessions(sessions)
      } catch (error) {
        console.error('Error loading chat sessions:', error)
      }
    }
  }, [chatSessions.length, setChatSessions])

  // Handle hydration
  useEffect(() => {
    setIsClient(true)
    // Initialize messages only on client side and if no messages exist
    if (messages.length === 0) {
      const initialMessage: Message = {
        id: '1',
        type: 'assistant',
        content: 'I\'m ready to help you with HR questions! 💬\n\n• Ask about company policies, benefits, and procedures\n• Get information about leave policies, attendance, and more\n• Request official documents (use "Documents" button or type "I need a document")\n• Upload PDFs for summarization (use "Summarize PDF" button or type "summarize PDF")\n• Powered by semantic search and AI assistance\n• Quick and accurate responses to your queries\n\n💡 **Quick Access:** Use the buttons below or type your commands!\n\nJust type your question and I\'ll help you find the information you need!',
        timestamp: new Date()
      }
      setMessages([initialMessage])
      
      // Create initial session
      const sessionId = Date.now().toString()
      const newSession: ChatSession = {
        id: sessionId,
        title: 'New Chat',
        messages: [initialMessage],
        createdAt: new Date(),
        updatedAt: new Date(),
        isActive: true
      }
      setCurrentSessionId(sessionId)
      setChatSessions([newSession])
    }
  }, [messages.length, setMessages, setCurrentSessionId, setChatSessions])

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    if (messagesContainerRef.current) {
      const scrollToBottom = () => {
        const container = messagesContainerRef.current
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      }
      
      // Use requestAnimationFrame to ensure DOM is updated
      requestAnimationFrame(() => {
        scrollToBottom()
      })
    }
  }, [messages, isLoading, showDocumentForm, showPDFUploader])

  // Focus input after message is sent
  useEffect(() => {
    if (!isLoading && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isLoading])

  // Debug form state changes
  useEffect(() => {
    console.log('Form state changed - showDocumentForm:', showDocumentForm, 'showPDFUploader:', showPDFUploader)
  }, [showDocumentForm, showPDFUploader])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && showChatHistory) {
        setShowChatHistory(false)
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [showChatHistory])

  // Check for document or PDF requests - Enhanced for various English proficiency levels
  const checkForFormTriggers = (message: string) => {
    const lowerMessage = message.toLowerCase().trim()
    
    // Document request triggers - comprehensive coverage for various English levels
    const documentTriggers = [
      // Basic needs
      'i need', 'i want', 'i require', 'i looking for', 'i searching for',
      'need', 'want', 'require', 'looking for', 'searching for', 'asking for',
      
      // Document variations
      'document', 'documents', 'doc', 'docs', 'paper', 'papers',
      'certificate', 'certificates', 'cert', 'certs', 'letter', 'letters',
      'form', 'forms', 'slip', 'slips', 'statement', 'statements',
      
      // Common misspellings and variations
      'documant', 'documnt', 'certificat', 'certifcat', 'letr', 'ltr',
      'dokument', 'dokumnt', 'sertifikat', 'sertifcat',
      
      // Action words
      'get', 'give', 'make', 'create', 'generate', 'produce', 'issue',
      'provide', 'send', 'download', 'print', 'copy', 'duplicate',
      
      // Specific document types (various spellings)
      'experience', 'experiance', 'employment', 'employmnt', 'salary', 'salry',
      'bonafide', 'bonafid', 'bonafied', 'noc', 'relieving', 'relieving',
      'offer', 'offr', 'appointment', 'appointmnt', 'promotion', 'promotn',
      'verification', 'verificatn', 'medical', 'medicl', 'insurance', 'insuranc',
      'travel', 'travl', 'visa', 'visa', 'business', 'busines', 'id card', 'idcard',
      'pf', 'pf statement', 'uan', 'tax', 'form 16', 'form16',
      
      // Common phrases in different English levels
      'help me get', 'can you give', 'please provide', 'i would like',
      'i need help', 'can you help', 'please help', 'help me',
      'show me', 'tell me', 'give me', 'send me', 'make for me',
      
      // Informal/casual language
      'gimme', 'wanna', 'gonna', 'lemme', 'pls', 'plz', 'thx', 'thanks',
      
      // Question formats
      'how to get', 'where to get', 'when can i get', 'what do i need',
      'can i have', 'may i have', 'is it possible to get',
      
      // Regional variations
      'kindly', 'please arrange', 'please issue', 'please make',
      'need urgently', 'want immediately', 'require asap', 'need fast'
    ]
    
    // PDF summarization triggers - various ways to express
    const pdfTriggers = [
      // Basic PDF actions
      'pdf', 'pdfs', 'file', 'files',
      
      // Summarization actions
      'summarize', 'summarise', 'summary', 'summaries', 'summarization', 'summarisation',
      'summariz', 'summaris', 'summry', 'summri', 'brief', 'briefing',
      
      // Upload/process actions
      'upload', 'uplod', 'process', 'proces', 'analyze', 'analyse', 'analyz',
      'read', 'reed', 'extract', 'extract', 'convert', 'convrt',
      
      // Common phrases
      'upload pdf', 'process pdf', 'analyze pdf', 'read pdf', 'extract from pdf',
      'summarize pdf', 'pdf summary', 'pdf analysis', 'pdf processing',
      
      // Informal variations
      'upload my pdf', 'process my pdf', 'read my file',
      'can you read', 'help me understand', 'what is in this',
      
      // Question formats
      'how to upload', 'where to upload', 'can i upload', 'is it possible to upload',
      'what does this say', 'what is this about', 'tell me about this', 'summarize this'
    ]
    
    // Check for PDF triggers first (more specific for PDF operations)
    const pdfSpecificKeywords = ['summarize', 'summarise', 'upload', 'process', 'analyze', 'analyse', 'read', 'extract']
    const hasPDFSpecificKeywords = pdfSpecificKeywords.some(keyword => lowerMessage.includes(keyword))
    
    if (hasPDFSpecificKeywords && pdfTriggers.some(trigger => lowerMessage.includes(trigger))) {
      console.log('PDF trigger detected:', lowerMessage)
      return 'pdf'
    }
    
    // Check for document triggers
    if (documentTriggers.some(trigger => lowerMessage.includes(trigger))) {
      console.log('Document trigger detected:', lowerMessage)
      return 'document'
    }
    
    // Additional fuzzy matching for common patterns
    const hasDocumentKeywords = ['certificate', 'letter', 'form', 'slip', 'statement', 'bonafide', 'noc', 'relieving', 'offer', 'appointment', 'promotion'].some(keyword => 
      lowerMessage.includes(keyword)
    )
    
    const hasPDFKeywords = ['pdf', 'summarize', 'summarise', 'upload', 'process', 'analyze', 'analyse'].some(keyword => 
      lowerMessage.includes(keyword)
    )
    
    if (hasPDFKeywords) {
      console.log('Fuzzy PDF trigger detected:', lowerMessage)
      return 'pdf'
    }
    
    if (hasDocumentKeywords) {
      console.log('Fuzzy document trigger detected:', lowerMessage)
      return 'document'
    }
    
    console.log('No trigger detected for:', lowerMessage)
    return null
  }

  // Simple message sending - exactly like HTML version's handleQAMessage
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    }

    setMessages((prev: Message[]) => {
      const newMessages = [...prev, userMessage]
      
      // Update current session
      if (currentSessionId) {
        updateCurrentSession(newMessages)
      }
      
      return newMessages
    })
    setInputMessage('')
    setIsLoading(true)

    // Check for form triggers
    const formType = checkForFormTriggers(inputMessage.trim())
    console.log('Form type detected:', formType, 'for message:', inputMessage.trim())
    
    if (formType === 'document') {
      console.log('Setting document form to true')
      setShowDocumentForm(true)
      setShowPDFUploader(false)
      addMessage('assistant', '📝 I\'ll help you request a document! Please fill out the form below to generate your document.')
      setIsLoading(false)
      return
    }
    
    if (formType === 'pdf') {
      console.log('Setting PDF uploader to true')
      setShowPDFUploader(true)
      setShowDocumentForm(false)
      addMessage('assistant', '📄 I\'ll help you summarize your PDF! Please upload your document below.')
      setIsLoading(false)
      return
    }
    
    // Fallback: Check for any document-related keywords that might have been missed
    const fallbackDocumentKeywords = ['document', 'certificate', 'letter', 'form', 'slip', 'statement']
    const hasDocumentKeywords = fallbackDocumentKeywords.some(keyword => 
      inputMessage.toLowerCase().includes(keyword)
    )
    
    if (hasDocumentKeywords && !formType) {
      console.log('Fallback document trigger detected')
      setShowDocumentForm(true)
      setShowPDFUploader(false)
      addMessage('assistant', '📝 I\'ll help you request a document! Please fill out the form below to generate your document.')
      setIsLoading(false)
      return
    }

    try {
      // Simple fetch to /chat API - exactly like HTML version
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputMessage.trim() })
      })

      if (!response.ok) {
        throw new Error(`QA API error: ${response.statusText}`)
      }

      const data = await response.json()

      if (data.response) {
        // Check if response is a special form trigger - same as HTML version
        if (data.response.startsWith('SHOW_FORM:')) {
          const parts = data.response.split(':')
          if (parts.length === 3) {
            const docType = parts[1]
            const docName = parts[2]
            const formMessage = `📝 Please fill in the details below to generate your ${docName}.`
            addMessage('assistant', formMessage)
          } else {
            addMessage('assistant', data.response)
          }
        } else {
          addMessage('assistant', data.response)
        }
      } else {
        addMessage('assistant', '❌ Sorry, I couldn\'t process your question. Please try again.')
      }

    } catch (error) {
      console.error('QA Error:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      addMessage('assistant', `❌ Sorry, I encountered an error processing your question: ${errorMessage}\n\nPlease try again or contact support if the issue persists.`)
    } finally {
      setIsLoading(false)
    }
  }

  // Simple message adding - same as HTML version
  const addMessage = (type: 'user' | 'assistant', content: string) => {
    const message: Message = {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date()
    }
    setMessages((prev: Message[]) => {
      const newMessages = [...prev, message]
      
      // Update current session
      if (currentSessionId) {
        updateCurrentSession(newMessages)
      }
      
      return newMessages
    })
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const closeForms = () => {
    setShowDocumentForm(false)
    setShowPDFUploader(false)
  }

  // Save chat sessions to localStorage
  const saveChatSessions = (sessions: ChatSession[]) => {
    try {
      localStorage.setItem('chatSessions', JSON.stringify(sessions))
    } catch (error) {
      console.error('Error saving chat sessions:', error)
    }
  }

  // Update current session
  const updateCurrentSession = (newMessages: Message[]) => {
          setChatSessions((prev: ChatSession[]) => {
        const updated = prev.map((session: ChatSession) => 
          session.id === currentSessionId 
            ? { 
                ...session, 
                messages: newMessages, 
                updatedAt: new Date(),
                title: generateSessionTitle(newMessages)
              }
            : { ...session, isActive: false }
        )
        saveChatSessions(updated)
        return updated
      })
  }

  // Generate session title from first user message
  const generateSessionTitle = (messages: Message[]): string => {
    const firstUserMessage = messages.find(msg => msg.type === 'user')
    if (firstUserMessage) {
      const content = firstUserMessage.content
      return content.length > 30 ? content.substring(0, 30) + '...' : content
    }
    return 'New Chat'
  }

  // New Chat functionality
  const handleNewChat = () => {
    // Save current session before creating new one
    if (currentSessionId && messages.length > 1) {
      updateCurrentSession(messages)
    }

    const initialMessage: Message = {
      id: Date.now().toString(),
      type: 'assistant',
      content: 'I\'m ready to help you with HR questions! 💬\n\n• Ask about company policies, benefits, and procedures\n• Get information about leave policies, attendance, and more\n• Request official documents (use "Documents" button or type "I need a document")\n• Upload PDFs for summarization (use "Summarize PDF" button or type "summarize PDF")\n• Powered by semantic search and AI assistance\n• Quick and accurate responses to your queries\n\n💡 **Quick Access:** Use the buttons below or type your commands!\n\nJust type your question and I\'ll help you find the information you need!',
      timestamp: new Date()
    }

    const sessionId = Date.now().toString()
    const newSession: ChatSession = {
      id: sessionId,
      title: 'New Chat',
      messages: [initialMessage],
      createdAt: new Date(),
      updatedAt: new Date(),
      isActive: true
    }

    setMessages([initialMessage])
    setCurrentSessionId(sessionId)
    setChatSessions((prev: ChatSession[]) => {
      const updated = [...prev.map((s: ChatSession) => ({ ...s, isActive: false })), newSession]
      saveChatSessions(updated)
      return updated
    })
    
    setInputMessage('')
    setShowDocumentForm(false)
    setShowPDFUploader(false)
    setEditingMessageId(null)
    setEditingContent('')
    setIsEditing(false)
    setIsDeleting(false)
    setShowChatHistory(false)
    
    // Focus on input
    if (inputRef.current) {
      inputRef.current.focus()
    }
    
    toast.success('New chat started!')
  }

  // Load chat session
  const loadChatSession = (sessionId: string) => {
    const session = chatSessions.find(s => s.id === sessionId)
    if (session) {
      setMessages(session.messages)
      setCurrentSessionId(sessionId)
      setChatSessions((prev: ChatSession[]) => prev.map((s: ChatSession) => ({ ...s, isActive: s.id === sessionId })))
      setShowChatHistory(false)
      
      // Focus on input
      if (inputRef.current) {
        inputRef.current.focus()
      }
    }
  }

  // Delete chat session
  const deleteChatSession = (sessionId: string) => {
    if (!confirm('Are you sure you want to delete this chat?')) return
    
    setChatSessions((prev: ChatSession[]) => {
      const updated = prev.filter((s: ChatSession) => s.id !== sessionId)
      saveChatSessions(updated)
      return updated
    })

    // If deleting current session, create new one
    if (sessionId === currentSessionId) {
      handleNewChat()
    }
    
    toast.success('Chat deleted successfully!')
  }

  // Clear all chat history
  const clearAllChatHistory = () => {
    const sessionCount = chatSessions.length
    const messageCount = chatSessions.reduce((total, session) => total + session.messages.length, 0)
    
    const confirmMessage = `Are you sure you want to clear all chat history?\n\nThis will delete:\n• ${sessionCount} chat session${sessionCount !== 1 ? 's' : ''}\n• ${messageCount} total message${messageCount !== 1 ? 's' : ''}\n\nThis action cannot be undone.`
    
    if (!confirm(confirmMessage)) return
    
    setChatSessions([])
    saveChatSessions([])
    
    // Create a new chat session
    handleNewChat()
    
    toast.success(`Cleared ${sessionCount} chat session${sessionCount !== 1 ? 's' : ''} and ${messageCount} message${messageCount !== 1 ? 's' : ''}!`)
  }

  // Edit message functionality
  const handleEditMessage = (message: Message) => {
    if (message.type !== 'user') return
    
    setEditingMessageId(message.id)
    setEditingContent(message.content)
    setIsEditing(true)
    
    // Focus on input for editing
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }

  const handleSaveEdit = async () => {
    if (!editingMessageId || !editingContent.trim()) return
    
    setIsEditing(true)
    
    try {
      // Find the edited message and its position
      const editedMessageIndex = messages.findIndex(msg => msg.id === editingMessageId)
      if (editedMessageIndex === -1) {
        throw new Error('Message not found')
      }

      // Update message in frontend
      setMessages((prev: Message[]) => {
        const updatedMessages = prev.map((msg: Message) => 
          msg.id === editingMessageId 
            ? { ...msg, content: editingContent.trim(), edited: true, editedAt: new Date() }
            : msg
        )
        
        // Update current session
        if (currentSessionId) {
          updateCurrentSession(updatedMessages)
        }
        
        return updatedMessages
      })
      
      // Call backend to update message
      const response = await fetch('/api/chat/edit-message', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messageId: editingMessageId,
          newContent: editingContent.trim()
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to update message')
      }

      // Remove the old response and get a new one
      await regenerateResponseForEditedMessage(editingMessageId, editingContent.trim())

      toast.success('Message updated and response regenerated!')
    } catch (error) {
      console.error('Error updating message:', error)
      toast.error('Failed to update message. Please try again.')
    } finally {
      setEditingMessageId(null)
      setEditingContent('')
      setIsEditing(false)
    }
  }

  // Regenerate response for edited message
  const regenerateResponseForEditedMessage = async (messageId: string, newContent: string) => {
    try {
      // Find the edited message and remove the response that follows it
      setMessages((prev: Message[]) => {
        const editedMessageIndex = prev.findIndex((msg: Message) => msg.id === messageId)
        if (editedMessageIndex === -1) return prev

        // Remove the response that follows the edited message
        const messagesWithoutResponse = prev.slice(0, editedMessageIndex + 1)
        
        // Update current session
        if (currentSessionId) {
          updateCurrentSession(messagesWithoutResponse)
        }
        
        return messagesWithoutResponse
      })

      // Get new response for the edited message
      setIsRegenerating(true)
      
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: newContent })
      })

      if (!response.ok) {
        throw new Error(`QA API error: ${response.statusText}`)
      }

      const data = await response.json()

      if (data.response) {
        // Check if response is a special form trigger
        if (data.response.startsWith('SHOW_FORM:')) {
          const parts = data.response.split(':')
          if (parts.length === 3) {
            const docType = parts[1]
            const docName = parts[2]
            const formMessage = `📝 Please fill in the details below to generate your ${docName}.`
            addMessage('assistant', formMessage)
          } else {
            addMessage('assistant', data.response)
          }
        } else {
          addMessage('assistant', data.response)
        }
      } else {
        addMessage('assistant', '❌ Sorry, I couldn\'t process your question. Please try again.')
      }

    } catch (error) {
      console.error('Error regenerating response:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      addMessage('assistant', `❌ Sorry, I encountered an error processing your question: ${errorMessage}\n\nPlease try again or contact support if the issue persists.`)
    } finally {
      setIsRegenerating(false)
    }
  }

  const handleCancelEdit = () => {
    setEditingMessageId(null)
    setEditingContent('')
    setIsEditing(false)
  }

  // Delete message functionality
  const handleDeleteMessage = async (messageId: string) => {
    if (!confirm('Are you sure you want to delete this message?')) return
    
    setIsDeleting(true)
    
    try {
      // Find the message and its position
      const messageIndex = messages.findIndex(msg => msg.id === messageId)
      if (messageIndex === -1) {
        throw new Error('Message not found')
      }

      const messageToDelete = messages[messageIndex]
      
      // Remove message and its corresponding response from frontend
      setMessages((prev: Message[]) => {
        let updatedMessages = [...prev]
        
        if (messageToDelete.type === 'user') {
          // For user messages, also remove the assistant response that follows
          const nextMessage = prev[messageIndex + 1]
          if (nextMessage && nextMessage.type === 'assistant') {
            // Remove both the user message and the assistant response
            updatedMessages = prev.filter((_: Message, index: number) => index !== messageIndex && index !== messageIndex + 1)
          } else {
            // Remove only the user message
            updatedMessages = prev.filter((_: Message, index: number) => index !== messageIndex)
          }
        } else {
          // For assistant messages, just remove the message
          updatedMessages = prev.filter((_: Message, index: number) => index !== messageIndex)
        }
        
        // Update current session
        if (currentSessionId) {
          updateCurrentSession(updatedMessages)
        }
        
        return updatedMessages
      })
      
      // Call backend to delete message
      const response = await fetch('/api/chat/delete-message', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messageId }),
      })

      if (!response.ok) {
        throw new Error('Failed to delete message')
      }

      const deletedCount = messageToDelete.type === 'user' && messages[messageIndex + 1]?.type === 'assistant' ? 2 : 1
      toast.success(`Message${deletedCount > 1 ? 's' : ''} deleted successfully!`)
    } catch (error) {
      console.error('Error deleting message:', error)
      toast.error('Failed to delete message. Please try again.')
    } finally {
      setIsDeleting(false)
    }
  }

  // Don't render until client-side hydration is complete
  if (!isClient) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Initializing chat...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Chat History Sidebar */}
      {showChatHistory && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40" onClick={() => setShowChatHistory(false)}>
          {/* Click outside indicator */}
          <div className="absolute top-4 left-4 text-white/80 text-sm bg-black/20 backdrop-blur-sm px-3 py-2 rounded-lg">
            Click outside or press ESC to close
          </div>
          <div className="fixed right-0 top-0 h-full w-96 bg-white/95 backdrop-blur-md shadow-2xl z-50 overflow-hidden border-l border-gray-200" onClick={(e) => e.stopPropagation()}>
            {/* Header */}
            <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 text-white p-6 relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent"></div>
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
                    <History className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">Chat History</h3>
                    <p className="text-blue-100 text-sm">
                      {chatSessions.length > 0 
                        ? `${chatSessions.length} conversation${chatSessions.length !== 1 ? 's' : ''}`
                        : 'Your conversation archive'
                      }
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {chatSessions.length > 0 && (
                    <button
                      onClick={clearAllChatHistory}
                      className="p-2 hover:bg-red-500/20 rounded-xl transition-all duration-200 hover:scale-105 group"
                      title="Clear all chat history"
                    >
                      <Trash className="w-5 h-5 text-red-200 group-hover:text-red-100" />
                    </button>
                  )}
                  <button
                    onClick={() => setShowChatHistory(false)}
                    className="p-3 hover:bg-white/20 rounded-xl transition-all duration-200 hover:scale-105 group"
                    title="Close chat history"
                  >
                    <X className="w-6 h-6 group-hover:rotate-90 transition-transform duration-200" />
                  </button>
                </div>
              </div>
            </div>

            {/* Additional Close Button - Top Right Corner */}
            <button
              onClick={() => setShowChatHistory(false)}
              className="absolute top-4 right-4 z-10 p-2 bg-white/20 backdrop-blur-sm hover:bg-white/30 rounded-full transition-all duration-200 hover:scale-110 group"
              title="Close"
            >
              <X className="w-4 h-4 text-white group-hover:rotate-90 transition-transform duration-200" />
            </button>

            {/* Content */}
            <div className="h-full overflow-y-auto bg-gradient-to-b from-gray-50 to-white relative">
              {/* Bottom Buttons */}
              <div className="sticky bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-white via-white/95 to-transparent space-y-3">
                {chatSessions.length > 0 && (
                  <button
                    onClick={clearAllChatHistory}
                    className="w-full py-3 px-4 bg-gradient-to-r from-red-100 to-red-200 hover:from-red-200 hover:to-red-300 text-red-700 rounded-xl transition-all duration-200 hover:shadow-md font-medium flex items-center justify-center gap-2 border border-red-200"
                  >
                    <Trash className="w-4 h-4" />
                    <span>Clear All Chat History</span>
                  </button>
                )}
                <button
                  onClick={() => setShowChatHistory(false)}
                  className="w-full py-3 px-4 bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 text-gray-700 rounded-xl transition-all duration-200 hover:shadow-md font-medium flex items-center justify-center gap-2"
                >
                  <X className="w-4 h-4" />
                  <span>Close Chat History</span>
                </button>
              </div>
              {chatSessions.length === 0 ? (
                <div className="p-8 text-center">
                  <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl flex items-center justify-center">
                    <History className="w-10 h-10 text-gray-400" />
                  </div>
                  <h4 className="text-lg font-semibold text-gray-700 mb-2">No conversations yet</h4>
                  <p className="text-gray-500 text-sm mb-6">Start chatting to see your history here</p>
                  <div className="w-32 h-1 bg-gradient-to-r from-blue-200 to-purple-200 rounded-full mx-auto"></div>
                </div>
              ) : (
                <div className="p-4 space-y-3">
                  {chatSessions.map((session) => (
                    <div
                      key={session.id}
                      className={`group relative p-4 rounded-2xl cursor-pointer transition-all duration-300 transform hover:scale-[1.02] ${
                        session.isActive
                          ? 'bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 shadow-lg'
                          : 'bg-white border border-gray-100 hover:border-gray-200 hover:shadow-lg'
                      }`}
                      onClick={() => loadChatSession(session.id)}
                    >
                      {/* Active indicator */}
                      {session.isActive && (
                        <div className="absolute top-3 right-3 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                      )}
                      
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-2">
                            <h4 className="font-semibold text-gray-900 truncate">
                              {session.title}
                            </h4>
                            {session.isActive && (
                              <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full font-medium">
                                Active
                              </span>
                            )}
                          </div>
                          
                          <div className="flex items-center gap-4 text-xs text-gray-500 mb-2">
                            <div className="flex items-center gap-1">
                              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                              <span>{session.messages.length} messages</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                              <span>{new Date(session.updatedAt).toLocaleDateString()}</span>
                            </div>
                          </div>
                          
                          <p className="text-xs text-gray-400">
                            Last updated: {new Date(session.updatedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        </div>
                        
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deleteChatSession(session.id)
                          }}
                          className="opacity-0 group-hover:opacity-100 p-2 hover:bg-red-50 rounded-xl transition-all duration-200 hover:scale-110 ml-3"
                          title="Delete chat"
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
          <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6" aria-hidden="true" />
            </div>
            <div>
              <h2 className="text-xl font-semibold">HR Q&A Chat</h2>
                <p className="text-blue-100 text-sm">
                  {chatSessions.find(s => s.isActive)?.title || 'Ask questions about policies, benefits, and procedures'}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowChatHistory(!showChatHistory)}
                className="flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-colors duration-200"
              >
                <History className="w-4 h-4" />
                <span className="text-sm font-medium">Chat History</span>
              </button>
              <button
                onClick={handleNewChat}
                className="flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-colors duration-200"
              >
                <Plus className="w-4 h-4" />
                <span className="text-sm font-medium">New Chat</span>
              </button>
            </div>
          </div>
        </div>

        {/* Messages Container - Fixed height with proper scrolling */}
        <div 
          ref={messagesContainerRef}
          className="h-[400px] md:h-[500px] overflow-y-auto overflow-x-hidden p-4 space-y-4 scroll-smooth"
          data-scrollable="true"
        >

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className="relative group">
              <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg rounded-2xl p-4 shadow-sm transition-all duration-300 hover:shadow-md ${
                  message.type === 'user'
                      ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white border border-blue-500/20'
                      : 'bg-gradient-to-br from-gray-50 to-white text-gray-800 border border-gray-200/50'
                  }`}
                >
                  <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
                  {message.edited && (
                    <div className={`text-xs mt-2 flex items-center gap-1 ${
                      message.type === 'user' ? 'text-blue-200' : 'text-gray-500'
                    }`}>
                      <div className="w-1 h-1 rounded-full bg-current"></div>
                      <span>edited</span>
                    </div>
                  )}
                </div>
                
                {/* Edit and Delete buttons for user messages */}
                {message.type === 'user' && (
                  <div className="absolute -bottom-3 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-all duration-300 scale-95 group-hover:scale-100">
                    <div className="flex items-center gap-1 bg-white/95 backdrop-blur-md border border-gray-200/50 rounded-2xl shadow-2xl px-3 py-2">
                      <div className="absolute inset-0 bg-gradient-to-r from-blue-50/50 to-purple-50/50 rounded-2xl"></div>
                      <div className="relative flex items-center gap-1">
                        <button
                          onClick={() => handleEditMessage(message)}
                          disabled={isEditing || isDeleting || isLoading || isRegenerating}
                          className="p-2 hover:bg-blue-100 rounded-xl transition-all duration-200 hover:scale-110 disabled:opacity-50 disabled:hover:scale-100 group/edit"
                          title="Edit message"
                        >
                          {isEditing || isLoading || isRegenerating ? (
                            <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                          ) : (
                            <div className="relative">
                              <Edit className="w-4 h-4 text-blue-600" />
                              <div className="absolute inset-0 bg-blue-600/20 rounded-full scale-0 group-hover/edit:scale-100 transition-transform duration-200"></div>
                            </div>
                          )}
                        </button>
                        <div className="w-px h-4 bg-gray-300/50"></div>
                        <button
                          onClick={() => handleDeleteMessage(message.id)}
                          disabled={isEditing || isDeleting || isLoading || isRegenerating}
                          className="p-2 hover:bg-red-100 rounded-xl transition-all duration-200 hover:scale-110 disabled:opacity-50 disabled:hover:scale-100 group/delete"
                          title="Delete message"
                        >
                          {isDeleting ? (
                            <Loader2 className="w-4 h-4 text-red-600 animate-spin" />
                          ) : (
                            <div className="relative">
                              <Trash2 className="w-4 h-4 text-red-600" />
                              <div className="absolute inset-0 bg-red-600/20 rounded-full scale-0 group-hover/delete:scale-100 transition-transform duration-200"></div>
                            </div>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {/* Inline Document Form */}
          {showDocumentForm && (
            <div className="flex justify-start">
              <div className="max-w-4xl w-full bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <FileCheck className="w-5 h-5 text-green-600" />
                    <span className="font-semibold text-gray-900">Document Request Form</span>
                  </div>
                  <button
                    onClick={closeForms}
                    className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  <ChatDocumentForm />
                </div>
              </div>
            </div>
          )}
          


          {/* Inline PDF Uploader */}
          {showPDFUploader && (
            <div className="flex justify-start">
              <div className="max-w-4xl w-full bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Upload className="w-5 h-5 text-purple-600" />
                    <span className="font-semibold text-gray-900">PDF Summarization</span>
                  </div>
                  <button
                    onClick={closeForms}
                    className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
                                 <div className="max-h-96 overflow-y-auto">
                  <ChatPDFUploader />
                 </div>
              </div>
            </div>
          )}
          
          {/* Typing indicator - same as HTML version */}
          {(isLoading || isRegenerating) && (
            <div className="flex justify-start">
              <div className="bg-gradient-to-br from-gray-50 to-white text-gray-800 rounded-2xl p-4 shadow-sm border border-gray-200/50">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center animate-pulse">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="flex items-center space-x-3">
                  <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    {isRegenerating && (
                      <span className="text-sm text-gray-600 font-medium">Regenerating response...</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200/50 p-6 bg-gradient-to-r from-gray-50/50 to-white">
          {isEditing ? (
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-sm text-gray-600 bg-blue-50/50 px-4 py-2 rounded-xl border border-blue-200/50">
                  <Edit className="w-4 h-4 text-blue-600" />
                  <span className="font-medium">Editing message...</span>
                </div>
                <div className="flex space-x-3">
                  <input
                    ref={inputRef}
                    type="text"
                    value={editingContent}
                    onChange={(e) => setEditingContent(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault()
                        handleSaveEdit()
                      }
                      if (e.key === 'Escape') {
                        handleCancelEdit()
                      }
                    }}
                    placeholder="Edit your message..."
                    className="flex-1 px-4 py-3 border border-gray-300/50 rounded-2xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white/80 backdrop-blur-sm shadow-sm transition-all duration-200 hover:shadow-md focus:shadow-lg"
                    disabled={isLoading}
                  />
                  <button
                    onClick={handleSaveEdit}
                    disabled={!editingContent.trim() || isLoading}
                    className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-2xl hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 disabled:hover:scale-100"
                  >
                    <CheckCircle className="w-4 h-4" />
                    <span className="font-medium">Save</span>
                  </button>
                  <button
                    onClick={handleCancelEdit}
                    disabled={isLoading}
                    className="px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-2xl hover:from-gray-600 hover:to-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 disabled:hover:scale-100"
                  >
                    <X className="w-4 h-4" />
                    <span className="font-medium">Cancel</span>
                  </button>
                </div>
              </div>
                      ) : (
              <div className="flex space-x-3">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your question here... (try 'I need a document' or 'summarize PDF')"
                  className="flex-1 px-4 py-3 border border-gray-300/50 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/80 backdrop-blur-sm shadow-sm transition-all duration-200 hover:shadow-md focus:shadow-lg"
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
                  className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 disabled:hover:scale-100"
            >
              <Send className="w-4 h-4" />
                  <span className="font-medium">Send</span>
            </button>
          </div>
            )}
        </div>
      </div>
    </div>
  )
}

