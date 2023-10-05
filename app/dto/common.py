from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import TypeVar
from typing import Generic

T = TypeVar("T", int, str)


class Error(BaseModel):
    code: int
    msg: str
    detail: str = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: Error

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "code": 401,
                    "msg": "Wrong password",
                    "detail": "Use `password reset` if you forgot password",
                }
            }
        }


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    payload: T
