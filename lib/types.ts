// Chat and Message Types
export interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  edited?: boolean
  editedAt?: Date
}

export interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
  isActive?: boolean
}

// Employee Types
export interface Employee {
  full_name: string
  employee_code: string
  designation: string
  department: string
  joining_date: string
  email?: string
  emp_id?: number
}

// API Response Types
export interface BaseAPIResponse {
  success: boolean
  error?: string
}

export interface ChatAPIResponse extends BaseAPIResponse {
  response?: string
  message?: string
}

export interface EmployeeSearchResponse extends BaseAPIResponse {
  suggestions?: Employee[]
  count?: number
}

export interface EmployeeByIdResponse extends BaseAPIResponse {
  employee?: Employee | null
}

export interface ValidationResult {
  is_valid: boolean
  employee_found: boolean
  matched_employee?: Employee | null
  errors: string[]
  warnings: string[]
}

export interface EmployeeValidationResponse extends BaseAPIResponse {
  validation_result?: ValidationResult
  is_valid?: boolean
  errors?: string[]
  warnings?: string[]
  matched_employee?: Employee | null
}

// Document Request Types
export interface DocumentRequest {
  doc_type: string
  doc_name: string
  employee_data?: Employee
}

// QA Engine Types
export interface QASuggestion {
  question: string
  answer: string
  similarity: number
  source: string
}

export interface QAStatistics {
  total_qa_pairs: number
  generated_qa_pairs: number
  manual_qa_pairs: number
  sources: Record<string, number>
  last_updated: string
}

// Form Data Types
export interface DocumentFormData {
  employeeName: string
  employeeId: string
  designation: string
  department: string
  joiningDate: string
  issueDate: string
  documentType: string
  relievingDate?: string
  purpose?: string
  salaryAmount?: string
  newDesignation?: string
  promotionDate?: string
}

// Error Types
export interface APIError {
  message: string
  status: number
  details?: string
}

// Loading States
export interface LoadingState {
  isLoading: boolean
  error?: string | null
  progress?: number
}

// Chat Commands
export type ChatCommand = 
  | 'search_employee'
  | 'fill_form'
  | 'document_request'
  | 'help'
  | 'status'
  | 'none'

export interface ChatCommandResult {
  command: ChatCommand
  response: string
  data?: any
}

// Health Check Types
export interface HealthStatus {
  status: 'ok' | 'error' | 'degraded'
  timestamp: string
  services: {
    frontend: {
      status: 'healthy' | 'unhealthy' | 'error'
      version?: string
    }
    backend: {
      status: 'healthy' | 'unhealthy' | 'unreachable' | 'error' | 'unknown'
      url?: string
      error?: string
    }
  }
  environment?: {
    node_env?: string
    backend_url?: string
  }
  error?: string
}

// Document Generation Types
export interface DocumentGenerationRequest {
  document_type: string
  document_name: string
  details: string
  user_id: string
}

export interface DocumentGenerationResponse {
  status: 'completed' | 'pending' | 'failed'
  request_id: string
  submitted_at: string
  error?: string
}

// PDF Processing Types
export interface PDFProcessingStatus {
  status: 'processing' | 'completed' | 'failed'
  progress: number
  message: string
  result?: any
  error?: string
}

// System Configuration Types
export interface SystemConfig {
  max_file_size: number
  supported_formats: string[]
  timeout_seconds: number
  retry_attempts: number
}

// Team Member Types
export interface TeamMember {
  name: string
  role: string
  department: string
  skills: string[]
}
