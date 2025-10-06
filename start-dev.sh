#!/bin/bash

echo "🚀 Starting Jio Chatbot Development Environment..."
echo

echo "📦 Installing frontend dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

echo
echo "🐍 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    echo "💡 Make sure Python and pip are installed"
    exit 1
fi

cd ..
echo
echo "✅ All dependencies installed successfully!"
echo
echo "🚀 Starting development servers..."
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo

npm run dev
