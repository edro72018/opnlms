import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import LMSException
from app.schemas.base import APIResponse
from app.api.auth import router as auth_router
from app.api.course import router as courses_router
from app.api.enrollments import router as enrollments_router
from app.api.users import router as users_router


def _aplicar_migraciones():
    from alembic.config import Config
    from alembic import command as alembic_command
    alembic_command.upgrade(Config("alembic.ini"), "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.get_running_loop().run_in_executor(None, _aplicar_migraciones)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(LMSException)
async def lms_exception_handler(request: Request, exc: LMSException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            message=exc.message,
            errors=[exc.message],
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    detail = str(exc) if settings.DEBUG else "Error interno del servidor"
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            message=detail,
            errors=[type(exc).__name__],
        ).model_dump(),
    )


@app.get("/health", tags=["sistema"])
async def health_check():
    return APIResponse(
        success=True,
        message=f"{settings.APP_NAME} v{settings.APP_VERSION} funcionando",
    )


@app.get("/health/db", tags=["sistema"])
async def health_db(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return APIResponse(
        success=True,
        message="Conexión a la base de datos OK",
        data={"db": settings.DATABASE_URL.split("://")[0]},
    )


app.include_router(auth_router, prefix="/api/v1")
app.include_router(courses_router, prefix="/api/v1")
app.include_router(enrollments_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
