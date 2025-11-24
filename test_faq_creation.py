"""
Test script to verify FAQ creation and audio generation.
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_create_faq():
    """Test creating a new FAQ and check if audio is generated."""

    # First, get an existing topic ID
    print("1. Fetching topics...")
    response = requests.get(f"{BASE_URL}/api/topics")
    topics = response.json()

    if not topics:
        print("❌ No topics found. Please seed the database first.")
        return

    topic_id = topics[0]["id"]
    print(f"   ✓ Using topic ID: {topic_id}")

    # Create a new FAQ without answer_audio_url
    print("\n2. Creating new FAQ without audio_url...")
    new_faq = {
        "topic_id": topic_id,
        "question": "Test question: What is the capital of France?",
        "answer": "The capital of France is Paris, a beautiful city known for its art, culture, and history.",
        "language": "en",
        # Note: NOT providing answer_audio_url
    }

    response = requests.post(
        f"{BASE_URL}/api/faqs",
        json=new_faq,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 201:
        print(f"❌ Failed to create FAQ: {response.status_code}")
        print(f"   Response: {response.text}")
        return

    created_faq = response.json()
    faq_id = created_faq["id"]
    print(f"   ✓ FAQ created with ID: {faq_id}")

    # Check if audio_url was generated
    print("\n3. Checking if audio was generated...")
    answer_audio_url = created_faq.get("answer_audio_url")

    if answer_audio_url:
        print(f"   ✓ Audio URL generated: {answer_audio_url}")
    else:
        print(f"   ❌ No audio URL in response!")
        print(f"   Response: {json.dumps(created_faq, indent=2)}")
        return

    # Fetch the FAQ again to verify
    print("\n4. Fetching FAQ to verify persistence...")
    response = requests.get(f"{BASE_URL}/api/faqs/{faq_id}")

    if response.status_code != 200:
        print(f"❌ Failed to fetch FAQ: {response.status_code}")
        return

    fetched_faq = response.json()
    fetched_audio_url = fetched_faq.get("answer_audio_url")

    if fetched_audio_url:
        print(f"   ✓ Audio URL in database: {fetched_audio_url}")
    else:
        print(f"   ❌ No audio URL in database!")
        print(f"   Response: {json.dumps(fetched_faq, indent=2)}")
        return

    print("\n✅ TEST PASSED: FAQ audio generation working correctly!")


if __name__ == "__main__":
    try:
        test_create_faq()
    except requests.exceptions.ConnectionError:
        print(
            "❌ Could not connect to server. Make sure it's running on http://localhost:8000"
        )
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
