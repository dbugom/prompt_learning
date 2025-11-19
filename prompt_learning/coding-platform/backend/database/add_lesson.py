"""
Script to add a new lesson to the database
Usage: python -m backend.database.add_lesson
"""

import asyncio
import sys
from database.connection import AsyncSessionLocal, init_db
from models.lesson import Lesson

async def add_lesson(lesson_data):
    """Add a single lesson to the database"""
    await init_db()

    async with AsyncSessionLocal() as session:
        # Check if lesson with same slug already exists
        from sqlalchemy import select
        result = await session.execute(
            select(Lesson).where(Lesson.slug == lesson_data["slug"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"❌ Lesson with slug '{lesson_data['slug']}' already exists")
            return False

        # Create new lesson
        lesson = Lesson(**lesson_data)
        session.add(lesson)
        await session.commit()

        print(f"✓ Successfully created lesson: {lesson_data['title']}")
        return True

# Example lesson - modify this with your own lesson data
NEW_LESSON = {
    "title": "Advanced Loops and Comprehensions",
    "slug": "advanced-loops-comprehensions",
    "description": "Master advanced iteration techniques in Python",
    "difficulty": "intermediate",
    "order": 6,
    "language": "python",
    "estimated_time": 40,
    "tags": ["loops", "comprehensions", "advanced"],
    "content": """# Advanced Loops and Comprehensions

In this lesson, you'll learn:
- List comprehensions
- Dictionary comprehensions
- Nested loops
- Advanced iteration techniques

## List Comprehensions

List comprehensions provide a concise way to create lists:

```python
# Traditional way
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10)]
```

## Your Task

Create a function called `get_evens(numbers)` that:
- Takes a list of numbers
- Returns only the even numbers
- Use a list comprehension

**Example:**
```python
print(get_evens([1, 2, 3, 4, 5, 6]))  # Output: [2, 4, 6]
```
""",
    "starter_code": """def get_evens(numbers):
    # Use list comprehension here
    pass

# Test your function
print(get_evens([1, 2, 3, 4, 5, 6]))
""",
    "solution_code": """def get_evens(numbers):
    return [n for n in numbers if n % 2 == 0]

print(get_evens([1, 2, 3, 4, 5, 6]))
""",
    "test_cases": [
        {
            "input": "",
            "expected_output": "[2, 4, 6]",
            "description": "Filter even numbers"
        }
    ]
}

if __name__ == "__main__":
    try:
        asyncio.run(add_lesson(NEW_LESSON))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
