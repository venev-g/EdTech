"""
Seed data module to populate the database with sample topics and FAQs.
This runs on application startup if the database is empty.
"""

from app.db import get_topics_collection, get_faqs_collection, insert_topic, insert_faq


def seed_database():
    """
    Insert sample topics and FAQs into the database if collections are empty.
    Creates 2 topics with 2-3 FAQs each in English and Hindi.
    """
    topics_collection = get_topics_collection()
    faqs_collection = get_faqs_collection()

    # Check if data already exists
    if topics_collection.count_documents({}) > 0:
        print("Database already contains topics. Skipping seed.")
        return

    print("Seeding database with sample data...")

    # Topic 1: Introduction to Python (English)
    topic1_id = insert_topic(
        title="Introduction to Python Programming",
        content_text=(
            "Python is a high-level, interpreted programming language known for its "
            "simplicity and readability. It was created by Guido van Rossum and first "
            "released in 1991. Python supports multiple programming paradigms including "
            "procedural, object-oriented, and functional programming. It is widely used "
            "for web development, data analysis, artificial intelligence, scientific "
            "computing, and automation."
        ),
        language="en",
        audio_url="/static/media/audio/topic_1.mp3",
    )

    # FAQs for Topic 1
    insert_faq(
        topic_id=topic1_id,
        question="What is Python used for?",
        answer=(
            "Python is used for a wide variety of applications including web development "
            "with frameworks like Django and Flask, data analysis and visualization with "
            "libraries like Pandas and Matplotlib, machine learning and AI with TensorFlow "
            "and PyTorch, automation and scripting, scientific computing, and much more."
        ),
        language="en",
        answer_audio_url="/static/media/audio/faq_1.mp3",
    )

    insert_faq(
        topic_id=topic1_id,
        question="Is Python difficult to learn?",
        answer=(
            "Python is considered one of the easiest programming languages to learn for "
            "beginners. Its syntax is clean and readable, resembling natural English. "
            "The language emphasizes code readability and simplicity, making it an excellent "
            "choice for those new to programming."
        ),
        language="en",
        answer_audio_url="/static/media/audio/faq_2.mp3",
    )

    insert_faq(
        topic_id=topic1_id,
        question="What are the advantages of Python?",
        answer=(
            "Python offers many advantages: it has simple and easy-to-learn syntax, "
            "extensive standard library and third-party packages, strong community support, "
            "cross-platform compatibility, excellent for rapid prototyping, and versatility "
            "across different domains like web, data science, and automation."
        ),
        language="en",
        answer_audio_url="/static/media/audio/faq_3.mp3",
    )

    # Topic 2: डेटा साइंस का परिचय (Introduction to Data Science in Hindi)
    topic2_id = insert_topic(
        title="डेटा साइंस का परिचय",
        content_text=(
            "डेटा साइंस एक बहु-विषयक क्षेत्र है जो डेटा से ज्ञान और अंतर्दृष्टि निकालने के लिए "
            "वैज्ञानिक तरीकों, प्रक्रियाओं, एल्गोरिदम और सिस्टम का उपयोग करता है। यह सांख्यिकी, "
            "गणित, कंप्यूटर विज्ञान और डोमेन विशेषज्ञता को जोड़ता है। डेटा साइंस का उपयोग व्यावसायिक "
            "निर्णय लेने, पूर्वानुमान मॉडलिंग, पैटर्न पहचान और बहुत कुछ के लिए किया जाता है।"
        ),
        language="hi",
        audio_url="/static/media/audio/topic_2.mp3",
    )

    # FAQs for Topic 2
    insert_faq(
        topic_id=topic2_id,
        question="डेटा साइंस क्यों महत्वपूर्ण है?",
        answer=(
            "डेटा साइंस महत्वपूर्ण है क्योंकि यह संगठनों को बड़ी मात्रा में डेटा से मूल्यवान "
            "अंतर्दृष्टि प्राप्त करने में मदद करता है। यह बेहतर निर्णय लेने, ग्राहक व्यवहार को "
            "समझने, व्यावसायिक प्रक्रियाओं को अनुकूलित करने और प्रतिस्पर्धात्मक लाभ प्राप्त करने "
            "में सहायता करता है।"
        ),
        language="hi",
        answer_audio_url="/static/media/audio/faq_4.mp3",
    )

    insert_faq(
        topic_id=topic2_id,
        question="डेटा साइंटिस्ट बनने के लिए क्या स्किल्स चाहिए?",
        answer=(
            "डेटा साइंटिस्ट बनने के लिए आपको प्रोग्रामिंग (Python, R), सांख्यिकी और गणित, "
            "मशीन लर्निंग, डेटा विज़ुअलाइज़ेशन, डेटाबेस और SQL, तथा डोमेन नॉलेज की आवश्यकता होती है। "
            "साथ ही समस्या-समाधान और विश्लेषणात्मक सोच भी महत्वपूर्ण हैं।"
        ),
        language="hi",
        answer_audio_url="/static/media/audio/faq_1.mp3",
    )

    print(f"✓ Created topic: {topic1_id} with 3 FAQs")
    print(f"✓ Created topic: {topic2_id} with 2 FAQs")
    print("Database seeding completed successfully!")


def clear_database():
    """
    Clear all data from the database.
    Use with caution - this will delete all topics and FAQs!
    """
    topics_collection = get_topics_collection()
    faqs_collection = get_faqs_collection()

    topics_result = topics_collection.delete_many({})
    faqs_result = faqs_collection.delete_many({})

    print(f"Deleted {topics_result.deleted_count} topics")
    print(f"Deleted {faqs_result.deleted_count} FAQs")
    print("Database cleared!")


if __name__ == "__main__":
    # Allow running this script directly for testing
    seed_database()
