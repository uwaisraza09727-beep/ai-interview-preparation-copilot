from typing import Any

from app.ai.rag.base import Retriever


class SimpleRetriever(Retriever):

    def __init__(self):
        pass

    async def retrieve(
        self,
        query_embedding: list[float],
        documents: list[dict[str, Any]],
        top_k: int = 3,
    ) -> list[dict[str, Any]]:

        if not documents:
            return []

        results = []

        for document in documents:

            embedding = document.get(
                "embedding"
            )

            if not embedding:
                continue

            score = self._cosine_similarity(
                query_embedding,
                embedding,
            )

            results.append(
                {
                    "document": document,
                    "score": score,
                }
            )

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results[:top_k]

    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:

        if len(vector_a) != len(vector_b):
            return 0.0

        dot_product = sum(
            a * b
            for a, b in zip(
                vector_a,
                vector_b,
            )
        )

        magnitude_a = sum(
            a * a
            for a in vector_a
        ) ** 0.5

        magnitude_b = sum(
            b * b
            for b in vector_b
        ) ** 0.5

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (
            magnitude_a * magnitude_b
        )