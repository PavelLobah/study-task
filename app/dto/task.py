from pydantic import BaseModel, Field
from datetime import datetime

class TaskId(BaseModel):
    issue_id: int = Field(..., alias="issue_id")


class TaskBase(BaseModel):
    name: str
    description: str = ""
    class Config:
        json_schema_extra = {
            "example": {
                "name": "My New Task1",
                "description": "Something to be done1",
            }
        }


class Task(TaskBase, TaskId):
    created_at: datetime
    class Config:
        json_schema_extra = {
            "example": {
                "issue_id": "1",
                "name": "My New Task",
                "description": "Something to be done",
                "created_at": "2023-09-28 23:59:59"
            }
        }


class TaskCollection(BaseModel):
    total: int = 0
    items: list[Task] = []
    class Config:
        json_schema_extra = {
            "example": {
                "total": "1",
                "items": [
                    {
                        "issue_id": "1",
                        "name": "My New Task",
                        "description": "Something to be done",
                    }
                ]
            }
        }


