import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/users_db", echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)

async def fill_db():
    async with async_session() as session:
        with open("users.json", "r") as f:
            users = json.load(f)
            for user_data in users:
                user = User(
                    name=user_data["name"],
                    surname=user_data["surname"],
                    password=user_data["password"]
                )
                session.add(user)
            await session.commit()

if __name__ == "__main__":
    asyncio.run(fill_db())