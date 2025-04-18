import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.models.user import User
from users_app.database.config import engine

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating user: {e}", exc_info=True)
            raise

    async def get_by_id(self, user_id: int) -> User | None:
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by id: {e}", exc_info=True)
            return None

    async def get_all(self) -> list[User]:
        try:
            query = select(User)
            result = await self.session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting all users: {e}", exc_info=True)
            return []

    async def update(self, user: User) -> User:
        try:
            await self.session.merge(user)
            await self.session.commit()
            return user
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating user: {e}", exc_info=True)
            raise

    async def delete(self, user: User) -> None:
        try:
            await self.session.delete(user)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting user: {e}", exc_info=True)
            raise
