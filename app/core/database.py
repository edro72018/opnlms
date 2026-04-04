from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi import Depends

# from app.core.exceptions import AuthError
# from fastapi import Depends, HTTPException
# from app.core.exceptions import AuthError


# El motor async — una sola instancia para toda la app
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # muestra las queries en consola si DEBUG=true
    pool_size=10,
    max_overflow=20,
)

# Fábrica de sesiones — cada request obtiene la suya
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependencia de FastAPI — inyecta la sesión en cada endpoint
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


"""
async def get_current_user(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db),
):

    Args:
        authorization (str, optional): _description_. Defaults to Header(...).
        db (AsyncSession, optional): _description_. Defaults to Depends(get_db).

    Raises:
        AuthError: _description_

    Returns:
        _type_: _description_

    # Dependencia reutilizable. Cualquier endpoint que la declare
    # recibe el usuario autenticado automáticamente.

    if not authorization.startswith("Bearer "):
        raise AuthError("Formato de token inválido. Usa: Bearer <token>")

    token = authorization.replace("Bearer ", "")

    from app.services.auth import AuthService

    service = AuthService(db)
    return await service.get_current_user(token)
"""

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    from app.services.auth import AuthService

    service = AuthService(db)
    return await service.get_current_user(token)
