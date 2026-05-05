"""AI chatbot service — streaming-capable OpenAI wrapper with Redis conversation memory."""

import json
import uuid
from collections.abc import AsyncGenerator

import redis.asyncio as aioredis
from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

CONVERSATION_TTL = 60 * 30       # 30 minutes idle expiry
MAX_HISTORY = 20                  # keep last N turns (10 exchanges)


async def _get_redis() -> aioredis.Redis:
    return aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def _load_history(session_id: str) -> list[dict]:
    r = await _get_redis()
    raw = await r.get(f"chat:{session_id}")
    await r.close()
    return json.loads(raw) if raw else []


async def _save_history(session_id: str, history: list[dict]) -> None:
    r = await _get_redis()
    await r.setex(f"chat:{session_id}", CONVERSATION_TTL, json.dumps(history[-MAX_HISTORY:]))
    await r.close()


async def chat(message: str, session_id: str | None = None) -> tuple[str, str]:
    """Single-turn chat with conversation memory. Returns (reply, session_id)."""
    sid = session_id or str(uuid.uuid4())
    history = await _load_history(sid)

    history.append({"role": "user", "content": message})

    messages = [{"role": "system", "content": settings.AI_SYSTEM_PROMPT}, *history]

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        max_tokens=512,
        temperature=0.7,
    )
    reply = response.choices[0].message.content.strip()

    history.append({"role": "assistant", "content": reply})
    await _save_history(sid, history)

    return reply, sid


async def chat_stream(message: str, session_id: str | None = None) -> AsyncGenerator[tuple[str, str], None]:
    """Streaming chat — yields (token, session_id) chunks."""
    sid = session_id or str(uuid.uuid4())
    history = await _load_history(sid)
    history.append({"role": "user", "content": message})

    messages = [{"role": "system", "content": settings.AI_SYSTEM_PROMPT}, *history]

    full_reply = ""
    async with client.chat.completions.stream(
        model=settings.OPENAI_MODEL,
        messages=messages,
        max_tokens=512,
        temperature=0.7,
    ) as stream:
        async for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            full_reply += token
            yield token, sid

    history.append({"role": "assistant", "content": full_reply})
    await _save_history(sid, history)