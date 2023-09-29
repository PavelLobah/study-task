from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI(
    title="sdfsd"
)
db = [
    {"id": 5, "name": "task1", "created_at": "2023-09-28"},
    {"id": 6, "name": "task2", "created_at": "2023-09-29"},
    {"id": 12, "name": "task3", "created_at": "2023-09-26"},
    {"id": 7, "name": "task4", "created_at": "2023-09-25"},
    {"id": 8, "name": "task5", "created_at": "2023-09-28"},
    {"id": 9, "name": "task6", "created_at": "2023-09-29"},
    {"id": 10, "name": "task7", "created_at": "2023-09-26"},
    {"id": 11, "name": "task8", "created_at": "2023-09-25"}
]

def search_by_id(task_id):
    return [task for task in db if task.get("id") == task_id]

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    return search_by_id(task_id)

@app.get("/tasks")
async def get_tasks():
    return [task for task in db]

@app.post("/tasks/{task_id}")
async def change_data_task(task_id: int, new_name: str, new_date:str):
    current_task=list(search_by_id(task_id))[0]
    current_task["name"],current_task["created_at"] = new_name,new_date
    return{"status":200, "data":current_task}

class Task(BaseModel):
    id: int
    name: str
    created_at: str


@app.put("/tasks/")
async def add_task(task: List[Task]):
    db.append(task)
    return{"status":200,"data":db}