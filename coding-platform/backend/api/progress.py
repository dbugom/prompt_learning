"""
Progress API endpoints
Tracks user progress through lessons
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database.connection import get_db
from models.user import User
from models.progress import UserProgress
from models.lesson import Lesson
from api.auth import get_current_user

router = APIRouter()

# Pydantic models
class ProgressUpdate(BaseModel):
    """Progress update model"""
    lesson_id: str
    is_completed: Optional[bool] = False
    score: Optional[int] = 0

class ProgressResponse(BaseModel):
    """Progress response model"""
    id: str
    user_id: str
    lesson_id: str
    is_completed: bool
    attempts: int
    best_score: int
    started_at: datetime
    completed_at: Optional[datetime]
    last_attempt_at: Optional[datetime]

    class Config:
        from_attributes = True

class LessonProgressItem(BaseModel):
    """Combined lesson and progress info"""
    lesson_id: str
    lesson_title: str
    lesson_slug: str
    difficulty: Optional[str]
    is_completed: bool
    attempts: int
    best_score: int
    progress_id: Optional[str]

class OverallProgress(BaseModel):
    """Overall user progress statistics"""
    total_lessons: int
    completed_lessons: int
    in_progress_lessons: int
    total_attempts: int
    average_score: float
    completion_rate: float

# API Endpoints
@router.get("/overview", response_model=OverallProgress)
async def get_progress_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get overall progress statistics for current user
    """
    # Get all published lessons
    lessons_result = await db.execute(
        select(Lesson).where(Lesson.is_published == True)
    )
    total_lessons = len(lessons_result.scalars().all())

    # Get user progress
    progress_result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress_records = progress_result.scalars().all()

    completed_lessons = sum(1 for p in progress_records if p.is_completed)
    in_progress_lessons = len(progress_records) - completed_lessons
    total_attempts = sum(p.attempts for p in progress_records)

    # Calculate average score
    avg_score = 0.0
    if progress_records:
        avg_score = sum(p.best_score for p in progress_records) / len(progress_records)

    # Calculate completion rate
    completion_rate = 0.0
    if total_lessons > 0:
        completion_rate = (completed_lessons / total_lessons) * 100

    return OverallProgress(
        total_lessons=total_lessons,
        completed_lessons=completed_lessons,
        in_progress_lessons=in_progress_lessons,
        total_attempts=total_attempts,
        average_score=round(avg_score, 2),
        completion_rate=round(completion_rate, 2)
    )

@router.get("/lessons", response_model=List[LessonProgressItem])
async def get_all_lessons_with_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all lessons with user progress information
    """
    # Get all published lessons
    lessons_result = await db.execute(
        select(Lesson)
        .where(Lesson.is_published == True)
        .order_by(Lesson.order)
    )
    lessons = lessons_result.scalars().all()

    # Get user progress for all lessons
    progress_result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress_records = {p.lesson_id: p for p in progress_result.scalars().all()}

    # Combine lesson and progress data
    result = []
    for lesson in lessons:
        progress = progress_records.get(lesson.id)
        result.append(LessonProgressItem(
            lesson_id=lesson.id,
            lesson_title=lesson.title,
            lesson_slug=lesson.slug,
            difficulty=lesson.difficulty,
            is_completed=progress.is_completed if progress else False,
            attempts=progress.attempts if progress else 0,
            best_score=progress.best_score if progress else 0,
            progress_id=progress.id if progress else None
        ))

    return result

@router.get("/lesson/{lesson_id}", response_model=ProgressResponse)
async def get_lesson_progress(
    lesson_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get progress for a specific lesson
    """
    result = await db.execute(
        select(UserProgress).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.lesson_id == lesson_id
            )
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found for this lesson"
        )

    return ProgressResponse.from_orm(progress)

@router.post("/lesson/{lesson_id}", response_model=ProgressResponse)
async def update_lesson_progress(
    lesson_id: str,
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update or create progress for a lesson
    """
    # Verify lesson exists
    lesson_result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = lesson_result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Get or create progress record
    progress_result = await db.execute(
        select(UserProgress).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.lesson_id == lesson_id
            )
        )
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        # Create new progress record
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            attempts=1,
            best_score=progress_data.score or 0,
            last_attempt_at=datetime.utcnow()
        )
        db.add(progress)
    else:
        # Update existing progress
        progress.attempts += 1
        progress.last_attempt_at = datetime.utcnow()

        # Update best score if current is better
        if progress_data.score and progress_data.score > progress.best_score:
            progress.best_score = progress_data.score

    # Mark as completed if specified
    if progress_data.is_completed and not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = datetime.utcnow()

    await db.commit()
    await db.refresh(progress)

    return ProgressResponse.from_orm(progress)

@router.delete("/lesson/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def reset_lesson_progress(
    lesson_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Reset progress for a specific lesson
    """
    result = await db.execute(
        select(UserProgress).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.lesson_id == lesson_id
            )
        )
    )
    progress = result.scalar_one_or_none()

    if progress:
        await db.delete(progress)
        await db.commit()

    return None
