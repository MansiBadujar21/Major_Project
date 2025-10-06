# Reliance Jio Infotech Solutions - AI-Powered HR Assistant

## 🚀 Project Overview

An advanced AI-powered HR assistant chatbot built as a college major project by a team of talented students. This comprehensive solution combines modern web technologies with cutting-edge AI to provide intelligent HR support, document processing, and certificate generation for Reliance Jio Infotech Solutions.

## 📸 Screenshots

### Login Page
![Login Page](./Project%20Images/Login_Page.png)

*Secure OTP-based authentication system with email verification for enhanced security.*

### OTP Verification Page
![OTP Page](./Project%20Images/Otp_Page.png)

*One-time password verification interface ensuring secure access to the HR assistant system.*

### Home Page
![Home Page](./Project%20Images/Home_Page.png)

*The main interface of the AI-powered HR Assistant showing the chat interface and document processing capabilities.*

## ✨ Key Features

### 🤖 **HR Q&A Chat System**
- **Hybrid AI Approach**: Combines semantic search with Google Gemini 2.0 Flash Exp
- **Local Embeddings**: Fast policy lookups using Sentence Transformers
- **Comprehensive Knowledge Base**: 500+ curated Q&A pairs covering company policies
- **Real-time Responses**: Instant answers with context-aware AI assistance
- **Multi-language Support**: Handles various English proficiency levels

### 📄 **Advanced PDF Document Processing**
- **Large File Support**: Handles PDFs up to 50MB with 30+ pages
- **Intelligent Table Extraction**: Advanced table detection and formatting
- **AI-Powered Summarization**: Comprehensive document summaries using Gemini 2.0
- **Progress Tracking**: Real-time processing status with intelligent chunking
- **Multiple Content Types**: Supports complex documents with mixed content

### 📜 **Document Generation System**
- **16 Document Types**: Complete range of official HR documents
- **Professional Templates**: Company-branded certificates and letters
- **Employee Validation**: Automatic verification against company records
- **Digital Signatures**: Enhanced security with verification elements
- **PDF Generation**: High-quality document output with ReportLab

### 🔐 **Security & Authentication**
- **OTP-based Login**: Secure email-based authentication system
- **Session Management**: Robust session handling with automatic logout
- **Input Validation**: Comprehensive security measures
- **Content Filtering**: Bad language detection and moderation
- **Middleware Protection**: Route-level authentication enforcement

## 🏗️ Architecture

### Frontend (Next.js 14)
- **Framework**: Next.js 14 with React 18 and TypeScript
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion for smooth interactions
- **State Management**: React hooks with context
- **Authentication**: Middleware-based route protection

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.12.0
- **AI Integration**: Google Gemini 2.0 Flash Exp
- **Semantic Search**: Sentence Transformers with local embeddings
- **Document Processing**: PyMuPDF, PDFPlumber, OpenCV, ReportLab
- **Database**: MongoDB Atlas (cloud) with local JSON fallbacks

### AI & ML Components
- **Hybrid QA Engine**: Combines semantic search with generative AI
- **Document Analysis**: Intelligent PDF structure analysis
- **Employee Validation**: Fuzzy matching and data verification
- **Content Filtering**: Bad language detection and moderation
- **Model Management**: AI models automatically downloaded on first run (not stored in Git)

## 🛠️ Technology Stack

### Frontend Technologies
```json
{
  "next": "14.2.3",
  "react": "18.3.1",
  "typescript": "5.6.2",
  "tailwindcss": "3.4.10",
  "framer-motion": "11.2.14",
  "lucide-react": "0.365.0",
  "react-hot-toast": "2.5.1",
  "axios": "^1.7.4",
  "react-dropzone": "^14.3.4"
}
```

### Backend Technologies
```python
# Core Framework
fastapi>=0.110,<1.0
uvicorn[standard]>=0.22,<1.0
python-dotenv>=1.0.0,<2.0

# AI & ML
google-generativeai>=0.8.0,<1.0
sentence-transformers>=2.2.2,<3.0
torch>=2.2,<3.0
transformers>=4.41,<5.0

# Document Processing
pymupdf>=1.23,<2.0
pdfplumber>=0.11,<1.0
opencv-python>=4.8,<5.0
pandas>=2.2,<3.0
reportlab>=4.0,<5.0
python-docx>=1.1,<2.0

# Security & Auth
PyJWT>=2.8,<3.0
passlib[bcrypt]>=1.7,<2.0
email-validator>=2.1,<3.0

# Database
motor>=3.3.0,<4.0
pymongo>=4.6.0,<5.0
```

## 📁 Project Structure

```
chatbot_project/
├── app/                          # Next.js frontend
│   ├── api/                      # API routes
│   │   ├── auth/                 # Authentication endpoints
│   │   │   ├── send-otp/         # OTP sending
│   │   │   ├── verify-otp/       # OTP verification
│   │   │   ├── me/               # User info
│   │   │   └── logout/           # Logout
│   │   ├── chat/                 # Chat functionality
│   │   ├── upload-pdf/           # PDF upload
│   │   ├── process-pdf/          # PDF processing
│   │   ├── download-summary-pdf/ # Summary download
│   │   ├── employee-search/      # Employee search
│   │   ├── employee-validate/    # Employee validation
│   │   ├── generate-document/    # Document generation
│   │   └── health/               # Health checks
│   ├── login/                    # Login page
│   ├── page.tsx                  # Main application
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Global styles
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── routers/              # API route handlers
│   │   │   ├── auth.py           # Authentication
│   │   │   ├── chat.py           # Chat functionality
│   │   │   ├── advanced_qa.py    # Advanced Q&A
│   │   │   ├── documents.py      # Document processing
│   │   │   ├── gemini_documents.py # PDF summarization
│   │   │   ├── certificates.py   # Certificate generation
│   │   │   ├── document_requests.py # Document requests
│   │   │   └── health.py         # Health checks
│   │   ├── services/             # Business logic
│   │   │   ├── qa_engine.py      # Hybrid QA engine
│   │   │   ├── gemini_summarizer.py # PDF summarization
│   │   │   ├── document_pdf_generator.py # Document generation
│   │   │   ├── certificate_generator.py # Certificate generation
│   │   │   ├── employee_validator.py # Employee validation
│   │   │   ├── pdf_analyzer.py   # PDF analysis
│   │   │   ├── doc_parser.py     # Document parsing
│   │   │   ├── document_request_handler.py # Request handling
│   │   │   ├── summary_pdf_generator.py # Summary generation
│   │   │   ├── bad_language_filter.py # Content filtering
│   │   │   ├── keyword_extractor.py # Keyword extraction
│   │   │   └── db.py             # Database service
│   │   ├── data/                 # JSON data files
│   │   │   ├── employees.json    # Employee database (500+ records)
│   │   │   ├── qa_dataset.json   # Q&A knowledge base
│   │   │   ├── bad_words.json    # Content filter
│   │   │   ├── document_requests.json # Request tracking
│   │   │   └── hr_notifications.log # HR notifications
│   │   ├── config.py             # Configuration
│   │   └── main.py               # FastAPI application
│   └── requirements.txt          # Python dependencies
├── components/                   # React components
│   ├── ChatInterface.tsx         # Main chat interface
│   ├── DocumentForm.tsx          # Document request form
│   ├── PDFUploader.tsx           # PDF processing interface
│   ├── Header.tsx                # Application header
│   ├── ModeSelector.tsx          # Mode switching
│   ├── LoadingSpinner.tsx        # Loading indicators
│   ├── ErrorBoundary.tsx         # Error handling
│   └── ValidationFeedback.tsx    # Form validation
├── lib/                          # Utility functions
│   ├── types.ts                  # TypeScript type definitions
│   └── utils.ts                  # Helper functions
├── org_data/                     # Organization documents
│   ├── policies/                 # HR policy PDFs
│   │   ├── attendance_policy.pdf
│   │   ├── code_of_conduct.pdf
│   │   ├── employee_handbook.pdf
│   │   ├── leave_policy.pdf
│   │   ├── onboarding.pdf
│   │   ├── performance_review.pdf
│   │   ├── reimbursement_policy.pdf
│   │   └── wfh_policy.pdf
│   └── it_policies/              # IT policy documents
│       ├── acceptable_use_policy.pdf
│       ├── device_policy.pdf
│       ├── helpdesk_guide.pdf
│       ├── password_policy.pdf
│       └── software_request_sop.pdf
├── scripts/                      # Utility scripts
│   └── ingest_employees.py       # Employee data ingestion
├── middleware.ts                 # Authentication middleware
├── package.json                  # Frontend dependencies
├── requirements.txt              # Backend dependencies
└── README.md                     # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.12.0
- Google Gemini API key
- Git

### Frontend Setup
```bash
# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local
# Add your Google Gemini API key to .env.local

# Start development server
npm run dev
```

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_GEMINI_API_KEY="your-api-key-here"

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Note**: AI models (Sentence Transformers) will be automatically downloaded on first run (~100MB). This may take a few minutes depending on your internet connection.

### Environment Variables

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NODE_ENV=development
```

#### Backend (.env)
```bash
# Google Gemini AI Configuration
GOOGLE_GEMINI_API_KEY=your-gemini-api-key-here

# Email Configuration (for OTP)
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

# JWT Security
JWT_SECRET=your-jwt-secret-key-change-in-production

# Backend Configuration
BACKEND_URL=http://localhost:8000
NODE_ENV=development

# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/hr_assistant?retryWrites=true&w=majority

# Optional Configuration
DISABLE_AUTH=false
ORG_NAME="Reliance Jio Infotech Solutions"
```

## 📋 API Endpoints

### Authentication
- `POST /api/auth/send-otp` - Send OTP to email
- `POST /api/auth/verify-otp` - Verify OTP and login
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user

### Chat & Q&A
- `POST /api/chat` - Send chat message
- `GET /api/advanced-qa/health` - QA system health check
- `POST /api/advanced-qa/query` - Advanced Q&A queries

### Document Processing
- `POST /api/upload-pdf` - Upload PDF for processing
- `POST /api/process-pdf` - Process uploaded PDF
- `GET /api/download-summary-pdf` - Download processed summary

### Document Generation
- `POST /api/generate-document` - Generate official documents
- `GET /api/employee-search` - Search employees
- `POST /api/employee-validate` - Validate employee data
- `GET /api/employee-by-id` - Get employee by ID

## 🎯 Core Features Deep Dive

### 1. Hybrid QA Engine
The system uses a sophisticated hybrid approach combining:
- **Semantic Search**: Local embeddings using Sentence Transformers for fast policy lookups
- **Generative AI**: Google Gemini 2.0 Flash Exp for contextual responses
- **Knowledge Base**: 500+ curated Q&A pairs with company policies
- **Fallback System**: Graceful degradation when AI services are unavailable

### 2. Advanced PDF Processing Pipeline
```python
# Comprehensive PDF processing workflow
1. Document Upload → File validation & size check (up to 50MB)
2. Structure Analysis → Intelligent content detection
3. Table Extraction → Advanced table detection and formatting
4. Content Chunking → Intelligent text segmentation
5. AI Processing → Gemini 2.0 summarization with context
6. Result Generation → Comprehensive summaries with tables
7. Output Delivery → Formatted results with download options
```

### 3. Document Generation System
- **16 Document Types**: Bonafide letters, experience certificates, offer letters, etc.
- **Professional Templates**: Company-branded design with ReportLab
- **Employee Validation**: Fuzzy matching against 500+ employee records
- **Digital Security**: Enhanced verification elements and signatures
- **Quality Assurance**: Comprehensive error handling and validation

### 4. Employee Management
- **500+ Employee Records**: Comprehensive database with real data
- **Fuzzy Search**: Handles name variations and typos
- **Multi-field Validation**: Employee ID, email, department verification
- **Real-time Feedback**: Instant validation results
- **Data Integrity**: Ensures accurate employee information

## 🎨 UI/UX Features

### Modern Design System
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Smooth Animations**: Framer Motion integration for fluid interactions
- **Accessibility**: WCAG compliant components
- **Error Handling**: Graceful error boundaries and user feedback

### Interactive Components
- **Real-time Chat**: Live message updates with typing indicators
- **Progress Tracking**: Upload and processing status with visual feedback
- **Toast Notifications**: User feedback system with react-hot-toast
- **Modal Dialogs**: Contextual information display
- **Form Validation**: Real-time validation with visual feedback

## 🔒 Security Features

### Authentication & Authorization
- **OTP-based Login**: Secure email verification system
- **Session Management**: Automatic timeout and logout
- **Middleware Protection**: Route-level authentication enforcement
- **CSRF Protection**: Built-in security measures
- **Input Sanitization**: XSS prevention

### Data Protection
- **Secure File Upload**: File type and size validation
- **Content Filtering**: Bad language detection and moderation
- **API Rate Limiting**: Request throttling
- **Error Handling**: Secure error responses
- **Environment Variables**: Secure configuration management

## 📊 Data Management

### Employee Database
- **500+ Records**: Comprehensive employee data with real information
- **Cloud Storage**: MongoDB Atlas (online database) - Employee data only
- **Local Storage**: JSON files for QA dataset, bad words, and document requests
- **Search Optimization**: Indexed for fast queries
- **Data Validation**: Integrity checks and fuzzy matching

### Policy Documents
- **16 Policy Types**: Complete HR and IT policy coverage
- **PDF Storage**: Organized document structure in org_data/
- **Version Control**: Document management
- **Access Control**: Role-based permissions

