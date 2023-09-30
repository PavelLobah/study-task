from fastapi import APIRouter
from dto import db
from typing import List
from operation.model import Task

router = APIRouter(
    tags=["Operation"]
)


@router.get("")
async def get_tasks():
    return [task for task in db]

def search_by_id(task_id)->list:
    if task_id not in db:             
        raise KeyError(f"DB: ключ task_id={task_id} не найден среди TASK")       
    return [task for task in db if task.get("id") == task_id][0]
        

@router.get("/{task_id}")
async def get_task(task_id: int):
    return search_by_id(task_id)

@router.get("/tasks")
async def get_tasks():
    return [task for task in db]

@router.post("/{task_id}")
async def change_data_task(task_id: int, new_name: str, new_date:str):
    current_task=list(search_by_id(task_id))[0]
    current_task["name"],current_task["created_at"] = new_name,new_date
    return{"status":200, "data":current_task}

@router.put("/")
async def add_task(task: List[Task]):
    db.append(task)
    return{"status":200,"data":db}