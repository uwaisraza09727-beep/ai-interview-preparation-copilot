from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self):

        self.dashboard_repository = DashboardRepository()

    async def get_dashboard(
        self,
        db: AsyncSession,
        user_id: str,
    ):

        return await self.dashboard_repository.get_dashboard_stats(
            db,
            user_id,
        )