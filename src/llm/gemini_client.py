# Shared Gemini client with retry and API error handling.

import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError, ServerError


load_dotenv()

# This project uses GEMINI_API_KEY from its local .env file.
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Add it to the project's .env file."
    )

# Prevent a Windows-level GOOGLE_API_KEY from competing with this project's key.
os.environ.pop("GOOGLE_API_KEY", None)

client = genai.Client(api_key=gemini_api_key)

MODEL_NAME = "gemini-3.8-flash"


def generate_with_retry(prompt, max_retries=5, initial_delay=2):
    """Generate Gemini content with retry handling for temporary failures."""
    delay = initial_delay

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            return response.text

        except ServerError as error:
            status_code = getattr(error, "code", None)

            # Retry temporary Gemini service outages.
            if status_code == 503 and attempt < max_retries - 1:
                print(
                    f"Gemini temporarily unavailable "
                    f"(attempt {attempt + 1}/{max_retries}). "
                    f"Retrying in {delay} seconds..."
                )
                time.sleep(delay)
                delay *= 2
                continue

            raise

        except ClientError as error:
            status_code = getattr(error, "code", None)

            # Quota exhaustion should not be repeatedly retried.
            if status_code == 429:
                raise RuntimeError(
                    "Gemini API quota has been exhausted. "
                    "Please wait for the quota to reset or use a billing-enabled API plan."
                ) from error

            raise