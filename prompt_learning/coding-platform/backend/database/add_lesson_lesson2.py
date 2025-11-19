"""
Script to add a new lesson to the database
Usage: python -m database.add_lesson_lesson2
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

# LESSON 2: Writing Clear and Specific Instructions
NEW_LESSON = {
    "title": "Writing Clear and Specific Instructions",
    "slug": "clear-instructions",
    "description": "Master the art of writing precise, unambiguous prompts that get you the results you want from LLMs.",
    "difficulty": "beginner",
    "order": 2,
    "language": "python",
    "estimated_time": 35,
    "tags": ["prompt-engineering", "prompt-design", "clarity", "specificity"],
    "content": """# Writing Clear and Specific Instructions

## Learning Objectives
- Understand why clarity and specificity matter in prompt engineering
- Learn techniques to make prompts more precise and effective
- Compare vague vs. specific prompts and their outputs
- Apply structural techniques to improve prompt quality
- Avoid common ambiguity pitfalls in prompt writing

## Introduction

The quality of an LLM's output is directly proportional to the quality of your input. Vague, ambiguous prompts lead to unpredictable, often unhelpful responses. Clear, specific instructions guide the model to generate exactly what you need.

Think of prompts like instructions to a very capable but literal assistant. If you ask "Write something about dogs," you might get a poem, a scientific article, or a list of dog breeds. But if you ask "Write a 3-paragraph informative article about Golden Retrievers for a family considering adopting one," you'll get precisely what you need.

This lesson teaches you the fundamental skill of crafting clear, specific prompts that consistently deliver high-quality results.

## Core Concepts

### The Six Elements of Specific Prompts

1. **Task Definition**: Exactly what should the model do?
2. **Context**: What background information is relevant?
3. **Format**: How should the output be structured?
4. **Length**: How long should the response be?
5. **Tone/Style**: What voice should the model use?
6. **Constraints**: What should be avoided or included?

## Your Task

Create a function that compares vague vs. specific prompts and demonstrates the difference in quality.
""",
    "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def compare_prompts() -> dict:
    \"\"\"
    Compare responses from vague vs. specific prompts.
    
    Returns:
        dict: Dictionary with 'vague_response' and 'specific_response' keys
    \"\"\"
    # TODO: Define your vague prompt
    vague_prompt = ""  # Your vague prompt here
    
    # TODO: Define your specific prompt
    specific_prompt = \"\"\"
    # Your specific, detailed prompt here
    # Remember to include: task, format, length, tone, constraints
    \"\"\"
    
    try:
        # TODO: Make API call with vague prompt
        vague_response = ""  # Get response for vague_prompt
        
        # TODO: Make API call with specific prompt
        specific_response = ""  # Get response for specific_prompt
        
        return {
            "vague_response": vague_response,
            "specific_response": specific_response
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Test your implementation
if __name__ == "__main__":
    results = compare_prompts()
    print("=== VAGUE PROMPT RESPONSE ===")
    print(results.get("vague_response", "No response"))
    print("\\n=== SPECIFIC PROMPT RESPONSE ===")
    print(results.get("specific_response", "No response"))
""",
    "solution_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def compare_prompts() -> dict:
    \"\"\"
    Compare responses from vague vs. specific prompts.
    
    Returns:
        dict: Dictionary with 'vague_response' and 'specific_response' keys
    \"\"\"
    # Vague prompt - lacks context, format, length, audience
    vague_prompt = "Write about artificial intelligence"
    
    # Specific prompt - includes all key elements
    specific_prompt = \"\"\"
Write a 4-sentence explanation of artificial intelligence for business executives, 
focusing on practical applications in customer service. Use non-technical language 
and include at least one concrete example.
\"\"\"
    
    try:
        # Get response for vague prompt
        vague_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": vague_prompt}],
            temperature=0.7,
            max_tokens=200
        )
        vague_response = vague_completion.choices[0].message.content
        
        # Get response for specific prompt
        specific_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": specific_prompt}],
            temperature=0.7,
            max_tokens=200
        )
        specific_response = specific_completion.choices[0].message.content
        
        return {
            "vague_response": vague_response,
            "specific_response": specific_response
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Test your implementation
if __name__ == "__main__":
    results = compare_prompts()
    print("=== VAGUE PROMPT RESPONSE ===")
    print(results.get("vague_response", "No response"))
    print("\\n=== SPECIFIC PROMPT RESPONSE ===")
    print(results.get("specific_response", "No response"))
""",
    "test_cases": [
        {
            "input": "",
            "expected_output": "contains:vague_response",
            "description": "Should return dictionary with vague_response key"
        },
        {
            "input": "",
            "expected_output": "contains:specific_response",
            "description": "Should return dictionary with specific_response key"
        }
    ]
}

if __name__ == "__main__":
    try:
        asyncio.run(add_lesson(NEW_LESSON))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
