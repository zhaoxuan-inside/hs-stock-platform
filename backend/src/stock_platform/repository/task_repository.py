from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.task import Task, TaskExecution, Scheduler, Message
from schema.task import TaskCreate, SchedulerCreate
from core.distributed_lock import get_lock
from datetime import datetime
from uuid import UUID


async def create_task(db: AsyncSession, task_create: TaskCreate) -> Task:
    task = Task(
        name=task_create.name,
        api_name=task_create.api_name,
        config_schema=task_create.config_schema
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task_by_id(db: AsyncSession, task_id: UUID) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def list_tasks(db: AsyncSession):
    result = await db.execute(select(Task).order_by(Task.created_at.desc()))
    return result.scalars().all()


async def update_task(db: AsyncSession, task_id: UUID, task_create: TaskCreate) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task:
        task.name = task_create.name
        task.api_name = task_create.api_name
        task.config_schema = task_create.config_schema
        await db.commit()
        await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: UUID) -> bool:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task:
        await db.delete(task)
        await db.commit()
        return True
    return False


async def create_task_execution(db: AsyncSession, task_id: UUID, status: str = "running",
                                total_count: int = 0) -> TaskExecution:
    lock = await get_lock(f"task:execution:{task_id}", expire=60, timeout=5)
    async with lock:
        execution = TaskExecution(
            task_id=task_id,
            status=status,
            total_count=total_count,
            start_time=datetime.now()
        )
        db.add(execution)
        await db.commit()
        await db.refresh(execution)
        return execution


async def update_task_execution(db: AsyncSession, execution_id: UUID, **kwargs) -> TaskExecution | None:
    lock = await get_lock(f"task:execution:update:{execution_id}", expire=30, timeout=5)
    async with lock:
        result = await db.execute(select(TaskExecution).where(TaskExecution.id == execution_id))
        execution = result.scalar_one_or_none()
        if execution:
            for key, value in kwargs.items():
                setattr(execution, key, value)
            await db.commit()
            await db.refresh(execution)
        return execution


async def get_task_execution(db: AsyncSession, execution_id: UUID) -> TaskExecution | None:
    result = await db.execute(select(TaskExecution).where(TaskExecution.id == execution_id))
    return result.scalar_one_or_none()


async def list_task_executions(db: AsyncSession, task_id: UUID | None = None, limit: int = 20):
    query = select(TaskExecution)
    if task_id:
        query = query.where(TaskExecution.task_id == task_id)
    query = query.order_by(TaskExecution.start_time.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_scheduler(db: AsyncSession, scheduler_create: SchedulerCreate) -> Scheduler:
    scheduler = Scheduler(
        name=scheduler_create.name,
        task_id=scheduler_create.task_id,
        cron_expression=scheduler_create.cron_expression,
        config=scheduler_create.config,
        status=scheduler_create.status
    )
    db.add(scheduler)
    await db.commit()
    await db.refresh(scheduler)
    return scheduler


async def get_scheduler_by_id(db: AsyncSession, scheduler_id: UUID) -> Scheduler | None:
    result = await db.execute(select(Scheduler).where(Scheduler.id == scheduler_id))
    return result.scalar_one_or_none()


async def list_schedulers(db: AsyncSession):
    result = await db.execute(select(Scheduler).order_by(Scheduler.created_at.desc()))
    return result.scalars().all()


async def update_scheduler_status(db: AsyncSession, scheduler_id: UUID, status: str) -> Scheduler | None:
    lock = await get_lock(f"scheduler:status:{scheduler_id}", expire=30, timeout=5)
    async with lock:
        result = await db.execute(select(Scheduler).where(Scheduler.id == scheduler_id))
        scheduler = result.scalar_one_or_none()
        if scheduler:
            scheduler.status = status
            await db.commit()
            await db.refresh(scheduler)
        return scheduler


async def create_message(db: AsyncSession, user_id: UUID, title: str, content: str,
                         type: str, related_task_id: UUID | None = None) -> Message:
    message = Message(
        user_id=user_id,
        title=title,
        content=content,
        type=type,
        related_task_id=related_task_id
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def list_messages(db: AsyncSession, user_id: UUID, status: str | None = None, limit: int = 20):
    query = select(Message).where(Message.user_id == user_id)
    if status:
        query = query.where(Message.status == status)
    query = query.order_by(Message.created_at.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def update_message_status(db: AsyncSession, message_id: UUID, status: str) -> Message | None:
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    if message:
        message.status = status
        await db.commit()
        await db.refresh(message)
    return message