"""
Text-to-Speech implementation using gTTS (Google Text-to-Speech).
Generates audio files dynamically from text content.
Falls back to hardcoded paths if gTTS is not available or fails.
"""

from typing import Dict, Any
import hashlib
from pathlib import Path


# Mapping of topic/FAQ identifiers to hardcoded audio files
TOPIC_AUDIO_MAP = {
    "1": "/static/media/audio/topic_1.mp3",
    "2": "/static/media/audio/topic_2.mp3",
}

FAQ_AUDIO_MAP = {
    "1": "/static/media/audio/faq_1.mp3",
    "2": "/static/media/audio/faq_2.mp3",
    "3": "/static/media/audio/faq_3.mp3",
    "4": "/static/media/audio/faq_4.mp3",
}


def _get_audio_index(text: str, max_index: int) -> str:
    """
    Generate a consistent index based on text hash.
    This ensures the same text always maps to the same audio file.
    """
    hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
    return str((hash_val % max_index) + 1)


def _generate_audio_filename(text: str, prefix: str = "audio") -> str:
    """
    Generate a unique filename based on text content hash.

    Args:
        text: Text content to hash
        prefix: Filename prefix (e.g., "topic", "faq")

    Returns:
        str: Filename like "topic_abc123def.mp3"
    """
    # Create a hash of the text for unique filename
    text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
    return f"{prefix}_{text_hash}.mp3"


def _ensure_audio_directory() -> Path:
    """
    Ensure the audio directory exists.

    Returns:
        Path: Path to the audio directory
    """
    audio_dir = Path("static/media/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)
    return audio_dir


def generate_tts_audio(
    text: str, language: str = "en", output_filename: str = None
) -> str:
    """
    Generate audio file from text using gTTS.

    Args:
        text: Text to convert to speech
        language: Language code ("en" for English, "hi" for Hindi, etc.)
        output_filename: Optional specific filename to use

    Returns:
        str: URL path to the generated audio file (e.g., "/static/media/audio/file.mp3")

    Raises:
        ImportError: If gTTS is not installed
        Exception: If audio generation fails
    """
    try:
        from gtts import gTTS

        # Ensure audio directory exists
        audio_dir = _ensure_audio_directory()

        # Generate filename if not provided
        if not output_filename:
            output_filename = _generate_audio_filename(text, "tts")

        # Full path to save the audio file
        output_path = audio_dir / output_filename

        # Check if file already exists to avoid regenerating
        if output_path.exists():
            print(f"[TTS] Using existing audio: {output_filename}")
            return f"/static/media/audio/{output_filename}"

        # Generate speech
        print(
            f"[TTS] Generating audio for text (length: {len(text)} chars, language: {language})..."
        )
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(str(output_path))

        print(f"[TTS] ✓ Audio generated: {output_filename}")
        return f"/static/media/audio/{output_filename}"

    except ImportError:
        print("[TTS] ERROR: gTTS not installed. Install with: pip install gtts")
        raise
    except Exception as e:
        print(f"[TTS] ERROR: Failed to generate audio: {e}")
        raise


def get_or_generate_audio_for_topic(topic: Dict[str, Any]) -> str:
    """
    Get or generate audio URL for a topic.

    Implementation:
    1. Check if audio_url already exists in topic
    2. If not, generate unique filename based on content
    3. Check if audio file already exists
    4. If not, generate audio using gTTS
    5. Save the audio file to static/media/audio/
    6. Return the URL path

    Args:
        topic: Dictionary containing topic data (must have 'id', 'title', 'content_text', 'language')

    Returns:
        str: URL path to the audio file
    """
    # If audio_url is already set, return it
    if topic.get("audio_url"):
        return topic["audio_url"]

    title = topic.get("title", "Unknown Topic")
    content_text = topic.get("content_text", "")
    language = topic.get("language", "en")

    # Try to generate audio using gTTS
    try:
        # Generate unique filename based on content
        filename = _generate_audio_filename(content_text, "topic")
        audio_url = generate_tts_audio(content_text, language, filename)
        print(f"[TTS] Generated audio for topic '{title}': {audio_url}")
        return audio_url

    except ImportError:
        # Fallback to hardcoded paths if gTTS not installed
        print(f"[TTS] Falling back to hardcoded audio for topic '{title}'")
        index = _get_audio_index(title, len(TOPIC_AUDIO_MAP))
        audio_url = TOPIC_AUDIO_MAP.get(index, "/static/media/audio/topic_1.mp3")
        return audio_url

    except Exception as e:
        # Fallback on any error
        print(f"[TTS] Error generating audio, using fallback: {e}")
        index = _get_audio_index(title, len(TOPIC_AUDIO_MAP))
        audio_url = TOPIC_AUDIO_MAP.get(index, "/static/media/audio/topic_1.mp3")
        return audio_url


def get_or_generate_audio_for_faq(faq: Dict[str, Any]) -> str:
    """
    Get or generate audio URL for an FAQ answer.

    Implementation:
    1. Check if answer_audio_url already exists
    2. If not, generate unique filename based on answer content
    3. Check if audio file already exists
    4. If not, generate audio using gTTS for the answer text
    5. Save the audio file to static/media/audio/
    6. Return the URL path

    Args:
        faq: Dictionary containing FAQ data (must have 'question', 'answer', 'language')

    Returns:
        str: URL path to the audio file
    """
    # If answer_audio_url is already set, return it
    if faq.get("answer_audio_url"):
        return faq["answer_audio_url"]

    question = faq.get("question", "Unknown Question")
    answer = faq.get("answer", "")
    language = faq.get("language", "en")

    # Try to generate audio using gTTS
    try:
        # Generate unique filename based on answer content
        filename = _generate_audio_filename(answer, "faq")
        audio_url = generate_tts_audio(answer, language, filename)
        print(f"[TTS] Generated audio for FAQ '{question}': {audio_url}")
        return audio_url

    except ImportError:
        # Fallback to hardcoded paths if gTTS not installed
        print(f"[TTS] Falling back to hardcoded audio for FAQ '{question}'")
        index = _get_audio_index(question, len(FAQ_AUDIO_MAP))
        audio_url = FAQ_AUDIO_MAP.get(index, "/static/media/audio/faq_1.mp3")
        return audio_url

    except Exception as e:
        # Fallback on any error
        print(f"[TTS] Error generating audio, using fallback: {e}")
        index = _get_audio_index(question, len(FAQ_AUDIO_MAP))
        audio_url = FAQ_AUDIO_MAP.get(index, "/static/media/audio/faq_1.mp3")
        return audio_url


def clear_generated_audio() -> int:
    """
    Clear all generated TTS audio files (keep fallback files).
    Useful for regenerating audio with different settings.

    Returns:
        int: Number of files deleted
    """
    audio_dir = Path("static/media/audio")
    if not audio_dir.exists():
        return 0

    count = 0
    # Delete files that match the generated pattern (topic_*, faq_*, tts_*)
    for pattern in ["topic_*.mp3", "faq_*.mp3", "tts_*.mp3"]:
        for file in audio_dir.glob(pattern):
            # Don't delete the numbered fallback files (topic_1.mp3, topic_2.mp3, etc.)
            if not file.stem.split("_")[-1].isdigit():
                file.unlink()
                count += 1
                print(f"[TTS] Deleted: {file.name}")

    return count
