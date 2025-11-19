"""
Script to add a new lesson to the database
Usage: python -m database.add_lesson
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
    "estimated_time": 30,
    "tags": ["prompt-engineering", "llm-basics", "openai", "introduction"],
    "content": """# Introduction to LLMs and Prompt Engineering

## Learning Objectives
- Understand what Large Language Models (LLMs) are and how they process text
- Learn about key parameters: temperature, max_tokens, and model selection
- Make your first API call to OpenAI's GPT models
- Understand tokens and how they affect API usage and costs
- Write effective basic prompts

## Introduction

Large Language Models (LLMs) have revolutionized how we interact with computers and process information. These AI models, trained on vast amounts of text data, can understand context, generate human-like responses, and assist with a wide variety of tasks from writing code to answering questions.

**Prompt Engineering** is the art and science of crafting effective inputs (prompts) to get the best possible outputs from LLMs. It's a crucial skill for developers, researchers, and anyone working with AI systems. Unlike traditional programming where you write precise instructions, prompt engineering involves communicating your intent in natural language while understanding the model's capabilities and limitations.

In this lesson, you'll learn the fundamentals of LLMs and make your first API call using Python and the OpenAI library.

## Core Concepts

### What are LLMs?

Large Language Models are neural networks trained on massive text datasets. They learn patterns, relationships, and structures in language, enabling them to:
- Generate coherent, contextually relevant text
- Answer questions based on learned knowledge
- Complete tasks like summarization, translation, and code generation
- Understand nuance, context, and even some reasoning

Popular LLMs include:
- **GPT-4 / GPT-3.5** (OpenAI) - General purpose, highly capable
- **Claude** (Anthropic) - Strong reasoning and safety features
- **Gemini** (Google) - Multimodal capabilities
- **Llama** (Meta) - Open source alternative

### Understanding Tokens

Tokens are the basic units that LLMs process. A token can be:
- A whole word: "hello" = 1 token
- Part of a word: "programming" = 2 tokens ("program" + "ming")
- Punctuation: "!" = 1 token

**Why tokens matter:**
- API pricing is based on tokens (input + output)
- Models have maximum token limits (context windows)
- GPT-3.5-turbo: ~4,096 tokens
- GPT-4: ~8,192 tokens (some versions up to 128k)

**Rule of thumb:** 1 token ≈ 4 characters or ≈ 0.75 words in English

### Key Parameters

When calling an LLM API, you control behavior through parameters:

**1. Temperature (0.0 - 2.0)**
- Controls randomness/creativity
- **0.0**: Deterministic, same output every time (good for factual tasks)
- **0.7**: Balanced creativity (default for most uses)
- **1.5+**: Very creative, unpredictable (good for brainstorming)

**2. Max Tokens**
- Maximum length of the response
- Prevents runaway costs and ensures concise answers
- Does NOT include input tokens

**3. Model Selection**
- **gpt-3.5-turbo**: Fast, cheap, good for simple tasks ($0.0015/1k tokens)
- **gpt-4**: Slower, expensive, best reasoning ($0.03/1k tokens)
- Choose based on task complexity and budget

## Your Task

Create a function called `ask_llm()` that takes a question and returns an LLM response with appropriate parameters.
""",
    "starter_code": """import os
from openai import OpenAI

# Initialize OpenAI client
# API key should be set in environment variable: OPENAI_API_KEY
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def ask_llm(question: str) -> str:
    \"\"\"
    Send a question to GPT-3.5-turbo and return the response.

    Args:
        question (str): The question to ask the LLM

    Returns:
        str: The LLM's response
    \"\"\"
    # TODO: Implement the API call
    # Hint: Use client.chat.completions.create()
    # Remember to set temperature=0.7 and max_tokens=200

    try:
        # Your code here
        pass
    except Exception as e:
        return f"Error: {str(e)}"

# Test your implementation
if __name__ == "__main__":
    test_question = "What is prompt engineering in one sentence?"
    response = ask_llm(test_question)
    print(f"Question: {test_question}")
    print(f"Answer: {response}")
""",
    "solution_code": """import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def ask_llm(question: str) -> str:
    \"\"\"
    Send a question to GPT-3.5-turbo and return the response.

    Args:
        question (str): The question to ask the LLM

    Returns:
        str: The LLM's response
    \"\"\"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Test your implementation
if __name__ == "__main__":
    test_question = "What is prompt engineering in one sentence?"
    response = ask_llm(test_question)
    print(f"Question: {test_question}")
    print(f"Answer: {response}")
""",
    "test_cases": [
        {
            "input": "",
            "expected_output": "contains:prompt engineering",
            "description": "Function should return a response about prompt engineering"
        }
    ]
}

if __name__ == "__main__":
    try:
        asyncio.run(add_lesson(NEW_LESSON))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
