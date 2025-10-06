from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field, validator
import re
import logging
from datetime import datetime

from ..services.bad_language_filter import BadLanguageFilter
from ..services.qa_engine import HybridQAEngine
from ..config import auth_disabled

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services with better error handling
bad_filter = None
qa_engine = None

def initialize_services():
    """Initialize chat services with enhanced error handling"""
    global bad_filter, qa_engine
    
    try:
        # Initialize bad language filter
        try:
            bad_filter = BadLanguageFilter()
            logger.info("✅ Bad language filter initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize bad language filter: {str(e)}")
            bad_filter = None
        
        # Initialize QA engine
        try:
            qa_engine = HybridQAEngine()
            logger.info("✅ QA engine initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize QA engine: {str(e)}")
            qa_engine = None
        
        if bad_filter and qa_engine:
            logger.info("✅ Chat services initialized successfully")
        else:
            logger.warning("⚠️ Some chat services failed to initialize")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize chat services: {str(e)}")
        bad_filter = None
        qa_engine = None

# Initialize services on module load
initialize_services()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000, description="Chat message")
    
    @validator('message')
    def validate_message(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Message must be a non-empty string')
            
        if not v.strip():
            raise ValueError('Message cannot be empty or contain only whitespace')
        
        # Check for excessive whitespace
        if len(v.strip()) < 1:
            raise ValueError('Message must contain non-whitespace characters')
        
        # Check for potentially harmful patterns
        harmful_patterns = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript protocol
            r'data:text/html',  # Data URLs
            r'vbscript:',  # VBScript protocol
            r'<iframe[^>]*>',  # Iframe tags
            r'on\w+\s*=',  # Event handlers
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Message contains potentially harmful content')
        
        return v.strip()


class ChatResponse(BaseModel):
    response: str
    success: bool = True
    error: Optional[str] = None
    timestamp: Optional[str] = None


def get_simple_response(message: str) -> str:
    """Get simple hardcoded responses - Enhanced for various English proficiency levels"""
    lower_message = message.lower().strip()
    
    # Enhanced greeting detection - various ways to say hello
    greeting_words = ['hello', 'hi', 'hey', 'hii', 'hiii', 'hallo', 'halo', 'hlo', 'hlw', 'hlo', 'hiiii']
    if any(word in lower_message for word in greeting_words):
        return "👋 Hello! I'm your Reliance Jio Infotech Solutions AI Assistant. I can help you with HR questions, document requests, and PDF processing. How can I assist you today?"
    
    # Enhanced help detection - various ways to ask for help
    help_words = ['help', 'what can you do', 'capabilities', 'help me', 'can you help', 'please help', 'i need help', 'what you can do', 'what do you do', 'how can you help', 'what services', 'what help', 'help pls', 'help plz']
    if any(word in lower_message for word in help_words):
        return "🤖 **Reliance Jio Infotech Solutions - Your Intelligent Companion**\n\nI can help you with three main services:\n\n💬 **HR Q&A Chat**\n• Ask about company policies, benefits, and procedures\n• Get information about leave policies, attendance, and more\n• Request official documents (type \"I need a document\")\n• Quick and accurate responses to your queries\n\n📄 **PDF Summarization**\n• Upload PDFs up to 50MB\n• Handles large documents (30+ pages)\n• Extracts and formats table data\n• Real-time processing with progress tracking\n\n📜 **Document Requests**\n• Request any of 16 official document types\n• Official Reliance Jio Infotech Solutions format\n• Professional document generation\n• Immediate download available\n• **Strict validation:** ALL fields must match exactly with employee records\n\n💡 **Quick Commands:**\n• Type \"qa\" or \"chat\" to switch to HR Q&A mode\n• Type \"summarize\" or \"pdf\" to switch to PDF mode\n• Type \"I need a document\" to request official documents\n• Search employees: \"search employee [name or ID]\"\n• Use the mode buttons above for quick switching\n\n⚠️ **Important:** Document generation requires ALL employee details to match our records exactly."
    
    # Enhanced salary detection - various ways to ask about salary
    salary_words = ['salary', 'compensation', 'pay', 'payment', 'money', 'income', 'earnings', 'wage', 'wages', 'paycheck', 'pay check', 'pay slip', 'payslip', 'salary slip', 'salaryslip', 'form 16', 'form16', 'tax', 'tax document', 'taxdoc']
    if any(word in lower_message for word in salary_words):
        return "💰 **Salary & Compensation**\n\nSalary information is confidential and varies by role and experience. For specific salary-related queries:\n\n• **Salary Slips:** Use Document Requests mode\n• **Tax Documents:** Request Form 16 through Document Requests\n• **Salary Certificate:** Available in Document Requests\n\nPlease use the Document Requests mode to generate official salary-related documents."
    
    # Enhanced document detection - various ways to ask for documents
    document_words = ['document', 'certificate', 'letter', 'documents', 'certificates', 'letters', 'doc', 'docs', 'cert', 'certs', 'form', 'forms', 'paper', 'papers', 'slip', 'slips', 'statement', 'statements', 'documant', 'certificat', 'letr', 'dokument', 'sertifikat']
    if any(word in lower_message for word in document_words):
        return "📜 **Document Requests**\n\nI can help you generate official documents. Please:\n\n1. **Switch to Document Requests mode** using the mode selector above\n2. **Select a document type** from the 16 available options\n3. **Fill in the required details**\n4. **Generate and download** your document\n\n**Available Documents:**\n• Bonafide / Employment Verification Letter\n• Experience Certificate\n• Offer Letter Copy\n• Appointment Letter Copy\n• Promotion Letter\n• Relieving Letter\n• Salary Slips\n• Form 16 / Tax Documents\n• Salary Certificate\n• PF Statement / UAN details\n• No Objection Certificate (NOC)\n• Non-Disclosure Agreement Copy\n• ID Card Replacement\n• Medical Insurance Card Copy\n• Business Travel Authorization Letter\n• Visa Support Letter\n\n⚠️ **Important:** Document generation requires ALL employee details to match our records exactly."
    
    # Enhanced employee search detection
    employee_words = ['employee', 'search', 'find', 'look for', 'searching', 'finding', 'looking', 'emp', 'employe', 'empl', 'searching for', 'looking for', 'find employee', 'search employee', 'look employee']
    if any(word in lower_message for word in employee_words):
        return "🔍 **Employee Search**\n\nTo search for employees:\n\n• Use the employee search feature in Document Requests mode\n• Type \"search employee [name or ID]\" for quick search\n• Auto-fill forms with \"fill form for [name or ID]\"\n\nEmployee search helps you find specific employees and auto-fill document forms with their details."
    
    # Enhanced thank you detection
    thank_words = ['thank', 'thanks', 'thx', 'thnx', 'thank you', 'thankyou', 'thanks a lot', 'thank u', 'thnks', 'thnk u', 'tq', 'tq so much']
    if any(word in lower_message for word in thank_words):
        return "🙏 You're welcome! I'm here to help you with all your document processing and certificate generation needs. Feel free to ask if you need anything else!"
    
    # Enhanced status detection
    status_words = ['status', 'health', 'working', 'system', 'server', 'online', 'offline', 'up', 'down', 'running', 'operational']
    if any(word in lower_message for word in status_words):
        return "🟢 **System Status:** All services are operational\n\n💬 **HR Q&A Chat:** Active\n📊 **PDF Processing:** Active\n📜 **Document Generation:** Active\n🌐 **API Endpoints:** All responding\n\nEverything is working perfectly! 🚀"
    
    # Enhanced PDF detection
    pdf_words = ['pdf', 'summarize', 'upload', 'process', 'analyze', 'read', 'extract', 'convert', 'summarise', 'summarization', 'summarisation', 'pdfs', 'document', 'documents', 'file', 'files', 'upload pdf', 'process pdf', 'analyze pdf', 'read pdf', 'extract from pdf', 'summarize pdf', 'pdf summary', 'pdf analysis', 'pdf processing']
    if any(word in lower_message for word in pdf_words):
        return "📄 **PDF Summarization**\n\nI can help you summarize PDF documents! 🚀\n\n• Upload any PDF (up to 50MB)\n• Handles large documents (30+ pages)\n• Extracts and formats table data\n• Powered by advanced processing for superior accuracy\n\nSimply switch to PDF Summarization mode and drag & drop or click to upload your PDF!"
    
    # Enhanced leave/policy detection
    leave_words = ['leave', 'policy', 'policies', 'attendance', 'absent', 'present', 'holiday', 'vacation', 'sick', 'medical', 'casual', 'annual', 'maternity', 'paternity', 'bereavement', 'compensatory', 'work from home', 'wfh', 'remote', 'hybrid']
    if any(word in lower_message for word in leave_words):
        return "📋 **Leave & Attendance Policies**\n\nI can help you with leave and attendance information:\n\n• **Leave Types:** Casual, Sick, Annual, Maternity, Paternity\n• **Attendance Policy:** Regular attendance requirements\n• **Work from Home:** WFH policies and procedures\n• **Holiday Calendar:** Company holidays and off days\n\nPlease ask specific questions about leave policies, and I'll provide detailed information!"
    
    # Enhanced benefits detection
    benefits_words = ['benefit', 'benefits', 'insurance', 'medical', 'health', 'dental', 'vision', 'pf', 'provident fund', 'gratuity', 'bonus', 'incentive', 'allowance', 'perks', 'facility', 'facilities']
    if any(word in lower_message for word in benefits_words):
        return "🏥 **Employee Benefits**\n\nI can help you with information about employee benefits:\n\n• **Medical Insurance:** Health coverage details\n• **Provident Fund:** PF contribution and withdrawal\n• **Gratuity:** Gratuity calculation and eligibility\n• **Other Benefits:** Allowances, bonuses, incentives\n\nPlease ask specific questions about benefits, and I'll provide detailed information!"
    
    # Default response
    return "💭 I understand you're asking about: \"" + message + "\"\n\nI can help you with:\n💬 **HR Q&A Chat** - Ask about company policies and procedures\n📄 **PDF Summarization** - Upload any PDF for comprehensive analysis\n📜 **Document Requests** - Request official documents through chat\n\n💡 **Quick Start:**\n• Switch to HR Q&A mode to ask questions\n• Upload a PDF file above for summarization\n• Type \"I need a document\" to request official documents\n• Use the mode buttons to switch between services\n• Search for employees: \"search employee [name or ID]\"\n\n⚠️ **Important:** Document generation requires ALL employee details to match our records exactly.\n\nHow would you like to proceed?"


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request) -> ChatResponse:
    """
    Process chat messages with simple responses - no AI models
    """
    start_time = datetime.now()
    
    try:
        # Log incoming request with client info
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"📨 Received chat request from {client_ip}: {req.message[:50]}...")
        
        # Validate message length
        if len(req.message) > 10000:
            logger.warning(f"Message too long: {len(req.message)} characters")
            raise HTTPException(
                status_code=400, 
                detail="Message is too long (maximum 10,000 characters)"
            )
        
        # Check if services are available
        if not bad_filter:
            logger.warning("Bad language filter not available - proceeding without filter")
        
        # Check for bad language (if filter is available)
        if bad_filter:
            try:
                if bad_filter.contains_bad_language(req.message):
                    logger.warning("Inappropriate language detected")
                    return ChatResponse(
                        response="Please keep the conversation respectful and professional.",
                        success=False,
                        error="Inappropriate language detected",
                        timestamp=datetime.now().isoformat()
                    )
            except Exception as filter_error:
                logger.error(f"Error in language filter: {str(filter_error)}")
                # Continue processing even if filter fails
        
        # Get AI-powered response using QA engine
        try:
            if qa_engine:
                answer = await qa_engine.answer(req.message)
            else:
                # Fallback to simple response if QA engine is not available
                answer = get_simple_response(req.message)
            
            # Ensure response is not empty
            if not answer.strip():
                logger.warning("Empty response generated")
                answer = "I apologize, but I didn't receive a proper response. Please try again."
            
            # Log response time
            response_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Chat response generated successfully in {response_time:.2f}s")
            
            return ChatResponse(
                response=answer,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as response_error:
            logger.error(f"Error generating response: {str(response_error)}")
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate response"
            )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to process message. Please try again."
        )


@router.get("/health")
async def chat_health() -> dict:
    """Health check endpoint for chat services"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "bad_language_filter": bad_filter is not None,
                "qa_engine": qa_engine is not None,
                "chat_responses": True  # Responses always available
            }
        }
        
        warnings = []
        if not bad_filter:
            warnings.append("Bad language filter not available")
        if not qa_engine:
            warnings.append("QA engine not available")
        
        if warnings:
            health_status["status"] = "degraded"
            health_status["warnings"] = warnings
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }


