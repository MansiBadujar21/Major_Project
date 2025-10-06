@echo off
echo 🚀 Starting Jio Chatbot Development Environment...
echo.

echo 📦 Installing frontend dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo 🐍 Installing backend dependencies...
cd backend
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    echo 💡 Make sure Python and pip are installed
    pause
    exit /b 1
)

cd ..
echo.
echo ✅ All dependencies installed successfully!
echo.
echo 🚀 Starting development servers...
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo.

call npm run dev
