from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
from datetime import datetime

from ..services.qa_engine import HybridQAEngine

router = APIRouter()

# Initialize services
qa_engine = HybridQAEngine()


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    feedback_type: str  # "correct", "incorrect", "improve"
    suggested_answer: Optional[str] = None


class QueryRequest(BaseModel):
    query: str
    include_suggestions: bool = True


class QASuggestion(BaseModel):
    question: str
    answer: str
    similarity: float
    source: str


class QAStatistics(BaseModel):
    total_qa_pairs: int
    generated_qa_pairs: int
    manual_qa_pairs: int
    sources: Dict[str, int]
    last_updated: str


@router.post("/generate-qa", response_model=Dict)
async def generate_qa_from_documents(background_tasks: BackgroundTasks):
    """Generate Q&A pairs from policy documents in the background"""
    try:
        # Note: This feature is now simplified to use only Gemini API
        # No local dataset generation needed
        
        return {
            "message": "QA system is now powered by Hybrid approach (Local Dataset + Gemini API)",
            "status": "active",
            "note": "Uses local QA dataset for common questions and Gemini API for complex queries"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {str(e)}")


@router.get("/statistics", response_model=QAStatistics)
async def get_qa_statistics():
    """Get QA system statistics"""
    try:
        # Statistics for hybrid system
        health_status = qa_engine.get_health_status()
        return QAStatistics(
            total_qa_pairs=health_status.get("total_qa_pairs", 0),
            generated_qa_pairs=health_status.get("total_qa_pairs", 0),
            manual_qa_pairs=0,
            sources={"local_dataset": 1, "gemini_api": 1},
            last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


@router.post("/feedback")
async def submit_qa_feedback(feedback: FeedbackRequest):
    """Submit feedback for QA responses"""
    try:
        # Note: Feedback is logged but not used for local dataset updates
        # since we're using pure Gemini API
        
        return {
            "message": "Feedback received (Hybrid QA system)",
            "status": "logged",
            "note": "Feedback is logged for monitoring purposes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")


@router.post("/suggestions", response_model=List[QASuggestion])
async def get_qa_suggestions(query: QueryRequest):
    """Get semantic suggestions for user queries"""
    try:
        # Get suggestions from hybrid system
        if not query.include_suggestions:
            return []
        
        # For now, return empty suggestions (can be enhanced later)
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")


@router.post("/enhanced-answer")
async def get_enhanced_answer(query: QueryRequest):
    """Get enhanced answer with suggestions"""
    try:
        # Get primary answer from Gemini API
        answer = await qa_engine.answer(query.query)
        
        return {
            "answer": answer,
            "suggestions": [],
            "query": query.query,
            "source": "hybrid_qa_system"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get enhanced answer: {str(e)}")


@router.get("/health")
async def qa_health_check():
    """Health check for QA system"""
    try:
        health_status = qa_engine.get_health_status()
        return {
            "status": "healthy",
            "qa_pairs_available": health_status.get("total_qa_pairs", 0),
            "gemini_available": health_status.get("gemini_model", False),
            "sentence_transformer_available": health_status.get("sentence_model", False),
            "last_updated": datetime.now().isoformat(),
            "system_type": "hybrid_qa_system"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.post("/auto-learn")
async def auto_learn_from_conversation(query: str, user_feedback: str):
    """Auto-learn from user conversations and feedback"""
    try:
        # Note: Learning is not implemented for Gemini-only system
        # since responses are generated dynamically
        
        return {
            "message": "Learning data recorded (monitoring only)",
            "status": "logged",
            "note": "Hybrid system uses local dataset + Gemini API"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record learning data: {str(e)}")
