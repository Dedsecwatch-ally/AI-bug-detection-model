#!/bin/bash
# start-dev.sh - Start the full development stack

echo "🚀 AI Bug Finder - Full Stack Startup"
echo "======================================"
echo ""
echo "This script will open 2 terminals:"
echo "1. FastAPI backend"
echo "2. React frontend (Vite)"
echo ""
echo "Prerequisites:"
echo "- Ollama installed and models downloaded: ollama list"
echo "- Python venv setup: cd backend && python3 -m venv venv"
echo "- Node packages installed: cd web-ui && npm install"
echo ""

echo "Starting backend..."
cd backend
PYTHONPATH=$(pwd) ./venv/bin/python -m uvicorn src.app:app --port 8000 &
BACKEND_PID=$!
sleep 2

echo ""
echo "Starting frontend..."
cd ../web-ui
npx vite &
FRONTEND_PID=$!

echo ""
echo "✅ Stack is starting!"
echo ""
echo "Frontend:  http://localhost:5173"
echo "Backend:   http://localhost:8000"
echo "Ollama:    (no longer required)"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
wait
