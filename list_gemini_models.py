#!/usr/bin/env python3
"""List available Gemini models."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from google import genai
from config import Config

# Initialize Gemini client
client = genai.Client(api_key=Config.GEMINI_API_KEY)

print("Available Gemini Models:\n")
print("=" * 60)

# List models using new API
try:
    models = client.models.list()
    for model in models:
        print(f"\n✓ Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        if hasattr(model, 'description'):
            print(f"  Description: {model.description}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"  Supported Methods: {', '.join(model.supported_generation_methods)}")
except Exception as e:
    print(f"Error listing models: {e}")

print("\n" + "=" * 60)
