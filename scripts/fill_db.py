import asyncio
import json
import sys
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from users_app.models.user import User

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/users_db", echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)

async def fill_db():
    async with async_session() as session:
        with open("scripts/data/users.json", "r") as f:
            users = json.load(f)
            for user_data in users:
                user = User(
                    name=user_data["name"],
                    surname=user_data["surname"],
                    password=User.hash_password(user_data["password"])
                )
                session.add(user)
            await session.commit()

if __name__ == "__main__":
    asyncio.run(fill_db())
