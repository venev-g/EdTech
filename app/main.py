"""
FastAPI main application for the Avatar Teacher platform.
Serves API endpoints and static files for the talking avatar teacher app.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List

from app.models import TopicCreate, Topic, TopicListItem, TopicWithFAQs, FAQCreate, FAQ
from app.db import (
    get_topic_by_id,
    get_faq_by_id,
    get_all_topics,
    get_faqs_by_topic_id,
    insert_topic,
    insert_faq,
    update_topic_audio,
    update_faq_audio,
    close_db,
)
from app.tts_stub import get_or_generate_audio_for_topic, get_or_generate_audio_for_faq
from app.seed_data import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Seeds the database on startup and closes connections on shutdown.
    """
    # Startup: seed database if empty
    print("Starting up Avatar Teacher API...")
    seed_database()

    yield

    # Shutdown: close database connections
    print("Shutting down Avatar Teacher API...")
    close_db()


# Initialize FastAPI app
app = FastAPI(
    title="Avatar Teacher API",
    description="API for a talking avatar teacher that explains topics and answers FAQs",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# API Routes
# ============================================================================


@app.get("/", response_class=FileResponse)
async def serve_index():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")


@app.get("/api/topics", response_model=List[TopicListItem])
async def list_topics():
    """
    Get a list of all available topics.
    Returns minimal topic info: id, title, language.
    """
    topics = get_all_topics()
    return topics


@app.get("/api/topics/{topic_id}", response_model=TopicWithFAQs)
async def get_topic(topic_id: str):
    """
    Get a specific topic by ID along with its FAQs.

    - Fetches topic from database
    - If audio_url is empty, generates it using TTS stub
    - Fetches all associated FAQs
    - Returns complete topic data with FAQs
    """
    # Get topic from database
    topic = get_topic_by_id(topic_id)

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id {topic_id} not found",
        )

    # Generate audio if not present
    if not topic.get("audio_url"):
        audio_url = get_or_generate_audio_for_topic(topic)
        update_topic_audio(topic_id, audio_url)
        topic["audio_url"] = audio_url

    # Get FAQs for this topic
    faqs = get_faqs_by_topic_id(topic_id)
    topic["faqs"] = faqs

    return topic


@app.get("/api/faqs/{faq_id}", response_model=FAQ)
async def get_faq(faq_id: str):
    """
    Get a specific FAQ by ID.

    - Fetches FAQ from database
    - If answer_audio_url is empty, generates it using TTS stub
    - Returns complete FAQ data
    """
    # Get FAQ from database
    faq = get_faq_by_id(faq_id)

    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FAQ with id {faq_id} not found",
        )

    # Generate audio if not present
    if not faq.get("answer_audio_url"):
        audio_url = get_or_generate_audio_for_faq(faq)
        update_faq_audio(faq_id, audio_url)
        faq["answer_audio_url"] = audio_url

    return faq


@app.post("/api/topics", response_model=Topic, status_code=status.HTTP_201_CREATED)
async def create_topic(topic: TopicCreate):
    """
    Create a new topic (admin endpoint).

    - Accepts topic data in request body
    - Automatically generates audio_url using TTS if not provided
    - Inserts into database
    - Returns the created topic with audio URL
    """
    # Insert topic into database
    topic_id = insert_topic(
        title=topic.title,
        content_text=topic.content_text,
        language=topic.language,
        audio_url=topic.audio_url,
        avatar_video_url=topic.avatar_video_url,
    )

    # Get the created topic
    created_topic = get_topic_by_id(topic_id)

    # Generate audio if not provided (check for None, empty string, or missing key)
    audio_url = created_topic.get("audio_url")
    if not audio_url or audio_url.strip() == "":
        print(f"[API] Generating audio for new topic (ID: {topic_id})...")
        try:
            audio_url = get_or_generate_audio_for_topic(created_topic)
            update_topic_audio(topic_id, audio_url)
            created_topic["audio_url"] = audio_url
            print(f"[API] ✓ Audio generated successfully: {audio_url}")
        except Exception as e:
            print(f"[API] ⚠️  Warning: Failed to generate audio for topic: {e}")
            # Don't fail the request if audio generation fails
            # The topic is still created successfully

    return created_topic


@app.post("/api/faqs", response_model=FAQ, status_code=status.HTTP_201_CREATED)
async def create_faq(faq: FAQCreate):
    """
    Create a new FAQ (admin endpoint).

    - Accepts FAQ data in request body
    - Automatically generates answer_audio_url using TTS if not provided
    - Inserts into database
    - Returns the created FAQ with audio URL
    """
    # Verify that the topic exists
    topic = get_topic_by_id(faq.topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id {faq.topic_id} not found",
        )

    # Insert FAQ into database
    faq_id = insert_faq(
        topic_id=faq.topic_id,
        question=faq.question,
        answer=faq.answer,
        language=faq.language,
        answer_audio_url=faq.answer_audio_url,
    )

    # Get the created FAQ
    created_faq = get_faq_by_id(faq_id)

    # Generate audio if not provided (check for None, empty string, or missing key)
    answer_audio_url = created_faq.get("answer_audio_url")
    if not answer_audio_url or answer_audio_url.strip() == "":
        print(f"[API] Generating audio for new FAQ (ID: {faq_id})...")
        try:
            audio_url = get_or_generate_audio_for_faq(created_faq)
            update_faq_audio(faq_id, audio_url)
            created_faq["answer_audio_url"] = audio_url
            print(f"[API] ✓ Audio generated successfully: {audio_url}")
        except Exception as e:
            print(f"[API] ⚠️  Warning: Failed to generate audio for FAQ: {e}")
            # Don't fail the request if audio generation fails
            # The FAQ is still created successfully

    return created_faq


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "avatar-teacher-api"}


# Mount static files (must be last to avoid route conflicts)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
