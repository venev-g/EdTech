# Avatar Teacher - Talking Avatar Education Platform

A prototype web application featuring a talking avatar teacher that explains educational topics and answers frequently asked questions. Built with FastAPI, MongoDB, and vanilla JavaScript.

## Features

- 🎥 **Interactive Avatar Videos**: Looping avatar videos for engaging visual learning
- 🔊 **Audio Explanations**: Text-to-speech audio for topic content and FAQ answers
- ❓ **FAQ System**: Interactive FAQ section for each topic
- 🌐 **Multilingual Support**: Supports English, Hindi, and mixed-language content
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🚀 **RESTful API**: Clean API architecture for easy extension

## Project Structure

```
EdTech/
├── app/
│   ├── main.py           # FastAPI application entrypoint
│   ├── models.py         # Pydantic models for Topic and FAQ
│   ├── db.py             # MongoDB connection and helper functions
│   ├── seed_data.py      # Sample data seeding function
│   └── tts_stub.py       # TTS stub for prototype (hardcoded audio paths)
├── static/
│   ├── index.html        # Main UI
│   ├── app.js            # Frontend JavaScript
│   ├── styles.css        # CSS styling
│   └── media/
│       ├── avatar_loop.mp4    # Avatar video (placeholder)
│       └── audio/
│           ├── topic_1.mp3    # Topic audio files (placeholders)
│           ├── topic_2.mp3
│           ├── faq_1.mp3      # FAQ audio files (placeholders)
│           └── ...
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: MongoDB (document database)
- **Frontend**: HTML, CSS, vanilla JavaScript
- **Audio**: Stub TTS implementation (ready for real TTS integration)

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB running locally or connection string to MongoDB Atlas
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory**:

   ```bash
   cd /home/ubuntu/EdTech
   ```

2. **Create and activate virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB connection** (optional):

   By default, the app connects to `mongodb://localhost:27017/`

   To use a different connection string, set the environment variable:

   ```bash
   export MONGODB_URI="mongodb://your-connection-string"
   ```

5. **Add media files** (optional for full functionality):

   - Place an `avatar_loop.mp4` video in `static/media/`
   - Add MP3 audio files in `static/media/audio/`:
     - `topic_1.mp3`, `topic_2.mp3` (topic explanations)
     - `faq_1.mp3`, `faq_2.mp3`, `faq_3.mp3`, `faq_4.mp3` (FAQ answers)

   See the README files in those directories for more details.

### Running the Application

1. **Start the FastAPI server**:

   ```bash
   python -m app.main
   ```

   Or using uvicorn directly:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application**:

   - Open your browser and navigate to: `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`

3. **The application will**:
   - Automatically seed the database with sample topics on first run
   - Create 2 sample topics (English and Hindi)
   - Add 2-3 FAQs per topic

## API Endpoints

### Public Endpoints

- `GET /` - Serve the main HTML page
- `GET /api/topics` - List all topics (minimal info)
- `GET /api/topics/{topic_id}` - Get topic details with FAQs
- `GET /api/faqs/{faq_id}` - Get FAQ details
- `GET /health` - Health check endpoint

### Admin Endpoints

- `POST /api/topics` - Create a new topic
- `POST /api/faqs` - Create a new FAQ

### Example API Calls

**Get all topics**:

```bash
curl http://localhost:8000/api/topics
```

**Get topic with FAQs**:

```bash
curl http://localhost:8000/api/topics/{topic_id}
```

**Create a new topic**:

```bash
curl -X POST http://localhost:8000/api/topics \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Web Development Basics",
    "content_text": "Learn the fundamentals of web development...",
    "language": "en"
  }'
```

## Usage

1. **Select a Topic**: Click on a topic from the sidebar
2. **Watch & Listen**: The avatar video plays and topic audio begins
3. **View FAQs**: After the topic audio finishes, FAQs appear
4. **Ask Questions**: Click on any FAQ to hear the answer

## Data Model

### Topics Collection

```javascript
{
  "_id": ObjectId,
  "title": String,
  "content_text": String,
  "language": String,        // "en", "hi", or "mixed"
  "audio_url": String,
  "avatar_video_url": String,
  "created_at": DateTime,
  "updated_at": DateTime
}
```

### FAQs Collection

```javascript
{
  "_id": ObjectId,
  "topic_id": String,        // Reference to topics._id
  "question": String,
  "answer": String,
  "language": String,
  "answer_audio_url": String,
  "created_at": DateTime,
  "updated_at": DateTime
}
```

## Extending the Application

### Adding Real TTS

The current implementation uses a stub TTS function. To integrate real TTS:

1. **Edit `app/tts_stub.py`**:

   - Implement `generate_tts_real()` function
   - Use services like:
     - Google Cloud Text-to-Speech
     - Amazon Polly
     - Azure Cognitive Services
     - gTTS (Google Text-to-Speech library)
     - pyttsx3 (offline TTS)

2. **Example with gTTS**:

   ```python
   from gtts import gTTS

   def generate_tts_real(text, language, output_path):
       tts = gTTS(text=text, lang=language)
       tts.save(output_path)
       return output_path
   ```

3. **Update the stub functions** to call the real TTS implementation

### Adding More Topics

You can add topics via:

1. **API** (recommended):

   ```bash
   curl -X POST http://localhost:8000/api/topics \
     -H "Content-Type: application/json" \
     -d '{"title": "...", "content_text": "...", "language": "en"}'
   ```

2. **Directly in MongoDB**:

   - Use MongoDB Compass or mongo shell
   - Insert into the `topics` collection

3. **Edit seed_data.py**:
   - Add more topics in the `seed_database()` function
   - Clear and re-seed: `python -m app.seed_data`

### Customizing the UI

- **Colors**: Edit CSS variables in `static/styles.css` (`:root` section)
- **Layout**: Modify `static/index.html`
- **Behavior**: Update `static/app.js`

## Development Notes

- The app uses hardcoded audio file paths for the prototype
- Audio files should be placed in `static/media/audio/`
- Video file should be in `static/media/avatar_loop.mp4`
- MongoDB connection is established on startup
- Database is seeded only if empty (safe to restart)

## Troubleshooting

**MongoDB connection error**:

- Ensure MongoDB is running: `sudo systemctl status mongod`
- Check connection string in environment or `app/db.py`

**Audio/Video not playing**:

- Check that media files exist in the correct paths
- Check browser console for 404 errors
- Verify file formats (MP4 for video, MP3 for audio)

**Port already in use**:

- Change the port: `uvicorn app.main:app --port 8001`
- Or kill the process using port 8000

## Future Enhancements

- [ ] Real-time TTS generation
- [ ] User authentication and progress tracking
- [ ] Quiz/assessment features
- [ ] Video recording and upload for custom avatars
- [ ] Multi-language UI (not just content)
- [ ] Mobile app version
- [ ] Analytics and learning insights
- [ ] Admin dashboard for content management

## License

This is a prototype application for educational purposes.

## Contact

For questions or suggestions, please refer to the project repository.
