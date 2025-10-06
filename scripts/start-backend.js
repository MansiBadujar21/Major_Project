#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.log('Starting FastAPI Backend Server...');

// Change to backend directory
const backendDir = path.join(__dirname, '..', 'backend');

// Start the FastAPI server using uvicorn
const backendProcess = spawn('uvicorn', ['app.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'], {
  cwd: backendDir,
  stdio: 'inherit',
  shell: true
});

backendProcess.on('error', (error) => {
  console.error('Failed to start backend server:', error.message);
  console.log('Make sure you have Python and uvicorn installed:');
  console.log('   pip install -r requirements.txt');
  process.exit(1);
});

backendProcess.on('exit', (code) => {
  if (code !== 0) {
    console.error(`Backend server exited with code ${code}`);
    process.exit(code);
  }
});

// Handle process termination
process.on('SIGINT', () => {
  console.log('\nShutting down backend server...');
  backendProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  console.log('\nShutting down backend server...');
  backendProcess.kill('SIGTERM');
});
