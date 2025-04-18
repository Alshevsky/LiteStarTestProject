import uvicorn
from litestar import Litestar, get
from litestar.openapi import OpenAPIConfig

from users_app.controllers.users_controller import UserController
from users_app.database.config import create_db_and_tables


@get("/")
async def get_root() -> str:
    return "Swagger API on route /docs"


app = Litestar(
    route_handlers=[get_root, UserController],
    openapi_config=OpenAPIConfig(
        title="Users API",
        version="1.0.0",
        description="API for managing users",
        use_handler_docstrings=True,
        path="/docs",
    ),
    lifespan=[create_db_and_tables],
    debug=False,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
