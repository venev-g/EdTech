#!/usr/bin/env python3
"""
Quick start script for Avatar Teacher application.
Checks environment and provides guidance.
"""

import sys
import subprocess
import os


def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_venv():
    """Check if virtual environment is activated"""
    if not hasattr(sys, "real_prefix") and not (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("⚠️  Virtual environment not activated")
        print("   Run: source .venv/bin/activate")
        return False
    print("✓ Virtual environment activated")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required = ["fastapi", "uvicorn", "pymongo", "pydantic"]
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} not installed")

    if missing:
        print("\n⚠️  Install dependencies:")
        print("   pip install -r requirements.txt")
        return False

    return True


def check_mongodb():
    """Check MongoDB connection"""
    try:
        from pymongo import MongoClient

        client = MongoClient(
            "mongodb://localhost:27017/", serverSelectionTimeoutMS=2000
        )
        client.server_info()
        print("✓ MongoDB connected")
        return True
    except Exception:
        print("⚠️  MongoDB not accessible")
        print("   Configure MONGODB_URI or start MongoDB")
        return False


def main():
    """Run all checks and provide guidance"""
    print("🎓 Avatar Teacher - Quick Start Check")
    print("=" * 50)

    checks = {
        "Python Version": check_python_version(),
        "Virtual Environment": check_venv(),
        "Dependencies": check_dependencies(),
        "MongoDB": check_mongodb(),
    }

    print("\n" + "=" * 50)

    if all(checks.values()):
        print("✓ All checks passed!")
        print("\nReady to start:")
        print("   python -m uvicorn app.main:app --reload")
        print("\nOr use the run script:")
        print("   ./run.sh")
        print("\nAccess at: http://localhost:8000")
    else:
        print("⚠️  Some checks failed")
        print("\nSetup steps:")
        print("1. Create virtual environment: python3 -m venv .venv")
        print("2. Activate it: source .venv/bin/activate")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Ensure MongoDB is running")
        print("5. Run the app: ./run.sh")

    print("\n📖 See PROJECT_README.md for detailed instructions")


if __name__ == "__main__":
    main()
