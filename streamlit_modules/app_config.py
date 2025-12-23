"""
Configuration and constants for Streamlit app.
"""

import os
import streamlit as st
from typing import Optional

# AI Features (optional - requires OpenAI API key)
try:
    from src.lbo_ai_validator import LBOModelAIValidator
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


def get_openai_api_key() -> Optional[str]:
    """
    Get OpenAI API key from Streamlit secrets or environment variable.

    Returns:
        API key string or None if not found
    """
    try:
        # Try Streamlit secrets first (recommended for production)
        api_key = st.secrets.get("openai", {}).get("api_key") or os.getenv("OPENAI_API_KEY")
    except (AttributeError, FileNotFoundError):
        # Fallback to environment variable
        api_key = os.getenv("OPENAI_API_KEY")

    return api_key


def initialize_session_state():
    """Initialize session state variables."""
    if 'saved_scenarios' not in st.session_state:
        st.session_state.saved_scenarios = {}

    if 'current_results' not in st.session_state:
        st.session_state.current_results = None

    if 'current_inputs' not in st.session_state:
        st.session_state.current_inputs = {}
