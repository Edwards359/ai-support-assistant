"""Optionally rewrites the deterministic draft reply in a friendlier tone via an LLM.

Without OPENAI_API_KEY, the deterministic template from support_service.py is
used as-is — no network call, safe to run out of the box. The category and
priority decision is never delegated to the model (see support_service.py).
"""
from __future__ import annotations

from app.config import settings


def polish_reply(message: str, category: str, draft_reply: str) -> str:
    if not settings.openai_api_key:
        return draft_reply

    try:
        from openai import OpenAI  # type: ignore[import-not-found]
    except ImportError:
        return draft_reply

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты сотрудник поддержки. Перепиши черновик ответа клиенту дружелюбнее, "
                    "сохранив весь смысл. Не придумывай новых фактов и не меняй категорию проблемы."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Категория: {category}\nСообщение клиента: {message}\n"
                    f"Черновик ответа: {draft_reply}"
                ),
            },
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or draft_reply
