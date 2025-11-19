import asyncio
import sys
from database.connection import AsyncSessionLocal, init_db
from models.lesson import Lesson

async def add_lesson(lesson_data):
    await init_db()
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Lesson).where(Lesson.slug == lesson_data["slug"])
        )
        existing = result.scalar_one_or_none()
        if existing:
            print(f"❌ Lesson with slug '{lesson_data['slug']}' already exists")
            return False
        lesson = Lesson(**lesson_data)
        session.add(lesson)
        await session.commit()
        print(f"✓ Successfully created lesson: {lesson_data['title']}")
        return True

NEW_LESSON = {
    "title": "Few-Shot Learning with Examples",
    "slug": "few-shot-learning",
    "description": "Learn how to use examples in your prompts to teach LLMs new tasks and get consistent, high-quality outputs.",
    "difficulty": "beginner",
    "order": 4,
    "language": "python",
    "estimated_time": 45,
    "tags": ["prompt-engineering", "few-shot", "in-context-learning", "examples"],
    "content": """# Few-Shot Learning with Examples

## Learning Objectives
- Understand zero-shot, one-shot, and few-shot learning paradigms
- Learn when and why to use examples in prompts
- Master techniques for selecting effective examples
- Build a few-shot classifier using the OpenAI API

## Introduction

One of the most powerful capabilities of LLMs is **in-context learning** - the ability to learn new tasks from examples provided in the prompt, without any model retraining.

This lesson covers:
- **Zero-shot**: No examples, just instructions
- **One-shot**: Single example
- **Few-shot**: Multiple examples (typically 2-5)

## Core Concepts

### The Learning Spectrum

**Zero-Shot Learning** - Relies entirely on the model's pre-existing knowledge
**One-Shot Learning** - Shows the model the desired pattern with one example
**Few-Shot Learning** - Multiple examples teach specific patterns and edge cases

### When to Use Few-Shot Learning

Use when you need consistent output formatting or the task is domain-specific.
Stick with zero-shot for common tasks where speed and cost matter.

## Your Task

Build a sentiment classifier that compares zero-shot vs. few-shot approaches.
""",
    "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def few_shot_classifier() -> dict:
    test_review = "Great acting but terrible plot"
    
    # TODO: Create zero-shot prompt (just the task, no examples)
    zero_shot_prompt = ""
    
    # TODO: Create few-shot prompt with 3 examples
    few_shot_prompt = \"\"\"
    Classify movie reviews as: Positive, Negative, or Mixed
    
    Examples:
    # TODO: Add your 3 examples here
    \"\"\"
    
    try:
        # TODO: Get both classifications
        return {
            "zero_shot_result": "",
            "few_shot_result": "",
            "examples_used": 3,
            "test_review": test_review
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = few_shot_classifier()
    print(f"Test Review: {results.get('test_review')}")
    print(f"Zero-Shot: {results.get('zero_shot_result')}")
    print(f"Few-Shot: {results.get('few_shot_result')}")
""",
    "solution_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def few_shot_classifier() -> dict:
    test_review = "Great acting but terrible plot"
    
    zero_shot_prompt = f\"\"\"Classify this movie review as Positive, Negative, or Mixed.

Review: "{test_review}"
Classification:\"\"\"
    
    few_shot_prompt = f\"\"\"Classify movie reviews as: Positive, Negative, or Mixed

Examples:
Review: "Absolutely brilliant! A masterpiece from start to finish." → Classification: Positive

Review: "Boring and poorly written. Waste of time." → Classification: Negative

Review: "Beautiful cinematography but the story was confusing." → Classification: Mixed

Now classify:
Review: "{test_review}" → Classification:\"\"\"
    
    try:
        zero_shot_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": zero_shot_prompt}],
            temperature=0.3,
            max_tokens=50
        )
        zero_shot_result = zero_shot_completion.choices[0].message.content.strip()
        
        few_shot_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": few_shot_prompt}],
            temperature=0.3,
            max_tokens=50
        )
        few_shot_result = few_shot_completion.choices[0].message.content.strip()
        
        return {
            "zero_shot_result": zero_shot_result,
            "few_shot_result": few_shot_result,
            "examples_used": 3,
            "test_review": test_review
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = few_shot_classifier()
    print(f"Test Review: {results.get('test_review')}")
    print(f"Zero-Shot: {results.get('zero_shot_result')}")
    print(f"Few-Shot: {results.get('few_shot_result')}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:zero_shot_result", "description": "Should return zero-shot classification"},
        {"input": "", "expected_output": "contains:few_shot_result", "description": "Should return few-shot classification"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
