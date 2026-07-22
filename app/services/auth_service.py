from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.password import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    async def register(
        self,
        db: AsyncSession,
        user_data: UserCreate,
    ) -> User:

        existing_user = await self.user_repository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        return await self.user_repository.create(
            db,
            user,
        )