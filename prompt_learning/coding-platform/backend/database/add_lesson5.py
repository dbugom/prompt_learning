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
    "title": "Prompt Templates and Variables",
    "slug": "prompt-templates",
    "description": "Learn to create reusable prompt templates with variable substitution for efficient and maintainable LLM applications.",
    "difficulty": "beginner",
    "order": 5,
    "language": "python",
    "estimated_time": 40,
    "tags": ["prompt-engineering", "templates", "variables", "reusability"],
    "content": """# Prompt Templates and Variables

## Learning Objectives
- Understand the benefits of prompt templates
- Learn variable substitution techniques in Python
- Master f-strings, format(), and template strings
- Create reusable, maintainable prompt functions
- Build a template library for common tasks

## Introduction

As you build more LLM applications, you'll find yourself writing similar prompts repeatedly. **Prompt templates** solve this problem by creating reusable patterns with placeholders for dynamic content.

Think of templates like functions in programming - instead of copying code everywhere, you define it once and reuse it with different inputs.

Benefits of prompt templates:
- **Consistency**: Same structure across similar tasks
- **Maintainability**: Update once, apply everywhere
- **Readability**: Clear separation of logic and content
- **Testability**: Easy to test with different inputs

## Core Concepts

### Why Templates Matter

**Without templates (repetitive):**
```python
prompt1 = "Translate 'Hello' to Spanish"
prompt2 = "Translate 'Goodbye' to Spanish"
prompt3 = "Translate 'Thank you' to Spanish"
```

**With templates (reusable):**
```python
def translate_prompt(text, language):
    return f"Translate '{text}' to {language}"

prompt1 = translate_prompt("Hello", "Spanish")
prompt2 = translate_prompt("Goodbye", "Spanish")
```

### Python String Formatting Methods

**1. f-strings (Recommended - Python 3.6+)**
- Most readable and concise
- Direct variable interpolation
```python
name = "Alice"
prompt = f"Hello, {name}!"  # "Hello, Alice!"
```

**2. format() method**
- Good for complex formatting
- Named and positional arguments
```python
prompt = "Hello, {}!".format(name)
prompt = "Hello, {user}!".format(user=name)
```

**3. Template strings (from string module)**
- Safe for user input (prevents code injection)
- Explicit placeholder syntax
```python
from string import Template
t = Template("Hello, $name!")
prompt = t.substitute(name="Alice")
```

### Template Design Patterns

**1. Simple Variable Substitution**
```python
def summarize_prompt(text, max_words):
    return f"Summarize this text in {max_words} words: {text}"
```

**2. Optional Parameters**
```python
def analyze_prompt(text, tone="neutral", detail_level="medium"):
    return f\"\"\"Analyze this text with {tone} tone and {detail_level} detail:

{text}\"\"\"
```

**3. Multi-Part Templates**
```python
SYSTEM_TEMPLATE = "You are a {role} assistant."
USER_TEMPLATE = "Please help me with: {task}"
```

## Your Task

Build a prompt template system for a customer support chatbot that handles multiple scenarios.
""",
    "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def create_support_templates():
    \"\"\"
    Create reusable prompt templates for customer support scenarios.

    Returns:
        dict: Results from different template applications
    \"\"\"

    # TODO: Create a template for product inquiry responses
    # Should accept: product_name, customer_name
    def product_inquiry_template(product_name: str, customer_name: str) -> str:
        # Your template here
        pass

    # TODO: Create a template for complaint handling
    # Should accept: issue_description, customer_name, priority (default="medium")
    def complaint_template(issue_description: str, customer_name: str, priority: str = "medium") -> str:
        # Your template here
        pass

    # TODO: Create a template for technical support
    # Should accept: problem, product, error_message (optional)
    def technical_support_template(problem: str, product: str, error_message: str = None) -> str:
        # Your template here
        pass

    # Test data
    test_cases = {
        "product_inquiry": {
            "product_name": "SmartWatch Pro",
            "customer_name": "Sarah"
        },
        "complaint": {
            "issue_description": "Product arrived damaged",
            "customer_name": "John",
            "priority": "high"
        },
        "technical_support": {
            "problem": "App won't sync",
            "product": "Fitness Tracker",
            "error_message": "Error 404: Device not found"
        }
    }

    try:
        # TODO: Generate prompts using your templates
        product_prompt = ""  # Use product_inquiry_template
        complaint_prompt = ""  # Use complaint_template
        tech_prompt = ""  # Use technical_support_template

        # TODO: Get LLM responses for each
        return {
            "product_inquiry_response": "",
            "complaint_response": "",
            "technical_support_response": "",
            "templates_created": 3
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = create_support_templates()
    for key, value in results.items():
        print(f"{key}: {value}\\n")
""",
    "solution_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def create_support_templates():
    \"\"\"
    Create reusable prompt templates for customer support scenarios.

    Returns:
        dict: Results from different template applications
    \"\"\"

    def product_inquiry_template(product_name: str, customer_name: str) -> str:
        return f\"\"\"You are a friendly customer support agent.

A customer named {customer_name} is asking about the {product_name}.
Provide helpful information about this product's key features and benefits.
Keep your response concise (2-3 sentences) and enthusiastic.\"\"\"

    def complaint_template(issue_description: str, customer_name: str, priority: str = "medium") -> str:
        urgency_map = {
            "low": "Please address this concern at your convenience.",
            "medium": "Please address this promptly.",
            "high": "This requires immediate attention and resolution."
        }
        urgency = urgency_map.get(priority, urgency_map["medium"])

        return f\"\"\"You are an empathetic customer support manager.

Customer: {customer_name}
Issue: {issue_description}
Priority: {priority.upper()}

{urgency}
Respond with empathy, acknowledge the issue, and provide a clear resolution plan in 3-4 sentences.\"\"\"

    def technical_support_template(problem: str, product: str, error_message: str = None) -> str:
        error_section = f"\\nError message: {error_message}" if error_message else ""

        return f\"\"\"You are a technical support specialist.

Product: {product}
Problem: {problem}{error_section}

Provide step-by-step troubleshooting instructions. Be clear, concise, and non-technical.
Limit response to 4-5 steps.\"\"\"

    # Test data
    test_cases = {
        "product_inquiry": {
            "product_name": "SmartWatch Pro",
            "customer_name": "Sarah"
        },
        "complaint": {
            "issue_description": "Product arrived damaged",
            "customer_name": "John",
            "priority": "high"
        },
        "technical_support": {
            "problem": "App won't sync",
            "product": "Fitness Tracker",
            "error_message": "Error 404: Device not found"
        }
    }

    try:
        # Generate prompts using templates
        product_prompt = product_inquiry_template(
            test_cases["product_inquiry"]["product_name"],
            test_cases["product_inquiry"]["customer_name"]
        )

        complaint_prompt = complaint_template(
            test_cases["complaint"]["issue_description"],
            test_cases["complaint"]["customer_name"],
            test_cases["complaint"]["priority"]
        )

        tech_prompt = technical_support_template(
            test_cases["technical_support"]["problem"],
            test_cases["technical_support"]["product"],
            test_cases["technical_support"]["error_message"]
        )

        # Get LLM responses
        product_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": product_prompt}],
            temperature=0.7,
            max_tokens=150
        ).choices[0].message.content

        complaint_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": complaint_prompt}],
            temperature=0.6,
            max_tokens=150
        ).choices[0].message.content

        tech_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": tech_prompt}],
            temperature=0.5,
            max_tokens=200
        ).choices[0].message.content

        return {
            "product_inquiry_response": product_response,
            "complaint_response": complaint_response,
            "technical_support_response": tech_response,
            "templates_created": 3
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = create_support_templates()
    for key, value in results.items():
        print(f"{key}: {value}\\n")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:product_inquiry_response", "description": "Should return product inquiry response"},
        {"input": "", "expected_output": "contains:templates_created", "description": "Should create 3 templates"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
