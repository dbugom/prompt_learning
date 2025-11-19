"""
Code submission model for tracking user code executions
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Float
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class CodeSubmission(Base):
    """
    Store code submissions and execution results
    """
    __tablename__ = "code_submissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(String, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True)

    # Code details
    code = Column(Text, nullable=False)
    language = Column(String(50), default="python")

    # Execution results
    output = Column(Text)
    error = Column(Text)
    execution_time = Column(Float)  # seconds
    memory_used = Column(Integer)  # bytes
    exit_code = Column(Integer)

    # Test results
    tests_passed = Column(Integer, default=0)
    tests_failed = Column(Integer, default=0)
    test_results = Column(JSON)  # Detailed test results

    # Status
    status = Column(String(50))  # pending, running, success, error, timeout
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<CodeSubmission {self.id} status={self.status}>"
