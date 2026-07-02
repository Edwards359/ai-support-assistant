"""Pydantic request/response models for the support triage API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class SupportRequestIn(BaseModel):
    message: str = Field(..., min_length=1)
    customer_id: str | None = None
    channel: str | None = None


class SupportAnalysis(BaseModel):
    category: str
    priority: str
    suggested_reply: str
    needs_human_review: bool
