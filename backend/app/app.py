from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.models.user_model import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.api.api_v1.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        initialize crucial application services
    """

    db_client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING).todolist

    await init_beanie(
        database=db_client,
        document_models=[
            User
        ]
    )
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(router, prefix=settings.API_V1_STR)
