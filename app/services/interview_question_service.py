from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gemini_question_generator import (
    GeminiQuestionGenerator,
)

from app.ai.rag.embeddings import (
    GeminiEmbeddingProvider,
)

from app.ai.rag.retriever import (
    SimpleRetriever,
)

from app.ai.rag.service import (
    RAGService,
)

from app.models.interview_question import (
    InterviewQuestion,
)

from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)

from app.repositories.resume_repository import (
    ResumeRepository,
)

from app.repositories.job_description_repository import (
    JobDescriptionRepository,
)


class InterviewQuestionService:

    def __init__(self):

        self.question_generator = (
            GeminiQuestionGenerator()
        )

        self.question_repository = (
            InterviewQuestionRepository()
        )

        self.resume_repository = (
            ResumeRepository()
        )

        self.job_description_repository = (
            JobDescriptionRepository()
        )

        self.rag_service = RAGService(
            GeminiEmbeddingProvider(),
            SimpleRetriever(),
        )

    async def generate_questions(
        self,
        db: AsyncSession,
        user_id: str,
        resume_id: str,
        job_description_id: str,
        category: str,
        difficulty: str,
        question_count: int,
    ) -> list[InterviewQuestion]:

        resume = await self.resume_repository.get_by_id(
            db,
            resume_id,
        )

        if not resume:
            raise ValueError(
                "Resume not found"
            )

        job_description = (
            await self.job_description_repository.get_by_id(
                db,
                job_description_id,
            )
        )

        if not job_description:
            raise ValueError(
                "Job Description not found"
            )

        if str(resume.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        if str(job_description.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        existing_questions = (
            await self.question_repository.get_existing_questions(
                db,
                user_id,
            )
        )

        documents = [
            {
                "text": resume.resume_text,
            },
            {
                "text": job_description.jd_text,
            },
        ]

        document_texts = [
            document["text"]
            for document in documents
            if document["text"]
        ]

        embeddings = (
            await self.rag_service.embed_documents(
                document_texts
            )
        )

        rag_documents = [
            {
                "text": text,
                "embedding": embedding,
            }
            for text, embedding in zip(
                document_texts,
                embeddings,
            )
        ]

        query = (
            f"{category} {difficulty} "
            "interview questions"
        )

        relevant_documents = (
            await self.rag_service.retrieve_relevant_documents(
                query=query,
                documents=rag_documents,
                top_k=2,
            )
        )

        context_parts = [
            item["document"]["text"]
            for item in relevant_documents
        ]

        rag_context = "\n\n".join(
            context_parts
        )

        questions = (
            await self.question_generator.generate_questions(
                resume_text=rag_context,
                jd_text=job_description.jd_text,
                category=category,
                difficulty=difficulty,
                question_count=question_count,
                existing_questions=existing_questions,
                rag_context=rag_context,
            )
        )

        filtered_questions = [
            item
            for item in questions.questions
            if item.question.strip().lower()
            not in existing_questions
        ]

        question_models = [
            InterviewQuestion(
                user_id=user_id,
                resume_id=resume.id,
                job_description_id=job_description.id,
                question=item.question,
                category=category,
                difficulty=difficulty,
                question_type=item.question_type,
            )
            for item in filtered_questions
        ]

        return await self.question_repository.create_many(
            db,
            question_models,
        )

    async def regenerate_questions(
        self,
        db: AsyncSession,
        user_id: str,
        resume_id: str,
        job_description_id: str,
        category: str,
        difficulty: str,
        question_count: int,
    ) -> list[InterviewQuestion]:

        return await self.generate_questions(
            db=db,
            user_id=user_id,
            resume_id=resume_id,
            job_description_id=job_description_id,
            category=category,
            difficulty=difficulty,
            question_count=question_count,
        )

    async def get_my_questions(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list[InterviewQuestion]:

        return await self.question_repository.get_all_by_user(
            db,
            user_id,
        )

    async def get_question(
        self,
        db: AsyncSession,
        question_id: str,
        user_id: str,
    ) -> InterviewQuestion:

        question = (
            await self.question_repository.get_by_id(
                db,
                question_id,
            )
        )

        if not question:
            raise ValueError(
                "Interview question not found"
            )

        if str(question.user_id) != user_id:
            raise ValueError(
                "Access denied"
            )

        return question