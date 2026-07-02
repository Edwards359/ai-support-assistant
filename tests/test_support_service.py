from app.services.support_service import analyze_message


def test_account_access_example_from_readme() -> None:
    result = analyze_message("I can't access my account after password reset.")
    assert result.category == "account_access"
    assert result.priority == "high"
    assert result.needs_human_review is True


def test_billing_message_classified_and_high_priority() -> None:
    result = analyze_message("I was charged twice for my subscription, please refund me.")
    assert result.category == "billing"
    assert result.priority == "high"


def test_feature_request_is_low_priority_and_not_flagged() -> None:
    result = analyze_message("It would be nice to have a dark mode, please add it.")
    assert result.category == "feature_request"
    assert result.priority == "low"
    assert result.needs_human_review is False


def test_urgent_wording_forces_high_priority_even_for_general_message() -> None:
    result = analyze_message("This is urgent, I need help right now!")
    assert result.priority == "high"


def test_unclassified_message_falls_back_to_general_inquiry_and_human_review() -> None:
    result = analyze_message("Just wanted to say hello and ask a general question.")
    assert result.category == "general_inquiry"
    assert result.needs_human_review is True


def test_russian_account_access_message() -> None:
    result = analyze_message("Не могу войти в аккаунт после смены пароля.")
    assert result.category == "account_access"
    assert result.priority == "high"
