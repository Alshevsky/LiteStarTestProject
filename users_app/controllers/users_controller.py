from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Parameter
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.database.config import get_session
from users_app.models.user import User
from users_app.repositories.user_repository import UserRepository
from users_app.dto.user import UserResponseDTO, UserCreateDTO, UserUpdateDTO, CreateUserDTO, UpdateUserDTO


class UserController(Controller):
    path = "/users"
    dependencies = {"session": Provide(get_session)}
    return_dto = UserResponseDTO

    @get()
    async def get_users(
        self,
        session: AsyncSession,
        limit: int = Parameter(gt=0, le=100, default=10),
        offset: int = Parameter(ge=0, default=0),
    ) -> list[UserResponseDTO]:
        repository = UserRepository(session)
        return await repository.get_all()

    @get("/{user_id:int}")
    async def get_user(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserResponseDTO | None:
        repository = UserRepository(session)
        return UserResponseDTO(await repository.get_by_id(user_id))

    @post(dto=UserCreateDTO)
    async def create_user(
        self,
        session: AsyncSession,
        data: CreateUserDTO,
    ) -> User:
        repository = UserRepository(session)
        user = User(
            name=data.name,
            surname=data.surname,
            password=data.password
        )
        return await repository.create(user)

    @put("/{user_id:int}", dto=UserUpdateDTO)
    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        data: UpdateUserDTO,
    ) -> User:
        repository = UserRepository(session)
        user = await repository.get_by_id(user_id)
        if user:
            if data.name is not None:
                user.name = data.name
            if data.surname is not None:
                user.surname = data.surname
            if data.password is not None:
                user.password = data.password
            return await repository.update(user)
        return None

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        repository = UserRepository(session)
        user = await repository.get_by_id(user_id)
        if user:
            await repository.delete(user)
