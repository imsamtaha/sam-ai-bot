#!/bin/bash

# Sam AI Bot - Build Script
# Builds and prepares the project for deployment

set -e  # Exit on error

echo "🏗️  Building Sam AI Bot..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Python version
echo -e "${BLUE}Step 1: Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Step 2: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Step 2: Creating virtual environment...${NC}"
    python -m venv venv
    echo "Virtual environment created"
else
    echo -e "${BLUE}Step 2: Virtual environment already exists${NC}"
fi
echo ""

# Step 3: Activate virtual environment
echo -e "${BLUE}Step 3: Activating virtual environment...${NC}"
source venv/bin/activate
echo "Virtual environment activated"
echo ""

# Step 4: Install dependencies
echo -e "${BLUE}Step 4: Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "Dependencies installed"
echo ""

# Step 5: Run linting and formatting checks
echo -e "${BLUE}Step 5: Running code quality checks...${NC}"
if command -v black &> /dev/null; then
    echo "Running Black formatter..."
    black . --check --diff || true
fi

if command -v flake8 &> /dev/null; then
    echo "Running Flake8 linter..."
    flake8 . --max-line-length=120 || true
fi

if command -v isort &> /dev/null; then
    echo "Running isort..."
    isort . --check-only --diff || true
fi

if command -v mypy &> /dev/null; then
    echo "Running MyPy type checker..."
    mypy . --ignore-missing-imports || true
fi
echo ""

# Step 6: Build completion message
echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Create .env file: cp .env.example .env"
echo "2. Update .env with your API keys"
echo "3. Run the bot: python main.py"
echo "4. Or run tests: ./test.sh"
echo ""