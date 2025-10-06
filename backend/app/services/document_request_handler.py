import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os

from .document_pdf_generator import DocumentPDFGenerator

class DocumentRequestHandler:
    """Handles document requests with step-by-step flow"""
    
    def __init__(self):
        self.documents_file = Path(__file__).parent.parent / "data" / "document_requests.json"
        self.supported_documents = {
            "1": "Bonafide / Employment Verification Letter",
            "2": "Experience Certificate", 
            "3": "Offer Letter Copy",
            "4": "Appointment Letter Copy",
            "5": "Promotion Letter",
            "6": "Relieving Letter",
            "7": "Salary Slips",
            "8": "Form 16 / Tax Documents",
            "9": "Salary Certificate",
            "10": "PF Statement / UAN details",
            "11": "No Objection Certificate (NOC)",
            "12": "Non-Disclosure Agreement Copy",
            "13": "ID Card Replacement",
            "14": "Medical Insurance Card Copy",
            "15": "Business Travel Authorization Letter",
            "16": "Visa Support Letter"
        }
        
        # Load existing requests
        self.requests = self._load_requests()
        
        # Initialize PDF generator
        self.pdf_generator = DocumentPDFGenerator()
    
    def _load_requests(self) -> List[Dict]:
        """Load existing document requests"""
        try:
            with open(self.documents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_requests(self):
        """Save document requests"""
        with open(self.documents_file, 'w', encoding='utf-8') as f:
            json.dump(self.requests, f, indent=2, ensure_ascii=False)
    
    def is_document_request(self, message: str) -> bool:
        """Check if message is requesting a document"""
        document_keywords = [
            "need document", "request document", "get document", 
            "document request", "i need a document", "want document",
            "require document", "asking for document", "document please"
        ]
        
        message_lower = message.lower().strip()
        return any(keyword in message_lower for keyword in document_keywords)
    
    def get_document_list(self) -> str:
        """Get the list of supported documents"""
        document_list = "Sure! Please choose the type of document you need:\n\n"
        
        for num, doc_name in self.supported_documents.items():
            document_list += f"{num}. {doc_name}\n"
        
        document_list += "\nPlease reply with the number (1-16) of the document you need."
        return document_list
    
    def validate_document_choice(self, choice: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate user's document choice"""
        choice = choice.strip()
        
        # Check if it's a number 1-16
        if choice.isdigit() and 1 <= int(choice) <= 16:
            doc_name = self.supported_documents[choice]
            return True, choice, doc_name
        
        # Check if it's a document name
        choice_lower = choice.lower()
        for num, doc_name in self.supported_documents.items():
            if choice_lower in doc_name.lower():
                return True, num, doc_name
        
        return False, None, None
    
    def get_document_details_prompt(self, doc_name: str) -> str:
        """Get the prompt for collecting document details"""
        base_prompt = f"You selected {doc_name}. Please provide the following details:\n\n"
        
        # Add a note about chat-based requests
        base_prompt += "💡 **Note:** You can provide these details in a simple text format, or use our form-based system for a better experience.\n\n"
        
        # Different prompts based on document type
        if "bonafide" in doc_name.lower() or "employment verification" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Purpose (e.g., bank loan, visa application, etc.)\n• Any specific requirements"
        
        elif "experience" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Date of joining\n• Date of leaving (if applicable)\n• Purpose"
        
        elif "offer letter" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Position/Designation\n• Department\n• Date of offer\n• Purpose of request"
        
        elif "appointment letter" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Position/Designation\n• Department\n• Date of appointment\n• Purpose of request"
        
        elif "salary" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Time period (e.g., last 3 months, specific month)\n• Purpose"
        
        elif "form 16" in doc_name.lower() or "tax" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Financial year (e.g., 2023-24)\n• Purpose"
        
        elif "pf" in doc_name.lower() or "uan" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• UAN number (if known)\n• Purpose"
        
        elif "noc" in doc_name.lower() or "no objection" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Purpose of NOC\n• Duration (if applicable)\n• Any specific conditions"
        
        elif "id card" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Reason for replacement (lost, damaged, etc.)\n• Date of incident (if applicable)"
        
        elif "medical insurance" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Policy number (if known)\n• Purpose of request"
        
        elif "travel authorization" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Destination\n• Purpose of travel\n• Travel dates\n• Duration of trip"
        
        elif "visa" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Destination country\n• Purpose of travel\n• Travel dates\n• Type of visa"
        
        elif "travel" in doc_name.lower():
            return base_prompt + "• Full Name\n• Employee ID\n• Destination\n• Purpose of travel\n• Travel dates\n• Estimated cost"
        
        else:
            return base_prompt + "• Full Name\n• Employee ID\n• Purpose\n• Any additional requirements"
    
    def validate_document_details(self, details: str, doc_type: str) -> Tuple[bool, str]:
        """Validate if required details are provided"""
        try:
            # Try to parse as JSON first (from form submission)
            import json
            details_dict = json.loads(details)
            
            # Validate JSON form data
            missing_fields = []
            
            # Check for required employee fields
            if not details_dict.get('employeeName', '').strip():
                missing_fields.append('Employee Name')
            if not details_dict.get('employeeId', '').strip():
                missing_fields.append('Employee ID')
            if not details_dict.get('designation', '').strip():
                missing_fields.append('Designation')
            if not details_dict.get('department', '').strip():
                missing_fields.append('Department')
            if not details_dict.get('joiningDate', '').strip():
                missing_fields.append('Joining Date')
            
            # Check for document-specific required fields
            # Note: Issue Date is automatically set to current date for all documents
            if doc_type == "1":  # Bonafide / Employment Verification Letter
                # No additional fields required beyond the basic employee fields
                pass
            elif doc_type == "2":  # Experience certificate
                if not details_dict.get('relievingDate', '').strip():
                    missing_fields.append('Relieving Date')
            elif doc_type == "3":  # Offer Letter Copy
                if not details_dict.get('salaryAmount', '').strip():
                    missing_fields.append('Salary Amount')
            elif doc_type == "4":  # Appointment Letter Copy
                if not details_dict.get('appointmentDate', '').strip():
                    missing_fields.append('Appointment Date')
            elif doc_type == "5":  # Promotion letter
                if not details_dict.get('promotionDate', '').strip():
                    missing_fields.append('Promotion Date')
                if not details_dict.get('newDesignation', '').strip():
                    missing_fields.append('New Designation')
            elif doc_type == "6":  # Relieving letter
                if not details_dict.get('relievingDate', '').strip():
                    missing_fields.append('Relieving Date')
            elif doc_type == "9":  # Salary certificate
                if not details_dict.get('salaryAmount', '').strip():
                    missing_fields.append('Salary Amount')
                if not details_dict.get('purpose', '').strip():
                    missing_fields.append('Purpose')
            elif doc_type == "11":  # NOC
                if not details_dict.get('nocPurpose', '').strip():
                    missing_fields.append('NOC Purpose')
                if not details_dict.get('effectiveDate', '').strip():
                    missing_fields.append('Effective Date')
            elif doc_type == "12":  # NDA
                if not details_dict.get('signingDate', '').strip():
                    missing_fields.append('Signing Date')
            elif doc_type == "13":  # ID Card Replacement
                if not details_dict.get('reason', '').strip():
                    missing_fields.append('Reason for Replacement')
            elif doc_type == "15":  # Business Travel Authorization
                if not details_dict.get('destination', '').strip():
                    missing_fields.append('Destination')
                if not details_dict.get('purpose', '').strip():
                    missing_fields.append('Purpose')
                if not details_dict.get('duration', '').strip():
                    missing_fields.append('Duration')
                if not details_dict.get('travelDate', '').strip():
                    missing_fields.append('Travel Date')
            elif doc_type == "7":  # Salary Slip
                if not details_dict.get('salaryAmount', '').strip():
                    missing_fields.append('Salary Amount')
            elif doc_type == "8":  # Form 16
                if not details_dict.get('salaryAmount', '').strip():
                    missing_fields.append('Salary Amount')
            elif doc_type == "10":  # PF Statement
                # No additional fields required beyond the basic employee fields
                pass
            elif doc_type == "14":  # Medical Insurance Card
                # No additional fields required beyond the basic employee fields
                pass
            elif doc_type == "16":  # Visa support
                if not details_dict.get('destination', '').strip():
                    missing_fields.append('Destination')
                if not details_dict.get('purpose', '').strip():
                    missing_fields.append('Purpose')
                if not details_dict.get('duration', '').strip():
                    missing_fields.append('Duration')
            
            if missing_fields:
                return False, f"Please provide: {', '.join(missing_fields)}"
            
            return True, "Details look good!"
            
        except (json.JSONDecodeError, TypeError):
            # If not JSON, treat as plain text (fallback for chat-based requests)
            details_lower = details.lower()
            
            # Check for basic required fields in text
            required_fields = ["name", "employee", "id"]
            missing_fields = []
            
            for field in required_fields:
                if field not in details_lower:
                    missing_fields.append(field)
            
            if missing_fields:
                return False, f"Please provide: {', '.join(missing_fields)}"
            
            return True, "Details look good!"
    
    def submit_document_request(self, doc_type: str, doc_name: str, details: str, user_id: str = "anonymous") -> Dict:
        """Submit a document request and generate PDF with enhanced error handling"""
        try:
            # Validate input parameters
            if not doc_type or not doc_name or not details:
                raise ValueError("Missing required parameters: doc_type, doc_name, and details are required")
            
            # Generate PDF immediately
            pdf_content = self.pdf_generator.generate_document_pdf(doc_type, doc_name, details, user_id)
            
            # Validate PDF content
            if not pdf_content or len(pdf_content) == 0:
                raise ValueError("Generated PDF is empty or invalid")
            
            # Ensure PDF content is bytes
            if isinstance(pdf_content, str):
                try:
                    pdf_content = pdf_content.encode('utf-8')
                except:
                    raise ValueError("Invalid PDF content format")
            
            request = {
                "id": f"DOC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "document_type": doc_type,
                "document_name": doc_name,
                "details": details,
                "user_id": user_id,
                "status": "completed",
                "submitted_at": datetime.now().isoformat(),
                "hr_notified": False,
                "pdf_generated": True,
                "pdf_content": pdf_content.hex() if isinstance(pdf_content, bytes) else pdf_content
            }
            
            # Add to requests list
            self.requests.append(request)
            self._save_requests()
            
            # Log for HR notification
            self._log_hr_notification(request)
            
            return request
            
        except Exception as e:
            # Log the specific error for debugging
            print(f"PDF generation error for document {doc_name}: {str(e)}")
            
            # Create a request with error information
            request = {
                "id": f"DOC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "document_type": doc_type,
                "document_name": doc_name,
                "details": details,
                "user_id": user_id,
                "status": "error",
                "submitted_at": datetime.now().isoformat(),
                "hr_notified": False,
                "pdf_generated": False,
                "error": str(e)
            }
            
            self.requests.append(request)
            self._save_requests()
            self._log_hr_notification(request)
            
            # Re-raise the exception to be handled by the caller
            raise e
    
    def _log_hr_notification(self, request: Dict):
        """Log document request for HR notification with enhanced error handling"""
        try:
            log_file = Path(__file__).parent.parent / "data" / "hr_notifications.log"
            
            notification = f"""
=== DOCUMENT REQUEST NOTIFICATION ===
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Request ID: {request['id']}
Document: {request['document_name']}
User: {request['user_id']}
Details: {request['details']}
Status: {request['status']}
=====================================
"""
            
            # Ensure directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(notification)
        except Exception as e:
            print(f"Error logging HR notification: {e}")
    
    def get_confirmation_message(self, doc_name: str, request_id: str, pdf_generated: bool = False, error: str = None) -> str:
        """Get confirmation message for submitted request with enhanced formatting"""
        if pdf_generated:
            return f"""✅ **Your {doc_name} has been generated successfully!**

📋 **Document Details:**
• Document: {doc_name}
• Request ID: `{request_id}`
• Status: Completed
• Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📄 **Download:**
• Your PDF document is ready for download
• Click the download button below to save the document
• The document is professionally formatted with company branding

📧 **Additional Information:**
• A copy has been sent to HR for record-keeping
• For any issues, contact HR at hr@reliancejio.com

🎉 **Thank you for using our document generation service!**"""
        
        elif error:
            return f"""⚠️ **Document generation encountered an issue.**

📋 **Request Details:**
• Document: {doc_name}
• Request ID: `{request_id}`
• Status: Pending HR Review
• Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

❌ **Issue:** {error}

📧 **Next Steps:**
• Your request has been sent to HR for manual processing
• HR will review and generate the document within 24-48 hours
• You'll receive an email confirmation when ready
• For urgent requests, contact HR directly at hr@reliancejio.com

📞 **Need Help?**
Contact HR at hr@reliancejio.com or call the HR helpline for assistance."""
        
        else:
            return f"""✅ **Your request for {doc_name} has been submitted to HR.**

📋 **Request Details:**
• Request ID: `{request_id}`
• Status: Pending
• Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📧 **Next Steps:**
• HR will review your request within 24-48 hours
• You'll receive an email confirmation
• For urgent requests, contact HR directly at hr@reliancejio.com

📞 **Need Help?**
Contact HR at hr@reliancejio.com or call the HR helpline for assistance."""
    
    def get_request_status(self, request_id: str) -> Optional[Dict]:
        """Get status of a document request with enhanced error handling"""
        try:
            if not request_id or not isinstance(request_id, str):
                return None
                
            for request in self.requests:
                if request.get('id') == request_id:
                    return request
            return None
        except Exception as e:
            print(f"Error getting request status: {str(e)}")
            return None
    
    def get_user_requests(self, user_id: str) -> List[Dict]:
        """Get all requests for a specific user with enhanced error handling"""
        try:
            if not user_id or not isinstance(user_id, str):
                return []
                
            return [req for req in self.requests if req.get('user_id') == user_id]
        except Exception as e:
            print(f"Error getting user requests: {str(e)}")
            return []
    
    def get_pending_requests_count(self) -> int:
        """Get count of pending requests with enhanced error handling"""
        try:
            return len([req for req in self.requests if req.get('status') == 'pending'])
        except Exception as e:
            print(f"Error getting pending requests count: {str(e)}")
            return 0
