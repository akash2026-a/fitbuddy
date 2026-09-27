from functools import lru_cache

from google import genai
from google.genai import types

from ..config import settings


SYSTEM_INSTRUCTION = """
You are FitBuddy, an evidence-aware fitness planning assistant.

Create practical, conservative fitness guidance.

Do not diagnose medical conditions or prescribe treatment.

Encourage the user to seek qualified medical or professional advice for:
- injuries
- pregnancy
- chronic disease
- severe pain
- eating disorders
- or other situations requiring individualized care

Never claim that a generated plan is a substitute for a qualified professional.
"""


@lru_cache
def get_client():
    """
    Create and cache the Gemini client.
    Returns None when no API key is configured.
    """
    if not settings.gemini_api_key:
        return None

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(prompt: str, model: str) -> str:
    """
    Send a prompt to Gemini and return the generated text.

    If no Gemini API key is configured, return an empty string
    so the application can use its local fallback.
    """

    client = get_client()

    if client is None:
        return ""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.6,
            max_output_tokens=5000,
        ),
    )

    return (response.text or "").strip()