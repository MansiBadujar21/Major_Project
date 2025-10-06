'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  FileCheck, 
  Download, 
  Eye, 
  Loader2,
  CheckCircle,
  Building,
  Shield,
  QrCode,
  Sparkles,
  Calendar,
  User,
  Briefcase,
  MapPin,
  DollarSign,
  FileText,
  CreditCard,
  Plane,
  Globe,
  Search,
  UserCheck,
  AlertTriangle,
  RefreshCw
} from 'lucide-react'
import toast from 'react-hot-toast'
import LoadingSpinner, { DocumentLoadingSpinner, SuccessSpinner } from './LoadingSpinner'
import ValidationFeedback, { ErrorFeedback, SuccessFeedback } from './ValidationFeedback'

interface DocumentType {
  id: string
  name: string
  description: string
  icon: any
  fields: FormField[]
}

interface FormField {
  id: string
  label: string
  type: string
  placeholder?: string
  required: boolean
}

interface Employee {
  full_name: string
  employee_code: string
  designation: string
  department: string
  joining_date: string
}

const documentTypes: DocumentType[] = [
  {
    id: "1",
    name: "Bonafide / Employment Verification Letter",
    description: "Official employment verification for banks, embassies, etc.",
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
    description: "Detailed work experience and performance certificate",
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
    description: "Official job offer letter with terms and conditions",
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
    description: "Official appointment confirmation letter",
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
    description: "Official promotion notification with new designation",
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
    description: "Official relieving letter upon resignation",
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
    description: "Monthly salary slip with detailed breakdown",
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
    description: "Tax deduction certificate for income tax filing",
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
    description: "Salary certificate for loan applications",
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
    description: "Provident Fund statement and UAN details",
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
    description: "NOC for higher studies or new employment",
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
    description: "Copy of signed NDA for reference",
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
    description: "Request for ID card replacement",
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
    description: "Copy of medical insurance card",
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
    description: "Authorization letter for business travel",
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
    description: "Support letter for visa applications",
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

export default function DocumentForm() {
  const [selectedDocument, setSelectedDocument] = useState<DocumentType | null>(null)
  const [formData, setFormData] = useState<Record<string, string>>({})
  const [generatedDocument, setGeneratedDocument] = useState<{ downloadUrl: string; previewUrl: string } | null>(null)
  const [employeeSearchQuery, setEmployeeSearchQuery] = useState('')
  const [employeeSuggestions, setEmployeeSuggestions] = useState<Employee[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [validationResult, setValidationResult] = useState<{ isValid: boolean; errors: string[] } | null>(null)
  const [isValidating, setIsValidating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showError, setShowError] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)

  const handleDocumentSelect = (document: DocumentType) => {
    setSelectedDocument(document)
    setFormData({})
    setGeneratedDocument(null)
    setError(null)
    setShowError(false)
    setValidationResult(null)
  }

  const handleInputChange = (fieldId: string, value: string) => {
    setFormData(prev => ({ ...prev, [fieldId]: value }))
    setValidationResult(null) // Clear validation when user makes changes
  }

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
        body: JSON.stringify({ query }),
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

  // Manual search function (for button click)
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

  // Auto-fill form with employee data
  const fillFormWithEmployee = (employee: Employee) => {
    const newFormData = {
      employeeName: employee.full_name,
      employeeId: employee.employee_code,
      designation: employee.designation,
      department: employee.department,
      joiningDate: convertDateFormat(employee.joining_date),
      issueDate: new Date().toISOString().split('T')[0], // Today's date
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

    // Validate required fields
    const missingFields = selectedDocument.fields
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
          documentType: selectedDocument.id,
          documentName: selectedDocument.name,
          formData: formData
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        const errorMessage = data.error || 'Failed to generate document'
        setError(errorMessage)
        setShowError(true)
        throw new Error(errorMessage)
      }

      // Validate response
      if (!data.success) {
        const errorMessage = data.error || 'Document generation failed'
        setError(errorMessage)
        setShowError(true)
        throw new Error(errorMessage)
      }

      setGeneratedDocument({
        downloadUrl: data.downloadUrl,
        previewUrl: data.previewUrl
      })

      toast.success(`${selectedDocument.name} generated successfully!`)
    } catch (error) {
      console.error('Error generating document:', error)
      const errorMessage = error instanceof Error ? error.message : 'Failed to generate document. Please try again.'
      setError(errorMessage)
      setShowError(true)
      toast.error(errorMessage)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleDownload = async () => {
    if (!generatedDocument) return

    try {
      console.log('Attempting to download from URL:', generatedDocument.downloadUrl)
      
      const response = await fetch(generatedDocument.downloadUrl)
      console.log('Download response status:', response.status)
      console.log('Download response headers:', Object.fromEntries(response.headers.entries()))
      
      if (!response.ok) {
        const errorText = await response.text()
        console.error('Download failed:', response.status, errorText)
        throw new Error(`Download failed: ${response.status} - ${errorText}`)
      }
      
      const blob = await response.blob()
      console.log('Download blob size:', blob.size)
      
      if (blob.size === 0) {
        throw new Error('Downloaded file is empty')
      }
      
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${selectedDocument?.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`
      a.style.display = 'none'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      toast.success('Document downloaded successfully!')
    } catch (error) {
      console.error('Error downloading document:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
      toast.error(`Failed to download document: ${errorMessage}`)
      
      // Fallback: try to open in new tab
      try {
        window.open(generatedDocument.downloadUrl, '_blank')
        toast.success('Opened document in new tab as fallback')
      } catch (fallbackError) {
        console.error('Fallback also failed:', fallbackError)
      }
    }
  }

  const handlePreview = () => {
    if (!generatedDocument) return
    
    console.log('Attempting to preview URL:', generatedDocument.previewUrl)
    try {
      // Open in new tab without download behavior
      const newWindow = window.open(generatedDocument.previewUrl, '_blank')
      if (!newWindow) {
        toast.error('Popup blocked. Please allow popups for this site.')
      }
    } catch (error) {
      console.error('Error opening preview:', error)
      toast.error('Failed to open preview')
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <FileCheck className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-semibold">Document Requests</h2>
              <p className="text-green-100 text-sm">Generate official HR documents with enhanced security features</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
          {/* Document Type Selection */}
          <div className="lg:col-span-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Document Type</h3>
            <div className="space-y-2 max-h-96 overflow-y-auto" data-scrollable="true">
              {documentTypes.map((doc) => {
                const Icon = doc.icon
                const isSelected = selectedDocument?.id === doc.id
                
                return (
                  <motion.button
                    key={doc.id}
                    onClick={() => handleDocumentSelect(doc)}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`
                      w-full p-4 rounded-lg border-2 transition-all duration-300 text-left
                      ${isSelected 
                        ? 'border-green-500 bg-green-50' 
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                      }
                    `}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`
                        p-2 rounded-lg
                        ${isSelected ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}
                      `}>
                        <Icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className={`font-medium ${isSelected ? 'text-green-900' : 'text-gray-900'}`}>
                          {doc.name}
                        </h4>
                        <p className={`text-sm ${isSelected ? 'text-green-700' : 'text-gray-600'}`}>
                          {doc.description}
                        </p>
                      </div>
                    </div>
                  </motion.button>
                )
              })}
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-2">
            {selectedDocument ? (
              <div>
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-3 bg-green-100 rounded-lg">
                    <selectedDocument.icon className="w-6 h-6 text-green-600" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">{selectedDocument.name}</h3>
                    <p className="text-gray-600">{selectedDocument.description}</p>
                  </div>
                </div>

                {/* Employee Search Section */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <Search className="w-5 h-5 text-blue-600" />
                    Quick Employee Search & Auto-fill
                  </h4>
                  <div className="flex gap-3">
                    <div className="flex-1">
                      <input
                        type="text"
                        value={employeeSearchQuery}
                        onChange={(e) => {
                          setEmployeeSearchQuery(e.target.value)
                          searchEmployees(e.target.value)
                        }}
                        placeholder="Search employee by name or ID..."
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <button
                      onClick={handleManualSearch}
                      disabled={isSearching}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors duration-200 flex items-center gap-2"
                    >
                      {isSearching ? (
                        <RefreshCw className="w-4 h-4 animate-spin" />
                      ) : (
                        <Search className="w-4 h-4" />
                      )}
                      Search
                    </button>
                  </div>
                  
                  {/* Employee Suggestions */}
                  {employeeSuggestions.length > 0 && (
                    <div className="mt-3 space-y-2">
                      <p className="text-sm text-gray-600">Found employees:</p>
                      {employeeSuggestions.map((emp, index) => (
                        <div
                          key={index}
                          className="p-3 bg-white border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
                          onClick={() => fillFormWithEmployee(emp)}
                        >
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="font-medium text-gray-900">{emp.full_name}</p>
                              <p className="text-sm text-gray-600">ID: {emp.employee_code} | {emp.designation}</p>
                            </div>
                            <UserCheck className="w-4 h-4 text-green-600" />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Validation Result */}
                {validationResult && (
                  <div className={`p-4 rounded-lg mb-6 ${
                    validationResult.isValid 
                      ? 'bg-green-50 border border-green-200' 
                      : 'bg-red-50 border border-red-200'
                  }`}>
                    <div className="flex items-center gap-2 mb-2">
                      {validationResult.isValid ? (
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      ) : (
                        <UserCheck className="w-5 h-5 text-red-600" />
                      )}
                      <span className={`font-medium ${
                        validationResult.isValid ? 'text-green-900' : 'text-red-900'
                      }`}>
                        Employee Validation {validationResult.isValid ? 'Passed' : 'Failed'}
                      </span>
                    </div>
                    {validationResult.errors.length > 0 && (
                      <ul className="text-sm text-red-700 space-y-1">
                        {validationResult.errors.map((error, index) => (
                          <li key={index}>• {error}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}

                {/* Error Display */}
                {showError && error && (
                  <ValidationFeedback 
                    type="error"
                    message="Document generation failed" 
                    details={[error]}
                    onClose={() => setShowError(false)}
                  />
                )}

                {/* Loading State */}
                {isGenerating && (
                  <div className="mb-6">
                    <DocumentLoadingSpinner message="Generating your document..." />
                  </div>
                )}

                {/* Premium Features */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4 mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-blue-600" />
                    Premium Certificate Features
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div className="flex items-center gap-2">
                      <Building className="w-4 h-4 text-blue-600" />
                      <span>Professional company logo and branding</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-green-600" />
                      <span>Digital signatures with security indicators</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <QrCode className="w-4 h-4 text-purple-600" />
                      <span>QR code for instant verification</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                      <span>Digital signatures and verification</span>
                    </div>
                  </div>
                </div>

                {/* Form Fields */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  {selectedDocument.fields.map((field) => (
                    <div key={field.id}>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        {field.label}
                      </label>
                      <input
                        type={field.type}
                        value={formData[field.id] || ''}
                        onChange={(e) => handleInputChange(field.id, e.target.value)}
                        placeholder={field.placeholder}
                        required={field.required}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                      />
                    </div>
                  ))}
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3">
                  <button
                    onClick={async () => {
                      if (formData.employeeId && formData.employeeName) {
                        const validation = await validateEmployeeData()
                        setValidationResult(validation)
                        
                        if (validation.isValid) {
                          toast.success('Employee validation passed!')
                        } else {
                          toast.error(`Validation failed: ${validation.errors.join(', ')}`)
                        }
                      } else {
                        toast.error('Please fill in Employee ID and Name first')
                      }
                    }}
                    disabled={isValidating || !formData.employeeId || !formData.employeeName}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
                  >
                    {isValidating ? (
                      <>
                        <RefreshCw className="w-5 h-5 animate-spin" />
                        Validating...
                      </>
                    ) : (
                      <>
                        <UserCheck className="w-5 h-5" />
                        Validate Employee
                      </>
                    )}
                  </button>
                  
                  <button
                    onClick={handleGenerateDocument}
                    disabled={!selectedDocument || !formData.employeeId || !formData.employeeName || isGenerating}
                    className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
                  >
                    {isGenerating ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <FileCheck className="w-5 h-5" />
                        Generate Document
                      </>
                    )}
                  </button>
                </div>

                {/* Generated Document Actions */}
                {generatedDocument && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg"
                  >
                    <div className="flex items-center gap-2 mb-3">
                      <CheckCircle className="w-5 h-5 text-green-600" />
                      <span className="font-semibold text-green-900">Document Generated Successfully!</span>
                    </div>
                    <div className="flex gap-3">
                      <button
                        onClick={handlePreview}
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                      >
                        <Eye className="w-4 h-4" />
                        Preview
                      </button>
                      <button
                        onClick={handleDownload}
                        className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                      >
                        <Download className="w-4 h-4" />
                        Download
                      </button>
                    </div>
                  </motion.div>
                )}
              </div>
            ) : (
              <div className="text-center py-12">
                <FileCheck className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Select a Document Type</h3>
                <p className="text-gray-600">Choose from 16 official document types to get started</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
