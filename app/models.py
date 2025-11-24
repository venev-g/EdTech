"""
Pydantic models for Topic and FAQ data structures.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TopicBase(BaseModel):
    """Base model for Topic with common fields."""

    title: str
    content_text: str
    language: str  # "en", "hi", or "mixed"
    audio_url: Optional[str] = None
    avatar_video_url: str = "/static/media/avatar_loop.mp4"


class TopicCreate(TopicBase):
    """Model for creating a new topic."""

    pass


class TopicListItem(BaseModel):
    """Minimal topic info for list view."""

    id: str
    title: str
    language: str


class Topic(TopicBase):
    """Full topic model with ID and timestamps."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "Introduction to Python",
                "content_text": "Python is a high-level programming language...",
                "language": "en",
                "audio_url": "/static/media/audio/topic_1.mp3",
                "avatar_video_url": "/static/media/avatar_loop.mp4",
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
            }
        }


class FAQBase(BaseModel):
    """Base model for FAQ with common fields."""

    topic_id: str
    question: str
    answer: str
    language: str
    answer_audio_url: Optional[str] = None


class FAQCreate(FAQBase):
    """Model for creating a new FAQ."""

    pass


class FAQListItem(BaseModel):
    """Minimal FAQ info for list view."""

    id: str
    question: str
    answer_audio_url: Optional[str] = None


class FAQ(FAQBase):
    """Full FAQ model with ID and timestamps."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439012",
                "topic_id": "507f1f77bcf86cd799439011",
                "question": "What is Python used for?",
                "answer": "Python is used for web development, data analysis...",
                "language": "en",
                "answer_audio_url": "/static/media/audio/faq_1.mp3",
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
            }
        }


class TopicWithFAQs(Topic):
    """Topic model with associated FAQs."""

    faqs: List[FAQListItem] = []
