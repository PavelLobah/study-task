from fastapi import FastAPI

from typing import List
from operation.model import Task
from operation.router import router as router_operation

app = FastAPI(
    title="StudTask",
    version="1.0",
    description="Performing training tasks using the FastAPI framework"
)

app.include_router(router_operation, prefix="/tasks")

