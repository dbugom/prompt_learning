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
    "title": "Role Prompting and System Messages",
    "slug": "role-prompting",
    "description": "Learn how to use system messages and role prompting to guide LLM behavior and create specialized AI assistants.",
    "difficulty": "beginner",
    "order": 3,
    "language": "python",
    "estimated_time": 40,
    "tags": ["prompt-engineering", "system-messages", "role-prompting", "personas"],
    "content": """# Role Prompting and System Messages

## Learning Objectives
- Understand the difference between system, user, and assistant messages
- Learn how to craft effective system prompts that define AI behavior
- Create specialized AI assistants using role prompting
- Apply persona techniques to control tone, style, and expertise level

## Introduction

One of the most powerful techniques in prompt engineering is **role prompting** - instructing the LLM to adopt a specific persona, expertise level, or behavioral pattern.

The OpenAI Chat Completions API uses three message roles:
- **System**: Sets the assistant's behavior, personality, and constraints
- **User**: The human's input or question
- **Assistant**: The AI's previous responses (for conversation context)

## Core Concepts

### The Three Message Roles

**System Message** - Sets the stage for how the AI should behave
**User Message** - The actual question or task from the human  
**Assistant Message** - AI's previous responses in the conversation

### Anatomy of an Effective System Prompt

A well-crafted system prompt should include:
1. Role/Identity
2. Expertise Level
3. Tone/Style
4. Constraints
5. Output Format

## Your Task

Create specialist assistants with different roles using system messages.
""",
    "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def create_specialist_assistant() -> dict:
    code_to_review = "result = [x**2 for x in range(1000000)]"
    user_message = f"Review this code: {code_to_review}"
    
    # TODO: Create system messages for different specialists
    system_explainer = ""  # Beginner-friendly explainer
    system_security = ""  # Security auditor
    system_performance = ""  # Performance optimizer
    
    try:
        # TODO: Get responses from each specialist
        return {
            "code_explainer": "",
            "security_auditor": "",
            "performance_optimizer": ""
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = create_specialist_assistant()
    print("=== CODE EXPLAINER ===")
    print(results.get("code_explainer"))
    print("\\n=== SECURITY AUDITOR ===")
    print(results.get("security_auditor"))
    print("\\n=== PERFORMANCE OPTIMIZER ===")
    print(results.get("performance_optimizer"))
""",
    "solution_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def create_specialist_assistant() -> dict:
    code_to_review = "result = [x**2 for x in range(1000000)]"
    user_message = f"Review this code: {code_to_review}"
    
    system_explainer = \"\"\"You are a patient programming teacher explaining code to complete beginners. 
Use simple language, everyday analogies, and avoid technical jargon. 
Break down what the code does step by step in 3-4 sentences.\"\"\"
    
    system_security = \"\"\"You are a senior security engineer reviewing code for vulnerabilities. 
Analyze for security issues, resource exhaustion attacks, and potential exploits. 
Provide technical analysis with specific security concerns. Be concise.\"\"\"
    
    system_performance = \"\"\"You are a performance optimization expert specializing in Python. 
Identify memory and CPU inefficiencies. Suggest specific optimizations with code examples. 
Focus on time/space complexity improvements. Keep response under 5 sentences.\"\"\"
    
    try:
        explainer_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_explainer},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        explainer_response = explainer_completion.choices[0].message.content
        
        security_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_security},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=150
        )
        security_response = security_completion.choices[0].message.content
        
        performance_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_performance},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=150
        )
        performance_response = performance_completion.choices[0].message.content
        
        return {
            "code_explainer": explainer_response,
            "security_auditor": security_response,
            "performance_optimizer": performance_response
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = create_specialist_assistant()
    print("=== CODE EXPLAINER ===")
    print(results.get("code_explainer"))
    print("\\n=== SECURITY AUDITOR ===")
    print(results.get("security_auditor"))
    print("\\n=== PERFORMANCE OPTIMIZER ===")
    print(results.get("performance_optimizer"))
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:code_explainer", "description": "Should return code explainer response"},
        {"input": "", "expected_output": "contains:security_auditor", "description": "Should return security auditor response"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
