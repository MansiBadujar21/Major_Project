import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, blue, white, Color
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io

from .employee_validator import EmployeeValidator

# Enhanced helper functions for premium design - Fixed to avoid image processing issues
def get_company_logo():
    """Generate a professional Reliance Jio logo using ReportLab - Fixed version"""
    # Return None to avoid image processing issues - will be handled in text-based design
    return None

def get_digital_signature(signer_name: str, designation: str):
    """Generate a professional digital signature with enhanced design - Fixed version"""
    # Return None to avoid image processing issues - will be handled in text-based design
    return None

def get_security_watermark():
    """Generate a professional security watermark - Fixed version"""
    # Return None to avoid image processing issues - will be handled in text-based design
    return None

def get_qr_code(certificate_id: str):
    """Generate a QR code placeholder for document verification - Fixed version"""
    # Return None to avoid image processing issues - will be handled in text-based design
    return None

def get_certificate_badge():
    """Generate a professional certificate badge - Fixed version"""
    # Return None to avoid image processing issues - will be handled in text-based design
    return None

class DocumentPDFGenerator:
    """Enhanced PDF Generator for all document types with professional design"""
    
    def __init__(self):
        self.employee_validator = EmployeeValidator()
        self.styles = getSampleStyleSheet()
        self.setup_enhanced_styles()
        
        # Company details
        self.company_name = "Reliance Jio Infotech Solutions"
        self.company_address = "Mumbai, Maharashtra, India"
        self.company_email = "hr@reliancejio.com"
        self.company_phone = "+91-22-3555-0000"
        self.company_website = "www.reliancejio.com"
        
        # Document templates
        self.document_templates = {
            "1": self.generate_bonafide_letter,
            "2": self.generate_experience_certificate,
            "3": self.generate_offer_letter,
            "4": self.generate_appointment_letter,
            "5": self.generate_promotion_letter,
            "6": self.generate_relieving_letter,
            "7": self.generate_salary_slip,
            "8": self.generate_form_16,
            "9": self.generate_salary_certificate,
            "10": self.generate_pf_statement,
            "11": self.generate_noc_letter,
            "12": self.generate_nda_copy,
            "13": self.generate_id_card_replacement,
            "14": self.generate_medical_insurance_card,
            "15": self.generate_travel_authorization,
            "16": self.generate_visa_support_letter
        }
    
    def setup_enhanced_styles(self):
        """Setup enhanced paragraph styles with professional formatting"""
        # Company header style
        self.company_header_style = ParagraphStyle(
            'CompanyHeader',
            parent=self.styles['Normal'],
            fontSize=18,
            spaceAfter=8,
            alignment=TA_CENTER,
            textColor=HexColor('#1e40af'),
            fontName='Helvetica-Bold',
            leading=22
        )
        
        # Company subtitle style
        self.company_subtitle_style = ParagraphStyle(
            'CompanySubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=HexColor('#374151'),
            fontName='Helvetica',
            leading=14
        )
        
        # Document title style
        self.document_title_style = ParagraphStyle(
            'DocumentTitle',
            parent=self.styles['Normal'],
            fontSize=16,
            spaceAfter=20,
            spaceBefore=20,
            alignment=TA_CENTER,
            textColor=HexColor('#1e40af'),
            fontName='Helvetica-Bold',
            leading=20
        )
        
        # Section heading style
        self.section_heading_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Normal'],
            fontSize=13,
            spaceAfter=10,
            spaceBefore=15,
            textColor=HexColor('#1e40af'),
            fontName='Helvetica-Bold',
            leading=16
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'NormalText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            spaceBefore=0,
            alignment=TA_JUSTIFY,
            fontName='Times-Roman',
            leading=15,
            firstLineIndent=20
        )
        
        # Salutation style
        self.salutation_style = ParagraphStyle(
            'Salutation',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=15,
            spaceBefore=0,
            alignment=TA_LEFT,
            fontName='Times-Roman',
            leading=16
        )
        
        # Closing style
        self.closing_style = ParagraphStyle(
            'Closing',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=20,
            spaceBefore=15,
            alignment=TA_LEFT,
            fontName='Times-Roman',
            leading=15
        )
        
        # Reference number style
        self.reference_style = ParagraphStyle(
            'Reference',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_RIGHT,
            textColor=HexColor('#6b7280'),
            fontName='Helvetica',
            leading=12
        )
        
        # Footer style
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=0,
            alignment=TA_CENTER,
            textColor=HexColor('#6b7280'),
            fontName='Helvetica',
            leading=11
        )

    def generate_document_pdf(self, doc_type: str, doc_name: str, details: str, user_id: str = "anonymous") -> bytes:
        """Generate PDF for any document type with enhanced error handling"""
        try:
            # Validate input parameters
            if not doc_type or not doc_name or not details:
                raise ValueError("Missing required parameters: doc_type, doc_name, and details are required")
            
            # Parse details to extract employee information
            employee_info = self._parse_employee_details(details)
            
            # Validate employee if information is provided
            if employee_info.get('employee_code'):
                try:
                    validation_result = self.employee_validator.validate_employee(employee_info)
                    if validation_result['is_valid']:
                        employee_info = validation_result['matched_employee']
                except Exception as validation_error:
                    print(f"Employee validation error: {validation_error}")
                    # Continue with provided employee info if validation fails
            
            # Generate PDF based on document type
            if doc_type in self.document_templates:
                pdf_bytes = self.document_templates[doc_type](doc_name, employee_info, details)
                if not pdf_bytes or len(pdf_bytes) == 0:
                    raise ValueError("Generated PDF is empty")
                return pdf_bytes
            else:
                raise ValueError(f"Unsupported document type: {doc_type}")
                
        except Exception as e:
            print(f"Error generating PDF: {e}")
            try:
                return self._generate_error_document(doc_name, str(e))
            except Exception as error_doc_error:
                print(f"Error generating error document: {error_doc_error}")
                # Return a minimal error PDF
                return self._generate_minimal_error_document(doc_name, str(e))

    def _parse_employee_details(self, details: str) -> Dict:
        """Parse employee details from text or JSON with enhanced error handling"""
        employee_info = {}
        try:
            import json
            details_dict = json.loads(details)
            
            # Map required fields with proper validation
            employee_info['full_name'] = details_dict.get('employeeName', 'Employee Name')
            employee_info['employee_code'] = details_dict.get('employeeId', '')
            employee_info['employee_id'] = details_dict.get('employeeId', '')
            employee_info['designation'] = details_dict.get('designation', 'Employee')
            employee_info['department'] = details_dict.get('department', 'General')
            employee_info['joining_date'] = details_dict.get('joiningDate', '')
            
            # Map all date fields properly
            if 'issueDate' in details_dict: employee_info['issue_date'] = details_dict['issueDate']
            if 'relievingDate' in details_dict: employee_info['relieving_date'] = details_dict['relievingDate']
            if 'appointmentDate' in details_dict: employee_info['appointment_date'] = details_dict['appointmentDate']
            if 'promotionDate' in details_dict: employee_info['promotion_date'] = details_dict['promotionDate']
            if 'effectiveDate' in details_dict: employee_info['effective_date'] = details_dict['effectiveDate']
            if 'signingDate' in details_dict: employee_info['signing_date'] = details_dict['signingDate']
            if 'travelDate' in details_dict: employee_info['travel_date'] = details_dict['travelDate']
            
            # Map other fields
            if 'salaryAmount' in details_dict: employee_info['salary_amount'] = details_dict['salaryAmount']
            if 'purpose' in details_dict: employee_info['purpose'] = details_dict['purpose']
            if 'nocPurpose' in details_dict: employee_info['noc_purpose'] = details_dict['nocPurpose']
            if 'destination' in details_dict: employee_info['destination'] = details_dict['destination']
            if 'duration' in details_dict: employee_info['duration'] = details_dict['duration']
            if 'newDesignation' in details_dict: employee_info['new_designation'] = details_dict['newDesignation']
            if 'reason' in details_dict: employee_info['reason'] = details_dict['reason']
            
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error parsing employee details: {e}")
            # Fallback to text parsing
            details_lower = details.lower()
            if "employee id" in details_lower or "emp" in details_lower:
                import re
                emp_match = re.search(r'emp[0-9]+', details_lower)
                if emp_match: employee_info['employee_id'] = emp_match.group().upper()
            if "name" in details_lower:
                lines = details.split('\n')
                for line in lines:
                    if "name" in line.lower():
                        name_part = line.split(':')[-1].strip()
                        if name_part: employee_info['full_name'] = name_part
            
            # Set defaults for missing fields
            if not employee_info.get('full_name'): employee_info['full_name'] = 'Employee Name'
            if not employee_info.get('employee_id'): employee_info['employee_id'] = ''
            if not employee_info.get('designation'): employee_info['designation'] = 'Employee'
            if not employee_info.get('department'): employee_info['department'] = 'General'
        
        return employee_info

    def _generate_error_document(self, doc_name: str, error: str) -> bytes:
        """Generate error document when PDF generation fails"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                              topMargin=2*cm, bottomMargin=2*cm)
        
        story = []
        
        # Add company header
        self._add_enhanced_company_header(story)
        
        # Error message
        story.append(Paragraph(f"Error Generating {doc_name}", self.document_title_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"An error occurred while generating your document: {error}", self.normal_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph("Please contact HR department for assistance.", self.normal_style))
        
        # Add footer
        self._add_enhanced_footer(story)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def _generate_minimal_error_document(self, doc_name: str, error: str) -> bytes:
        """Generate minimal error document when even error document generation fails"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                              topMargin=2*cm, bottomMargin=2*cm)
        
        story = []
        
        # Minimal error message
        story.append(Paragraph("Document Generation Error", self.document_title_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Failed to generate {doc_name}", self.normal_style))
        story.append(Paragraph(f"Error: {error}", self.normal_style))
        story.append(Paragraph("Please contact HR department for assistance.", self.normal_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def _add_enhanced_company_header(self, story: List):
        """Add enhanced company header with logo and professional styling"""
        # Company header (without logo to avoid image processing issues)
        story.append(Paragraph("RELIANCE JIO INFOTECH SOLUTIONS", self.company_header_style))
        story.append(Paragraph("A Subsidiary of Reliance Industries Limited", self.company_subtitle_style))
        story.append(Paragraph("📍 Registered Office: Maker Chambers IV, Nariman Point, Mumbai - 400021", self.company_subtitle_style))
        story.append(Paragraph("📋 CIN: L17110MH2007PLC169642 | GST: 27AABCR0000A1Z5", self.company_subtitle_style))
        story.append(Paragraph("📞 Phone: +91-22-3555-5000 | 📧 Email: hr@reliancejio.com", self.company_subtitle_style))
        story.append(Paragraph("🌐 Website: www.reliancejio.com", self.company_subtitle_style))
        story.append(Spacer(1, 15))

    def _add_enhanced_footer(self, story: List):
        """Add enhanced footer with security features"""
        story.append(Spacer(1, 20))
        story.append(Paragraph("🔒 This is a digitally generated document with enhanced security features", self.footer_style))
        story.append(Paragraph("📄 Document ID: RJI-" + datetime.now().strftime('%Y%m%d%H%M%S'), self.footer_style))
        story.append(Paragraph("⚡ Generated on: " + datetime.now().strftime('%d-%m-%Y at %H:%M:%S'), self.footer_style))
        story.append(Paragraph("🛡️ Protected by Reliance Jio Infotech Solutions Security Protocol", self.footer_style))

    def _add_signature_section(self, story: List, signatory_name: str, designation: str):
        """Add enhanced signature section with digital signatures"""
        story.append(Spacer(1, 20))
        story.append(Paragraph("✍️ Authorized Digital Signatures:", self.section_heading_style))
        story.append(Spacer(1, 10))
        
        # Create signature table with text-based signatures
        signature_data = [
            ['', ''],
            ['', '']
        ]
        
        signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ]))
        
        # Add text-based signatures instead of images
        sig1_text = Paragraph(f"<b>{signatory_name}</b><br/>{designation}<br/>Date: {datetime.now().strftime('%d-%m-%Y')}", self.normal_style)
        sig2_text = Paragraph(f"<b>Priya Sharma</b><br/>Senior HR Manager<br/>Date: {datetime.now().strftime('%d-%m-%Y')}", self.normal_style)
        
        # Replace table cells with text signatures
        signature_table._argW[0] = 3*inch
        signature_table._argW[1] = 3*inch
        signature_table._cellvalues[0][0] = sig1_text
        signature_table._cellvalues[0][1] = sig2_text
        
        story.append(signature_table)
        story.append(Spacer(1, 15))

    def _format_date(self, date_str: str) -> str:
        """Format date string to professional format"""
        if not date_str:
            return datetime.now().strftime('%d-%m-%Y')
        try:
            # Handle different date formats
            if '-' in date_str:
                if len(date_str.split('-')[0]) == 4:  # YYYY-MM-DD
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                else:  # DD-MM-YYYY
                    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            elif '/' in date_str:
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            else:
                return date_str
            return date_obj.strftime('%d-%m-%Y')
        except:
            return date_str

    def add_enhanced_border_and_watermark(self, canvas, doc):
        """Add enhanced border and watermark to the document"""
        # Enhanced border
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        canvas.setLineWidth(3)
        canvas.rect(0.5*inch, 0.5*inch, doc.width + 1.4*inch, doc.height + 1*inch, fill=0)
        
        # Inner border
        canvas.setStrokeColor(colors.HexColor('#d1d5db'))
        canvas.setLineWidth(1)
        canvas.rect(0.6*inch, 0.6*inch, doc.width + 1.2*inch, doc.height + 0.8*inch, fill=0)
        
        # Corner decorations
        corner_size = 0.3*inch
        for x, y in [(0.5*inch, doc.height + 1*inch), (doc.width + 1.4*inch, doc.height + 1*inch), 
                     (0.5*inch, 0.5*inch), (doc.width + 1.4*inch, 0.5*inch)]:
            canvas.setFillColor(colors.HexColor('#1e40af'))
            canvas.rect(x, y, corner_size, corner_size, fill=1)
            canvas.setFillColor(colors.white)
            canvas.circle(x + corner_size/2, y + corner_size/2, corner_size/4, fill=1)
        
        # Security watermark text (instead of image)
        canvas.setFillColor(colors.HexColor('#1e40af'))
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(doc.width + 0.2*inch, 0.2*inch, "SECURE")
        
        # QR Code text (instead of image)
        canvas.setFillColor(colors.HexColor('#1e40af'))
        canvas.setFont("Helvetica-Bold", 6)
        canvas.drawString(0.2*inch, 0.2*inch, f"RJI-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        # Page number
        canvas.setFillColor(colors.HexColor('#6b7280'))
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(doc.width/2 + 0.7*inch, 0.3*inch, f"Page {canvas.getPageNumber()}")

    def _add_certificate_badge_text(self, story: List):
        """Add certificate badge as text instead of image"""
        story.append(Paragraph("🏆 OFFICIAL CERTIFICATE 🏆", self.section_heading_style))
        story.append(Spacer(1, 15))

    def _get_current_issue_date(self):
        """Get current date as issue date for document generation"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        return current_date, self._format_date(current_date)

    def generate_bonafide_letter(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional bonafide letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("🎓 BONAFIDE CERTIFICATE 🎓", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-BON-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        purpose = employee_info.get('purpose', 'Official purposes')
        
        # Main Certificate Text
        cert_text_1 = f"""
This is to certify that <b>{employee_name}</b>, bearing Employee ID <b>{employee_id}</b>, is currently employed with <b>Reliance Jio Infotech Solutions</b> as <b>{designation}</b> in the <b>{department}</b> department.
        """
        story.append(Paragraph(cert_text_1, self.normal_style))
        
        cert_text_2 = f"""
The employee has been associated with our organization since <b>{joining_date}</b> and is working with us on a full-time basis. This bonafide certificate is issued for <b>{purpose}</b> and confirms the employment status of the above-mentioned individual with our organization.
        """
        story.append(Paragraph(cert_text_2, self.normal_style))
        
        cert_text_3 = f"""
The information provided herein is true and accurate to the best of our knowledge and belief. This certificate is valid for 30 days from the date of issue and should be used for the intended purpose only.
        """
        story.append(Paragraph(cert_text_3, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Issue Date', formatted_issue_date],
            ['Certificate Type', 'Bonafide Certificate'],
            ['Purpose', purpose],
            ['Status', 'Active Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()

    def generate_experience_certificate(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional experience certificate with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("🏆 EXPERIENCE CERTIFICATE 🏆", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        relieving_date = employee_info.get('relieving_date', '')
        formatted_relieving_date = self._format_date(relieving_date)
        ref_number = f"Reference No: RJI-EXP-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        relieving_date = self._format_date(employee_info.get('relieving_date', ''))
        
        # Main Certificate Text
        cert_text_1 = f"""
This is to certify that <b>{employee_name}</b>, bearing Employee ID <b>{employee_id}</b>, was employed with <b>Reliance Jio Infotech Solutions</b> as <b>{designation}</b> in the <b>{department}</b> department.
        """
        story.append(Paragraph(cert_text_1, self.normal_style))
        
        cert_text_2 = f"""
The employee was associated with our organization from <b>{joining_date}</b> to <b>{relieving_date}</b> and was relieved from services after completing all necessary formalities and handover procedures.
        """
        story.append(Paragraph(cert_text_2, self.normal_style))
        
        cert_text_3 = f"""
During the tenure, the employee demonstrated professional competence, maintained good conduct, and contributed positively to the organization's growth and success. The employee's performance was consistently satisfactory and met the organization's standards.
        """
        story.append(Paragraph(cert_text_3, self.normal_style))
        
        cert_text_4 = f"""
This certificate is issued for official purposes and confirms the employment details and work experience of the above-mentioned individual with our organization. The information provided herein is true and accurate to the best of our knowledge and belief.
        """
        story.append(Paragraph(cert_text_4, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Relieving Date', relieving_date],
            ['Total Experience', f"{self._calculate_experience(joining_date, relieving_date)}"],
            ['Issue Date', formatted_issue_date],
            ['Certificate Type', 'Experience Certificate'],
            ['Status', 'Relieved Employee'],
            ['Validity', 'Permanent Record']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()

    def _calculate_experience(self, joining_date: str, relieving_date: str) -> str:
        """Calculate total experience duration"""
        try:
            join = datetime.strptime(joining_date, '%d-%m-%Y')
            relieve = datetime.strptime(relieving_date, '%d-%m-%Y')
            diff = relieve - join
            years = diff.days // 365
            months = (diff.days % 365) // 30
            days = (diff.days % 365) % 30
            
            if years > 0:
                return f"{years} year(s), {months} month(s), {days} day(s)"
            elif months > 0:
                return f"{months} month(s), {days} day(s)"
            else:
                return f"{days} day(s)"
        except:
            return "Not specified"

    def generate_salary_certificate(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional salary certificate with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("💰 SALARY CERTIFICATE 💰", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-SAL-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        salary_amount = employee_info.get('salary_amount', '')
        purpose = employee_info.get('purpose', 'Official purposes')
        
        # Main Certificate Text
        cert_text_1 = f"""
This is to certify that <b>{employee_name}</b>, bearing Employee ID <b>{employee_id}</b>, is currently employed with <b>Reliance Jio Infotech Solutions</b> as <b>{designation}</b> in the <b>{department}</b> department.
        """
        story.append(Paragraph(cert_text_1, self.normal_style))
        
        cert_text_2 = f"""
The employee has been associated with our organization since <b>{joining_date}</b> and is currently drawing a salary of <b>₹{salary_amount}</b> per month from our organization. The salary is paid through bank transfer on the last working day of each month.
        """
        story.append(Paragraph(cert_text_2, self.normal_style))
        
        cert_text_3 = f"""
This salary certificate is issued for <b>{purpose}</b> and confirms the current salary details of the above-mentioned individual with our organization. The salary information provided herein is true and accurate to the best of our knowledge and belief.
        """
        story.append(Paragraph(cert_text_3, self.normal_style))
        
        cert_text_4 = f"""
The employee's salary is subject to applicable taxes and deductions as per the Income Tax Act and other statutory requirements. This certificate is valid for 30 days from the date of issue and should be used for the intended purpose only.
        """
        story.append(Paragraph(cert_text_4, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Current Salary', f"₹{salary_amount}"],
            ['Salary Frequency', 'Monthly'],
            ['Payment Mode', 'Bank Transfer'],
            ['Issue Date', formatted_issue_date],
            ['Certificate Type', 'Salary Certificate'],
            ['Purpose', purpose],
            ['Status', 'Active Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()

    def generate_noc_letter(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional NOC letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📋 NO OBJECTION CERTIFICATE (NOC) 📋", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-NOC-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        relieving_date = self._format_date(employee_info.get('relieving_date', ''))
        purpose = employee_info.get('purpose', 'Official purposes')
        
        # Main Certificate Text
        noc_text_1 = f"""
This is to certify that <b>{employee_name}</b>, bearing Employee ID <b>{employee_id}</b>, is currently employed with <b>Reliance Jio Infotech Solutions</b> as <b>{designation}</b> in the <b>{department}</b> department.
        """
        story.append(Paragraph(noc_text_1, self.normal_style))
        
        noc_text_2 = f"""
The employee has been associated with our organization since <b>{joining_date}</b> and has submitted a resignation letter with a relieving date of <b>{relieving_date}</b>. The employee has completed all necessary formalities and handover procedures as per company policy.
        """
        story.append(Paragraph(noc_text_2, self.normal_style))
        
        noc_text_3 = f"""
We hereby issue this No Objection Certificate (NOC) stating that we have no objection to the employee's future employment or any other activities as requested for <b>{purpose}</b>. The employee has cleared all dues and pending formalities with our organization.
        """
        story.append(Paragraph(noc_text_3, self.normal_style))
        
        noc_text_4 = f"""
This NOC is issued for official purposes and confirms that there are no pending issues or objections from our organization regarding the employee's future endeavors. The information provided herein is true and accurate to the best of our knowledge and belief.
        """
        story.append(Paragraph(noc_text_4, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Relieving Date', relieving_date],
            ['Notice Period', 'As per company policy'],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'No Objection Certificate'],
            ['Purpose', purpose],
            ['Status', 'Relieved Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()

    def generate_visa_support_letter(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional visa support letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("✈️ VISA SUPPORT LETTER ✈️", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-VISA-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        salary_amount = employee_info.get('salary_amount', '')
        purpose = employee_info.get('purpose', 'Business travel')
        
        # Main Certificate Text
        visa_text_1 = f"""
This is to certify that <b>{employee_name}</b>, bearing Employee ID <b>{employee_id}</b>, is currently employed with <b>Reliance Jio Infotech Solutions</b> as <b>{designation}</b> in the <b>{department}</b> department.
        """
        story.append(Paragraph(visa_text_1, self.normal_style))
        
        visa_text_2 = f"""
The employee has been associated with our organization since <b>{joining_date}</b> and is currently drawing a salary of <b>₹{salary_amount}</b> per month. The employee is a permanent employee of our organization and is required to travel for <b>{purpose}</b>.
        """
        story.append(Paragraph(visa_text_2, self.normal_style))
        
        visa_text_3 = f"""
We hereby confirm that the employee's travel is sponsored by our organization and all expenses related to the trip will be borne by Reliance Jio Infotech Solutions. The employee will return to India after completing the assigned work.
        """
        story.append(Paragraph(visa_text_3, self.normal_style))
        
        visa_text_4 = f"""
This visa support letter is issued for official purposes and confirms the employment status and travel sponsorship of the above-mentioned individual. The information provided herein is true and accurate to the best of our knowledge and belief.
        """
        story.append(Paragraph(visa_text_4, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Current Salary', f"₹{salary_amount}"],
            ['Employment Type', 'Permanent'],
            ['Travel Purpose', purpose],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'Visa Support Letter'],
            ['Status', 'Active Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()

    def generate_offer_letter(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional offer letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📄 OFFER LETTER 📄", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-OFF-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        salary_amount = employee_info.get('salary_amount', '')
        appointment_date = self._format_date(employee_info.get('appointment_date', ''))
        
        # Main Offer Letter Text
        offer_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(offer_text_1, self.salutation_style))
        
        offer_text_2 = f"""
We are pleased to offer you the position of <b>{designation}</b> in the <b>{department}</b> department at <b>Reliance Jio Infotech Solutions</b>. This offer is based on your qualifications, experience, and the interview process you have successfully completed.
        """
        story.append(Paragraph(offer_text_2, self.normal_style))
        
        offer_text_3 = f"""
<b>Position Details:</b><br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Appointment Date: {appointment_date}<br/>
• Salary: ₹{salary_amount} per month
        """
        story.append(Paragraph(offer_text_3, self.normal_style))
        
        offer_text_4 = f"""
<b>Terms and Conditions:</b><br/>
• This offer is valid for 30 days from the date of issue<br/>
• You will be on probation for the first 6 months<br/>
• Your employment will be subject to verification of documents and references<br/>
• You will be required to sign an employment agreement and NDA<br/>
• The company reserves the right to modify terms based on business requirements
        """
        story.append(Paragraph(offer_text_4, self.normal_style))
        
        offer_text_5 = f"""
Please confirm your acceptance of this offer by signing and returning a copy of this letter within 7 days. We look forward to welcoming you to the Reliance Jio Infotech Solutions team.
        """
        story.append(Paragraph(offer_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Appointment Date', appointment_date],
            ['Salary Offered', f"₹{salary_amount}"],
            ['Employment Type', 'Full-time'],
            ['Probation Period', '6 months'],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'Offer Letter'],
            ['Status', 'Pending Acceptance'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()

    def generate_appointment_letter(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional appointment letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📋 APPOINTMENT LETTER 📋", self.document_title_style))
        
        # Reference Number
        appointment_date = employee_info.get('appointment_date', datetime.now().strftime('%Y-%m-%d'))
        formatted_date = self._format_date(appointment_date)
        ref_number = f"Reference No: RJI-APT-{employee_info.get('employee_id', '')}-{appointment_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        appointment_date = self._format_date(employee_info.get('appointment_date', ''))
        salary_amount = employee_info.get('salary_amount', '')
        
        # Main Appointment Letter Text
        apt_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(apt_text_1, self.salutation_style))
        
        apt_text_2 = f"""
We are pleased to confirm your appointment as <b>{designation}</b> in the <b>{department}</b> department at <b>Reliance Jio Infotech Solutions</b> with effect from <b>{appointment_date}</b>.
        """
        story.append(Paragraph(apt_text_2, self.normal_style))
        
        apt_text_3 = f"""
<b>Appointment Details:</b><br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Appointment Date: {appointment_date}<br/>
• Salary: ₹{salary_amount} per month
        """
        story.append(Paragraph(apt_text_3, self.normal_style))
        
        apt_text_4 = f"""
<b>Terms of Employment:</b><br/>
• Your employment will be governed by the company's policies and procedures<br/>
• You will be on probation for the first 6 months from the date of joining<br/>
• Upon successful completion of probation, you will be confirmed in the position<br/>
• Your employment is subject to verification of all submitted documents<br/>
• You will be required to comply with all company rules and regulations
        """
        story.append(Paragraph(apt_text_4, self.normal_style))
        
        apt_text_5 = f"""
We welcome you to the Reliance Jio Infotech Solutions family and look forward to a long and mutually beneficial association. Please sign and return a copy of this appointment letter as confirmation of your acceptance.
        """
        story.append(Paragraph(apt_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Appointment Date', appointment_date],
            ['Salary', f"₹{salary_amount}"],
            ['Employment Type', 'Full-time'],
            ['Probation Period', '6 months'],
            ['Issue Date', formatted_date],
            ['Document Type', 'Appointment Letter'],
            ['Status', 'Active Employee'],
            ['Validity', 'Permanent Record']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()

    def generate_promotion_letter(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional promotion letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📄 PROMOTION LETTER 📄", self.document_title_style))
        
        # Reference Number
        promotion_date = employee_info.get('promotion_date', datetime.now().strftime('%Y-%m-%d'))
        formatted_date = self._format_date(promotion_date)
        ref_number = f"Reference No: RJI-PR-{employee_info.get('employee_id', '')}-{promotion_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        salary_amount = employee_info.get('salary_amount', '')
        promotion_date = self._format_date(employee_info.get('promotion_date', ''))
        
        # Promotion Letter Content
        promotion_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(promotion_text_1, self.salutation_style))
        
        promotion_text_2 = f"""
We are pleased to inform you that you have been promoted to the position of <b>{designation}</b> in the <b>{department}</b> department at <b>Reliance Jio Infotech Solutions</b> with effect from <b>{promotion_date}</b>.
        """
        story.append(Paragraph(promotion_text_2, self.normal_style))
        
        promotion_text_3 = f"""
This promotion is in recognition of your outstanding performance, dedication, and valuable contributions to our organization. Your hard work and commitment have been exemplary and we are confident that you will continue to excel in your new role.
        """
        story.append(Paragraph(promotion_text_3, self.normal_style))
        
        promotion_text_4 = f"""
<b>Promotion Details:</b><br/>
• New Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Promotion Date: {promotion_date}<br/>
• New Salary: ₹{salary_amount} per month
        """
        story.append(Paragraph(promotion_text_4, self.normal_style))
        
        promotion_text_5 = f"""
<b>Terms of Promotion:</b><br/>
• This promotion is effective from {promotion_date}<br/>
• You will be on probation for 6 months in the new position<br/>
• Your employment will be governed by the company's policies and procedures<br/>
• This promotion is subject to verification of all submitted documents<br/>
• You will be required to comply with all company rules and regulations
        """
        story.append(Paragraph(promotion_text_5, self.normal_style))
        
        promotion_text_6 = f"""
We congratulate you on this well-deserved promotion and look forward to your continued success in your new role. Please sign and return a copy of this promotion letter as confirmation of your acceptance.
        """
        story.append(Paragraph(promotion_text_6, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['New Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Promotion Date', promotion_date],
            ['New Salary', f"₹{salary_amount}"],
            ['Employment Type', 'Full-time'],
            ['Probation Period', '6 months'],
            ['Issue Date', formatted_date],
            ['Document Type', 'Promotion Letter'],
            ['Status', 'Active Employee'],
            ['Validity', 'Permanent Record']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_relieving_letter(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional relieving letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📄 RELIEVING LETTER 📄", self.document_title_style))
        
        # Reference Number
        relieving_date = employee_info.get('relieving_date', datetime.now().strftime('%Y-%m-%d'))
        formatted_date = self._format_date(relieving_date)
        ref_number = f"Reference No: RJI-RL-{employee_info.get('employee_id', '')}-{relieving_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        relieving_date = self._format_date(employee_info.get('relieving_date', ''))
        
        # Relieving Letter Content
        relieving_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(relieving_text_1, self.salutation_style))
        
        relieving_text_2 = f"""
This is to confirm that you have been relieved from your services with <b>Reliance Jio Infotech Solutions</b> with effect from <b>{relieving_date}</b> after completing all necessary formalities and handover procedures as per company policy.
        """
        story.append(Paragraph(relieving_text_2, self.normal_style))
        
        relieving_text_3 = f"""
We acknowledge your resignation and confirm that you have completed all required formalities including handover of responsibilities, return of company property, and clearance of all pending dues. Your exit formalities have been completed satisfactorily.
        """
        story.append(Paragraph(relieving_text_3, self.normal_style))
        
        relieving_text_4 = f"""
<b>Relieving Details:</b><br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Relieving Date: {relieving_date}<br/>
• Notice Period: As per company policy
        """
        story.append(Paragraph(relieving_text_4, self.normal_style))
        
        relieving_text_5 = f"""
<b>Clearance Status:</b><br/>
• All company property has been returned in good condition<br/>
• Handover of responsibilities has been completed<br/>
• All pending dues have been cleared<br/>
• Exit formalities have been completed satisfactorily<br/>
• No outstanding issues remain with the organization
        """
        story.append(Paragraph(relieving_text_5, self.normal_style))
        
        relieving_text_6 = f"""
We wish you success in your future endeavors and thank you for your contributions to our organization. This relieving letter is issued for official purposes and confirms your separation from Reliance Jio Infotech Solutions.
        """
        story.append(Paragraph(relieving_text_6, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Relieving Date', relieving_date],
            ['Notice Period', 'As per company policy'],
            ['Clearance Status', 'Completed'],
            ['Issue Date', formatted_date],
            ['Document Type', 'Relieving Letter'],
            ['Status', 'Relieved Employee'],
            ['Validity', 'Permanent Record']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_salary_slip(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional salary slip with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📋 SALARY SLIP 📋", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-SL-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        relieving_date = self._format_date(employee_info.get('relieving_date', ''))
        salary_amount = employee_info.get('salary_amount', '')
        
        # Salary Slip Content
        salary_slip_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(salary_slip_text_1, self.salutation_style))
        
        salary_slip_text_2 = f"""
This is to certify that you have been paid a salary of <b>₹{salary_amount}</b> for the month of <b>{formatted_issue_date.split('-')[1]}</b> from {self.company_name}. The salary has been credited to your registered bank account on the last working day of the month.
        """
        story.append(Paragraph(salary_slip_text_2, self.normal_style))
        
        salary_slip_text_3 = f"""
<b>Salary Details:</b><br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Relieving Date: {relieving_date}<br/>
• Salary Amount: ₹{salary_amount}<br/>
• Payment Mode: Bank Transfer<br/>
• Payment Date: {formatted_issue_date}
        """
        story.append(Paragraph(salary_slip_text_3, self.normal_style))
        
        salary_slip_text_4 = f"""
<b>Salary Breakdown:</b><br/>
• Basic Salary: ₹{int(float(salary_amount) * 0.5)}<br/>
• House Rent Allowance: ₹{int(float(salary_amount) * 0.2)}<br/>
• Special Allowance: ₹{int(float(salary_amount) * 0.3)}<br/>
• Total Gross Salary: ₹{salary_amount}<br/>
• Professional Tax: ₹200<br/>
• Net Salary Paid: ₹{int(float(salary_amount) - 200)}
        """
        story.append(Paragraph(salary_slip_text_4, self.normal_style))
        
        salary_slip_text_5 = f"""
<b>Important Notes:</b><br/>
• This salary slip is a proof of payment and should be kept in your personal records<br/>
• The salary is subject to applicable taxes and deductions as per Income Tax Act<br/>
• No salary will be paid after the relieving date<br/>
• All dues and pending formalities must be cleared by the employee on or before the relieving date<br/>
• This salary slip is valid for 30 days from the date of issue
        """
        story.append(Paragraph(salary_slip_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Relieving Date', relieving_date],
            ['Salary Month', formatted_issue_date.split('-')[1]],
            ['Gross Salary', f"₹{salary_amount}"],
            ['Net Salary', f"₹{int(float(salary_amount) - 200)}"],
            ['Payment Mode', 'Bank Transfer'],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'Salary Slip'],
            ['Status', 'Active Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_form_16(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional Form 16 with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📄 FORM 16 📄", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-F16-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        relieving_date = self._format_date(employee_info.get('relieving_date', ''))
        assessment_year = formatted_issue_date.split('-')[2]
        
        # Form 16 Content
        form_16_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(form_16_text_1, self.salutation_style))
        
        form_16_text_2 = f"""
This is to certify that you have been issued Form 16 for the assessment year <b>{assessment_year}</b> from <b>Reliance Jio Infotech Solutions</b>. This document contains details of your salary income and tax deducted at source (TDS) for the financial year {int(assessment_year)-1}-{assessment_year}.
        """
        story.append(Paragraph(form_16_text_2, self.normal_style))
        
        form_16_text_3 = f"""
<b>Form 16 Details:</b><br/>
• Assessment Year: {assessment_year}<br/>
• Financial Year: {int(assessment_year)-1}-{assessment_year}<br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Relieving Date: {relieving_date}
        """
        story.append(Paragraph(form_16_text_3, self.normal_style))
        
        form_16_text_4 = f"""
<b>Important Information:</b><br/>
• Form 16 is a mandatory document for income tax assessment<br/>
• It must be submitted to the Income Tax Department within 30 days of issuance<br/>
• This document contains details of your salary income and TDS<br/>
• Please verify all details before filing your income tax return<br/>
• Keep this document safely for future reference
        """
        story.append(Paragraph(form_16_text_4, self.normal_style))
        
        form_16_text_5 = f"""
<b>Terms and Conditions:</b><br/>
• Form 16 is issued as per Income Tax Act, 1961<br/>
• No Form 16 will be issued after the relieving date<br/>
• All dues and pending formalities must be cleared by the employee<br/>
• This Form 16 is valid for 30 days from the date of issue<br/>
• For any discrepancies, please contact the HR department immediately
        """
        story.append(Paragraph(form_16_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Relieving Date', relieving_date],
            ['Assessment Year', assessment_year],
            ['Financial Year', f"{int(assessment_year)-1}-{assessment_year}"],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'Form 16'],
            ['Status', 'Active Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_pf_statement(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional PF statement with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📋 PF STATEMENT 📋", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-PF-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        relieving_date = self._format_date(employee_info.get('relieving_date', ''))
        
        # PF Statement Content
        pf_statement_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(pf_statement_text_1, self.salutation_style))
        
        pf_statement_text_2 = f"""
This is to certify that you have been issued a Provident Fund (PF) Statement for the month of <b>{formatted_issue_date.split('-')[1]}</b> from <b>Reliance Jio Infotech Solutions</b>. This statement contains details of your PF contributions and account balance.
        """
        story.append(Paragraph(pf_statement_text_2, self.normal_style))
        
        pf_statement_text_3 = f"""
<b>PF Statement Details:</b><br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Relieving Date: {relieving_date}<br/>
• UAN Number: {employee_id}1234567890
        """
        story.append(Paragraph(pf_statement_text_3, self.normal_style))
        
        pf_statement_text_4 = f"""
<b>PF Account Information:</b><br/>
• PF Account Number: RJI{employee_id}PF<br/>
• Employee Contribution: 12% of Basic Salary<br/>
• Employer Contribution: 12% of Basic Salary<br/>
• Total Contribution: 24% of Basic Salary<br/>
• Interest Rate: As per EPFO guidelines
        """
        story.append(Paragraph(pf_statement_text_4, self.normal_style))
        
        pf_statement_text_5 = f"""
<b>Important Notes:</b><br/>
• PF Statement is a mandatory document for your Provident Fund account<br/>
• It must be submitted to the PF Department within 30 days of issuance<br/>
• No PF Statement will be issued after the relieving date<br/>
• All dues and pending formalities must be cleared by the employee<br/>
• This PF Statement is valid for 30 days from the date of issue
        """
        story.append(Paragraph(pf_statement_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Relieving Date', relieving_date],
            ['UAN Number', f"{employee_id}1234567890"],
            ['PF Account Number', f"RJI{employee_id}PF"],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'PF Statement'],
            ['Status', 'Active Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_nda_copy(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional NDA copy with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("📄 NON-DISCLOSURE AGREEMENT (NDA) COPY 📄", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-NDA-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        relieving_date = self._format_date(employee_info.get('relieving_date', ''))
        
        # NDA Copy Content
        nda_copy_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(nda_copy_text_1, self.salutation_style))
        
        nda_copy_text_2 = f"""
This is to certify that you have been issued a Non-Disclosure Agreement (NDA) copy for the assessment year <b>{formatted_issue_date.split('-')[2]}</b> from <b>Reliance Jio Infotech Solutions</b>. This document contains the terms and conditions of your confidentiality agreement.
        """
        story.append(Paragraph(nda_copy_text_2, self.normal_style))
        
        nda_copy_text_3 = f"""
<b>NDA Copy Details:</b><br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Employee ID: {employee_id}<br/>
• Joining Date: {joining_date}<br/>
• Relieving Date: {relieving_date}<br/>
• NDA Reference: RJI-NDA-{employee_id}
        """
        story.append(Paragraph(nda_copy_text_3, self.normal_style))
        
        nda_copy_text_4 = f"""
<b>NDA Terms and Conditions:</b><br/>
• You are bound by confidentiality obligations during and after employment<br/>
• You must not disclose any proprietary or confidential information<br/>
• This agreement remains in effect for 5 years after employment termination<br/>
• Violation may result in legal action and damages<br/>
• All intellectual property belongs to the company
        """
        story.append(Paragraph(nda_copy_text_4, self.normal_style))
        
        nda_copy_text_5 = f"""
<b>Important Notes:</b><br/>
• NDA Copy is a mandatory document for your employment records<br/>
• It must be kept safely for future reference<br/>
• No NDA Copy will be issued after the relieving date<br/>
• All terms and conditions remain binding<br/>
• This NDA Copy is valid for 30 days from the date of issue
        """
        story.append(Paragraph(nda_copy_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Relieving Date', relieving_date],
            ['NDA Reference', f"RJI-NDA-{employee_id}"],
            ['Validity Period', '5 years after employment'],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'NDA Copy'],
            ['Status', 'Active Employee'],
            ['Validity', '30 days from issue date']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_id_card_replacement(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional ID card replacement request with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("🆔 ID CARD REPLACEMENT REQUEST 🆔", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-ID-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        reason = employee_info.get('reason', 'Lost/Damaged')
        
        # ID Card Replacement Content
        id_replacement_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(id_replacement_text_1, self.salutation_style))
        
        id_replacement_text_2 = f"""
This is to confirm that your request for ID card replacement has been received and processed by <b>Reliance Jio Infotech Solutions</b>. Your new ID card will be issued within 3-5 working days.
        """
        story.append(Paragraph(id_replacement_text_2, self.normal_style))
        
        id_replacement_text_3 = f"""
<b>Replacement Details:</b><br/>
• Employee Name: {employee_name}<br/>
• Employee ID: {employee_id}<br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Reason for Replacement: {reason}<br/>
• Request Date: {formatted_issue_date}<br/>
• Expected Delivery: 3-5 working days
        """
        story.append(Paragraph(id_replacement_text_3, self.normal_style))
        
        id_replacement_text_4 = f"""
<b>Important Information:</b><br/>
• Please collect your new ID card from the HR department<br/>
• You will need to sign a receipt upon collection<br/>
• The old ID card (if found) should be returned immediately<br/>
• A replacement fee of ₹100 may be charged for lost cards<br/>
• Damaged cards can be replaced free of charge
        """
        story.append(Paragraph(id_replacement_text_4, self.normal_style))
        
        id_replacement_text_5 = f"""
<b>Security Guidelines:</b><br/>
• Keep your ID card safe and secure at all times<br/>
• Do not share your ID card with unauthorized persons<br/>
• Report any loss or theft immediately to security<br/>
• The ID card is company property and must be returned upon separation<br/>
• Unauthorized duplication is strictly prohibited
        """
        story.append(Paragraph(id_replacement_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Reason for Replacement', reason],
            ['Request Date', formatted_issue_date],
            ['Expected Delivery', '3-5 working days'],
            ['Replacement Fee', '₹100 (if lost)'],
            ['Document Type', 'ID Card Replacement Request'],
            ['Status', 'Processing'],
            ['Validity', 'Until new card is issued']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_medical_insurance_card(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional medical insurance card copy with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("🏥 MEDICAL INSURANCE CARD COPY 🏥", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-MED-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        
        # Medical Insurance Card Content
        med_card_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(med_card_text_1, self.salutation_style))
        
        med_card_text_2 = f"""
This is to certify that you have been issued a Medical Insurance Card copy from <b>Reliance Jio Infotech Solutions</b>. This document contains details of your medical insurance coverage and policy information.
        """
        story.append(Paragraph(med_card_text_2, self.normal_style))
        
        med_card_text_3 = f"""
<b>Medical Insurance Details:</b><br/>
• Employee Name: {employee_name}<br/>
• Employee ID: {employee_id}<br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Joining Date: {joining_date}<br/>
• Policy Number: RJI-MED-{employee_id}<br/>
• Insurance Provider: Reliance Health Insurance
        """
        story.append(Paragraph(med_card_text_3, self.normal_style))
        
        med_card_text_4 = f"""
<b>Coverage Details:</b><br/>
• Sum Insured: ₹5,00,000 per annum<br/>
• Coverage Type: Family Floater<br/>
• Network Hospitals: 5000+ across India<br/>
• Pre-existing Conditions: Covered after 48 months<br/>
• Maternity Coverage: ₹50,000<br/>
• Dental Coverage: ₹10,000
        """
        story.append(Paragraph(med_card_text_4, self.normal_style))
        
        med_card_text_5 = f"""
<b>Important Information:</b><br/>
• This card is valid for the current financial year<br/>
• Present this card at network hospitals for cashless treatment<br/>
• Keep this document safely for future reference<br/>
• For any claims, contact the insurance provider directly<br/>
• Coverage is subject to policy terms and conditions
        """
        story.append(Paragraph(med_card_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Policy Number', f"RJI-MED-{employee_id}"],
            ['Insurance Provider', 'Reliance Health Insurance'],
            ['Sum Insured', '₹5,00,000'],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'Medical Insurance Card Copy'],
            ['Status', 'Active Employee'],
            ['Validity', 'Current Financial Year']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_travel_authorization(self, doc_name: str, employee_info: Dict, details: str) -> bytes:
        """Generate professional business travel authorization letter with enhanced design"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1.2*inch, rightMargin=1.2*inch, 
                              topMargin=1.0*inch, bottomMargin=1.0*inch)
        
        story = []
        
        # Enhanced Company Header
        self._add_enhanced_company_header(story)
        
        # Document Title with Badge
        story.append(Paragraph("✈️ BUSINESS TRAVEL AUTHORIZATION LETTER ✈️", self.document_title_style))
        
        # Reference Number - Issue date should be current date when document is generated
        current_issue_date, formatted_issue_date = self._get_current_issue_date()
        ref_number = f"Reference No: RJI-TRAVEL-{employee_info.get('employee_id', '')}-{current_issue_date.replace('-', '')}"
        story.append(Paragraph(ref_number, self.reference_style))
        story.append(Spacer(1, 5))
        
        # Certificate Badge (text-based)
        self._add_certificate_badge_text(story)
        
        # Employee Details
        employee_name = employee_info.get('full_name', '')
        employee_id = employee_info.get('employee_id', '')  # Use actual employee ID from form
        designation = employee_info.get('designation', '')
        department = employee_info.get('department', '')
        joining_date = self._format_date(employee_info.get('joining_date', ''))
        destination = employee_info.get('destination', '')
        purpose = employee_info.get('purpose', '')
        duration = employee_info.get('duration', '')
        travel_date = self._format_date(employee_info.get('travel_date', ''))
        
        # Travel Authorization Content
        travel_auth_text_1 = f"""
Dear <b>{employee_name}</b>,
        """
        story.append(Paragraph(travel_auth_text_1, self.salutation_style))
        
        travel_auth_text_2 = f"""
This is to authorize your business travel to <b>{destination}</b> from <b>Reliance Jio Infotech Solutions</b>. This authorization letter confirms that your travel is sponsored by our organization for official business purposes.
        """
        story.append(Paragraph(travel_auth_text_2, self.normal_style))
        
        travel_auth_text_3 = f"""
<b>Travel Authorization Details:</b><br/>
• Employee Name: {employee_name}<br/>
• Employee ID: {employee_id}<br/>
• Designation: {designation}<br/>
• Department: {department}<br/>
• Destination: {destination}<br/>
• Purpose of Travel: {purpose}<br/>
• Duration: {duration}<br/>
• Travel Date: {travel_date}
        """
        story.append(Paragraph(travel_auth_text_3, self.normal_style))
        
        travel_auth_text_4 = f"""
<b>Travel Arrangements:</b><br/>
• All travel expenses will be borne by Reliance Jio Infotech Solutions<br/>
• Accommodation will be arranged by the company<br/>
• Daily allowance will be provided as per company policy<br/>
• Return travel will be arranged after completion of business<br/>
• Emergency contact: HR Department (+91-22-3555-5000)
        """
        story.append(Paragraph(travel_auth_text_4, self.normal_style))
        
        travel_auth_text_5 = f"""
<b>Important Guidelines:</b><br/>
• Please carry this authorization letter during travel<br/>
• Follow all company travel policies and procedures<br/>
• Submit expense reports within 7 days of return<br/>
• Maintain professional conduct throughout the trip<br/>
• Contact HR immediately in case of any issues
        """
        story.append(Paragraph(travel_auth_text_5, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Enhanced Employee Details Table
        employee_data = [
            ['Employee Name', employee_name],
            ['Employee ID', employee_id],
            ['Designation', designation],
            ['Department', department],
            ['Joining Date', joining_date],
            ['Destination', destination],
            ['Purpose', purpose],
            ['Duration', duration],
            ['Travel Date', travel_date],
            ['Issue Date', formatted_issue_date],
            ['Document Type', 'Business Travel Authorization'],
            ['Status', 'Authorized'],
            ['Validity', 'Until return from travel']
        ]
        
        employee_table = Table(employee_data, colWidths=[2.2*inch, 4.8*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Signature Section
        self._add_signature_section(story, "Rajesh Kumar", "HR Director")
        
        # Enhanced Footer
        self._add_enhanced_footer(story)
        
        # Build PDF with enhanced border
        doc.build(story, onFirstPage=self.add_enhanced_border_and_watermark, onLaterPages=self.add_enhanced_border_and_watermark)
        
        buffer.seek(0)
        return buffer.getvalue()
