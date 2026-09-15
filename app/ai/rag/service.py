from typing import Any

from app.ai.rag.base import (
    EmbeddingProvider,
    Retriever,
)


class RAGService:

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        retriever: Retriever,
    ):

        self.embedding_provider = (
            embedding_provider
        )

        self.retriever = retriever

    async def retrieve_relevant_documents(
        self,
        query: str,
        documents: list[dict[str, Any]],
        top_k: int = 3,
    ) -> list[dict[str, Any]]:

        if not query.strip():
            return []

        if not documents:
            return []

        query_embedding = (
            await self.embedding_provider.embed(
                query
            )
        )

        return await self.retriever.retrieve(
            query_embedding,
            documents,
            top_k,
        )

    async def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:

        embeddings = []

        for document in documents:

            if not document.strip():
                continue

            embedding = (
                await self.embedding_provider.embed(
                    document
                )
            )

            embeddings.append(
                embedding
            )

        return embeddings