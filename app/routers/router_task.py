from fastapi import APIRouter, Body, Path
from app.dto.common import ErrorResponse, SuccessResponse
from fastapi import status
from app.exceptions import JsonException
import app.dto.task as dto
from app.db.postgres_db import db
from datetime import datetime
from loguru import logger as log

# Условно моделируем имя таблицы, в которой хранятся данные
TABLE_NAME = "tasks"

router = APIRouter(
    tags=["task"],
)

@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(issue: dto.TaskBase = Body(...)) -> SuccessResponse[dto.TaskId]:
    """
    Создает задачу согласно модели IssueBase (JSON передается в body)
    Возвращает модель IssueId - которая содержит идентификатор созданной задачи
    """
    issue_id = db.add(TABLE_NAME, dto.Task, issue)
    return SuccessResponse[dto.TaskId](payload=issue_id)


@router.get("/task")
async def get_all_tasks() -> SuccessResponse[dto.TaskCollection]:
    """
    Возвращает все задачи в модели IssueCollection
    Требуемый список задач доступен под именем items
    """
    items = db.get_all(TABLE_NAME)
    payload = dto.TaskCollection(items=items, total=len(items))
    return SuccessResponse[dto.TaskCollection](payload=payload)


@router.get("/task/{issue_id}", responses={404: {"model": ErrorResponse}}, )
async def get_one_task_by_id(issue_id: str = Path(...)) -> SuccessResponse[dto.Task]:
    """
    Возвращает одну задачу по заданному issue_id
    """
    issue = db.get_one(TABLE_NAME, issue_id)
    if not issue:
        raise JsonException(
            status_code=404,
            msg=f"Issue not found",
            detail=f"Requested issue `{issue_id}` does not exist. It could be deleted or moved."
        )
    return SuccessResponse[dto.Task](payload=issue)


@router.put("/task/{issue_id}", response_model=SuccessResponse[dto.Task], responses={404: {"model": ErrorResponse}})
async def update_one_task_by_id(issue_id: str = Path(...), issue: dto.TaskBase = Body(...)):
    """
    Полностью заменяет все данные задачи с issue_id
    Данные берутся из объекта IssueBase (JSON передается в body)
    Возвращает обновленную задачу
    """
    updated_issue = db.update_one(TABLE_NAME, dto.Task, issue_id, issue)
    if not updated_issue:
        raise JsonException(
            status_code=404,
            msg=f"Issue not found",
            detail=f"Requested issue `{issue_id}` does not exist. It can't be updated."
        )
    return SuccessResponse[dto.Task](payload=updated_issue)


@router.patch("/task/{issue_id}", response_model=SuccessResponse[dto.Task], responses={404: {"model": ErrorResponse}})
async def partial_update_one_task_by_id(issue_id: str = Path(...), issue: dto.TaskBase = Body(...)):
    """
    Частично заменяет данные задачи с issue_id
    Только заданные поля берутся из объекта IssueBase (JSON передается в body)
    Возвращает обновленную задачу
    """
    updated_issue = db.update_one(TABLE_NAME, dto.Task, issue_id, issue)
    if not updated_issue:
        raise JsonException(
            status_code=404,
            msg=f"Issue not found",
            detail=f"Requested issue `{issue_id}` does not exist. It can't be updated."
        )
    return SuccessResponse[dto.Task](payload=updated_issue)


@router.delete("/task/{issue_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": ErrorResponse}})
async def delete_one_task_by_id(issue_id: str = Path(...)):
    """
    Удаляет задачу по заданному issue_id
    Возвращает статус 204 (без тела ответа)
    """
    exists = db.delete_one(TABLE_NAME, issue_id)
    if not exists:
        raise JsonException(
            status_code=404,
            msg=f"Issue not found",
            detail=f"Requested issue `{issue_id}` does not exist. It can't be deleted."
        )
    return
