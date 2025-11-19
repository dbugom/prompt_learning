"""
Code Execution API endpoints
Handles secure code execution via Piston engine
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import httpx
import os
import time
from loguru import logger

from database.connection import get_db
from models.user import User
from models.submission import CodeSubmission
from models.lesson import Lesson
from api.auth import get_current_user

router = APIRouter()

# Piston configuration
PISTON_URL = os.getenv("PISTON_URL", "http://piston:2000")

# Pydantic models
class CodeExecuteRequest(BaseModel):
    """Code execution request"""
    code: str = Field(..., max_length=10000)
    language: str = Field(default="python", pattern="^(python|javascript|java|cpp|c|go|rust)$")
    stdin: Optional[str] = ""
    lesson_id: Optional[str] = None

class TestCase(BaseModel):
    """Test case model"""
    input: str
    expected_output: str
    description: Optional[str] = None

class CodeExecuteResponse(BaseModel):
    """Code execution response"""
    output: str
    error: Optional[str] = None
    execution_time: float
    status: str
    submission_id: str
    test_results: Optional[List[Dict[str, Any]]] = None

class PistonRuntime(BaseModel):
    """Piston runtime information"""
    language: str
    version: str
    aliases: List[str]

# Helper functions
async def execute_code_on_piston(code: str, language: str, stdin: str = "") -> Dict[str, Any]:
    """
    Execute code on Piston engine
    """
    # Map language to Piston runtime
    language_map = {
        "python": "python",
        "javascript": "javascript",
        "java": "java",
        "cpp": "cpp",
        "c": "c",
        "go": "go",
        "rust": "rust"
    }

    piston_language = language_map.get(language, "python")

    # Prepare request payload
    payload = {
        "language": piston_language,
        "version": "*",  # Use latest version
        "files": [
            {
                "name": f"main.{get_file_extension(language)}",
                "content": code
            }
        ],
        "stdin": stdin,
        "args": [],
        "compile_timeout": 10000,  # 10 seconds
        "run_timeout": 10000,  # 10 seconds
        "compile_memory_limit": 512000000,  # 512MB
        "run_memory_limit": 512000000  # 512MB
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            start_time = time.time()
            response = await client.post(f"{PISTON_URL}/api/v2/execute", json=payload)
            execution_time = time.time() - start_time

            if response.status_code != 200:
                logger.error(f"Piston error: {response.text}")
                return {
                    "output": "",
                    "error": f"Execution engine error: {response.text}",
                    "execution_time": execution_time,
                    "status": "error"
                }

            result = response.json()

            return {
                "output": result.get("run", {}).get("stdout", ""),
                "error": result.get("run", {}).get("stderr", "") or result.get("compile", {}).get("stderr", ""),
                "execution_time": execution_time,
                "status": "success" if not result.get("run", {}).get("stderr") else "error",
                "exit_code": result.get("run", {}).get("code", 0)
            }

    except httpx.TimeoutException:
        logger.error("Piston timeout")
        return {
            "output": "",
            "error": "Execution timeout (maximum 10 seconds)",
            "execution_time": 10.0,
            "status": "timeout"
        }
    except Exception as e:
        logger.error(f"Piston execution error: {e}")
        return {
            "output": "",
            "error": f"Execution error: {str(e)}",
            "execution_time": 0.0,
            "status": "error"
        }

def get_file_extension(language: str) -> str:
    """Get file extension for language"""
    extensions = {
        "python": "py",
        "javascript": "js",
        "java": "java",
        "cpp": "cpp",
        "c": "c",
        "go": "go",
        "rust": "rs"
    }
    return extensions.get(language, "txt")

async def run_test_cases(code: str, language: str, test_cases: List[Dict]) -> List[Dict[str, Any]]:
    """
    Run code against test cases
    """
    results = []

    for i, test_case in enumerate(test_cases):
        test_input = test_case.get("input", "")
        expected_output = test_case.get("expected_output", "").strip()

        # Execute code with test input
        execution_result = await execute_code_on_piston(code, language, test_input)

        actual_output = execution_result["output"].strip()
        passed = actual_output == expected_output and execution_result["status"] == "success"

        results.append({
            "test_number": i + 1,
            "description": test_case.get("description", f"Test {i + 1}"),
            "input": test_input,
            "expected_output": expected_output,
            "actual_output": actual_output,
            "passed": passed,
            "error": execution_result.get("error")
        })

    return results

# API Endpoints
@router.post("/execute", response_model=CodeExecuteResponse)
async def execute_code(
    request: CodeExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Execute code securely via Piston engine
    """
    # Input validation
    if len(request.code.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code cannot be empty"
        )

    # Security check: Basic malicious code detection
    dangerous_patterns = [
        "import os",
        "import subprocess",
        "import sys",
        "__import__",
        "eval(",
        "exec(",
        "compile(",
    ]

    code_lower = request.code.lower()
    for pattern in dangerous_patterns:
        if pattern.lower() in code_lower:
            logger.warning(f"Dangerous code pattern detected: {pattern} by user {current_user.username}")
            # Allow but log - Piston provides sandboxing

    # Execute code
    execution_result = await execute_code_on_piston(
        request.code,
        request.language,
        request.stdin or ""
    )

    # If lesson_id provided, run test cases
    test_results = None
    tests_passed = 0
    tests_failed = 0

    if request.lesson_id:
        result = await db.execute(select(Lesson).where(Lesson.id == request.lesson_id))
        lesson = result.scalar_one_or_none()

        if lesson and lesson.test_cases:
            test_results = await run_test_cases(
                request.code,
                request.language,
                lesson.test_cases
            )
            tests_passed = sum(1 for t in test_results if t["passed"])
            tests_failed = len(test_results) - tests_passed

    # Save submission to database
    submission = CodeSubmission(
        user_id=current_user.id,
        lesson_id=request.lesson_id,
        code=request.code,
        language=request.language,
        output=execution_result["output"],
        error=execution_result.get("error"),
        execution_time=execution_result["execution_time"],
        exit_code=execution_result.get("exit_code", 0),
        status=execution_result["status"],
        tests_passed=tests_passed,
        tests_failed=tests_failed,
        test_results=test_results
    )

    db.add(submission)

    # Update user stats
    current_user.total_submissions += 1
    if execution_result["status"] == "success" and tests_failed == 0:
        current_user.successful_submissions += 1

    await db.commit()
    await db.refresh(submission)

    return CodeExecuteResponse(
        output=execution_result["output"],
        error=execution_result.get("error"),
        execution_time=execution_result["execution_time"],
        status=execution_result["status"],
        submission_id=submission.id,
        test_results=test_results
    )

@router.get("/runtimes", response_model=List[PistonRuntime])
async def get_runtimes():
    """
    Get available runtimes from Piston
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{PISTON_URL}/api/v2/runtimes")

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Cannot fetch runtimes from execution engine"
                )

            runtimes = response.json()
            return runtimes

    except Exception as e:
        logger.error(f"Error fetching runtimes: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Execution engine unavailable"
        )

@router.get("/submissions/{submission_id}")
async def get_submission(
    submission_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get submission details
    """
    result = await db.execute(
        select(CodeSubmission).where(
            CodeSubmission.id == submission_id,
            CodeSubmission.user_id == current_user.id
        )
    )
    submission = result.scalar_one_or_none()

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    return submission

@router.get("/submissions")
async def get_user_submissions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    offset: int = 0
):
    """
    Get user's submission history
    """
    result = await db.execute(
        select(CodeSubmission)
        .where(CodeSubmission.user_id == current_user.id)
        .order_by(CodeSubmission.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    submissions = result.scalars().all()

    return {
        "submissions": submissions,
        "total": len(submissions),
        "limit": limit,
        "offset": offset
    }
