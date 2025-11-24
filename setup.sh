#!/bin/bash
# Complete setup script for Avatar Teacher application

echo "╔════════════════════════════════════════════════╗"
echo "║   🎓 Avatar Teacher - Complete Setup         ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    echo "   Please run this script from the EdTech directory"
    exit 1
fi

# Step 1: Virtual Environment
echo "📦 Step 1: Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "   ✓ Virtual environment created"
else
    echo "   ✓ Virtual environment already exists"
fi

# Step 2: Activate and install
echo ""
echo "📥 Step 2: Installing dependencies..."
source .venv/bin/activate

pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "   ✓ All dependencies installed successfully"
else
    echo "   ❌ Failed to install dependencies"
    exit 1
fi

# Step 3: Check MongoDB
echo ""
echo "🔍 Step 3: Checking MongoDB..."
if command -v mongosh &> /dev/null; then
    if mongosh --eval "db.version()" --quiet &> /dev/null; then
        echo "   ✓ MongoDB is running and accessible"
    else
        echo "   ⚠️  MongoDB CLI found but can't connect"
        echo "      Make sure MongoDB is running"
    fi
elif command -v mongo &> /dev/null; then
    if mongo --eval "db.version()" --quiet &> /dev/null; then
        echo "   ✓ MongoDB is running and accessible"
    else
        echo "   ⚠️  MongoDB CLI found but can't connect"
        echo "      Make sure MongoDB is running"
    fi
else
    echo "   ⚠️  MongoDB CLI not found"
    echo "      Install MongoDB or use MongoDB Atlas"
    echo "      Set MONGODB_URI environment variable for remote connection"
fi

# Step 4: Check Python imports
echo ""
echo "🐍 Step 4: Verifying Python packages..."
python -c "import fastapi, uvicorn, pymongo, pydantic" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ All Python packages imported successfully"
else
    echo "   ❌ Some packages failed to import"
    exit 1
fi

# Step 5: Optional - Generate audio files
echo ""
echo "🔊 Step 5: Audio files (optional)..."
if python -c "import gtts" 2>/dev/null; then
    echo "   ✓ gTTS is installed"
    read -p "   Generate sample audio files? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python generate_sample_audio.py
    fi
else
    echo "   ℹ️  gTTS not installed (optional)"
    echo "      To generate audio: pip install gtts && python generate_sample_audio.py"
    echo "      Or add your own MP3 files to static/media/audio/"
fi

# Summary
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                           ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "🚀 Quick Start:"
echo "   1. Start the server:"
echo "      ./run.sh"
echo ""
echo "   2. Open your browser:"
echo "      http://localhost:8000"
echo ""
echo "   3. View API documentation:"
echo "      http://localhost:8000/docs"
echo ""
echo "📚 Documentation:"
echo "   - PROJECT_README.md (comprehensive guide)"
echo "   - SUMMARY.md (quick overview)"
echo ""
echo "💡 Tips:"
echo "   - Add avatar_loop.mp4 to static/media/"
echo "   - Add audio files or run generate_sample_audio.py"
echo "   - Check quick_start.py for environment status"
echo ""
echo "Happy teaching! 🎓"
