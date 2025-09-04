import logging
import time
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.concurrency import iterate_in_threadpool

from .background import write_log

logger = logging.getLogger("API")

app = FastAPI()


@app.middleware("http")
async def middleware(request: Request, call_next):
    try:
        req_body = await request.json()
    except Exception:
        req_body = None

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    res_body = [section async for section in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(res_body))

    # Handle responses with no body (like DELETE 204)
    if res_body:
        res_body = res_body[0].decode()
    else:
        res_body = None

    # Add the background task to the response object to queue the job
    response.background = BackgroundTask(write_log, request, response, req_body, res_body, process_time)
    return response


class Task(BaseModel):
    id: int
    title: str
    done: bool


class NewTask(BaseModel):
    title: str


class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None


tasks = {}
ids = []


@app.post("/tasks", status_code=201, response_model=Task)
def create_task(task: NewTask):
    id = len(ids) + 1
    ids.append(1)
    new_task = {"id": id, "title": task.title, "done": False}
    tasks[id] = new_task
    return new_task


@app.get("/tasks", status_code=200, response_model=List[Task])
def get_tasks():
    return list(tasks.values())


@app.patch("/tasks/{task_id}", status_code=200, response_model=Task)
def update_task(task_id: int, update_task: UpdateTask):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with given id :{task_id} not found")
    update_data = update_task.model_dump(exclude_unset=True)
    task_ = Task(**task)
    updated_task = task_.model_copy(update=update_data)
    tasks[task_id] = jsonable_encoder(updated_task)
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with given id :{task_id} not found")
    del tasks[task_id]
    return None
