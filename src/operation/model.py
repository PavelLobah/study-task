from pydantic import BaseModel
from datetime import datetime
# from fastapi.responses import FileResponse

class Task(BaseModel):
    id: int
    name: str
    created_at: datetime

# class ResponseTaskDto(BaseModel):
#       result: bool 
#       payload: Task = None
#       error: RespError = None