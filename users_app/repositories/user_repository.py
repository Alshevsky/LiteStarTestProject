import logging

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import delete, select, update

from users_app.dto.user import UpdateUserDTO
from users_app.models.user import User

logger = logging.getLogger(__name__)


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User

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
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by id: {e}", exc_info=True)
            return None

    async def get_by_name(self, name: str) -> User | None:
        try:
            stmt = select(User).where(User.name == name)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by name: {e}", exc_info=True)
            return None

    async def get_all(self) -> list[User]:
        try:
            stmt = select(User)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting all users: {e}", exc_info=True)
            return []

    async def update(self, user: User, data: UpdateUserDTO) -> User:
        try:
            print(data.to_dict(exclude_none=True))
            stmt = update(User).values(**data.to_dict(exclude_none=True)).where(User.id == user.id)
            await self.session.execute(stmt)
            await self.session.commit()
            user = await self.get_by_id(user.id)
            return user
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating user: {e}", exc_info=True)
            raise

    async def delete(self, user: User) -> None:
        try:
            stmt = delete(User).where(User.id == user.id)
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting user: {e}", exc_info=True)
            raise
