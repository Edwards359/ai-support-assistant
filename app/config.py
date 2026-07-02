"""Application settings, loaded from environment (.env supported via python-dotenv)."""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = os.environ.get("APP_NAME", "AI Support Assistant")
    # If set, llm_client will call OpenAI to word the draft reply;
    # otherwise it falls back to a deterministic template reply.
    openai_api_key: str | None = os.environ.get("OPENAI_API_KEY") or None
    openai_model: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
