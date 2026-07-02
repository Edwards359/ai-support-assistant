"""API routes: analyze a support request, list known categories."""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas import SupportAnalysis, SupportRequestIn
from app.services.llm_client import polish_reply
from app.services.support_service import CATEGORIES, analyze_message

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/support/categories")
def list_categories() -> list[str]:
    return list(CATEGORIES)


@router.post("/support/analyze", response_model=SupportAnalysis)
def analyze_support_request(payload: SupportRequestIn) -> SupportAnalysis:
    result = analyze_message(payload.message)
    reply = polish_reply(payload.message, result.category, result.suggested_reply)
    return SupportAnalysis(
        category=result.category,
        priority=result.priority,
        suggested_reply=reply,
        needs_human_review=result.needs_human_review,
    )
