#!/usr/bin/env python3
"""
Generate sample audio files using gTTS (Google Text-to-Speech).
This is optional - the app will work without real audio files.

Usage:
    pip install gtts
    python generate_sample_audio.py
"""

try:
    from gtts import gTTS
    import os

    AUDIO_DIR = "static/media/audio"

    # Ensure directory exists
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Sample texts for audio generation
    audio_content = {
        "topic_1.mp3": {
            "text": (
                "Python is a high-level, interpreted programming language known for its "
                "simplicity and readability. It was created by Guido van Rossum and first "
                "released in 1991. Python supports multiple programming paradigms including "
                "procedural, object-oriented, and functional programming. It is widely used "
                "for web development, data analysis, artificial intelligence, scientific "
                "computing, and automation."
            ),
            "lang": "en",
        },
        "topic_2.mp3": {
            "text": (
                "डेटा साइंस एक बहु-विषयक क्षेत्र है जो डेटा से ज्ञान और अंतर्दृष्टि निकालने के लिए "
                "वैज्ञानिक तरीकों, प्रक्रियाओं, एल्गोरिदम और सिस्टम का उपयोग करता है।"
            ),
            "lang": "hi",
        },
        "faq_1.mp3": {
            "text": (
                "Python is used for a wide variety of applications including web development "
                "with frameworks like Django and Flask, data analysis and visualization with "
                "libraries like Pandas and Matplotlib, machine learning and AI with TensorFlow "
                "and PyTorch, automation and scripting, scientific computing, and much more."
            ),
            "lang": "en",
        },
        "faq_2.mp3": {
            "text": (
                "Python is considered one of the easiest programming languages to learn for "
                "beginners. Its syntax is clean and readable, resembling natural English."
            ),
            "lang": "en",
        },
        "faq_3.mp3": {
            "text": (
                "Python offers many advantages: it has simple and easy-to-learn syntax, "
                "extensive standard library and third-party packages, strong community support, "
                "cross-platform compatibility, and excellent for rapid prototyping."
            ),
            "lang": "en",
        },
        "faq_4.mp3": {
            "text": (
                "डेटा साइंस महत्वपूर्ण है क्योंकि यह संगठनों को बड़ी मात्रा में डेटा से मूल्यवान "
                "अंतर्दृष्टि प्राप्त करने में मदद करता है।"
            ),
            "lang": "hi",
        },
    }

    print("Generating sample audio files using gTTS...")
    print("-" * 50)

    for filename, content in audio_content.items():
        output_path = os.path.join(AUDIO_DIR, filename)

        if os.path.exists(output_path):
            print(f"⊘ Skipping {filename} (already exists)")
            continue

        try:
            tts = gTTS(text=content["text"], lang=content["lang"], slow=False)
            tts.save(output_path)
            print(f"✓ Generated {filename}")
        except Exception as e:
            print(f"✗ Failed to generate {filename}: {e}")

    print("-" * 50)
    print("Audio generation complete!")
    print(f"Files saved in: {AUDIO_DIR}")

except ImportError:
    print("gTTS library not installed.")
    print("To generate audio files, run: pip install gtts")
    print("\nAlternatively, you can:")
    print("1. Use online TTS services to generate MP3 files")
    print("2. Record your own audio")
    print("3. Use other TTS libraries (pyttsx3, Azure Speech, etc.)")
    print("\nThe app will work without real audio files (for development).")
except Exception as e:
    print(f"Error: {e}")
