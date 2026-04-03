"""Configuration for SummarizerAgent project."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from google.genai import types

MODEL_NAME = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


def configure_google_api_key() -> None:
    """Load GOOGLE_API_KEY from .env/environment for local development."""
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY is not set. Add it to .env or environment variables.")
