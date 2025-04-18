import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.models.user import User
from users_app.repositories.user_repository import UserRepository


@pytest.fixture
def test_user():
    return User(name="Test", surname="User", password="test_password")


@pytest.fixture
def test_user_data():
    return {"name": "Test", "surname": "User", "password": "test_password"}


@pytest.fixture
def test_user_update_data():
    return {"name": "Updated", "surname": "User", "password": "new_password"}


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient, test_user_data):
    response = await async_client.post("/users", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_user_data["name"]
    assert data["surname"] == test_user_data["surname"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_users(async_client: AsyncClient, test_user, session: AsyncSession):
    repository = UserRepository(session=session)
    await repository.create(test_user)

    response = await async_client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all("password" not in user for user in data)


@pytest.mark.asyncio
async def test_get_user(async_client: AsyncClient, test_user, session: AsyncSession):
    repository = UserRepository(session=session)
    await repository.create(test_user)

    response = await async_client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user.name
    assert data["surname"] == test_user.surname
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_nonexistent_user(async_client: AsyncClient):
    response = await async_client.get("/users/999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(async_client: AsyncClient, test_user, test_user_update_data, session: AsyncSession):
    repository = UserRepository(session=session)
    test_user.name = "Test_Update"
    await repository.create(test_user)

    user = await repository.get_by_id(test_user.id)
    assert user is not None

    response = await async_client.put(f"/users/{user.id}", json=test_user_update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user_update_data["name"]
    assert data["surname"] == test_user_update_data["surname"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_update_nonexistent_user(async_client: AsyncClient, test_user_update_data):
    response = await async_client.put("/users/999999", json=test_user_update_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient, test_user, session: AsyncSession):
    repository = UserRepository(session=session)
    test_user.name = "Test_Delete"
    await repository.create(test_user)

    user = await repository.get_by_id(test_user.id)
    assert user is not None

    response = await async_client.delete(f"/users/{test_user.id}")
    assert response.status_code == 204

    deleted_user = await repository.get_by_id(test_user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_delete_nonexistent_user(async_client: AsyncClient):
    response = await async_client.delete("/users/999999")
    assert response.status_code == 404
