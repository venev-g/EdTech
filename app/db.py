"""
MongoDB database connection and helper functions.
"""

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional, Dict, Any
from datetime import datetime
import os

load_dotenv()  # Load environment variables from .env file

# MongoDB connection string - can be configured via environment variable
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "edtech_avatar_teacher"

# Global client instance
_client: Optional[MongoClient] = None
_db: Optional[Database] = None


def get_db() -> Database:
    """
    Get MongoDB database instance.
    Creates connection if it doesn't exist.
    """
    global _client, _db

    if _db is None:
        _client = MongoClient(MONGODB_URI)
        _db = _client[DATABASE_NAME]

    return _db


def get_topics_collection() -> Collection:
    """Get the topics collection."""
    return get_db()["topics"]


def get_faqs_collection() -> Collection:
    """Get the FAQs collection."""
    return get_db()["faqs"]


def close_db():
    """Close the MongoDB connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None


def object_id_to_str(doc: Optional[Dict[Any, Any]]) -> Optional[Dict[str, Any]]:
    """
    Convert MongoDB document's ObjectId to string.
    Returns None if doc is None.
    """
    if doc is None:
        return None

    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]

    return doc


def validate_object_id(id_str: str) -> bool:
    """Check if a string is a valid ObjectId."""
    try:
        ObjectId(id_str)
        return True
    except Exception:
        return False


def insert_topic(
    title: str,
    content_text: str,
    language: str,
    audio_url: Optional[str] = None,
    avatar_video_url: str = "/static/media/avatar_loop.mp4",
) -> str:
    """
    Insert a new topic into the database.
    Returns the inserted topic's ID as a string.
    """
    topics = get_topics_collection()
    now = datetime.utcnow()

    topic_doc = {
        "title": title,
        "content_text": content_text,
        "language": language,
        "audio_url": audio_url,
        "avatar_video_url": avatar_video_url,
        "created_at": now,
        "updated_at": now,
    }

    result = topics.insert_one(topic_doc)
    return str(result.inserted_id)


def insert_faq(
    topic_id: str,
    question: str,
    answer: str,
    language: str,
    answer_audio_url: Optional[str] = None,
) -> str:
    """
    Insert a new FAQ into the database.
    Returns the inserted FAQ's ID as a string.
    """
    faqs = get_faqs_collection()
    now = datetime.utcnow()

    faq_doc = {
        "topic_id": topic_id,
        "question": question,
        "answer": answer,
        "language": language,
        "answer_audio_url": answer_audio_url,
        "created_at": now,
        "updated_at": now,
    }

    result = faqs.insert_one(faq_doc)
    return str(result.inserted_id)


def update_topic_audio(topic_id: str, audio_url: str) -> bool:
    """
    Update the audio_url for a topic.
    Returns True if successful, False otherwise.
    """
    topics = get_topics_collection()
    result = topics.update_one(
        {"_id": ObjectId(topic_id)},
        {"$set": {"audio_url": audio_url, "updated_at": datetime.utcnow()}},
    )
    return result.modified_count > 0


def update_faq_audio(faq_id: str, answer_audio_url: str) -> bool:
    """
    Update the answer_audio_url for an FAQ.
    Returns True if successful, False otherwise.
    """
    faqs = get_faqs_collection()
    result = faqs.update_one(
        {"_id": ObjectId(faq_id)},
        {
            "$set": {
                "answer_audio_url": answer_audio_url,
                "updated_at": datetime.utcnow(),
            }
        },
    )
    return result.modified_count > 0


def get_topic_by_id(topic_id: str) -> Optional[Dict[str, Any]]:
    """Get a topic by its ID."""
    if not validate_object_id(topic_id):
        return None

    topics = get_topics_collection()
    topic = topics.find_one({"_id": ObjectId(topic_id)})
    return object_id_to_str(topic)


def get_faq_by_id(faq_id: str) -> Optional[Dict[str, Any]]:
    """Get an FAQ by its ID."""
    if not validate_object_id(faq_id):
        return None

    faqs = get_faqs_collection()
    faq = faqs.find_one({"_id": ObjectId(faq_id)})
    return object_id_to_str(faq)


def get_all_topics() -> list:
    """Get all topics (minimal info for list view)."""
    topics = get_topics_collection()
    result = []
    for topic in topics.find():
        result.append(
            {
                "id": str(topic["_id"]),
                "title": topic["title"],
                "language": topic["language"],
            }
        )
    return result


def get_faqs_by_topic_id(topic_id: str) -> list:
    """Get all FAQs for a specific topic."""
    faqs = get_faqs_collection()
    result = []
    for faq in faqs.find({"topic_id": topic_id}):
        result.append(
            {
                "id": str(faq["_id"]),
                "question": faq["question"],
                "answer_audio_url": faq.get("answer_audio_url"),
            }
        )
    return result
