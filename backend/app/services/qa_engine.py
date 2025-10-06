import os
import re
from typing import Optional, List, Dict, Tuple
from datetime import datetime
import asyncio
import logging
import json
from pathlib import Path

import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np

from .document_request_handler import DocumentRequestHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HybridQAEngine:
    def __init__(self) -> None:
        # Initialize with safe defaults
        self.gemini_model = None
        self.sentence_model = None
        self.qa_dataset = []
        self.qa_embeddings = []
        self.doc_handler = None
        self._current_document_request = None
        
        # Initialize services with better error handling
        self._initialize_gemini()
        self._initialize_sentence_transformer()
        self._load_qa_dataset()
        
        # Initialize document request handler with better error handling
        try:
            self.doc_handler = DocumentRequestHandler()
            logger.info("✅ Document request handler initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize document request handler: {str(e)}")
            self.doc_handler = None
    
    def _initialize_gemini(self):
        """Initialize Gemini model with enhanced error handling"""
        try:
            api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
            if not api_key:
                logger.warning("⚠️ GOOGLE_GEMINI_API_KEY not found in environment variables")
                return
            
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("✅ Gemini model initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini model: {str(e)}")
            self.gemini_model = None

    def _initialize_sentence_transformer(self):
        """Initialize sentence transformer for semantic search"""
        try:
            # Set cache directory to use existing models
            import os
            models_dir = Path(__file__).parent.parent.parent.parent / "models"
            cache_dir = models_dir / "sentence-transformers"
            
            # Set environment variables for model caching
            os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(cache_dir)
            os.environ["HF_HOME"] = str(models_dir)
            os.environ["TRANSFORMERS_CACHE"] = str(models_dir / "transformers")
            
            # Check if model files exist
            model_path = cache_dir / "models--sentence-transformers--all-MiniLM-L6-v2"
            logger.info(f"🔍 Checking model path: {model_path}")
            logger.info(f"🔍 Cache directory: {cache_dir}")
            logger.info(f"🔍 Models directory: {models_dir}")
            
            if not model_path.exists():
                logger.warning(f"⚠️ Model not found at {model_path}, will download")
            else:
                logger.info(f"✅ Found existing model at {model_path}")
            
            # Try to use local model path first
            model_path = cache_dir / "models--sentence-transformers--all-MiniLM-L6-v2" / "snapshots" / "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
            if model_path.exists():
                logger.info(f"✅ Using local model from {model_path}")
                self.sentence_model = SentenceTransformer(str(model_path))
            else:
                logger.info("⚠️ Local model not found, using cache directory")
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=str(cache_dir))
            logger.info("✅ Sentence transformer initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize sentence transformer: {str(e)}")
            self.sentence_model = None
    
    def _load_qa_dataset(self):
        """Load QA dataset and pre-compute embeddings"""
        try:
            qa_file = Path(__file__).parent.parent / "data" / "qa_dataset.json"
            logger.info(f"🔍 Loading QA dataset from: {qa_file}")
            
            if not qa_file.exists():
                logger.warning("⚠️ QA dataset file not found")
                return
            
            # Check file size
            file_size = qa_file.stat().st_size
            logger.info(f"📁 QA dataset file size: {file_size} bytes")
            
            # Read file content first to check for issues
            with open(qa_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"📄 File content length: {len(content)} characters")
            
            # Parse JSON with better error handling
            try:
                self.qa_dataset = json.loads(content)
                logger.info(f"📊 Successfully parsed JSON with {len(self.qa_dataset)} QA pairs")
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON parsing error: {str(e)}")
                logger.error(f"❌ Error at line {e.lineno}, column {e.colno}")
                # Try to show the problematic area
                lines = content.split('\n')
                if e.lineno <= len(lines):
                    logger.error(f"❌ Problematic line {e.lineno}: {lines[e.lineno-1]}")
                return
            
            # Validate dataset structure
            if not isinstance(self.qa_dataset, list):
                logger.error("❌ QA dataset is not a list")
                self.qa_dataset = []
                return
            
            # Count valid QA pairs
            valid_pairs = 0
            for i, qa in enumerate(self.qa_dataset):
                if isinstance(qa, dict) and 'question' in qa and 'answer' in qa:
                    valid_pairs += 1
                else:
                    logger.warning(f"⚠️ Invalid QA pair at index {i}: {qa}")
            
            logger.info(f"📊 Found {valid_pairs} valid QA pairs out of {len(self.qa_dataset)} total entries")
            
            # Pre-compute embeddings for all questions
            if self.sentence_model and self.qa_dataset:
                questions = [qa['question'] for qa in self.qa_dataset if isinstance(qa, dict) and 'question' in qa]
                logger.info(f"🔄 Computing embeddings for {len(questions)} questions...")
                self.qa_embeddings = self.sentence_model.encode(questions)
                logger.info(f"✅ Successfully computed embeddings for {len(self.qa_embeddings)} questions")
            else:
                logger.warning("⚠️ Could not compute embeddings - sentence model not available or dataset empty")
            
        except Exception as e:
            logger.error(f"❌ Failed to load QA dataset: {str(e)}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            self.qa_dataset = []
            self.qa_embeddings = []
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for better matching"""
        import re
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Fix common typos
        text = re.sub(r'\bpollicy\b', 'policy', text)
        text = re.sub(r'\battendance\b', 'attendance', text)
        text = re.sub(r'\bleave\b', 'leave', text)
        text = re.sub(r'\bwfh\b', 'work from home', text)
        
        # Normalize greeting variations
        text = re.sub(r'\bheyy+\b', 'hey', text)  # heyyy -> hey
        text = re.sub(r'\bhelloo+\b', 'hello', text)  # hellooo -> hello
        text = re.sub(r'\bhii+\b', 'hi', text)  # hiii -> hi
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove punctuation except for important ones
        text = re.sub(r'[^\w\s\-]', ' ', text)
        
        # Remove extra whitespace again
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_keywords(self, text: str) -> set:
        """Extract important keywords from text"""
        # Common HR and policy keywords with better categorization
        hr_keywords = {
            # Policy types
            'policy', 'policies', 'attendance', 'leave', 'work', 'home', 'wfh', 'dress', 'code', 'conduct', 'handbook', 'onboarding', 'performance', 'reimbursement',
            'device', 'password', 'software', 'helpdesk', 'it', 'support', 'acceptable', 'use', 'sop', 'procedure',
            
            # Benefits and compensation
            'benefits', 'salary', 'compensation', 'bonus', 'insurance', 'health', 'dental', 'vision', 'wellness',
            
            # Time and attendance
            'time', 'hours', 'tardiness', 'late', 'early', 'overtime', 'schedule', 'flexible',
            
            # Leave and time off
            'vacation', 'holiday', 'sick', 'emergency', 'pto', 'paid', 'unpaid', 'carry', 'over',
            
            # Workplace behavior
            'respect', 'dignity', 'harassment', 'discrimination', 'ethics', 'ethical', 'unethical', 'violation', 'report', 'retaliation',
            
            # Training and development
            'training', 'development', 'certification', 'workshop', 'conference', 'career',
            
            # General HR terms
            'hr', 'human', 'resource', 'employee', 'employer', 'company', 'organization', 'workplace', 'manager', 'supervisor',
            
            # Emotion and greeting keywords
            'hello', 'hi', 'hey', 'good', 'morning', 'afternoon', 'evening', 'how', 'are', 'you',
            'feel', 'ok', 'well', 'going', 'everything', 'fine', 'great', 'thanks', 'thank', 'welcome', 'bye', 'goodbye'
        }
        
        # Extract words from text
        words = set(self._preprocess_text(text).split())
        
        # Return intersection with HR keywords
        return words.intersection(hr_keywords)
    
    def _keyword_similarity(self, user_question: str, dataset_question: str) -> float:
        """Calculate keyword-based similarity"""
        user_keywords = self._extract_keywords(user_question)
        dataset_keywords = self._extract_keywords(dataset_question)
        
        if not user_keywords or not dataset_keywords:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(user_keywords.intersection(dataset_keywords))
        union = len(user_keywords.union(dataset_keywords))
        
        return intersection / union if union > 0 else 0.0
    
    def _find_similar_question(self, user_question: str, threshold: float = 0.75) -> Optional[Dict]:
        """Find most similar question from dataset using improved semantic search"""
        if not self.sentence_model or not self.qa_embeddings or not self.qa_dataset:
            logger.warning("⚠️ Missing required components for semantic search")
            return None
        
        # Additional safety check for embeddings
        if len(self.qa_embeddings) == 0 or len(self.qa_dataset) == 0:
            logger.warning("⚠️ Empty embeddings or dataset")
            return None
        
        try:
            # Preprocess user question
            processed_question = self._preprocess_text(user_question)
            logger.info(f"🔍 Processing question: '{user_question}' -> '{processed_question}'")
            
            # Encode user question
            user_embedding = self.sentence_model.encode([processed_question])
            
            # Calculate semantic similarities
            similarities = np.dot(self.qa_embeddings, user_embedding.T).flatten()
            
            # Find top matches (keep as numpy array for argsort)
            top_indices = np.argsort(similarities)[::-1][:10]  # Top 10 matches for better selection
            
            # Convert to list after finding indices
            similarities = similarities.tolist()
            
            best_match = None
            best_score = 0.0
            
            for idx in top_indices:
                idx = int(idx)
                dataset_question = self.qa_dataset[idx]['question']
                
                # Semantic similarity
                semantic_sim = float(similarities[idx])
                
                # Keyword similarity
                keyword_sim = self._keyword_similarity(processed_question, dataset_question)
                
                # Combined score (weighted average) - increased weight for keywords
                combined_score = (semantic_sim * 0.5) + (keyword_sim * 0.5)
                
                logger.info(f"🔍 Match {idx}: '{dataset_question}' - Semantic: {semantic_sim:.3f}, Keywords: {keyword_sim:.3f}, Combined: {combined_score:.3f}")
                
                # Additional validation: check for exact keyword matches
                user_keywords = self._extract_keywords(processed_question)
                dataset_keywords = self._extract_keywords(dataset_question)
                
                # If user is asking about a specific policy, ensure the dataset question is about the same policy
                policy_keywords = ['policy', 'policies', 'attendance', 'leave', 'wfh', 'dress', 'conduct', 'handbook', 'onboarding', 'performance', 'reimbursement', 'it', 'device', 'password', 'software', 'helpdesk']
                user_policy_keywords = user_keywords.intersection(set(policy_keywords))
                dataset_policy_keywords = dataset_keywords.intersection(set(policy_keywords))
                
                # If user is asking about a specific policy, dataset must contain similar policy keywords
                if user_policy_keywords and not dataset_policy_keywords.intersection(user_policy_keywords):
                    logger.info(f"⚠️ Policy keyword mismatch - User: {user_policy_keywords}, Dataset: {dataset_policy_keywords}")
                    continue
                
                # For short questions, require higher keyword similarity
                if len(processed_question.split()) <= 3 and keyword_sim < 0.4:
                    logger.info(f"⚠️ Short question requires higher keyword similarity: {keyword_sim:.3f}")
                    continue
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_match = {
                        'qa_pair': self.qa_dataset[idx],
                        'similarity': combined_score,
                        'semantic_similarity': semantic_sim,
                        'keyword_similarity': keyword_sim,
                        'index': idx
                    }
            
            logger.info(f"🔍 Best combined score: {best_score:.3f} (threshold: {threshold})")
            
            # Adaptive threshold based on question length and complexity
            adaptive_threshold = threshold
            if len(processed_question.split()) <= 3:  # Short questions
                adaptive_threshold = threshold - 0.05  # Reduced reduction
            elif len(processed_question.split()) >= 10:  # Long questions
                adaptive_threshold = threshold + 0.1
            
            # Additional validation for policy questions
            if 'policy' in processed_question.lower():
                # For policy questions, require higher threshold
                adaptive_threshold = max(adaptive_threshold, 0.7)
                
                # Ensure the matched question is actually about a policy
                if best_match:
                    matched_question = best_match['qa_pair']['question'].lower()
                    if 'policy' not in matched_question and not any(policy in matched_question for policy in ['attendance', 'leave', 'wfh', 'dress', 'conduct', 'handbook', 'onboarding', 'performance', 'reimbursement', 'it', 'device', 'password', 'software', 'helpdesk']):
                        logger.info(f"⚠️ Policy question matched with non-policy answer: {matched_question}")
                        return None
            
            if best_score >= adaptive_threshold:
                return best_match
            
            return None
                
        except Exception as e:
            logger.error(f"❌ Error in semantic search: {str(e)}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return None
    
    async def _gemini_answer(self, question: str) -> str:
        """Generate answer using Gemini API"""
        if not self.gemini_model:
            return "I apologize, but I'm currently unable to process your request. Please try again later."
        
        try:
            # Enhanced prompt for better responses
            prompt = f"""
            You are an AI assistant for Reliance Jio Infotech Solutions. 
            Answer the following question about company policies, procedures, or general HR matters.
            Be helpful, professional, and accurate. If you're not sure about something, say so.
            
            **Available Policy Topics:**
            - Attendance Policy (work hours, tardiness)
            - Leave Policy (20 days annual leave, submission requirements)
            - Work From Home Policy (3 days/week, manager approval)
            - Dress Code Policy (business casual)
            - Performance Review Policy (bi-annual reviews)
            - Reimbursement Policy (30-day submission, receipts required)
            - Code of Conduct (respect, zero tolerance for harassment)
            - Employee Handbook (mission, values, policies)
            - Onboarding (2-week program, mandatory training)
            - IT Policies (device, password, software, helpdesk)
            
            **Important Guidelines:**
            - For general policy questions, provide an overview of the policy
            - For specific scenarios, provide practical guidance
            - Always include contact information when relevant
            - Be friendly and professional in tone
            - If the question is unclear, ask for clarification
            - For greetings and emotion-based questions, respond warmly and professionally
            - For "how are you" type questions, respond positively about being ready to help
            
            **Question:** {question}
            
            Please provide a clear, helpful response based on the available policy information:
            """
            
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
            
        except Exception as e:
            logger.error(f"❌ Gemini API error: {str(e)}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again later."
    
    async def answer(self, question: str) -> str:
        """Main method to answer questions using hybrid approach"""
        if not question or not question.strip():
            return "Please provide a question so I can help you."
        
        question = question.strip()
        
        # Step 0: Handle common greetings and basic questions first
        processed_question = self._preprocess_text(question)
        
        # Check for greetings and emotion-based questions
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you']
        emotion_keywords = ['how are you', 'how do you feel', 'are you ok', 'are you well', 'how is it going', 'how is everything']
        
        if any(greeting in processed_question for greeting in greeting_keywords):
            # Try to find exact greeting match first
            for qa in self.qa_dataset:
                if isinstance(qa, dict) and 'question' in qa:
                    qa_lower = qa['question'].lower()
                    if qa_lower in processed_question or processed_question in qa_lower:
                        return qa['answer']
        
        # Check for emotion-based questions specifically
        if any(emotion in processed_question for emotion in emotion_keywords):
            # Look for the "how are you" response specifically
            for qa in self.qa_dataset:
                if isinstance(qa, dict) and 'question' in qa:
                    if 'how are you' in qa['question'].lower():
                        return qa['answer']
        
        # Check for "what can you do" type questions
        capability_keywords = ['what can you do', 'help', 'capabilities', 'features']
        if any(keyword in processed_question for keyword in capability_keywords):
            for qa in self.qa_dataset:
                if isinstance(qa, dict) and 'question' in qa:
                    if 'what can you do' in qa['question'].lower() or 'help' in qa['question'].lower():
                        return qa['answer']
        
        # Step 1: Check for document request keywords and numeric selections
        document_keywords = [
            'document', 'need document', 'request document', 'get document', 'want document',
            'experience letter', 'employment letter', 'salary slip', 'form 16', 'bonafide',
            'certificate', 'noc', 'relieving letter', 'offer letter', 'appointment letter',
            'promotion letter', 'pf statement', 'uan details', 'medical insurance',
            'id card', 'visa support', 'travel authorization'
        ]
        
        # Check if it's a numeric document selection (1-16)
        if self.doc_handler and question.strip().isdigit() and 1 <= int(question.strip()) <= 16:
            try:
                doc_number = question.strip()
                doc_name = self.doc_handler.supported_documents.get(doc_number)
                if doc_name:
                    logger.info(f"📄 User selected document: {doc_number} - {doc_name}")
                    return self.doc_handler.get_document_details_prompt(doc_name)
            except Exception as e:
                logger.error(f"❌ Document selection error: {str(e)}")
        
        # Check if user is providing document details (contains common document-related keywords)
        if self.doc_handler and any(keyword in question.lower() for keyword in ['name:', 'employee id:', 'id:', 'department:', 'designation:', 'joining date:', 'purpose:']):
            try:
                # This looks like document details being provided
                return """📝 **Document Request Details Received**

Thank you for providing the details! I've received your document request information.

**Next Steps:**
1. Your request has been logged in our system
2. HR will review and process your request
3. You'll receive a confirmation email with tracking details
4. The document will be generated and sent to you within 2-3 business days

**Contact HR:**
• Email: hr@reliancejio.com
• Phone: Available through internal directory

If you need immediate assistance, please contact HR directly."""
            except Exception as e:
                logger.error(f"❌ Document details processing error: {str(e)}")
        
        # Check for document request keywords
        if self.doc_handler and any(keyword in question.lower() for keyword in document_keywords):
            try:
                # Check if it's a specific document request
                if any(specific_doc in question.lower() for specific_doc in ['experience letter', 'employment letter', 'salary slip', 'form 16', 'bonafide', 'certificate']):
                    # Use the specific document handler
                    return self._handle_specific_document_request(question)
                
                # If no specific match found, use document handler
                return self.doc_handler.get_document_list()
            except Exception as e:
                logger.error(f"❌ Document request error: {str(e)}")
        
        # Step 2: Try semantic search in local dataset
        try:
            similar_qa = self._find_similar_question(question)
            
            if similar_qa:
                similarity_score = float(similar_qa['similarity'])
                semantic_score = float(similar_qa.get('semantic_similarity', 0))
                keyword_score = float(similar_qa.get('keyword_similarity', 0))
                
                logger.info(f"✅ Found similar question in dataset - Combined: {similarity_score:.3f}, Semantic: {semantic_score:.3f}, Keywords: {keyword_score:.3f}")
                
                # Use stricter threshold for policy questions
                threshold = 0.7  # Increased base threshold
                
                # For policy questions, require higher threshold
                if 'policy' in processed_question.lower():
                    threshold = 0.75  # Higher threshold for policy questions
                    
                    # Additional validation for policy questions
                    qa_question = similar_qa['qa_pair']['question'].lower()
                    
                    # Check if the matched question is actually about a policy
                    policy_indicators = ['policy', 'attendance', 'leave', 'wfh', 'dress', 'conduct', 'handbook', 'onboarding', 'performance', 'reimbursement', 'it', 'device', 'password', 'software', 'helpdesk']
                    if not any(indicator in qa_question for indicator in policy_indicators):
                        logger.info(f"⚠️ Policy question matched with non-policy answer: {qa_question}")
                        # Continue to next step instead of returning incorrect answer
                        pass
                    else:
                        # For policy questions, prefer general policy descriptions
                        if 'what does' in qa_question and 'describe' in qa_question:
                            threshold = 0.65  # Slightly lower for policy descriptions
                        elif 'what is' in processed_question and 'what is' in qa_question:
                            threshold = 0.65  # Slightly lower for "what is" questions
                        else:
                            # For specific policy questions, require very high similarity
                            threshold = 0.8
                
                # For non-policy questions, use standard threshold
                else:
                    if semantic_score > 0.85 or keyword_score > 0.6:
                        threshold = 0.65  # Lower threshold for high-quality matches
                
                if similarity_score >= threshold:
                    return similar_qa['qa_pair']['answer']
                else:
                    logger.info(f"⚠️ Similarity score {similarity_score:.3f} below threshold {threshold}")
        except Exception as e:
            logger.error(f"❌ Error in semantic search: {str(e)}")
            # Continue to keyword fallback
        
        # Step 2.5: Try keyword-based fallback
        try:
            logger.info("🔍 Trying keyword-based fallback search...")
            user_keywords = self._extract_keywords(question)
            logger.info(f"🔍 Extracted keywords: {user_keywords}")
            
            if user_keywords:
                best_keyword_match = None
                best_keyword_score = 0.0
                
                for i, qa in enumerate(self.qa_dataset):
                    dataset_keywords = self._extract_keywords(qa['question'])
                    if dataset_keywords:
                        keyword_sim = self._keyword_similarity(question, qa['question'])
                        
                        # Higher threshold for keyword matching
                        if keyword_sim > best_keyword_score and keyword_sim > 0.5:  # Increased minimum threshold
                            # Additional validation for policy questions
                            if 'policy' in processed_question.lower():
                                qa_question = qa['question'].lower()
                                policy_indicators = ['policy', 'attendance', 'leave', 'wfh', 'dress', 'conduct', 'handbook', 'onboarding', 'performance', 'reimbursement', 'it', 'device', 'password', 'software', 'helpdesk']
                                if not any(indicator in qa_question for indicator in policy_indicators):
                                    logger.info(f"⚠️ Policy question keyword match with non-policy answer: {qa_question}")
                                    continue
                            
                            best_keyword_score = keyword_sim
                            best_keyword_match = {
                                'qa_pair': qa,
                                'similarity': keyword_sim,
                                'index': i
                            }
                
                if best_keyword_match and best_keyword_match['similarity'] > 0.6:  # Higher final threshold
                    logger.info(f"✅ Found keyword-based match (score: {best_keyword_match['similarity']:.3f})")
                    return best_keyword_match['qa_pair']['answer']
                else:
                    logger.info(f"⚠️ Keyword match score {best_keyword_match['similarity']:.3f if best_keyword_match else 0:.3f} below threshold 0.6")
        except Exception as e:
            logger.error(f"❌ Error in keyword fallback: {str(e)}")
        
        # Step 3: Use Gemini API for complex questions
        try:
            logger.info("🔄 Using Gemini API for complex question")
            return await self._gemini_answer(question)
        except Exception as e:
            logger.error(f"❌ Error in Gemini API: {str(e)}")
            # Fallback to simple response
            return f"Hello! I'm your Reliance Jio Infotech Solutions AI Assistant. I can help you with HR questions, document requests, and PDF processing. You asked: '{question}'. How can I assist you today?"
    
    def _handle_specific_document_request(self, question: str) -> str:
        """Handle specific document requests with better responses"""
        question_lower = question.lower()
        
        # Experience letter
        if 'experience letter' in question_lower or 'experience certificate' in question_lower:
            return """**Experience Certificate Request**

To request an Experience Certificate, please follow these steps:

📋 **Required Information:**
• Full Name (as per employee records)
• Employee ID
• Date of joining
• Date of leaving (if applicable)
• Purpose of the certificate

📞 **Contact HR:**
• Email: hr@reliancejio.com
• Phone: Available through internal directory

⏱️ **Processing Time:** 3-5 business days

You can also use our Document Request System by typing "I need a document" and selecting option 2 for Experience Certificate."""

        # Employment verification letter
        elif 'employment' in question_lower and ('letter' in question_lower or 'verification' in question_lower):
            return """**Employment Verification Letter Request**

To request an Employment Verification Letter, please provide:

📋 **Required Information:**
• Full Name (as per employee records)
• Employee ID
• Purpose (e.g., bank loan, visa application, etc.)
• Any specific requirements

📞 **Contact HR:**
• Email: hr@reliancejio.com
• Phone: Available through internal directory

⏱️ **Processing Time:** 2-3 business days

You can also use our Document Request System by typing "I need a document" and selecting option 1 for Bonafide/Employment Verification Letter."""

        # Salary slip
        elif 'salary slip' in question_lower or 'payslip' in question_lower:
            return """**Salary Slip Request**

To request Salary Slips, please provide:

📋 **Required Information:**
• Full Name (as per employee records)
• Employee ID
• Time period (e.g., last 3 months, specific month)
• Purpose

📞 **Contact HR:**
• Email: hr@reliancejio.com
• Phone: Available through internal directory

⏱️ **Processing Time:** 1-2 business days

You can also use our Document Request System by typing "I need a document" and selecting option 7 for Salary Slips."""

        # Form 16
        elif 'form 16' in question_lower or 'tax' in question_lower:
            return """**Form 16 / Tax Documents Request**

To request Form 16 or Tax Documents, please provide:

📋 **Required Information:**
• Full Name (as per employee records)
• Employee ID
• Financial year (e.g., 2023-24)
• Purpose

📞 **Contact HR:**
• Email: hr@reliancejio.com
• Phone: Available through internal directory

⏱️ **Processing Time:** 3-5 business days

You can also use our Document Request System by typing "I need a document" and selecting option 8 for Form 16/Tax Documents."""

        # Default document response
        else:
            return self.doc_handler.get_document_list()

    def get_health_status(self) -> Dict:
        """Get health status of QA engine components"""
        return {
            "gemini_model": self.gemini_model is not None,
            "sentence_model": self.sentence_model is not None,
            "qa_dataset_loaded": len(self.qa_dataset) > 0,
            "qa_embeddings_ready": len(self.qa_embeddings) > 0,
            "document_handler": self.doc_handler is not None,
            "total_qa_pairs": len(self.qa_dataset)
        }


