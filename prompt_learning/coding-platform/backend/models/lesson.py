"""
Lesson model for storing course content
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, Boolean
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class Lesson(Base):
    """
    Lesson model for storing educational content
    """
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    content = Column(Text, nullable=False)  # Markdown content
    difficulty = Column(String(50))  # beginner, intermediate, advanced
    order = Column(Integer, default=0)  # For sorting lessons

    # Code exercise
    starter_code = Column(Text)  # Initial code template
    solution_code = Column(Text)  # Model solution (hidden from students)
    test_cases = Column(JSON)  # Array of test cases with input/expected output

    # Metadata
    language = Column(String(50), default="python")
    estimated_time = Column(Integer)  # minutes
    tags = Column(JSON)  # Array of tags

    # Status
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Lesson {self.title}>"
