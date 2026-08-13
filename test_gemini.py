from google import genai

from app.core.config.settings import settings


client = genai.Client(
    api_key=settings.gemini_api_key,
)

response = client.models.generate_content(
    model=settings.gemini_model,
    contents="Say hello in one sentence.",
)

print(response.text)