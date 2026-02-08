#!/bin/bash

# Market Research App - Full Setup and Start Script
# Usage: ./start.sh

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$PROJECT_DIR/MarketResearchUI"
VENV_DIR="$PROJECT_DIR/venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  Market Research App - Setup & Start"
echo "=========================================="

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Node.js found: $(node --version)"

if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} npm found: $(npm --version)"

# Check for .env file
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "\n${YELLOW}No .env file found.${NC}"
    read -p "Enter your OpenAI API key: " api_key
    echo "OPENAI_API_KEY=$api_key" > "$PROJECT_DIR/.env"
    echo -e "${GREEN}✓${NC} Created .env file"
else
    echo -e "${GREEN}✓${NC} .env file exists"
fi

# Setup Python virtual environment
echo -e "\n${YELLOW}Setting up Python environment...${NC}"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r "$PROJECT_DIR/requirements.txt"
echo -e "${GREEN}✓${NC} Python dependencies installed"

# Setup Node.js frontend
echo -e "\n${YELLOW}Setting up frontend...${NC}"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "Installing Node dependencies (this may take a minute)..."
    cd "$FRONTEND_DIR"
    npm install --silent
    cd "$PROJECT_DIR"
    echo -e "${GREEN}✓${NC} Node dependencies installed"
else
    echo -e "${GREEN}✓${NC} Node dependencies exist"
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo -e "${GREEN}✓${NC} Servers stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo -e "\n${YELLOW}Starting backend server...${NC}"
cd "$PROJECT_DIR"
python api_backend.py &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Backend running at http://localhost:8000"
        break
    fi
    sleep 1
done

# Start frontend
echo -e "\n${YELLOW}Starting frontend server...${NC}"
cd "$FRONTEND_DIR"
npm start &
FRONTEND_PID=$!

echo -e "\n${GREEN}=========================================="
echo "  Application is running!"
echo "==========================================${NC}"
echo ""
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo ""

# Wait for processes
wait
