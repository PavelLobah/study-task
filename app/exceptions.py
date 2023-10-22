from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger as log
from app.dto.common import ErrorResponse, Error


class JsonException(Exception):
    def __init__(self, status_code: int, msg: str, detail: str = None):
        self.status_code = status_code
        self.response = ErrorResponse(
            success=False,
            error=Error(code=status_code, msg=msg, detail=detail)
        )


async def json_exception_handler(_: Request, e: JsonException):
    """
    It is disgusting to catch an error not in JSON but in plain text.
    Whenever there is an error - we will return JSON.
    :param _: Request
    :param e: JsonException
    :return: response
    """
    response = JSONResponse(
        content=e.response.model_dump(), status_code=e.status_code)
    log.warning("JsonException: " + str(e.response))
    return response
