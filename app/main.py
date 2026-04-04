from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import LMSException
from app.schemas.base import APIResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.auth import router as auth_router
from app.api.course import router as courses_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.enrollments import router as enrollments_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi

security = HTTPBearer()

"""


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


@app.get("/health", tags=["sistema"])
async def health_check():
    return APIResponse(
        success=True,
        message=f"{settings.APP_NAME} v{settings.APP_VERSION} funcionando",
    )


@app.get("/health/db", tags=["sistema"])
async def health_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT version()"))
    version = result.scalar()
    return APIResponse(
        success=True,
        message="OK",
        data={"postgres_version": version},
    )


app.include_router(auth_router, prefix="/api/v1")

app.include_router(courses_router, prefix="/api/v1")

app.include_router(enrollments_router, prefix="/api/v1")