### Knowledge Base
- **500+ Q&A Pairs**: Curated knowledge base covering company policies
- **Semantic Search**: Fast retrieval using local embeddings
- **AI Enhancement**: Generative responses using Gemini 2.0
- **Continuous Learning**: Expandable knowledge base

## 🧪 Testing & Quality Assurance

### Code Quality
- **TypeScript**: Full type safety throughout the application
- **ESLint**: Code linting and formatting
- **Error Boundaries**: Graceful error handling
- **Logging**: Comprehensive system logging

### Performance Optimization
- **Code Splitting**: Dynamic imports for better performance
- **Image Optimization**: Next.js image optimization
- **Caching**: API response caching
- **Bundle Analysis**: Performance monitoring

## 👥 Development Team

### Team Members
1. **Devyani Suresh Deore** - Brand Manager (Marketing)
   - Frontend Development, UI/UX Design, Project Management

2. **Ashwini Anil Nikumbh** - Account Executive (Finance)
   - Backend Development, Database Design, API Development

3. **Khushbu Arun Jain** - HR Specialist (Human Resources)
   - AI Integration, Business Logic, Testing

4. **Mansi Anil Badgujar** - Software Engineer (IT)
   - Full Stack Development, DevOps, System Architecture

### Project Scope
This is a **college major project** demonstrating:
- Modern web development practices
- AI/ML integration in enterprise applications
- Collaborative development methodologies
- Real-world problem solving

## 🗄️ Database Architecture

### MongoDB Atlas Setup (Recommended)
For online database access, migrate to MongoDB Atlas:

```bash
# Install MongoDB dependencies
pip install motor pymongo

# Update your .env file with MongoDB URI
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/hr_assistant?retryWrites=true&w=majority
```

### MongoDB Atlas Benefits
- ✅ **Free Tier**: 512MB storage, perfect for college projects
- ✅ **Cloud Access**: Employee data accessible from anywhere
- ✅ **Auto-scaling**: Handles traffic spikes automatically
- ✅ **Backup & Security**: Built-in data protection
- ✅ **Real-time Sync**: Multiple users can access employee data simultaneously

### Hybrid Data Storage
- **Employee Data**: Stored in MongoDB Atlas (cloud)
- **QA Dataset**: Kept locally in JSON files for fast access
- **Bad Words**: Kept locally in JSON files
- **Document Requests**: Stored locally in JSON files

## 🚀 Deployment

### Production Setup
```bash
# Frontend Build
npm run build
npm start

# Backend Deployment
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Configuration
```bash
# Production environment variables
NODE_ENV=production
BACKEND_URL=https://your-backend-domain.com
GOOGLE_GEMINI_API_KEY=your-production-api-key
```

## 📈 Performance Metrics

### System Capabilities
- **Response Time**: < 2 seconds for chat responses
- **File Processing**: Up to 50MB PDFs with 30+ pages
- **Concurrent Users**: 100+ simultaneous users
- **Uptime**: 99.9% availability target

### AI Performance
- **Accuracy**: 95%+ for policy questions
- **Processing Speed**: 30+ page PDFs in < 5 minutes
- **Memory Usage**: Optimized for production deployment

## 🔧 Troubleshooting

### Common Issues
1. **API Connection Errors**: Check backend server status
2. **PDF Upload Failures**: Verify file size and format
3. **Authentication Issues**: Clear browser cache and cookies
4. **AI Response Delays**: Check Gemini API quota
5. **Model Download Issues**: Ensure stable internet connection for first-time model downloads

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
export LOG_LEVEL=DEBUG
```

## 📚 Documentation

### Additional Resources
- [API Documentation](http://localhost:8000/docs) - FastAPI auto-generated docs
- [Component Library](./components/) - React component documentation
- [Service Documentation](./backend/app/services/) - Backend service details

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is developed as a college major project for educational purposes. All rights reserved by the development team.

## 🤝 Support

For technical support or questions:
- **Email**: hr@reliancejio.com
- **Documentation**: See internal wiki
- **Issues**: Use GitHub issues for bug reports

---

**Built with ❤️ by the College Project Team**

*Advanced AI-Powered Document Processing & HR Q&A System*

**Team Members:**
- **Devyani Suresh Deore** - Brand Manager (Marketing)
- **Ashwini Anil Nikumbh** - Account Executive (Finance) 
- **Khushbu Arun Jain** - HR Specialist (Human Resources)
- **Mansi Anil Badgujar** - Software Engineer (IT)
