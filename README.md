## 🇷🇺 Обзор для заказчика

**AI Support Assistant** — AI‑ассистент для первичной обработки support‑запросов.

- **Для чего:** снять часть нагрузки с команды поддержки за счёт автоматического триажа и черновиков ответов.
- **Что делает:** принимает текст обращения, определяет категорию и приоритет, формирует draft‑ответ и помечает, нужен ли человеческий просмотр.
- **Где полезен:** customer support, helpdesk, service desk, внутренняя поддержка сотрудников.
- **Пример кейса:** клиент пишет “не могу войти после смены пароля” → ассистент помечает запрос как `account_access`, ставит высокий приоритет и предлагает вежливый черновик ответа.

Дальше в README показано:
- как API вписывается в существующий support‑workflow,
- какие поля возвращает анализ (category, priority, suggested_reply, needs_human_review),
- где остаётся human‑in‑the‑loop и как можно дообучать промпты под тон и политику компании.

---

# AI Support Assistant
_First-line support request analysis API_

## Overview
AI Support Assistant is a backend template for automating the first step in customer support:  
it accepts incoming support messages, classifies them, assigns a priority, and generates a draft reply.

## Business problem
Support teams handle many repetitive, low-complexity requests.  
Agents spend time triaging tickets and writing similar responses again and again.

## Solution
This project provides a clean API that:
- analyzes a support message,
- predicts a category and priority,
- generates a draft reply,
- signals whether a human should review the answer.

It is designed as a starting point for support intake automation and “AI triage”.

## Key features
- **Support request analysis** via `/support/analyze`
- **Category and priority suggestion**
- **Draft reply generation (prompt-based)**
- **Explicit `needs_human_review` flag**
- **FastAPI API** that can sit in front of your helpdesk system

## Architecture

```text
User Request
  ↓
Support Analyzer (FastAPI)
  ↓
Classification Logic
  ↓
Prompt Layer
  ↓
LLM Client (mock or real)
  ↓
Structured Output (JSON)
```

## Tech stack
- Python 3.11+
- FastAPI
- Pydantic
- python-dotenv

## API endpoints
- `POST /support/analyze` — analyze a support request
- `GET /support/categories` — list known categories
- `GET /health` — health check

## Example request / response

### POST /support/analyze

**Request:**

```json
{
  "message": "I can’t access my account after password reset.",
  "customer_id": "12345",
  "channel": "web"
}
```

**Response (example):**

```json
{
  "category": "account_access",
  "priority": "high",
  "suggested_reply": "It looks like you are having trouble accessing your account after a password reset. Please try logging out from all devices and resetting your password once more using the 'Forgot password' link...",
  "needs_human_review": true
}
```

## Use cases
- customer support triage
- helpdesk / service desk intake
- routing and prioritization of tickets
- support automation prototypes for clients

## Prompt engineering relevance
Prompt design controls:
- how we explain the situation to the model,
- how conservative or “confident” draft replies are,
- when we mark `needs_human_review = true`.

The service exposes a clear prompt-building step that can be iterated together with the support team.

## Possible integrations
- existing ticketing systems (Zendesk, Freshdesk, etc.)
- internal helpdesk tools
- chat widgets or bots that send messages to this API

## Project structure

```text
ai-support-assistant/
  app/
    __init__.py
    main.py
    config.py
    schemas.py
    routes.py
    services/
      __init__.py
      support_service.py
      llm_client.py
  data/
    README.md
  .env.example
  .gitignore
  requirements.txt
  README.md
```

## Future improvements
- Add more advanced classification (e.g. embeddings + clustering).
- Log analyzed tickets and compare categories vs agent decisions.
- Add per-client configuration (categories, reply templates).
- Connect to a real LLM provider and ticket system.