from litestar import Controller, Response, delete, get, post, put, status_codes
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.params import Parameter
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.database.config import get_session
from users_app.dto.user import CreateUserDTO, UpdateUserDTO, UserDTO
from users_app.models.user import User
from users_app.repositories.user_repository import UserRepository


class UserController(Controller):
    path = "/users"
    dependencies = {"session": Provide(get_session)}
    include_in_schema = True

    @get()
    async def get_users(
        self,
        session: AsyncSession,
        limit: int = Parameter(gt=0, le=100, default=10),
        offset: int = Parameter(ge=0, default=0),
    ) -> list[UserDTO]:
        repository = UserRepository(session=session)
        users = await repository.get_all()
        return [
            UserDTO(
                id=user.id, name=user.name, surname=user.surname, created_at=user.created_at, updated_at=user.updated_at
            )
            for user in users
        ]

    @get("/{user_id:int}")
    async def get_user(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserDTO | None:
        repository = UserRepository(session=session)
        if user := await repository.get_by_id(user_id):
            return UserDTO(
                id=user.id, name=user.name, surname=user.surname, created_at=user.created_at, updated_at=user.updated_at
            )
        raise HTTPException(status_code=status_codes.HTTP_404_NOT_FOUND, detail="User not found")

    @post()
    async def create_user(
        self,
        session: AsyncSession,
        data: CreateUserDTO,
    ) -> Response:
        repository = UserRepository(session=session)
        user = User(name=data.name, surname=data.surname, password=data.password)
        user.hash_current_password()
        await repository.create(user)
        created_user = await repository.get_by_id(user.id)
        return Response(
            content=UserDTO(
                id=created_user.id,
                name=created_user.name,
                surname=created_user.surname,
                created_at=created_user.created_at,
                updated_at=created_user.updated_at,
            ),
            status_code=status_codes.HTTP_201_CREATED,
        )

    @put("/{user_id:int}")
    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        data: UpdateUserDTO,
    ) -> Response:
        repository = UserRepository(session=session)
        if user := await repository.get_by_id(user_id):
            await repository.update(user, data)
            return Response(
                content=UserDTO(
                    id=user.id,
                    name=user.name,
                    surname=user.surname,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                ),
                status_code=status_codes.HTTP_200_OK,
            )
        raise HTTPException(status_code=status_codes.HTTP_404_NOT_FOUND, detail="User not found")

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        repository = UserRepository(session=session)
        if user := await repository.get_by_id(user_id):
            await repository.delete(user)
            return
        raise HTTPException(status_code=status_codes.HTTP_404_NOT_FOUND, detail="User not found")
