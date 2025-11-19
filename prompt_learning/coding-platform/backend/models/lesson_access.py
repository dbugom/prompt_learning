"""
Lesson access control model for managing student access to specific lessons
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class UserLessonAccess(Base):
    """
    Controls which lessons are accessible to which users
    By default, all lessons are accessible to all users.
    This table is used to RESTRICT access (blacklist approach).

    If a record exists with is_enabled=False, the user cannot access that lesson.
    If no record exists, the user CAN access the lesson (default allow).
    """
    __tablename__ = "user_lesson_access"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(String, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)

    # Access control
    is_enabled = Column(Boolean, default=True, nullable=False)

    # Audit fields
    disabled_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"))  # Admin who disabled
    disabled_reason = Column(String(500))  # Optional reason for disabling

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Ensure one record per user-lesson combination
    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='uq_user_lesson'),
    )

    def __repr__(self):
        status = "enabled" if self.is_enabled else "disabled"
        return f"<UserLessonAccess user={self.user_id} lesson={self.lesson_id} {status}>"
