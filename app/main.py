from fastapi import FastAPI
from loguru import logger as log
from app.routers import router_task
from app.exceptions import JsonException, json_exception_handler
from app.db.db import database, Task
from app.settings import get_settings


settings = get_settings()

print(settings.title, settings.version, settings.description)

app = FastAPI(title=settings.title, version=settings.version,
              description=settings.title)
app.include_router(router_task.router)
app.add_exception_handler(JsonException, json_exception_handler)


# @app.on_event('startup')
# async def app_startup():
#     db.init_schema(router_task.TABLE_NAME, "issue_id")
#     log.success("Service started.")
#     return

@app.get("/")
async def read_root():
    return await Task.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await Task.objects.get_or_create(description="task1")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

if __name__ == "__main__":
    log.error(
        "Run me like: uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload")
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="localhost", port=8000, reload=True)
