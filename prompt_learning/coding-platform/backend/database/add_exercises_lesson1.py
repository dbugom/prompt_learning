import asyncio
import sys
from database.connection import AsyncSessionLocal, init_db
from models.lesson import Lesson
from sqlalchemy import select, text

async def add_exercises_to_lesson1():
    """Add practical exercises to Lesson 1"""
    await init_db()

    # First, ensure the exercises column exists
    async with AsyncSessionLocal() as session:
        try:
            # Add column if it doesn't exist
            await session.execute(text(
                "ALTER TABLE lessons ADD COLUMN IF NOT EXISTS exercises JSON"
            ))
            await session.commit()
            print("✓ Ensured exercises column exists")
        except Exception as e:
            print(f"Note: {e}")
            await session.rollback()

    # Now update Lesson 1 with exercises
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Lesson).where(Lesson.slug == "intro-to-llms")
        )
        lesson = result.scalar_one_or_none()

        if not lesson:
            print("❌ Lesson 1 (intro-to-llms) not found")
            return False

        # Define the practical exercises
        exercises = [
            {
                "id": 1,
                "title": "Exercise 1: Deterministic Responses",
                "question": """Your task: Modify the code to get a **deterministic response** (consistent output each time).

Ask the question: "What is 2+2?" and ensure you get the same answer every time you run it.

Requirements:
- Use temperature=0.2 for consistency
- Set max_tokens=20
- The output should be consistent across multiple runs""",
                "hint": "Lower temperature values (0-0.3) produce more deterministic results. Use temperature=0.2",
                "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def deterministic_answer():
    # TODO: Modify the parameters below
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        temperature=0.7,  # TODO: Change this
        max_tokens=100    # TODO: Change this
    )
    return response.choices[0].message.content

# Test it
result = deterministic_answer()
print(f"Answer: {result}")
""",
                "solution_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def deterministic_answer():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        temperature=0.2,  # Low temperature for consistency
        max_tokens=20     # Short response
    )
    return response.choices[0].message.content

# Test it
result = deterministic_answer()
print(f"Answer: {result}")
""",
                "validation": {
                    "type": "code_check",
                    "checks": [
                        {"contains": "temperature=0.2", "message": "Temperature should be 0.2"},
                        {"contains": "max_tokens=20", "message": "max_tokens should be 20"}
                    ]
                }
            },
            {
                "id": 2,
                "title": "Exercise 2: Control Response Length",
                "question": """Your task: Create a function that generates a **one-sentence summary** of prompt engineering.

Requirements:
- Use max_tokens=30 to keep it very short
- Ask: "Explain prompt engineering in one sentence"
- The response should be concise (around 15-25 words)""",
                "hint": "Use max_tokens=30 to limit response length. Lower max_tokens = shorter responses",
                "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def short_summary():
    # TODO: Add the correct parameters
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Explain prompt engineering in one sentence"}],
        # TODO: Add temperature and max_tokens
    )
    return response.choices[0].message.content

# Test it
summary = short_summary()
print(f"Summary: {summary}")
print(f"Word count: {len(summary.split())}")
""",
                "solution_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def short_summary():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Explain prompt engineering in one sentence"}],
        temperature=0.7,
        max_tokens=30  # Limit response length
    )
    return response.choices[0].message.content

# Test it
summary = short_summary()
print(f"Summary: {summary}")
print(f"Word count: {len(summary.split())}")
""",
                "validation": {
                    "type": "code_check",
                    "checks": [
                        {"contains": "max_tokens=30", "message": "max_tokens should be 30"}
                    ]
                }
            }
        ]

        # Update the lesson with exercises
        lesson.exercises = exercises
        await session.commit()

        print(f"✓ Successfully added {len(exercises)} exercises to Lesson 1: {lesson.title}")
        print("\nExercises added:")
        for ex in exercises:
            print(f"  - {ex['title']}")

        return True

if __name__ == "__main__":
    asyncio.run(add_exercises_to_lesson1())
