"""
Lessons API endpoints
Manages educational content and lessons
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from database.connection import get_db
from models.user import User
from models.lesson import Lesson
from api.auth import get_current_user

router = APIRouter()

# Pydantic models
class TestCaseModel(BaseModel):
    """Test case model"""
    input: str
    expected_output: str
    description: Optional[str] = None

class LessonCreate(BaseModel):
    """Lesson creation model"""
    title: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    description: Optional[str] = None
    content: str
    difficulty: Optional[str] = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    order: int = 0
    starter_code: Optional[str] = None
    solution_code: Optional[str] = None
    test_cases: Optional[List[Dict[str, str]]] = None
    language: str = Field(default="python")
    estimated_time: Optional[int] = None
    tags: Optional[List[str]] = None

class LessonUpdate(BaseModel):
    """Lesson update model"""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    difficulty: Optional[str] = None
    order: Optional[int] = None
    starter_code: Optional[str] = None
    solution_code: Optional[str] = None
    test_cases: Optional[List[Dict[str, str]]] = None
    estimated_time: Optional[int] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None

class LessonResponse(BaseModel):
    """Lesson response model"""
    id: str
    title: str
    slug: str
    description: Optional[str]
    content: str
    difficulty: Optional[str]
    order: int
    starter_code: Optional[str]
    # solution_code is not exposed to students
    test_cases: Optional[List[Dict[str, str]]]
    language: str
    estimated_time: Optional[int]
    tags: Optional[List[str]]
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LessonListItem(BaseModel):
    """Lesson list item (summary)"""
    id: str
    title: str
    slug: str
    description: Optional[str]
    difficulty: Optional[str]
    order: int
    language: str
    estimated_time: Optional[int]
    tags: Optional[List[str]]

    class Config:
        from_attributes = True

# API Endpoints
@router.get("", response_model=List[LessonListItem])
async def get_lessons(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all published lessons (sorted by order)
    """
    result = await db.execute(
        select(Lesson)
        .where(Lesson.is_published == True)
        .order_by(Lesson.order)
    )
    lessons = result.scalars().all()

    return [LessonListItem.from_orm(lesson) for lesson in lessons]

@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get lesson by ID
    """
    result = await db.execute(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.is_published == True
        )
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    return LessonResponse.from_orm(lesson)

@router.get("/slug/{slug}", response_model=LessonResponse)
async def get_lesson_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get lesson by slug
    """
    result = await db.execute(
        select(Lesson).where(
            Lesson.slug == slug,
            Lesson.is_published == True
        )
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    return LessonResponse.from_orm(lesson)

@router.post("", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson_data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new lesson (admin only)
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create lessons"
        )

    # Check if slug already exists
    result = await db.execute(select(Lesson).where(Lesson.slug == lesson_data.slug))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lesson with this slug already exists"
        )

    # Create lesson
    new_lesson = Lesson(
        title=lesson_data.title,
        slug=lesson_data.slug,
        description=lesson_data.description,
        content=lesson_data.content,
        difficulty=lesson_data.difficulty,
        order=lesson_data.order,
        starter_code=lesson_data.starter_code,
        solution_code=lesson_data.solution_code,
        test_cases=lesson_data.test_cases,
        language=lesson_data.language,
        estimated_time=lesson_data.estimated_time,
        tags=lesson_data.tags
    )

    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)

    return LessonResponse.from_orm(new_lesson)

@router.put("/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: str,
    lesson_data: LessonUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a lesson (admin only)
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update lessons"
        )

    # Get lesson
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Update fields
    update_data = lesson_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)

    await db.commit()
    await db.refresh(lesson)

    return LessonResponse.from_orm(lesson)

@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a lesson (admin only)
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete lessons"
        )

    # Get lesson
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    await db.delete(lesson)
    await db.commit()

    return None
