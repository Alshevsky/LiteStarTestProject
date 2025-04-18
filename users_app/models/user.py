from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from users_app.database.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def hash_current_password(self) -> str:
        self.password = self.hash_password(self.password)
