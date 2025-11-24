# 🎓 Avatar Teacher - Getting Started Checklist

## ✅ Pre-Flight Checklist

### 1. Environment Setup

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Virtual environment activated (`source .venv/bin/activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] MongoDB running or connection string configured

### 2. Project Files Verification

- [ ] All files present in correct directories
- [ ] Scripts are executable (`chmod +x *.sh`)
- [ ] No import errors (check with `python quick_start.py`)

### 3. Media Files (Optional but Recommended)

- [ ] Avatar video at `static/media/avatar_loop.mp4`
- [ ] Audio files in `static/media/audio/`:
  - [ ] topic_1.mp3 (English - Python intro)
  - [ ] topic_2.mp3 (Hindi - Data Science intro)
  - [ ] faq_1.mp3, faq_2.mp3, faq_3.mp3, faq_4.mp3

## 🚀 Launch Sequence

### Option A: Automated Setup (Recommended)

```bash
./setup.sh    # Complete setup including dependencies
./run.sh      # Start the server
```

### Option B: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Testing Steps

### 1. Backend API Test

```bash
# Check if server is running
curl http://localhost:8000/health

# Should return: {"status": "healthy", "service": "avatar-teacher-api"}
```

### 2. Database Test

```bash
# Get topics list
curl http://localhost:8000/api/topics

# Should return 2 topics (Python & Data Science)
```

### 3. Frontend Test

- [ ] Open http://localhost:8000 in browser
- [ ] See welcome screen with 4 features
- [ ] See 2 topics in sidebar (with language badges)
- [ ] Click first topic
- [ ] Video player appears (may show error if no video file)
- [ ] Topic content displays
- [ ] Audio player appears (may show error if no audio file)
- [ ] FAQ section appears (after audio or immediately)
- [ ] Click an FAQ
- [ ] FAQ answer appears in purple card

### 4. API Documentation Test

- [ ] Open http://localhost:8000/docs
- [ ] See Swagger UI with all endpoints
- [ ] Try "GET /api/topics" endpoint
- [ ] See JSON response with topics

## 📝 First Use Walkthrough

### Expected Behavior (Without Media Files)

1. **Server starts** → Database seeded with 2 topics + 5 FAQs
2. **Open browser** → Welcome screen appears
3. **Click topic** → UI updates, video/audio show placeholder/error
4. **FAQs appear** → Can click to view answers
5. **Switch topics** → Works normally

### Expected Behavior (With Media Files)

1. **Server starts** → Database seeded
2. **Open browser** → Welcome screen
3. **Click topic** → Video plays, audio plays
4. **Wait for audio** → FAQs appear after audio ends
5. **Click FAQ** → FAQ audio plays, video continues looping
6. **Switch topics** → New video/audio plays

## 🎨 Adding Media Files

### Quick Test (No Real Files)

The app works without media files for testing the UI and API.

### Adding Avatar Video

```bash
# Option 1: Use a sample video (any MP4)
cp your_video.mp4 static/media/avatar_loop.mp4

# Option 2: Create a placeholder
# Use any video editing software to create a 10-second loop
```

### Generating Audio Files

```bash
# Install gTTS
pip install gtts

# Run the generator
python generate_sample_audio.py

# Or manually create with gTTS
python -c "from gtts import gTTS; gTTS('Hello').save('static/media/audio/test.mp3')"
```

### Manual Audio Creation

- Use online TTS: https://ttsmp3.com/
- Or record your own audio
- Or use professional TTS services

## 🐛 Troubleshooting

### Problem: "MongoDB connection failed"

**Solution:**

- Check MongoDB is running: `sudo systemctl status mongod`
- Or start it: `sudo systemctl start mongod`
- Or use MongoDB Atlas and set MONGODB_URI

### Problem: "Port 8000 already in use"

**Solution:**

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --port 8001
```

### Problem: "Import errors"

**Solution:**

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: "Video/Audio not playing"

**Solution:**

- Check files exist: `ls static/media/ static/media/audio/`
- Check browser console for 404 errors
- For development, the app works without media files

### Problem: "Database not seeding"

**Solution:**

```bash
# Manually run seed script
python -c "from app.seed_data import seed_database; seed_database()"

# Or clear and re-seed
python -c "from app.seed_data import clear_database, seed_database; clear_database(); seed_database()"
```

## 📚 Next Steps

### Phase 1: Test the Prototype

- [x] Install and run
- [ ] Test all features
- [ ] Try creating topics via API
- [ ] Test on mobile browser

### Phase 2: Add Real Content

- [ ] Add your avatar video
- [ ] Generate or record audio files
- [ ] Add more topics and FAQs
- [ ] Customize styling (colors, fonts)

### Phase 3: Integrate Real TTS

- [ ] Choose TTS service (gTTS, AWS Polly, Azure, etc.)
- [ ] Implement in `app/tts_stub.py`
- [ ] Test audio generation
- [ ] Update database with new audio URLs

### Phase 4: Production Ready

- [ ] Set up production MongoDB (Atlas)
- [ ] Configure environment variables
- [ ] Add user authentication (optional)
- [ ] Deploy to server/cloud
- [ ] Add monitoring and logging
- [ ] Set up SSL/HTTPS

## 🎯 Quick Commands Reference

```bash
# Setup
./setup.sh

# Run server
./run.sh

# Check environment
python quick_start.py

# Generate audio
python generate_sample_audio.py

# Manual run
source .venv/bin/activate
uvicorn app.main:app --reload

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/api/topics

# View logs
# Logs appear in terminal where server is running

# Stop server
# Press Ctrl+C in terminal
```

## 📖 Documentation Quick Links

- **Setup Guide**: `PROJECT_README.md`
- **Quick Overview**: `SUMMARY.md`
- **File Structure**: `PROJECT_STRUCTURE.txt`
- **This Checklist**: `GETTING_STARTED.md`
- **API Docs**: http://localhost:8000/docs (when running)

## ✨ Success Criteria

You'll know it's working when:

- ✅ Server starts without errors
- ✅ Can access http://localhost:8000
- ✅ See 2 topics in sidebar
- ✅ Can click topics and see content
- ✅ FAQs appear and are clickable
- ✅ API returns JSON at /api/topics

## 🎉 You're Ready!

The Avatar Teacher platform is now set up and ready for:

- ✅ Development
- ✅ Testing
- ✅ Demonstration
- ✅ Feature additions
- ✅ Production deployment (with media files)

Happy teaching! 🎓

---

**Need help?** Check the troubleshooting section above or review the comprehensive documentation in `PROJECT_README.md`.
