"""
User model for authentication and user management
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class User(Base):
    """
    User model for storing user information
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Track usage
    total_submissions = Column(Integer, default=0)
    successful_submissions = Column(Integer, default=0)

    def __repr__(self):
        return f"<User {self.username}>"
