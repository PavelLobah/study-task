from fastapi import FastAPI
from loguru import logger as log
import uvicorn
from app.routers import (
    router_task,
)
from app.exceptions import JsonException, json_exception_handler
from app.db.db import db
from app.settings import get_settings

settings = get_settings()

print(settings.title, settings.version, settings.description)

app = FastAPI(title=settings.title, version=settings.version,
              description=settings.title)
app.include_router(router_task.router)
app.add_exception_handler(JsonException, json_exception_handler)


@app.on_event('startup')
async def app_startup():
    db.init_schema(router_task.TABLE_NAME, "issue_id")
    log.success("Service started.")
    return


# if __name__ == "__main__":
#     log.error(
#         "Run me like: uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload")
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8002, reload=True)