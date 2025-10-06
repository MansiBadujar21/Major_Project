from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
import json


class SummaryPDFGenerator:
    """Generate well-formatted PDF summaries from JSON data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'CustomSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Times-Roman'
        )
        
        # Key points style
        self.key_points_style = ParagraphStyle(
            'CustomKeyPoints',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=20,
            fontName='Times-Roman'
        )
    
    def generate_summary_pdf(self, summary_data: dict, original_filename: str) -> BytesIO:
        """
        Generate a well-formatted PDF summary
        
        Args:
            summary_data: Dictionary containing summary information
            original_filename: Original PDF filename
            
        Returns:
            BytesIO object containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        
        story = []
        
        # Title
        title = Paragraph("📋 PDF Summary Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Document info
        info_data = [
            ["Original File:", original_filename],
            ["Document Type:", summary_data.get('document_type', 'Unknown')],
            ["Total Pages:", str(summary_data.get('total_pages', 'Unknown'))],
            ["Processing Time:", f"{summary_data.get('processing_time', 0):.2f} seconds"],
            ["Generated On:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Executive Summary
        if summary_data.get('executive_summary'):
            story.append(Paragraph("📝 Executive Summary", self.section_style))
            summary_text = summary_data['executive_summary']
            # Split into paragraphs for better formatting
            paragraphs = summary_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), self.body_style))
            story.append(Spacer(1, 12))
        
        # Key Points
        if summary_data.get('key_points') and len(summary_data['key_points']) > 0:
            story.append(Paragraph("🎯 Key Points", self.section_style))
            for i, point in enumerate(summary_data['key_points'], 1):
                point_text = f"• {point}"
                story.append(Paragraph(point_text, self.key_points_style))
            story.append(Spacer(1, 12))
        
        # Tables Found
        if summary_data.get('tables') and len(summary_data['tables']) > 0:
            story.append(Paragraph("📊 Tables Found", self.section_style))
            story.append(Paragraph(f"Total tables extracted: {len(summary_data['tables'])}", self.body_style))
            story.append(Spacer(1, 8))
            
            for i, table in enumerate(summary_data['tables'], 1):
                story.append(Paragraph(f"Table {i}: {table.get('title', 'Untitled')}", self.body_style))
                story.append(Paragraph(f"Dimensions: {table.get('dimensions', 'Unknown')}", self.body_style))
                story.append(Spacer(1, 6))
        
        # Section Summaries
        if summary_data.get('section_summaries') and len(summary_data['section_summaries']) > 0:
            story.append(PageBreak())
            story.append(Paragraph("📑 Section Summaries", self.section_style))
            
            for section in summary_data['section_summaries']:
                if section.get('title'):
                    story.append(Paragraph(f"<b>{section['title']}</b>", self.body_style))
                if section.get('summary'):
                    story.append(Paragraph(section['summary'], self.body_style))
                story.append(Spacer(1, 8))
        
        # Footer
        story.append(Spacer(1, 20))
        footer_text = f"Generated by Reliance Jio Infotech Solutions AI Assistant | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        footer = Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer


def generate_summary_pdf(summary_data: dict, original_filename: str) -> BytesIO:
    """Convenience function to generate summary PDF"""
    generator = SummaryPDFGenerator()
    return generator.generate_summary_pdf(summary_data, original_filename)
