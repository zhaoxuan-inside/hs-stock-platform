from sqlalchemy import Column, Integer, String, Float, Decimal, Date, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.database import Base
import uuid


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    api_name = Column(String(128), nullable=False)
    config_schema = Column(JSONB, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class TaskExecution(Base):
    __tablename__ = "task_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    status = Column(String(32), nullable=False)
    progress = Column(Integer, nullable=False, default=0)
    completed_count = Column(Integer, nullable=False, default=0)
    total_count = Column(Integer, nullable=False, default=0)
    current_item = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    error_message = Column(Text)
    result = Column(JSONB)
    progress_data = Column(JSONB)


class Scheduler(Base):
    __tablename__ = "schedulers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    cron_expression = Column(String(64), nullable=False)
    config = Column(JSONB)
    status = Column(String(32), nullable=False, default="active")
    last_run_time = Column(DateTime)
    next_run_time = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(32), nullable=False)
    related_task_id = Column(UUID(as_uuid=True))
    status = Column(String(32), nullable=False, default="unread")
    created_at = Column(DateTime, nullable=False, server_default=func.now())