"""Deterministic keyword-based triage: category + priority for a support message.

No LLM calls here — classification must be predictable and explainable to a
support team. Only the reply *wording* (llm_client.py) may optionally use an
LLM; the category/priority decision never does.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

CATEGORIES = ("account_access", "billing", "bug_report", "feature_request", "general_inquiry")

_CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "account_access": (
        "access",
        "login",
        "log in",
        "password",
        "account",
        "войти",
        "вход",
        "пароль",
        "доступ",
        "логин",
    ),
    "billing": (
        "invoice",
        "billing",
        "payment",
        "charge",
        "refund",
        "subscription",
        "оплат",
        "счет",
        "счёт",
        "возврат",
        "платеж",
        "платёж",
    ),
    "bug_report": (
        "bug",
        "error",
        "crash",
        "broken",
        "not working",
        "doesn't work",
        "ошибка",
        "не работает",
        "баг",
        "падает",
    ),
    "feature_request": (
        "feature",
        "would be nice",
        "please add",
        "suggestion",
        "предложение",
        "добавьте",
        "хотелось бы",
    ),
}

_URGENT_WORDS = (
    "urgent",
    "asap",
    "immediately",
    "critical",
    "срочно",
    "немедленно",
    "критично",
)


def _matches_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def classify_category(message: str) -> str:
    text = message.lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        if _matches_any(text, keywords):
            return category
    return "general_inquiry"


def classify_priority(message: str, category: str) -> str:
    text = message.lower()
    if _matches_any(text, _URGENT_WORDS) or "!!!" in message:
        return "high"
    if category in ("account_access", "billing", "bug_report"):
        return "high"
    if category == "feature_request":
        return "low"
    return "medium"


_TEMPLATES: dict[str, str] = {
    "account_access": (
        "It looks like you are having trouble accessing your account. Please try logging out "
        "from all devices and resetting your password using the 'Forgot password' link. Let us "
        "know if that does not resolve it."
    ),
    "billing": (
        "Thanks for reaching out about billing. We are looking into your account and will follow "
        "up with the details of the charge/refund shortly."
    ),
    "bug_report": (
        "Sorry for the trouble — thanks for reporting this. Could you share the exact steps to "
        "reproduce the issue (and a screenshot, if possible)? We will investigate right away."
    ),
    "feature_request": (
        "Thanks for the suggestion! We have logged this as a feature request and will consider it "
        "for a future release."
    ),
    "general_inquiry": (
        "Thanks for reaching out. Could you share a few more details so we can help you faster?"
    ),
}


def draft_reply(category: str) -> str:
    return _TEMPLATES.get(category, _TEMPLATES["general_inquiry"])


def needs_human_review(category: str, priority: str) -> bool:
    # High-priority tickets and anything outside the well-covered templates
    # go to a human — a wrong automated reply is worse than a short delay.
    return priority == "high" or category == "general_inquiry"


@dataclass
class SupportAnalysisResult:
    category: str
    priority: str
    suggested_reply: str
    needs_human_review: bool


_WS_RE = re.compile(r"\s+")


def analyze_message(message: str) -> SupportAnalysisResult:
    normalized = _WS_RE.sub(" ", message).strip()
    category = classify_category(normalized)
    priority = classify_priority(normalized, category)
    return SupportAnalysisResult(
        category=category,
        priority=priority,
        suggested_reply=draft_reply(category),
        needs_human_review=needs_human_review(category, priority),
    )
