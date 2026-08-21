from google import genai

from app.ai.rag.base import (
    EmbeddingProvider,
)

from app.core.config.settings import (
    settings,
)


class GeminiEmbeddingProvider(
    EmbeddingProvider,
):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        self.model = "gemini-embedding-001"

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        response = await self.client.aio.models.embed_content(
            model=self.model,
            contents=text,
        )

        return response.embeddings[0].values