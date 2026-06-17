from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Dict, Any


class TaskCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    api_name: str = Field(..., min_length=1, max_length=128)
    config_schema: Dict[str, Any]


class TaskResponse(BaseModel):
    id: UUID
    name: str
    api_name: str
    config_schema: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskExecutionResponse(BaseModel):
    id: UUID
    task_id: UUID
    status: str
    progress: int
    completed_count: int
    total_count: int
    current_item: str | None
    start_time: datetime
    end_time: datetime | None
    error_message: str | None
    result: Dict[str, Any] | None
    progress_data: Dict[str, Any] | None

    class Config:
        from_attributes = True


class TaskExecutionCreate(BaseModel):
    task_id: UUID
    status: str = "running"
    total_count: int = 0


class SchedulerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    task_id: UUID
    cron_expression: str = Field(..., min_length=1, max_length=64)
    config: Dict[str, Any] | None = None
    status: str = "active"


class SchedulerResponse(BaseModel):
    id: UUID
    name: str
    task_id: UUID
    cron_expression: str
    config: Dict[str, Any] | None
    status: str
    last_run_time: datetime | None
    next_run_time: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True