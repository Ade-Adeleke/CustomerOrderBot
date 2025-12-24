#!/usr/bin/env python
"""
Entry point to run the TechGear Pro Customer Support Chatbot
Usage: streamlit run run.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the app module - this runs the Streamlit code
import src.app
