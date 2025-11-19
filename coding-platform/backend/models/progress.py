"""
User progress model for tracking lesson completion
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class UserProgress(Base):
    """
    Track user progress through lessons
    """
    __tablename__ = "user_progress"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(String, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)

    # Progress tracking
    is_completed = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    best_score = Column(Integer, default=0)  # Percentage 0-100

    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    last_attempt_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<UserProgress user={self.user_id} lesson={self.lesson_id}>"
