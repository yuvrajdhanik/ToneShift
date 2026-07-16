from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

from prompts import (
    build_prompt,
    build_verification_prompt,
    build_back_translation_prompt
)

import os
import time
import json

# ------------------------------------
# Load Environment Variables
# ------------------------------------

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found. Set it in either .env or Streamlit Secrets."
    )

# ------------------------------------
# Models
# ------------------------------------

REWRITE_MODEL = "google/gemini-2.5-flash"
BACK_TRANSLATE_MODEL = "google/gemini-2.5-flash"
VERIFY_MODEL = "google/gemini-2.5-flash"

# ------------------------------------
# OpenRouter Client
# ------------------------------------

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "ToneShift"
    }
)

# ------------------------------------
# Rewrite Text
# ------------------------------------

def rewrite_text(
    text: str,
    length: int,
    tone: int
) -> str:

    prompt = build_prompt(
        text=text,
        length=length,
        tone=tone
    )

    retries = 3

    for attempt in range(retries):

        try:

            completion = client.chat.completions.create(

                model=REWRITE_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": "You are ToneShift."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.05,
                max_completion_tokens=700

            )

            return completion.choices[0].message.content.strip()

        except Exception as e:

            if attempt == retries - 1:
                return f"❌ Error: {str(e)}"

            time.sleep(2)

# ------------------------------------
# Back Translation
# ------------------------------------

def back_translate(
    rewritten: str
) -> str:

    prompt = build_back_translation_prompt(
        rewritten
    )

    retries = 3

    for attempt in range(retries):

        try:

            completion = client.chat.completions.create(

                model=BACK_TRANSLATE_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": "You are ToneShift."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0,
                max_completion_tokens=700

            )

            return completion.choices[0].message.content.strip()

        except Exception as e:

            if attempt == retries - 1:
                return f"❌ Error: {str(e)}"

            time.sleep(2)

# ------------------------------------
# Meaning Verification
# ------------------------------------

def verify_meaning(
    original: str,
    rewritten: str
):

    prompt = build_verification_prompt(
        original=original,
        rewritten=rewritten
    )

    retries = 3

    for attempt in range(retries):

        try:

            completion = client.chat.completions.create(

                model=VERIFY_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": "You are ToneShift's semantic evaluator."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0,
                max_completion_tokens=150

            )

            content = completion.choices[0].message.content.strip()

            start = content.find("{")
            end = content.rfind("}") + 1

            result = json.loads(content[start:end])

            return result

        except json.JSONDecodeError:

            if attempt == retries - 1:
                return {
                    "similarity": 0,
                    "status": "Verification Failed",
                    "drift": "Unknown",
                    "reason": "The model returned invalid JSON."
                }

            time.sleep(2)

        except Exception as e:

            if attempt == retries - 1:
                return {
                    "similarity": 0,
                    "status": "Verification Failed",
                    "drift": "Unknown",
                    "reason": str(e)
                }

            time.sleep(2)