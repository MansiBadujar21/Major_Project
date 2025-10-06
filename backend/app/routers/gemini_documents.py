from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import asyncio
import uuid
import hashlib
import json
from datetime import datetime
import os

from ..services.gemini_summarizer import GeminiSummarizer, SummaryResult
from ..services.keyword_extractor import KeywordExtractor
from ..services.doc_parser import parse_document
from ..services.summary_pdf_generator import generate_summary_pdf
from ..config import auth_disabled

router = APIRouter()

# Initialize services
gemini_summarizer = GeminiSummarizer()
keyword_extractor = KeywordExtractor()

# In-memory storage for job status (in production, use Redis or database)
job_status = {}


class GeminiSummarizeResponse(BaseModel):
    document_type: str
    executive_summary: str
    key_points: List[str]
    tables: List[Dict]
    section_summaries: List[Dict]
    total_pages: int
    processing_time: float
    model_used: str
    keywords: List[str]
    markdown_summary: str


class JobStatus:
    def __init__(self, job_id: str, filename: str):
        self.job_id = job_id
        self.filename = filename
        self.status = "processing"
        self.progress = 0
        self.message = "Initializing..."
        self.result = None
        self.error = None
        self.created_at = datetime.now()


@router.post("/upload-gemini", response_model=GeminiSummarizeResponse)
async def upload_pdf_gemini(file: UploadFile = File(...)):
    """
    Upload PDF for Gemini-powered summarization
    Handles large documents (30+ pages) with intelligent chunking
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check file size (limit to 50MB)
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:  # 50MB
        raise HTTPException(status_code=400, detail="File size too large. Maximum 50MB allowed.")
    
    try:
        # Extract keywords from raw text
        raw_text = parse_document(file.filename, content)
        keywords = keyword_extractor.extract(raw_text)
        
        # Process with Gemini
        result = await gemini_summarizer.summarize_pdf(file.filename, content)
        
        # Format tables for response
        tables_data = []
        for table in result.tables:
            tables_data.append({
                "id": table.id,
                "title": table.title,
                "dimensions": f"{table.row_count} rows × {table.col_count} columns",
                "markdown": table.markdown,
                "data_preview": table.data.head(5).to_dict('records')
            })
        
        return GeminiSummarizeResponse(
            document_type=result.document_type,
            executive_summary=result.executive_summary,
            key_points=result.key_points,
            tables=tables_data,
            section_summaries=result.section_summaries,
            total_pages=result.total_pages,
            processing_time=result.processing_time,
            model_used=result.model_used,
            keywords=keywords,
            markdown_summary=result.executive_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")


@router.post("/upload-gemini-async")
async def upload_gemini_async(file: UploadFile = File(...)):
    """Upload PDF for async processing with Gemini"""
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        if file.size > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=400, detail="File size must be less than 50MB")
        
        # Read file content
        content = await file.read()
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Create job status
        job_status[job_id] = JobStatus(job_id, file.filename)
        
        # Start background processing
        asyncio.create_task(process_pdf_async(job_id, file.filename, content))
        
        return {
            "job_id": job_id,
            "filename": file.filename,
            "status": "processing",
            "message": "PDF processing started"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Get status of a processing job"""
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_status[job_id]
    
    response = {
        "job_id": job.job_id,
        "filename": job.filename,
        "status": job.status,
        "progress": job.progress,
        "message": job.message,
        "created_at": job.created_at.isoformat()
    }
    
    if job.status == "completed":
        response["result"] = job.result
    elif job.status == "failed":
        response["error"] = job.error
    
    return response


async def process_pdf_async(job_id: str, filename: str, content: bytes):
    """Background task to process PDF"""
    try:
        job = job_status[job_id]
        
        # Update status
        job.status = "processing"
        job.progress = 10
        job.message = "Analyzing document structure..."
        
        # Process with Gemini
        result = await gemini_summarizer.summarize_pdf(filename, content)
        
        # Update job with result
        job.status = "completed"
        job.progress = 100
        job.message = "Processing completed"
        job.result = {
            "executive_summary": result.executive_summary,
            "key_points": result.key_points,
            "tables": [table.dict() for table in result.tables],
            "section_summaries": result.section_summaries,
            "document_type": result.document_type,
            "total_pages": result.total_pages,
            "processing_time": result.processing_time,
            "model_used": result.model_used
        }
        
    except Exception as e:
        job = job_status[job_id]
        job.status = "failed"
        job.error = str(e)
        job.message = f"Processing failed: {str(e)}"


@router.delete("/cleanup/{job_id}")
async def cleanup_job(job_id: str):
    """Clean up completed job data"""
    if job_id in job_status:
        del job_status[job_id]
    return {"message": "Job cleaned up"}


@router.post("/download-summary-pdf")
async def download_summary_pdf(request: Dict[str, Any]):
    """Download summary as PDF instead of JSON"""
    try:
        summary_data = request.get('summary_data')
        original_filename = request.get('original_filename', 'document.pdf')
        
        if not summary_data:
            raise HTTPException(status_code=400, detail="Summary data is required")
        
        # Generate PDF
        pdf_buffer = generate_summary_pdf(summary_data, original_filename)
        
        # Create filename
        pdf_filename = f"{original_filename.replace('.pdf', '')}_summary.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={pdf_filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for Gemini service"""
    try:
        # Test Gemini connection
        test_prompt = "Hello, this is a health check."
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            gemini_summarizer.executor,
            gemini_summarizer.model.generate_content,
            test_prompt
        )
        
        return {
            "status": "healthy",
            "gemini_connection": "ok",
            "model_used": "gemini-2.0-flash-exp",
            "message": "Gemini service is operational"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
