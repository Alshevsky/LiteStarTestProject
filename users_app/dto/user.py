from dataclasses import asdict, dataclass
from datetime import datetime

from litestar.dto import DataclassDTO, DTOConfig


@dataclass
class UserDTO:
    id: int
    name: str
    surname: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class CreateUserDTO:
    name: str
    surname: str
    password: str


@dataclass
class UpdateUserDTO:
    name: str | None = None
    surname: str | None = None
    password: str | None = None

    def to_dict(self, exclude_none: bool = True):
        if not exclude_none:
            return asdict(self)
        return {k: v for k, v in asdict(self).items() if v is not None}


class UserResponseDTO(DataclassDTO[UserDTO]):
    config = DTOConfig(
        exclude={"password"},
        rename_fields={"created_at": "createdAt", "updated_at": "updatedAt"},
    )


class UserCreateDTO(DataclassDTO[CreateUserDTO]):
    config = DTOConfig()


class UserUpdateDTO(DataclassDTO[UpdateUserDTO]):
    config = DTOConfig()
