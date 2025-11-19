"""
Admin API endpoints for managing lesson access control
Only accessible to users with is_admin=True
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from database.connection import get_db
from models.user import User
from models.lesson import Lesson
from models.lesson_access import UserLessonAccess
from api.auth import get_current_user
import uuid

router = APIRouter()

# Pydantic models
class LessonAccessUpdate(BaseModel):
    """Model for updating lesson access"""
    is_enabled: bool
    disabled_reason: Optional[str] = Field(None, max_length=500)

class LessonAccessResponse(BaseModel):
    """Response model for lesson access"""
    id: str
    user_id: str
    lesson_id: str
    is_enabled: bool
    disabled_by: Optional[str]
    disabled_reason: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserLessonAccessInfo(BaseModel):
    """Combined info about user's access to a lesson"""
    lesson_id: str
    lesson_title: str
    lesson_slug: str
    is_enabled: bool
    access_record_id: Optional[str]
    disabled_reason: Optional[str]

class StudentInfo(BaseModel):
    """Basic student information"""
    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool

# Dependency to check admin status
async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verify that the current user is an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This operation requires administrator privileges"
        )
    return current_user

# ============================================================================
# ADMIN ENDPOINTS - Manage Lesson Access for Students
# ============================================================================

@router.get("/students", response_model=List[StudentInfo])
async def get_all_students(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Get list of all students (non-admin users)
    """
    result = await db.execute(
        select(User).where(User.is_admin == False).order_by(User.username)
    )
    students = result.scalars().all()
    return students

@router.get("/students/{user_id}/lessons", response_model=List[UserLessonAccessInfo])
async def get_student_lesson_access(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Get all lessons and their access status for a specific student
    """
    # Verify student exists
    student_result = await db.execute(select(User).where(User.id == user_id))
    student = student_result.scalar_one_or_none()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Get all lessons
    lessons_result = await db.execute(
        select(Lesson).where(Lesson.is_published == True).order_by(Lesson.order)
    )
    lessons = lessons_result.scalars().all()

    # Get access records for this student
    access_result = await db.execute(
        select(UserLessonAccess).where(UserLessonAccess.user_id == user_id)
    )
    access_records = {record.lesson_id: record for record in access_result.scalars().all()}

    # Build response
    response = []
    for lesson in lessons:
        access_record = access_records.get(lesson.id)
        response.append(UserLessonAccessInfo(
            lesson_id=lesson.id,
            lesson_title=lesson.title,
            lesson_slug=lesson.slug,
            is_enabled=access_record.is_enabled if access_record else True,  # Default: enabled
            access_record_id=access_record.id if access_record else None,
            disabled_reason=access_record.disabled_reason if access_record else None
        ))

    return response

@router.put("/students/{user_id}/lessons/{lesson_id}/access")
async def update_lesson_access(
    user_id: str,
    lesson_id: str,
    access_data: LessonAccessUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Enable or disable a lesson for a specific student
    """
    # Verify student exists
    student_result = await db.execute(select(User).where(User.id == user_id))
    student = student_result.scalar_one_or_none()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Verify lesson exists
    lesson_result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Check if access record already exists
    access_result = await db.execute(
        select(UserLessonAccess).where(
            and_(
                UserLessonAccess.user_id == user_id,
                UserLessonAccess.lesson_id == lesson_id
            )
        )
    )
    access_record = access_result.scalar_one_or_none()

    if access_record:
        # Update existing record
        access_record.is_enabled = access_data.is_enabled
        access_record.disabled_by = admin.id if not access_data.is_enabled else None
        access_record.disabled_reason = access_data.disabled_reason if not access_data.is_enabled else None
    else:
        # Create new record
        access_record = UserLessonAccess(
            id=str(uuid.uuid4()),
            user_id=user_id,
            lesson_id=lesson_id,
            is_enabled=access_data.is_enabled,
            disabled_by=admin.id if not access_data.is_enabled else None,
            disabled_reason=access_data.disabled_reason
        )
        db.add(access_record)

    await db.commit()
    await db.refresh(access_record)

    action = "enabled" if access_data.is_enabled else "disabled"
    return {
        "success": True,
        "message": f"Lesson '{lesson.title}' {action} for student '{student.username}'",
        "access_record": LessonAccessResponse.model_validate(access_record)
    }

@router.delete("/students/{user_id}/lessons/{lesson_id}/access")
async def remove_lesson_access_restriction(
    user_id: str,
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Remove access restriction (revert to default allow)
    This deletes the access record, allowing default access
    """
    # Find the access record
    access_result = await db.execute(
        select(UserLessonAccess).where(
            and_(
                UserLessonAccess.user_id == user_id,
                UserLessonAccess.lesson_id == lesson_id
            )
        )
    )
    access_record = access_result.scalar_one_or_none()

    if not access_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No access restriction found for this user-lesson combination"
        )

    await db.delete(access_record)
    await db.commit()

    return {
        "success": True,
        "message": "Access restriction removed. Student now has default access to this lesson."
    }

@router.post("/students/{user_id}/lessons/disable-all")
async def disable_all_lessons_for_student(
    user_id: str,
    reason: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Disable all lessons for a student (useful for account suspension)
    """
    # Verify student exists
    student_result = await db.execute(select(User).where(User.id == user_id))
    student = student_result.scalar_one_or_none()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Get all lessons
    lessons_result = await db.execute(
        select(Lesson).where(Lesson.is_published == True)
    )
    lessons = lessons_result.scalars().all()

    disabled_count = 0
    for lesson in lessons:
        # Check if record exists
        access_result = await db.execute(
            select(UserLessonAccess).where(
                and_(
                    UserLessonAccess.user_id == user_id,
                    UserLessonAccess.lesson_id == lesson.id
                )
            )
        )
        access_record = access_result.scalar_one_or_none()

        if access_record:
            access_record.is_enabled = False
            access_record.disabled_by = admin.id
            access_record.disabled_reason = reason
        else:
            access_record = UserLessonAccess(
                id=str(uuid.uuid4()),
                user_id=user_id,
                lesson_id=lesson.id,
                is_enabled=False,
                disabled_by=admin.id,
                disabled_reason=reason
            )
            db.add(access_record)

        disabled_count += 1

    await db.commit()

    return {
        "success": True,
        "message": f"Disabled {disabled_count} lessons for student '{student.username}'",
        "disabled_count": disabled_count
    }

@router.post("/students/{user_id}/lessons/enable-all")
async def enable_all_lessons_for_student(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Enable all lessons for a student (remove all restrictions)
    """
    # Verify student exists
    student_result = await db.execute(select(User).where(User.id == user_id))
    student = student_result.scalar_one_or_none()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Delete all access records for this student (revert to default allow)
    await db.execute(
        select(UserLessonAccess).where(UserLessonAccess.user_id == user_id)
    )
    result = await db.execute(
        select(UserLessonAccess).where(UserLessonAccess.user_id == user_id)
    )
    records = result.scalars().all()

    count = 0
    for record in records:
        await db.delete(record)
        count += 1

    await db.commit()

    return {
        "success": True,
        "message": f"Enabled all lessons for student '{student.username}'. Removed {count} restrictions.",
        "removed_count": count
    }
