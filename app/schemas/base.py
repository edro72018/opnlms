from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: str = "OK"
    errors: Optional[list[str]] = None
