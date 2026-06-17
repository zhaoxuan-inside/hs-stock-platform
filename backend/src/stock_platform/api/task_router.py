from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schema.task import TaskCreate, TaskResponse, TaskExecutionResponse, TaskExecutionCreate, \
    SchedulerCreate, SchedulerResponse
from repository.task_repository import create_task, get_task_by_id, list_tasks, update_task, delete_task, \
    create_task_execution, update_task_execution, get_task_execution, list_task_executions, \
    create_scheduler, get_scheduler_by_id, list_schedulers, update_scheduler_status, \
    create_message, list_messages, update_message_status
from core.database import get_db
from fastapi import HTTPException
from uuid import UUID

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_api(task_create: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task_create)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    return task


@router.get("/")
async def list_task_api(db: AsyncSession = Depends(get_db)):
    return await list_tasks(db)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_api(task_id: UUID, task_create: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = await update_task(db, task_id, task_create)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_api(task_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")


@router.post("/executions/", response_model=TaskExecutionResponse, status_code=status.HTTP_201_CREATED)
async def create_task_execution_api(task_execution_create: TaskExecutionCreate, db: AsyncSession = Depends(get_db)):
    return await create_task_execution(db, task_execution_create.task_id, task_execution_create.status,
                                      task_execution_create.total_count)


@router.get("/executions/{execution_id}", response_model=TaskExecutionResponse)
async def get_task_execution_api(execution_id: UUID, db: AsyncSession = Depends(get_db)):
    execution = await get_task_execution(db, execution_id)
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务执行记录不存在")
    return execution


@router.get("/executions/")
async def list_task_executions_api(
    task_id: UUID | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await list_task_executions(db, task_id, limit)


@router.put("/executions/{execution_id}")
async def update_task_execution_api(
    execution_id: UUID,
    status: str | None = None,
    progress: int | None = None,
    completed_count: int | None = None,
    current_item: str | None = None,
    end_time: str | None = None,
    error_message: str | None = None,
    result: dict | None = None,
    progress_data: dict | None = None,
    db: AsyncSession = Depends(get_db)
):
    kwargs = {}
    if status is not None:
        kwargs["status"] = status
    if progress is not None:
        kwargs["progress"] = progress
    if completed_count is not None:
        kwargs["completed_count"] = completed_count
    if current_item is not None:
        kwargs["current_item"] = current_item
    if end_time is not None:
        kwargs["end_time"] = end_time
    if error_message is not None:
        kwargs["error_message"] = error_message
    if result is not None:
        kwargs["result"] = result
    if progress_data is not None:
        kwargs["progress_data"] = progress_data
    
    execution = await update_task_execution(db, execution_id, **kwargs)
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务执行记录不存在")
    return execution


@router.post("/schedulers/", response_model=SchedulerResponse, status_code=status.HTTP_201_CREATED)
async def create_scheduler_api(scheduler_create: SchedulerCreate, db: AsyncSession = Depends(get_db)):
    return await create_scheduler(db, scheduler_create)


@router.get("/schedulers/{scheduler_id}", response_model=SchedulerResponse)
async def get_scheduler(scheduler_id: UUID, db: AsyncSession = Depends(get_db)):
    scheduler = await get_scheduler_by_id(db, scheduler_id)
    if not scheduler:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="调度器不存在")
    return scheduler


@router.get("/schedulers/")
async def list_schedulers_api(db: AsyncSession = Depends(get_db)):
    return await list_schedulers(db)


@router.put("/schedulers/{scheduler_id}/status", response_model=SchedulerResponse)
async def update_scheduler_status_api(scheduler_id: UUID, status: str, db: AsyncSession = Depends(get_db)):
    scheduler = await update_scheduler_status(db, scheduler_id, status)
    if not scheduler:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="调度器不存在")
    return scheduler


@router.post("/messages/", status_code=status.HTTP_201_CREATED)
async def create_message_api(
    user_id: UUID,
    title: str,
    content: str,
    type: str,
    related_task_id: UUID | None = None,
    db: AsyncSession = Depends(get_db)
):
    return await create_message(db, user_id, title, content, type, related_task_id)


@router.get("/messages/")
async def list_messages_api(
    user_id: UUID,
    status: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await list_messages(db, user_id, status, limit)


@router.put("/messages/{message_id}/status")
async def update_message_status_api(message_id: UUID, status: str, db: AsyncSession = Depends(get_db)):
    message = await update_message_status(db, message_id, status)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")
    return message