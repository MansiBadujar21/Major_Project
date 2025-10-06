import os
import json
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
from ..config import get_mongodb_uri

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.employees_collection = None
        self.qa_collection = None
        self.document_requests_collection = None
        self.bad_words_collection = None
        
    async def connect(self):
        """Connect to MongoDB Atlas (optional) or use local JSON files"""
        try:
            # Get MongoDB connection string from environment
            mongo_uri = get_mongodb_uri()
            
            if mongo_uri and "mongodb+srv://" in mongo_uri:
                # Try to connect to MongoDB Atlas
                try:
                    self.client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
                    self.db = self.client.hr_assistant
                    self.employees_collection = self.db.employees
                    
                    # Test connection
                    await self.client.admin.command('ping')
                    logger.info("✅ Connected to MongoDB Atlas successfully")
                    
                except Exception as e:
                    logger.warning(f"⚠️ MongoDB Atlas connection failed: {str(e)}")
                    logger.info("🔄 Falling back to local JSON files")
                    self.client = None
                    self.db = None
                    self.employees_collection = None
            else:
                logger.info("📁 Using local JSON files (no MongoDB URI configured)")
                
        except Exception as e:
            logger.error(f"❌ Database connection error: {str(e)}")
            logger.info("🔄 Falling back to local JSON files")
            self.client = None
            self.db = None
            self.employees_collection = None
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✅ Disconnected from MongoDB")
    
    async def _initialize_data(self):
        """Initialize data - this is now handled by manual upload"""
        if self.employees_collection:
            try:
                employee_count = await self.employees_collection.count_documents({})
                logger.info(f"✅ MongoDB Atlas has {employee_count} employee records")
            except Exception as e:
                logger.warning(f"⚠️ Could not check MongoDB employee count: {str(e)}")
        else:
            logger.info("📁 Using local JSON files for employee data")
    
    async def _load_employees_from_json(self):
        """Load employees from JSON file to MongoDB"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "employees.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                employees = json.load(f)
            
            if employees:
                await self.employees_collection.insert_many(employees)
                logger.info(f"✅ Loaded {len(employees)} employees to MongoDB")
        except Exception as e:
            logger.error(f"❌ Failed to load employees: {str(e)}")
    
    async def _load_qa_from_json(self):
        """Load QA dataset from JSON file to MongoDB"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "qa_dataset.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                qa_data = json.load(f)
            
            if qa_data:
                await self.qa_collection.insert_many(qa_data)
                logger.info(f"✅ Loaded {len(qa_data)} QA pairs to MongoDB")
        except Exception as e:
            logger.error(f"❌ Failed to load QA data: {str(e)}")
    
    async def _load_bad_words_from_json(self):
        """Load bad words from JSON file to MongoDB"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "bad_words.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                bad_words = json.load(f)
            
            if bad_words:
                await self.bad_words_collection.insert_many(bad_words)
                logger.info(f"✅ Loaded {len(bad_words)} bad words to MongoDB")
        except Exception as e:
            logger.error(f"❌ Failed to load bad words: {str(e)}")
    
    # Employee operations
    async def get_all_employees(self) -> List[Dict]:
        """Get all employees"""
        cursor = self.employees_collection.find({})
        return await cursor.to_list(length=None)
    
    async def search_employees(self, query: str) -> List[Dict]:
        """Search employees by name or employee code"""
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {"full_name": {"$regex": query, "$options": "i"}},
                        {"employee_code": {"$regex": query, "$options": "i"}},
                        {"email": {"$regex": query, "$options": "i"}}
                    ]
                }
            },
            {"$limit": 10}
        ]
        cursor = self.employees_collection.aggregate(pipeline)
        return await cursor.to_list(length=None)
    
    async def get_employee_by_id(self, emp_id: int) -> Optional[Dict]:
        """Get employee by ID from MongoDB Atlas or local JSON"""
        if self.employees_collection:
            try:
                return await self.employees_collection.find_one({"emp_id": emp_id})
            except Exception as e:
                logger.warning(f"⚠️ MongoDB query failed, falling back to JSON: {str(e)}")
        
        # Fallback to local JSON file
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "employees.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                employees = json.load(f)
            
            for employee in employees:
                if employee.get("emp_id") == emp_id:
                    return employee
            return None
        except Exception as e:
            logger.error(f"❌ Failed to get employee from JSON: {str(e)}")
            return None
    
    async def validate_employee(self, employee_data: Dict) -> Dict:
        """Validate employee data"""
        # Implementation for employee validation
        pass
    
    # QA operations - Keep local JSON files
    async def get_qa_dataset(self) -> List[Dict]:
        """Get all QA pairs from local JSON file"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "qa_dataset.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Failed to load QA dataset from JSON: {str(e)}")
            return []
    
    async def add_qa_pair(self, question: str, answer: str):
        """Add new QA pair to local JSON file"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "qa_dataset.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                qa_data = json.load(f)
            
            qa_data.append({"question": question, "answer": answer})
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(qa_data, f, indent=2, ensure_ascii=False)
                
            logger.info("✅ Added new QA pair to local JSON file")
        except Exception as e:
            logger.error(f"❌ Failed to add QA pair: {str(e)}")
    
    # Document requests operations - Keep local JSON files
    async def save_document_request(self, request_data: Dict):
        """Save document request to local JSON file"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "document_requests.json")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    requests = json.load(f)
            except FileNotFoundError:
                requests = []
            
            requests.append(request_data)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(requests, f, indent=2, ensure_ascii=False)
                
            logger.info("✅ Document request saved to local JSON file")
        except Exception as e:
            logger.error(f"❌ Failed to save document request: {str(e)}")
    
    async def get_document_requests(self) -> List[Dict]:
        """Get all document requests from local JSON file"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "document_requests.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            logger.error(f"❌ Failed to load document requests: {str(e)}")
            return []
    
    # Bad words operations - Keep local JSON files
    async def get_bad_words(self) -> List[str]:
        """Get all bad words from local JSON file"""
        try:
            json_file = os.path.join(os.path.dirname(__file__), "..", "data", "bad_words.json")
            with open(json_file, 'r', encoding='utf-8') as f:
                bad_words_data = json.load(f)
            return [word["word"] for word in bad_words_data]
        except Exception as e:
            logger.error(f"❌ Failed to load bad words from JSON: {str(e)}")
            return []

# Global database instance
db_service = DatabaseService()


