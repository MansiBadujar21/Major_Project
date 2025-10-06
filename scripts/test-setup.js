#!/usr/bin/env node

const { spawn } = require('child_process');
const http = require('http');

console.log('🧪 Testing Unified Development Setup...\n');

// Test function to check if a port is listening
function testPort(port, name) {
  return new Promise((resolve) => {
    const req = http.request({
      hostname: 'localhost',
      port: port,
      path: '/',
      method: 'GET',
      timeout: 2000
    }, (res) => {
      console.log(`✅ ${name} is running on port ${port}`);
      resolve(true);
    });

    req.on('error', () => {
      console.log(`❌ ${name} is not running on port ${port}`);
      resolve(false);
    });

    req.on('timeout', () => {
      console.log(`⏰ ${name} timeout on port ${port}`);
      resolve(false);
    });

    req.end();
  });
}

// Test both ports
async function testSetup() {
  console.log('Testing ports...\n');
  
  const frontendRunning = await testPort(3000, 'Frontend (Next.js)');
  const backendRunning = await testPort(8000, 'Backend (FastAPI)');
  
  console.log('\n📊 Test Results:');
  console.log(`Frontend: ${frontendRunning ? '✅ Running' : '❌ Not Running'}`);
  console.log(`Backend: ${backendRunning ? '✅ Running' : '❌ Not Running'}`);
  
  if (frontendRunning && backendRunning) {
    console.log('\n🎉 Unified development setup is working correctly!');
    console.log('🌐 Frontend: http://localhost:3000');
    console.log('🔧 Backend: http://localhost:8000');
    console.log('📚 API Docs: http://localhost:8000/docs');
  } else {
    console.log('\n⚠️ Some services are not running. Please check:');
    if (!frontendRunning) {
      console.log('   - Frontend: Make sure Next.js is installed and running');
    }
    if (!backendRunning) {
      console.log('   - Backend: Make sure Python dependencies are installed');
      console.log('   - Run: npm run install:backend');
    }
  }
}

testSetup();
