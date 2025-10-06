import re
from io import BytesIO
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
import logging

from ..services.certificate_generator import generate_bonafide_pdf
from ..services.employee_validator import EmployeeValidator
from ..services.db import db_service
from ..config import auth_disabled

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services with better error handling
employee_validator = None

def initialize_services():
    """Initialize certificate services with enhanced error handling"""
    global employee_validator
    
    try:
        # Initialize employee validator
        try:
            employee_validator = EmployeeValidator()
            logger.info("✅ Employee validator initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize employee validator: {str(e)}")
            employee_validator = None
            
        if employee_validator:
            logger.info("✅ All certificate services initialized successfully")
        else:
            logger.warning("⚠️ Some certificate services failed to initialize")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize certificate services: {str(e)}")
        employee_validator = None

# Initialize services on module load
initialize_services()

def org_name():
    """Get organization name with fallback"""
    return "Reliance Jio Infotech Solutions"

# Utility function to validate input content
def validate_input_content(content: str, max_length: int = 100) -> { 'is_valid': bool, 'error': str }:
    """Validate input content for security and length"""
    if not content or not isinstance(content, str):
        return { 'is_valid': False, 'error': 'Content is required and must be a string' }
    
    trimmed = content.strip()
    if len(trimmed) == 0:
        return { 'is_valid': False, 'error': 'Content cannot be empty or contain only whitespace' }
    
    if len(trimmed) > max_length:
        return { 'is_valid': False, 'error': f'Content is too long (maximum {max_length} characters)' }
    
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
        if re.search(pattern, trimmed, re.IGNORECASE):
            return { 'is_valid': False, 'error': 'Content contains potentially harmful patterns' }
    
    return { 'is_valid': True, 'error': None }

class CertRequest(BaseModel):
    emp_id: str = Field(..., min_length=1, max_length=50, description="Employee ID")
    organization_name: Optional[str] = Field(None, max_length=100, description="Organization name")
    
    @validator('emp_id')
    def validate_emp_id(cls, v):
        validation = validate_input_content(v, 50)
        if not validation['is_valid']:
            raise ValueError(validation['error'])
        return v.strip()
    
    @validator('organization_name')
    def validate_org_name(cls, v):
        if v is not None:
            validation = validate_input_content(v, 100)
            if not validation['is_valid']:
                raise ValueError(validation['error'])
            return v.strip()
        return v

@router.post("/bonafide")
async def bonafide(req: CertRequest, request: Request):
    """Generate bonafide certificate with enhanced error handling"""
    start_time = datetime.now()
    
    try:
        # Log request
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"📄 Bonafide certificate request from {client_ip}: {req.emp_id}")
        
        # Get employee data from MongoDB
        employee = await db_service.get_employee_by_id(int(req.emp_id))
        if not employee:
            logger.warning(f"Employee not found: {req.emp_id}")
            raise HTTPException(status_code=404, detail="Employee not found")

        # Generate certificate
        organization = req.organization_name or org_name()
        pdf_bytes = generate_bonafide_pdf(employee, organization)
        
        # Log success
        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Bonafide certificate generated successfully in {response_time:.2f}s")
        
        return StreamingResponse(
            BytesIO(pdf_bytes), 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=bonafide_{req.emp_id}.pdf"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error generating bonafide certificate: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate certificate")

@router.get("/employee-suggestions/{partial_name}")
async def get_employee_suggestions(partial_name: str, limit: int = 5, request: Request = None):
    """Get employee suggestions based on partial name or ID with enhanced error handling"""
    start_time = datetime.now()
    
    try:
        # Log request
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"🔍 Employee suggestions request from {client_ip}: {partial_name}")
        
        # Check if services are available
        if not employee_validator:
            logger.error("Employee validator not available")
            raise HTTPException(status_code=503, detail="Employee search service is temporarily unavailable")
        
        # Validate input parameters
        validation = validate_input_content(partial_name, 100)
        if not validation['is_valid']:
            logger.warning(f"Invalid partial name: {validation['error']}")
            raise HTTPException(status_code=400, detail=validation['error'])
        
        # Sanitize input
        partial_name = partial_name.strip()
        
        # Validate limit parameter
        if limit < 1 or limit > 20:
            limit = 5  # Default to 5 if invalid
            logger.info(f"Invalid limit parameter, using default: {limit}")
        
        # Get suggestions
        suggestions = employee_validator.get_employee_suggestions(partial_name, limit)
        
        # Log success
        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Employee suggestions completed in {response_time:.2f}s, found {len(suggestions)} results")
        
        return {
            "success": True,
            "suggestions": suggestions,
            "count": len(suggestions),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting employee suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")

@router.post("/validate-employee")
async def validate_employee(employee_data: dict, request: Request = None):
    """Validate employee data against records with enhanced error handling"""
    start_time = datetime.now()
    
    try:
        # Log request
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"✅ Employee validation request from {client_ip}")
        
        # Check if services are available
        if not employee_validator:
            logger.error("Employee validator not available")
            raise HTTPException(status_code=503, detail="Employee validation service is temporarily unavailable")
        
        # Validate input
        if not employee_data or not isinstance(employee_data, dict):
            logger.warning("Invalid employee data format")
            raise HTTPException(status_code=400, detail="Employee data must be a valid dictionary")
        
        # Perform validation
        validation_result = employee_validator.validate_employee(employee_data)
        
        # Log success
        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Employee validation completed in {response_time:.2f}s")
        
        return {
            "is_valid": validation_result.get('is_valid', False),
            "errors": validation_result.get('errors', []),
            "warnings": validation_result.get('warnings', []),
            "matched_employee": validation_result.get('matched_employee', None),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error validating employee: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.get("/employee/{employee_id}")
async def get_employee_by_id(employee_id: str, request: Request = None):
    """Get employee details by ID with enhanced error handling"""
    start_time = datetime.now()
    
    try:
        # Log request
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"👤 Employee lookup request from {client_ip}: {employee_id}")
        
        # Check if services are available
        if not employee_validator:
            logger.error("Employee validator not available")
            raise HTTPException(status_code=503, detail="Employee lookup service is temporarily unavailable")
        
        # Validate input
        validation = validate_input_content(employee_id, 50)
        if not validation['is_valid']:
            logger.warning(f"Invalid employee ID: {validation['error']}")
            raise HTTPException(status_code=400, detail=validation['error'])
        
        # Sanitize input
        employee_id = employee_id.strip()
        
        # Get employee data
        employee = employee_validator.get_employee_by_id(employee_id)
        
        # Log success
        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Employee lookup completed in {response_time:.2f}s")
        
        if employee:
            return {
                "success": True,
                "employee": employee,
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.warning(f"Employee not found: {employee_id}")
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "Employee not found",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting employee by ID: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get employee: {str(e)}")

@router.get("/health")
async def certificate_health_check():
    """Health check for certificate services"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "database": db_service.employees_collection is not None,
                "employee_validator": employee_validator is not None
            }
        }
        
        if db_service.employees_collection is None or not employee_validator:
            health_status["status"] = "degraded"
            health_status["warnings"] = []
            
            if db_service.employees_collection is None:
                health_status["warnings"].append("Database not available")
            if not employee_validator:
                health_status["warnings"].append("Employee validator not available")
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }


