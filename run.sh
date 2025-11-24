#!/bin/bash
# Run script for Avatar Teacher application

echo "🎓 Starting Avatar Teacher Application..."
echo "========================================"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Run: source .venv/bin/activate"
    exit 1
fi

# Check if MongoDB is running (local)
if command -v mongod &> /dev/null; then
    if ! pgrep -x mongod > /dev/null; then
        echo "⚠️  MongoDB doesn't appear to be running locally"
        echo "   Make sure MongoDB is running or configure MONGODB_URI"
    fi
fi

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Dependencies not installed!"
    echo "Run: pip install -r requirements.txt"
    exit 1
fi

echo "✓ Environment checks passed"
echo ""
echo "Starting FastAPI server..."
echo "Access the app at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Run the application
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
