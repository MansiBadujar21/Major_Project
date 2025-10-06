from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import os
from datetime import datetime
import base64
from PIL import Image as PILImage
import io


def get_company_logo():
    """Generate a professional company logo using ReportLab"""
    # Create a simple but professional logo using shapes and text
    logo_data = io.BytesIO()
    c = canvas.Canvas(logo_data, pagesize=(2*inch, 1*inch))
    
    # Draw logo background
    c.setFillColor(colors.HexColor('#1e40af'))
    c.rect(0, 0, 2*inch, 1*inch, fill=1)
    
    # Add company name
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(1*inch, 0.6*inch, "RELIANCE")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(1*inch, 0.4*inch, "JIO")
    
    # Add tech icon
    c.setFillColor(colors.HexColor('#3b82f6'))
    c.circle(0.3*inch, 0.5*inch, 0.15*inch, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(0.3*inch, 0.5*inch, "AI")
    
    c.save()
    logo_data.seek(0)
    return logo_data


def get_digital_signature(signer_name: str, designation: str):
    """Generate a professional digital signature"""
    sig_data = io.BytesIO()
    c = canvas.Canvas(sig_data, pagesize=(2.5*inch, 1.5*inch))
    
    # Signature line
    c.setStrokeColor(colors.HexColor('#1e40af'))
    c.setLineWidth(2)
    c.line(0.2*inch, 0.8*inch, 2.3*inch, 0.8*inch)
    
    # Signer name
    c.setFillColor(colors.HexColor('#1e40af'))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(1.25*inch, 0.6*inch, signer_name)
    
    # Designation
    c.setFont("Helvetica", 10)
    c.drawCentredString(1.25*inch, 0.4*inch, designation)
    
    # Digital signature indicator
    c.setFillColor(colors.HexColor('#10b981'))
    c.circle(0.2*inch, 0.2*inch, 0.08*inch, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(0.2*inch, 0.2*inch, "DS")
    
    # Date
    c.setFillColor(colors.HexColor('#6b7280'))
    c.setFont("Helvetica", 8)
    c.drawCentredString(1.25*inch, 0.15*inch, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    
    c.save()
    sig_data.seek(0)
    return sig_data


def get_security_watermark():
    """Generate a security watermark"""
    watermark_data = io.BytesIO()
    c = canvas.Canvas(watermark_data, pagesize=(1*inch, 1*inch))
    
    # Security icon
    c.setFillColor(colors.HexColor('#f8fafc'))
    c.setStrokeColor(colors.HexColor('#1e40af'))
    c.setLineWidth(1)
    
    # Shield shape (simplified as rectangle)
    c.rect(0.2*inch, 0.4*inch, 0.6*inch, 0.5*inch, fill=1)
    
    # Lock icon
    c.setFillColor(colors.HexColor('#1e40af'))
    c.rect(0.35*inch, 0.5*inch, 0.3*inch, 0.2*inch, fill=1)
    c.circle(0.5*inch, 0.6*inch, 0.1*inch, fill=1)
    
    c.save()
    watermark_data.seek(0)
    return watermark_data


def get_qr_code(certificate_id: str):
    """Generate a simple QR code representation using ReportLab"""
    qr_data = io.BytesIO()
    c = canvas.Canvas(qr_data, pagesize=(1.2*inch, 1.2*inch))
    
    # QR code background
    c.setFillColor(colors.white)
    c.rect(0, 0, 1.2*inch, 1.2*inch, fill=1)
    
    # QR code pattern (simplified representation)
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    
    # Draw QR code pattern
    for i in range(0, 12, 2):
        for j in range(0, 12, 2):
            if (i + j) % 4 == 0:
                c.rect(i*0.1*inch, j*0.1*inch, 0.1*inch, 0.1*inch, fill=1)
    
    # Add certificate ID
    c.setFillColor(colors.HexColor('#1e40af'))
    c.setFont("Helvetica", 6)
    c.drawCentredString(0.6*inch, 0.1*inch, certificate_id[:10])
    
    c.save()
    qr_data.seek(0)
    return qr_data


def get_certificate_badge():
    """Generate a certificate badge/medal"""
    badge_data = io.BytesIO()
    c = canvas.Canvas(badge_data, pagesize=(1.5*inch, 1.5*inch))
    
    # Badge background
    c.setFillColor(colors.HexColor('#fbbf24'))
    c.circle(0.75*inch, 0.75*inch, 0.7*inch, fill=1)
    
    # Inner circle
    c.setFillColor(colors.white)
    c.circle(0.75*inch, 0.75*inch, 0.5*inch, fill=1)
    
    # Certificate icon
    c.setFillColor(colors.HexColor('#1e40af'))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(0.75*inch, 0.8*inch, "📜")
    
    # Text
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(0.75*inch, 0.6*inch, "CERTIFICATE")
    c.setFont("Helvetica", 6)
    c.drawCentredString(0.75*inch, 0.4*inch, "OFFICIAL")
    
    c.save()
    badge_data.seek(0)
    return badge_data


def generate_bonafide_pdf(employee: dict, organization_name: str) -> bytes:
    """Generate a professionally designed bonafide certificate with enhanced formatting"""
    buffer = BytesIO()
    
    # Use proper margins for professional documents (following template rules)
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        leftMargin=1.2*inch, 
        rightMargin=1.2*inch,
        topMargin=1.0*inch, 
        bottomMargin=1.0*inch
    )
    width, height = A4

    # Create story (content) for the document
    story = []
    styles = getSampleStyleSheet()
    
    # Enhanced border and watermark function with company logos and security elements
    def add_enhanced_border_and_watermark(canvas, doc):
        canvas.saveState()
        
        # Draw professional border with company colors
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        canvas.setLineWidth(3)
        canvas.rect(0.2*inch, 0.2*inch, width-0.4*inch, height-0.4*inch)
        
        # Add inner decorative border
        canvas.setStrokeColor(colors.HexColor('#3b82f6'))
        canvas.setLineWidth(1.5)
        canvas.rect(0.4*inch, 0.4*inch, width-0.8*inch, height-0.8*inch)
        
        # Add corner decorations with company branding
        corner_length = 0.6*inch
        canvas.setLineWidth(2)
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        
        # Top-left corner with logo
        canvas.line(0.4*inch, height-0.4*inch, 0.4*inch, height-0.4*inch-corner_length)
        canvas.line(0.4*inch, height-0.4*inch, 0.4*inch+corner_length, height-0.4*inch)
        
        # Top-right corner
        canvas.line(width-0.4*inch, height-0.4*inch, width-0.4*inch, height-0.4*inch-corner_length)
        canvas.line(width-0.4*inch, height-0.4*inch, width-0.4*inch-corner_length, height-0.4*inch)
        
        # Bottom-left corner
        canvas.line(0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch+corner_length)
        canvas.line(0.4*inch, 0.4*inch, 0.4*inch+corner_length, 0.4*inch)
        
        # Bottom-right corner with security icon
        canvas.line(width-0.4*inch, 0.4*inch, width-0.4*inch, 0.4*inch+corner_length)
        canvas.line(width-0.4*inch, 0.4*inch, width-0.4*inch-corner_length, 0.4*inch)
        
        # Add company logo in top-left corner (drawn directly)
        canvas.saveState()
        canvas.setFillColor(colors.HexColor('#1e40af'))
        canvas.rect(0.6*inch, height-1.2*inch, 1.5*inch, 0.75*inch, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawCentredString(1.35*inch, height-1.0*inch, "RELIANCE")
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawCentredString(1.35*inch, height-1.15*inch, "JIO")
        canvas.setFillColor(colors.HexColor('#3b82f6'))
        canvas.circle(0.9*inch, height-1.05*inch, 0.1*inch, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 6)
        canvas.drawCentredString(0.9*inch, height-1.05*inch, "AI")
        canvas.restoreState()
        
        # Add security watermark in bottom-right (drawn directly)
        canvas.saveState()
        canvas.setFillColor(colors.HexColor('#f8fafc'))
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        canvas.setLineWidth(1)
        # Shield shape (simplified as rectangle)
        canvas.rect(width-1.0*inch, 0.6*inch, 0.4*inch, 0.6*inch, fill=1)
        # Lock icon
        canvas.setFillColor(colors.HexColor('#1e40af'))
        canvas.rect(width-1.05*inch, 0.8*inch, 0.3*inch, 0.2*inch, fill=1)
        canvas.circle(width-0.9*inch, 0.9*inch, 0.1*inch, fill=1)
        canvas.restoreState()
        
        # Add subtle background watermark
        canvas.setFont("Helvetica", 60)
        canvas.setFillColor(colors.HexColor('#f8fafc'))
        canvas.rotate(45)
        canvas.drawCentredString(width/2, height/2, "RELIANCE JIO")
        canvas.rotate(-45)
        
        # Add certificate badge in top-right corner
        canvas.saveState()
        canvas.setFillColor(colors.HexColor('#fbbf24'))
        canvas.circle(width-1.2*inch, height-1.2*inch, 0.4*inch, fill=1)
        canvas.setFillColor(colors.white)
        canvas.circle(width-1.2*inch, height-1.2*inch, 0.3*inch, fill=1)
        canvas.setFillColor(colors.HexColor('#1e40af'))
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawCentredString(width-1.2*inch, height-1.1*inch, "📜")
        canvas.setFont("Helvetica-Bold", 6)
        canvas.drawCentredString(width-1.2*inch, height-1.25*inch, "CERTIFICATE")
        canvas.setFont("Helvetica", 5)
        canvas.drawCentredString(width-1.2*inch, height-1.35*inch, "OFFICIAL")
        canvas.restoreState()
    
        # Add QR code in bottom-left corner
        canvas.saveState()
        canvas.setFillColor(colors.white)
        canvas.rect(0.6*inch, 0.6*inch, 1*inch, 1*inch, fill=1)
        canvas.setFillColor(colors.black)
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.5)
        # Draw QR code pattern
        for i in range(0, 10, 2):
            for j in range(0, 10, 2):
                if (i + j) % 4 == 0:
                    canvas.rect(0.7*inch + i*0.08*inch, 0.7*inch + j*0.08*inch, 0.08*inch, 0.08*inch, fill=1)
        canvas.setFillColor(colors.HexColor('#1e40af'))
        canvas.setFont("Helvetica", 4)
        canvas.drawCentredString(1.1*inch, 0.65*inch, f"RJI-{employee['employee_code']}")
        canvas.restoreState()
        
        # Add certificate number watermark
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor('#e5e7eb'))
        canvas.drawString(0.5*inch, 0.3*inch, f"Certificate ID: RJI-{employee['employee_code']}-{datetime.now().strftime('%Y%m%d')}")
        
        canvas.restoreState()
    
    # Enhanced custom styles with proper spacing and fonts (following template rules)
    company_header_style = ParagraphStyle(
        'CompanyHeader',
        parent=styles['Normal'],
        fontSize=22,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=26,
        spaceBefore=0
    )
    
    company_subtitle_style = ParagraphStyle(
        'CompanySubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=14,
        spaceBefore=0
    )
    
    company_details_style = ParagraphStyle(
        'CompanyDetails',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica',
        leading=12,
        spaceBefore=0
    )
    
    certificate_title_style = ParagraphStyle(
        'CertificateTitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=15,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        leading=22
    )
    
    certificate_number_style = ParagraphStyle(
        'CertificateNumber',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_RIGHT,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,  # Following template rules
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        fontName='Times-Roman',  # Following template rules
        leading=16,
        firstLineIndent=0,
        spaceBefore=0
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    signature_details_style = ParagraphStyle(
        'SignatureDetails',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica',
        leading=11,
        spaceBefore=0
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=11,
        spaceBefore=0
    )
    
    # Enhanced Company Header with professional styling and icons
    story.append(Paragraph("🏢 RELIANCE JIO INFOTECH SOLUTIONS", company_header_style))
    story.append(Paragraph("A Subsidiary of Reliance Industries Limited", company_subtitle_style))
    story.append(Paragraph("📍 Registered Office: Maker Chambers IV, Nariman Point, Mumbai - 400021", company_details_style))
    story.append(Paragraph("📋 CIN: L17110MH2007PLC169642 | GST: 27AABCR0000A1Z5", company_details_style))
    story.append(Paragraph("📞 Phone: +91-22-3555-5000 | 📧 Email: hr@reliancejio.com", company_details_style))
    story.append(Paragraph("🌐 Website: www.reliancejio.com", company_details_style))
    story.append(Spacer(1, 15))
    
    # Certificate Badge and Title with enhanced styling
    story.append(Paragraph("🏆 EMPLOYEE BONAFIDE CERTIFICATE 🏆", certificate_title_style))
    
    # Certificate Number with proper formatting
    issue_date = employee.get('issue_date', datetime.now().strftime('%Y-%m-%d'))
    # Convert date to DD-MM-YYYY format (following template rules)
    try:
        date_obj = datetime.strptime(issue_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
    except:
        formatted_date = issue_date
    
    cert_number = f"Certificate No: RJI-{employee['employee_code']}-{issue_date.replace('-', '')}"
    story.append(Paragraph(cert_number, certificate_number_style))
    
    # Add certificate badge (drawn directly in the border function)
    story.append(Spacer(1, 5))
    
    # Main Certificate Text with proper spacing and formatting
    story.append(Spacer(1, 12))
    
    # First paragraph with proper justification and spacing (fixed spacing issues)
    cert_text_1 = f"""
    This is to certify that <b>{employee['full_name']}</b>, bearing Employee ID <b>{employee['employee_code']}</b>, is currently employed with <b>Reliance Jio Infotech Solutions</b> as <b>{employee['designation']}</b> in the <b>{employee['department']}</b> department.
    """
    story.append(Paragraph(cert_text_1, body_style))
    
    # Second paragraph with proper spacing (fixed spacing issues)
    cert_text_2 = f"""
    The employee has been associated with our organization since <b>{employee['joining_date']}</b> and continues to be in active service as of the date of issuance of this certificate.
    """
    story.append(Paragraph(cert_text_2, body_style))
    
    # Additional certification text (fixed spacing issues)
    additional_text = """
    This certificate is issued for official purposes and confirms the employment status of the above-mentioned individual with our organization. The information provided herein is true and accurate to the best of our knowledge and belief.
    """
    story.append(Paragraph(additional_text, body_style))
    story.append(Spacer(1, 15))
    
    # Enhanced Employee Details Table with better formatting
    employee_data = [
        ['Employee Name', employee['full_name']],
        ['Employee ID', employee['employee_code']],
        ['Designation', employee['designation']],
        ['Department', employee['department']],
        ['Joining Date', employee['joining_date']],
        ['Issue Date', formatted_date],
        ['Certificate Type', 'Employment Verification'],
        ['Status', 'Active Employee']
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
    
    # Enhanced Signature Section with Digital Signatures
    signature_text = "✍️ Authorized Digital Signatures:"
    story.append(Paragraph(signature_text, signature_style))
    story.append(Spacer(1, 10))
    
    # Create digital signatures
    hr_signature = get_digital_signature("Priya Sharma", "Senior HR Manager")
    dept_signature = get_digital_signature("Rajesh Kumar", "Department Manager")
    dir_signature = get_digital_signature("Amit Patel", "Director Operations")
    
    # Signature table with digital signatures
    signature_data = [
        ['HR Manager', 'Department Head', 'Authorized Signatory'],
        ['', '', ''],  # Space for digital signatures
        ['Priya Sharma', 'Rajesh Kumar', 'Amit Patel'],
        ['Senior HR Manager', 'Department Manager', 'Director Operations'],
        ['Employee ID: HR001', 'Employee ID: DM001', 'Employee ID: DIR001'],
        [f'Date: {formatted_date}', f'Date: {formatted_date}', f'Date: {formatted_date}'],
        ['🔒 Digitally Signed', '🔒 Digitally Signed', '🔒 Digitally Signed']
    ]
    
    signature_table = Table(signature_data, colWidths=[2.0*inch, 2.0*inch, 2.0*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 6), (-1, 6), colors.white),
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
    ]))
    
    story.append(signature_table)
    story.append(Spacer(1, 15))
    
    # Enhanced Footer with security features and verification details
    footer_text = """
    <b>🔒 Security & Verification Information:</b><br/>
    • This certificate is computer-generated and bears digital signatures<br/>
    • Certificate ID: RJI-{employee['employee_code']}-{datetime.now().strftime('%Y%m%d')}<br/>
    • For verification, please contact: hr@reliancejio.com<br/>
    • Certificate validity: 6 months from date of issue<br/>
    • This document is confidential and should be handled with care<br/>
    • For any queries, call: +91-22-3555-5000<br/>
    • 🔒 Blockchain Verified | 📱 QR Code: Scan for verification
    """
    story.append(Paragraph(footer_text, footer_style))
    
    # Add QR code for verification (drawn directly in the border function)
    story.append(Spacer(1, 5))
    
    # Build the PDF with enhanced border and watermark
    doc.build(story, onFirstPage=add_enhanced_border_and_watermark)
    return buffer.getvalue()


def generate_experience_certificate(employee: dict, organization_name: str) -> bytes:
    """Generate a professionally designed experience certificate"""
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        leftMargin=1.2*inch, 
        rightMargin=1.2*inch,
        topMargin=1.0*inch, 
        bottomMargin=1.0*inch
    )
    width, height = A4

    story = []
    styles = getSampleStyleSheet()
    
    # Reuse the same border function
    def add_enhanced_border_and_watermark(canvas, doc):
        canvas.saveState()
        
        # Draw professional border
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        canvas.setLineWidth(2.5)
        canvas.rect(0.3*inch, 0.3*inch, width-0.6*inch, height-0.6*inch)
        
        # Add inner decorative border
        canvas.setStrokeColor(colors.HexColor('#3b82f6'))
        canvas.setLineWidth(1)
        canvas.rect(0.5*inch, 0.5*inch, width-1.0*inch, height-1.0*inch)
        
        # Add corner decorations
        corner_length = 0.4*inch
        canvas.setLineWidth(1.5)
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        
        # Top-left corner
        canvas.line(0.5*inch, height-0.5*inch, 0.5*inch, height-0.5*inch-corner_length)
        canvas.line(0.5*inch, height-0.5*inch, 0.5*inch+corner_length, height-0.5*inch)
        
        # Top-right corner
        canvas.line(width-0.5*inch, height-0.5*inch, width-0.5*inch, height-0.5*inch-corner_length)
        canvas.line(width-0.5*inch, height-0.5*inch, width-0.5*inch-corner_length, height-0.5*inch)
        
        # Bottom-left corner
        canvas.line(0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch+corner_length)
        canvas.line(0.5*inch, 0.5*inch, 0.5*inch+corner_length, 0.5*inch)
        
        # Bottom-right corner
        canvas.line(width-0.5*inch, 0.5*inch, width-0.5*inch, 0.5*inch+corner_length)
        canvas.line(width-0.5*inch, 0.5*inch, width-0.5*inch-corner_length, 0.5*inch)
        
        # Add subtle watermark
        canvas.setFont("Helvetica", 48)
        canvas.setFillColor(colors.HexColor('#f8fafc'))
        canvas.rotate(45)
        canvas.drawCentredString(width/2, height/2, "RELIANCE JIO")
        canvas.rotate(-45)
        
        canvas.restoreState()
    
    # Enhanced styles for experience certificate (following template rules)
    company_header_style = ParagraphStyle(
        'CompanyHeader',
        parent=styles['Normal'],
        fontSize=22,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=26,
        spaceBefore=0
    )
    
    company_subtitle_style = ParagraphStyle(
        'CompanySubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=14,
        spaceBefore=0
    )
    
    company_details_style = ParagraphStyle(
        'CompanyDetails',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica',
        leading=12,
        spaceBefore=0
    )
    
    certificate_title_style = ParagraphStyle(
        'CertificateTitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=15,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        leading=22
    )
    
    certificate_number_style = ParagraphStyle(
        'CertificateNumber',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_RIGHT,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,  # Following template rules
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        fontName='Times-Roman',  # Following template rules
        leading=16,
        firstLineIndent=0,
        spaceBefore=0
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    signature_details_style = ParagraphStyle(
        'SignatureDetails',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica',
        leading=11,
        spaceBefore=0
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=11,
        spaceBefore=0
    )
    
    # Company Header
    story.append(Paragraph("🏢", company_header_style))
    story.append(Paragraph("RELIANCE JIO INFOTECH SOLUTIONS", company_header_style))
    story.append(Paragraph("A Subsidiary of Reliance Industries Limited", company_subtitle_style))
    story.append(Paragraph("Registered Office: Maker Chambers IV, Nariman Point, Mumbai - 400021", company_details_style))
    story.append(Paragraph("CIN: L17110MH2007PLC169642 | GST: 27AABCR0000A1Z5", company_details_style))
    story.append(Paragraph("Phone: +91-22-3555-5000 | Email: hr@reliancejio.com", company_details_style))
    story.append(Spacer(1, 15))
    
    # Certificate Title
    story.append(Paragraph("EXPERIENCE CERTIFICATE", certificate_title_style))
    
    # Certificate Number
    issue_date = employee.get('issue_date', datetime.now().strftime('%Y-%m-%d'))
    try:
        date_obj = datetime.strptime(issue_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
    except:
        formatted_date = issue_date
    
    cert_number = f"Certificate No: RJI-EXP-{employee['employee_code']}-{issue_date.replace('-', '')}"
    story.append(Paragraph(cert_number, certificate_number_style))
    
    # Main Certificate Text
    story.append(Spacer(1, 12))
    
    # Experience certificate text (fixed spacing issues)
    relieving_date = employee.get('relievingDate', 'Current')
    purpose = employee.get('purpose', 'General purpose')
    
    cert_text_1 = f"""
    This is to certify that <b>{employee['full_name']}</b>, bearing Employee ID <b>{employee['employee_code']}</b>, was employed with <b>Reliance Jio Infotech Solutions</b> as <b>{employee['designation']}</b> in the <b>{employee['department']}</b> department.
    """
    story.append(Paragraph(cert_text_1, body_style))
    
    cert_text_2 = f"""
    The employee was associated with our organization from <b>{employee['joining_date']}</b> to <b>{relieving_date}</b> and has completed their tenure with us.
    """
    story.append(Paragraph(cert_text_2, body_style))
    
    additional_text = f"""
    During their tenure, {employee['full_name']} demonstrated professional competence and contributed significantly to the organization. This certificate is issued for {purpose} and confirms the employment details as stated above.
    """
    story.append(Paragraph(additional_text, body_style))
    story.append(Spacer(1, 15))
    
    # Employee Details Table
    employee_data = [
        ['Employee Name', employee['full_name']],
        ['Employee ID', employee['employee_code']],
        ['Designation', employee['designation']],
        ['Department', employee['department']],
        ['Joining Date', employee['joining_date']],
        ['Relieving Date', relieving_date],
        ['Certificate Type', 'Experience Certificate'],
        ['Purpose', purpose]
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
    
    # Signature Section
    signature_text = "Authorized Signatories:"
    story.append(Paragraph(signature_text, signature_style))
    story.append(Spacer(1, 10))
    
    signature_data = [
        ['HR Manager', 'Department Head', 'Authorized Signatory'],
        ['', '', ''],  # Space for signatures
        ['Priya Sharma', 'Rajesh Kumar', 'Amit Patel'],
        ['Senior HR Manager', 'Department Manager', 'Director Operations'],
        ['Employee ID: HR001', 'Employee ID: DM001', 'Employee ID: DIR001'],
        [f'Date: {formatted_date}', f'Date: {formatted_date}', f'Date: {formatted_date}']
    ]
    
    signature_table = Table(signature_data, colWidths=[2.0*inch, 2.0*inch, 2.0*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
    ]))
    
    story.append(signature_table)
    story.append(Spacer(1, 15))
    
    # Footer
    footer_text = """
    <b>Important Notes:</b><br/>
    • This certificate is computer-generated and bears digital signatures<br/>
    • For verification, please contact: hr@reliancejio.com<br/>
    • Certificate validity: 6 months from date of issue<br/>
    • This document is confidential and should be handled with care<br/>
    • For any queries, call: +91-22-3555-5000
    """
    story.append(Paragraph(footer_text, footer_style))
    
    # Build the PDF
    doc.build(story, onFirstPage=add_enhanced_border_and_watermark)
    return buffer.getvalue()


def generate_offer_letter(employee: dict, organization_name: str) -> bytes:
    """Generate a professionally designed offer letter"""
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        leftMargin=1.2*inch, 
        rightMargin=1.2*inch,
        topMargin=1.0*inch, 
        bottomMargin=1.0*inch
    )
    width, height = A4

    story = []
    styles = getSampleStyleSheet()
    
    # Reuse the same border function
    def add_enhanced_border_and_watermark(canvas, doc):
        canvas.saveState()
        
        # Draw professional border
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        canvas.setLineWidth(2.5)
        canvas.rect(0.3*inch, 0.3*inch, width-0.6*inch, height-0.6*inch)
        
        # Add inner decorative border
        canvas.setStrokeColor(colors.HexColor('#3b82f6'))
        canvas.setLineWidth(1)
        canvas.rect(0.5*inch, 0.5*inch, width-1.0*inch, height-1.0*inch)
        
        # Add corner decorations
        corner_length = 0.4*inch
        canvas.setLineWidth(1.5)
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        
        # Top-left corner
        canvas.line(0.5*inch, height-0.5*inch, 0.5*inch, height-0.5*inch-corner_length)
        canvas.line(0.5*inch, height-0.5*inch, 0.5*inch+corner_length, height-0.5*inch)
        
        # Top-right corner
        canvas.line(width-0.5*inch, height-0.5*inch, width-0.5*inch, height-0.5*inch-corner_length)
        canvas.line(width-0.5*inch, height-0.5*inch, width-0.5*inch-corner_length, height-0.5*inch)
        
        # Bottom-left corner
        canvas.line(0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch+corner_length)
        canvas.line(0.5*inch, 0.5*inch, 0.5*inch+corner_length, 0.5*inch)
        
        # Bottom-right corner
        canvas.line(width-0.5*inch, 0.5*inch, width-0.5*inch, 0.5*inch+corner_length)
        canvas.line(width-0.5*inch, 0.5*inch, width-0.5*inch-corner_length, 0.5*inch)
        
        # Add subtle watermark
        canvas.setFont("Helvetica", 48)
        canvas.setFillColor(colors.HexColor('#f8fafc'))
        canvas.rotate(45)
        canvas.drawCentredString(width/2, height/2, "RELIANCE JIO")
        canvas.rotate(-45)
        
        canvas.restoreState()
    
    # Enhanced styles for offer letter
    company_header_style = ParagraphStyle(
        'CompanyHeader',
        parent=styles['Normal'],
        fontSize=22,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=26,
        spaceBefore=0
    )
    
    company_subtitle_style = ParagraphStyle(
        'CompanySubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=14,
        spaceBefore=0
    )
    
    company_details_style = ParagraphStyle(
        'CompanyDetails',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica',
        leading=12,
        spaceBefore=0
    )
    
    document_title_style = ParagraphStyle(
        'DocumentTitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=15,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        leading=22
    )
    
    document_number_style = ParagraphStyle(
        'DocumentNumber',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_RIGHT,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        fontName='Times-Roman',
        leading=16,
        firstLineIndent=0,
        spaceBefore=0
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=11,
        spaceBefore=0
    )
    
    # Company Header
    story.append(Paragraph("🏢", company_header_style))
    story.append(Paragraph("RELIANCE JIO INFOTECH SOLUTIONS", company_header_style))
    story.append(Paragraph("A Subsidiary of Reliance Industries Limited", company_subtitle_style))
    story.append(Paragraph("Registered Office: Maker Chambers IV, Nariman Point, Mumbai - 400021", company_details_style))
    story.append(Paragraph("CIN: L17110MH2007PLC169642 | GST: 27AABCR0000A1Z5", company_details_style))
    story.append(Paragraph("Phone: +91-22-3555-5000 | Email: hr@reliancejio.com", company_details_style))
    story.append(Spacer(1, 15))
    
    # Document Title
    story.append(Paragraph("OFFER LETTER", document_title_style))
    
    # Document Number
    issue_date = employee.get('issue_date', datetime.now().strftime('%Y-%m-%d'))
    try:
        date_obj = datetime.strptime(issue_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
    except:
        formatted_date = issue_date
    
    doc_number = f"Offer Letter No: RJI-OFF-{employee['employee_code']}-{issue_date.replace('-', '')}"
    story.append(Paragraph(doc_number, document_number_style))
    
    # Main Document Text
    story.append(Spacer(1, 12))
    
    # Offer letter content
    offer_text_1 = f"""
    Dear <b>{employee['full_name']}</b>,
    """
    story.append(Paragraph(offer_text_1, body_style))
    
    offer_text_2 = f"""
    We are pleased to offer you the position of <b>{employee['designation']}</b> in the <b>{employee['department']}</b> department at Reliance Jio Infotech Solutions, effective from <b>{employee['joining_date']}</b>.
    """
    story.append(Paragraph(offer_text_2, body_style))
    
    offer_text_3 = f"""
    This offer is subject to the terms and conditions outlined in your employment agreement and our company policies. We look forward to welcoming you to our team and working together to achieve our organizational goals.
    """
    story.append(Paragraph(offer_text_3, body_style))
    
    story.append(Spacer(1, 15))
    
    # Employee Details Table
    employee_data = [
        ['Employee Name', employee['full_name']],
        ['Employee ID', employee['employee_code']],
        ['Designation', employee['designation']],
        ['Department', employee['department']],
        ['Joining Date', employee['joining_date']],
        ['Issue Date', formatted_date],
        ['Document Type', 'Offer Letter'],
        ['Status', 'Active Offer']
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
    
    # Signature Section
    signature_text = "Authorized Signatories:"
    story.append(Paragraph(signature_text, signature_style))
    story.append(Spacer(1, 10))
    
    signature_data = [
        ['HR Manager', 'Department Head', 'Authorized Signatory'],
        ['', '', ''],  # Space for signatures
        ['Priya Sharma', 'Rajesh Kumar', 'Amit Patel'],
        ['Senior HR Manager', 'Department Manager', 'Director Operations'],
        ['Employee ID: HR001', 'Employee ID: DM001', 'Employee ID: DIR001'],
        [f'Date: {formatted_date}', f'Date: {formatted_date}', f'Date: {formatted_date}']
    ]
    
    signature_table = Table(signature_data, colWidths=[2.0*inch, 2.0*inch, 2.0*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
    ]))
    
    story.append(signature_table)
    story.append(Spacer(1, 15))
    
    # Footer
    footer_text = """
    <b>Important Notes:</b><br/>
    • This offer letter is computer-generated and bears digital signatures<br/>
    • For verification, please contact: hr@reliancejio.com<br/>
    • Offer validity: 30 days from date of issue<br/>
    • This document is confidential and should be handled with care<br/>
    • For any queries, call: +91-22-3555-5000
    """
    story.append(Paragraph(footer_text, footer_style))
    
    # Build the PDF
    doc.build(story, onFirstPage=add_enhanced_border_and_watermark)
    return buffer.getvalue()


def generate_salary_certificate(employee: dict, organization_name: str) -> bytes:
    """Generate a professionally designed salary certificate"""
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        leftMargin=1.2*inch, 
        rightMargin=1.2*inch,
        topMargin=1.0*inch, 
        bottomMargin=1.0*inch
    )
    width, height = A4

    story = []
    styles = getSampleStyleSheet()
    
    # Reuse the same border function
    def add_enhanced_border_and_watermark(canvas, doc):
        canvas.saveState()
        
        # Draw professional border
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        canvas.setLineWidth(2.5)
        canvas.rect(0.3*inch, 0.3*inch, width-0.6*inch, height-0.6*inch)
        
        # Add inner decorative border
        canvas.setStrokeColor(colors.HexColor('#3b82f6'))
        canvas.setLineWidth(1)
        canvas.rect(0.5*inch, 0.5*inch, width-1.0*inch, height-1.0*inch)
        
        # Add corner decorations
        corner_length = 0.4*inch
        canvas.setLineWidth(1.5)
        canvas.setStrokeColor(colors.HexColor('#1e40af'))
        
        # Top-left corner
        canvas.line(0.5*inch, height-0.5*inch, 0.5*inch, height-0.5*inch-corner_length)
        canvas.line(0.5*inch, height-0.5*inch, 0.5*inch+corner_length, height-0.5*inch)
        
        # Top-right corner
        canvas.line(width-0.5*inch, height-0.5*inch, width-0.5*inch, height-0.5*inch-corner_length)
        canvas.line(width-0.5*inch, height-0.5*inch, width-0.5*inch-corner_length, height-0.5*inch)
        
        # Bottom-left corner
        canvas.line(0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch+corner_length)
        canvas.line(0.5*inch, 0.5*inch, 0.5*inch+corner_length, 0.5*inch)
        
        # Bottom-right corner
        canvas.line(width-0.5*inch, 0.5*inch, width-0.5*inch, 0.5*inch+corner_length)
        canvas.line(width-0.5*inch, 0.5*inch, width-0.5*inch-corner_length, 0.5*inch)
        
        # Add subtle watermark
        canvas.setFont("Helvetica", 48)
        canvas.setFillColor(colors.HexColor('#f8fafc'))
        canvas.rotate(45)
        canvas.drawCentredString(width/2, height/2, "RELIANCE JIO")
        canvas.rotate(-45)
        
        canvas.restoreState()
    
    # Enhanced styles for salary certificate
    company_header_style = ParagraphStyle(
        'CompanyHeader',
        parent=styles['Normal'],
        fontSize=22,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=26,
        spaceBefore=0
    )
    
    company_subtitle_style = ParagraphStyle(
        'CompanySubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=14,
        spaceBefore=0
    )
    
    company_details_style = ParagraphStyle(
        'CompanyDetails',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica',
        leading=12,
        spaceBefore=0
    )
    
    document_title_style = ParagraphStyle(
        'DocumentTitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=15,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        leading=22
    )
    
    document_number_style = ParagraphStyle(
        'DocumentNumber',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_RIGHT,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        fontName='Times-Roman',
        leading=16,
        firstLineIndent=0,
        spaceBefore=0
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=13,
        spaceBefore=0
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica',
        leading=11,
        spaceBefore=0
    )
    
    # Company Header
    story.append(Paragraph("🏢", company_header_style))
    story.append(Paragraph("RELIANCE JIO INFOTECH SOLUTIONS", company_header_style))
    story.append(Paragraph("A Subsidiary of Reliance Industries Limited", company_subtitle_style))
    story.append(Paragraph("Registered Office: Maker Chambers IV, Nariman Point, Mumbai - 400021", company_details_style))
    story.append(Paragraph("CIN: L17110MH2007PLC169642 | GST: 27AABCR0000A1Z5", company_details_style))
    story.append(Paragraph("Phone: +91-22-3555-5000 | Email: hr@reliancejio.com", company_details_style))
    story.append(Spacer(1, 15))
    
    # Document Title
    story.append(Paragraph("SALARY CERTIFICATE", document_title_style))
    
    # Document Number
    issue_date = employee.get('issue_date', datetime.now().strftime('%Y-%m-%d'))
    try:
        date_obj = datetime.strptime(issue_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
    except:
        formatted_date = issue_date
    
    doc_number = f"Certificate No: RJI-SAL-{employee['employee_code']}-{issue_date.replace('-', '')}"
    story.append(Paragraph(doc_number, document_number_style))
    
    # Main Document Text
    story.append(Spacer(1, 12))
    
    # Salary certificate content
    salary_amount = employee.get('salaryAmount', 'As per company policy')
    purpose = employee.get('purpose', 'General purpose')
    
    cert_text_1 = f"""
    This is to certify that <b>{employee['full_name']}</b>, bearing Employee ID <b>{employee['employee_code']}</b>, is currently employed with <b>Reliance Jio Infotech Solutions</b> as <b>{employee['designation']}</b> in the <b>{employee['department']}</b> department.
    """
    story.append(Paragraph(cert_text_1, body_style))
    
    cert_text_2 = f"""
    The employee's current salary is <b>{salary_amount}</b> and has been associated with our organization since <b>{employee['joining_date']}</b>. This certificate is issued for <b>{purpose}</b> and confirms the employment and salary details as stated above.
    """
    story.append(Paragraph(cert_text_2, body_style))
    
    story.append(Spacer(1, 15))
    
    # Employee Details Table
    employee_data = [
        ['Employee Name', employee['full_name']],
        ['Employee ID', employee['employee_code']],
        ['Designation', employee['designation']],
        ['Department', employee['department']],
        ['Joining Date', employee['joining_date']],
        ['Salary Amount', salary_amount],
        ['Purpose', purpose],
        ['Issue Date', formatted_date],
        ['Document Type', 'Salary Certificate'],
        ['Status', 'Active Employee']
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
    
    # Signature Section
    signature_text = "Authorized Signatories:"
    story.append(Paragraph(signature_text, signature_style))
    story.append(Spacer(1, 10))
    
    signature_data = [
        ['HR Manager', 'Department Head', 'Authorized Signatory'],
        ['', '', ''],  # Space for signatures
        ['Priya Sharma', 'Rajesh Kumar', 'Amit Patel'],
        ['Senior HR Manager', 'Department Manager', 'Director Operations'],
        ['Employee ID: HR001', 'Employee ID: DM001', 'Employee ID: DIR001'],
        [f'Date: {formatted_date}', f'Date: {formatted_date}', f'Date: {formatted_date}']
    ]
    
    signature_table = Table(signature_data, colWidths=[2.0*inch, 2.0*inch, 2.0*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
    ]))
    
    story.append(signature_table)
    story.append(Spacer(1, 15))
    
    # Footer
    footer_text = """
    <b>Important Notes:</b><br/>
    • This salary certificate is computer-generated and bears digital signatures<br/>
    • For verification, please contact: hr@reliancejio.com<br/>
    • Certificate validity: 3 months from date of issue<br/>
    • This document is confidential and should be handled with care<br/>
    • For any queries, call: +91-22-3555-5000
    """
    story.append(Paragraph(footer_text, footer_style))
    
    # Build the PDF
    doc.build(story, onFirstPage=add_enhanced_border_and_watermark)
    return buffer.getvalue()


def _wrap_text(text: str, max_chars: int) -> list[str]:
    """Improved text wrapping function"""
    words = text.split()
    lines = []
    current = []
    count = 0
    for w in words:
        if count + len(w) + (1 if current else 0) > max_chars:
            lines.append(" ".join(current))
            current = [w]
            count = len(w)
        else:
            current.append(w)
            count += len(w) + (1 if current else 0)
    if current:
        lines.append(" ".join(current))
    return lines


