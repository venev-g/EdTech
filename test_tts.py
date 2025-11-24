#!/usr/bin/env python3
"""
Test script for TTS functionality.
Demonstrates audio generation with gTTS.
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))


def test_tts_installation():
    """Check if gTTS is installed."""
    try:
        import gtts

        print("✓ gTTS is installed")
        return True
    except ImportError:
        print("✗ gTTS not installed")
        print("  Install with: pip install gtts")
        return False


def test_audio_generation():
    """Test generating audio files."""
    from app.tts_stub import generate_tts_audio, _ensure_audio_directory

    print("\nTesting audio generation...")
    print("-" * 50)

    # Ensure directory exists
    _ensure_audio_directory()

    # Test 1: English audio
    try:
        text_en = "Hello! This is a test of the text-to-speech system."
        url = generate_tts_audio(text_en, "en", "test_english.mp3")
        print(f"✓ English audio generated: {url}")
    except Exception as e:
        print(f"✗ Failed to generate English audio: {e}")

    # Test 2: Hindi audio
    try:
        text_hi = "नमस्ते! यह टेक्स्ट-टू-स्पीच सिस्टम का परीक्षण है।"
        url = generate_tts_audio(text_hi, "hi", "test_hindi.mp3")
        print(f"✓ Hindi audio generated: {url}")
    except Exception as e:
        print(f"✗ Failed to generate Hindi audio: {e}")

    # Test 3: Check files exist
    audio_dir = Path("static/media/audio")
    files = list(audio_dir.glob("test_*.mp3"))
    print(f"\n✓ Generated {len(files)} test audio files")
    for f in files:
        size = f.stat().st_size / 1024  # KB
        print(f"  - {f.name} ({size:.1f} KB)")


def test_topic_audio():
    """Test topic audio generation."""
    from app.tts_stub import get_or_generate_audio_for_topic

    print("\nTesting topic audio generation...")
    print("-" * 50)

    # Sample topic
    topic = {
        "id": "test123",
        "title": "Test Topic",
        "content_text": "This is a test topic for demonstrating audio generation.",
        "language": "en",
    }

    try:
        url = get_or_generate_audio_for_topic(topic)
        print(f"✓ Topic audio URL: {url}")

        # Check if file exists
        file_path = Path(url.lstrip("/"))
        if file_path.exists():
            size = file_path.stat().st_size / 1024
            print(f"  File size: {size:.1f} KB")
    except Exception as e:
        print(f"✗ Failed: {e}")


def test_faq_audio():
    """Test FAQ audio generation."""
    from app.tts_stub import get_or_generate_audio_for_faq

    print("\nTesting FAQ audio generation...")
    print("-" * 50)

    # Sample FAQ
    faq = {
        "id": "faq123",
        "question": "What is this test about?",
        "answer": "This is a test to demonstrate FAQ audio generation using text-to-speech.",
        "language": "en",
    }

    try:
        url = get_or_generate_audio_for_faq(faq)
        print(f"✓ FAQ audio URL: {url}")

        # Check if file exists
        file_path = Path(url.lstrip("/"))
        if file_path.exists():
            size = file_path.stat().st_size / 1024
            print(f"  File size: {size:.1f} KB")
    except Exception as e:
        print(f"✗ Failed: {e}")


def main():
    """Run all tests."""
    print("=" * 50)
    print("TTS Functionality Test")
    print("=" * 50)

    if not test_tts_installation():
        print("\nPlease install gTTS first:")
        print("  pip install gtts")
        return

    test_audio_generation()
    test_topic_audio()
    test_faq_audio()

    print("\n" + "=" * 50)
    print("Testing complete!")
    print("=" * 50)

    # List all generated files
    audio_dir = Path("static/media/audio")
    if audio_dir.exists():
        all_files = list(audio_dir.glob("*.mp3"))
        if all_files:
            print(f"\nAll audio files in {audio_dir}:")
            for f in sorted(all_files):
                size = f.stat().st_size / 1024
                print(f"  - {f.name} ({size:.1f} KB)")


if __name__ == "__main__":
    main()
