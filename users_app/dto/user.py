from datetime import datetime
from litestar.dto import DataclassDTO, DTOConfig
from dataclasses import dataclass

@dataclass
class UserDTO:
    id: int
    name: str
    surname: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John",
                "surname": "Doe",
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z"
            }
        }

@dataclass
class CreateUserDTO:
    name: str
    surname: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "surname": "Doe",
                "password": "secure_password123"
            }
        }

@dataclass
class UpdateUserDTO:
    name: str | None = None
    surname: str | None = None
    password: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "surname": "Smith",
                "password": "new_secure_password123"
            }
        }

class UserResponseDTO(DataclassDTO[UserDTO]):
    config = DTOConfig(
        exclude={"password"},
        rename_fields={"created_at": "createdAt", "updated_at": "updatedAt"}
    )

class UserCreateDTO(DataclassDTO[CreateUserDTO]):
    config = DTOConfig()

class UserUpdateDTO(DataclassDTO[UpdateUserDTO]):
    config = DTOConfig() 
