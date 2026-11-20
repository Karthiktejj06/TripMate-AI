import os
from groq import Groq

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

class LLMError(RuntimeError):
    pass

def generate_text(system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
    """Call Groq and return the assistant's text response."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise LLMError("GROQ_API_KEY is missing. Add it to your .env file.")

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        content = response.choices[0].message.content
        return (content or "").strip()
    except Exception as exc:
        raise LLMError(f"Groq request failed: {exc}") from exc
