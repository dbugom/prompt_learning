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
    "title": "Introduction to LangChain",
    "slug": "intro-to-langchain",
    "description": "Learn the fundamentals of LangChain, the powerful framework for building LLM applications with PromptTemplates and LLMChains.",
    "difficulty": "intermediate",
    "order": 9,
    "language": "python",
    "estimated_time": 55,
    "tags": ["prompt-engineering", "langchain", "framework", "templates", "intermediate"],
    "content": """# Introduction to LangChain

## Learning Objectives
- Understand what LangChain is and why it's useful
- Learn core LangChain concepts: Models, Prompts, Chains
- Use PromptTemplate for reusable prompts
- Build your first LLMChain
- Compare raw API calls vs. LangChain approach

## Introduction

**LangChain** is a framework for developing applications powered by language models. It provides:

- **Abstractions**: High-level components for common LLM patterns
- **Chains**: Connect multiple LLM calls and logic
- **Memory**: Maintain conversation context
- **Agents**: LLMs that can use tools and make decisions
- **Integrations**: Works with OpenAI, Anthropic, HuggingFace, and more

**Why use LangChain?**

Without LangChain (raw API):
```python
# Repetitive, hard to maintain
response1 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Translate {text} to Spanish"}]
)
response2 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Translate {text} to French"}]
)
```

With LangChain:
```python
# Clean, reusable, composable
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

template = PromptTemplate.from_template("Translate {text} to {language}")
chain = LLMChain(llm=llm, prompt=template)

spanish = chain.run(text="Hello", language="Spanish")
french = chain.run(text="Hello", language="French")
```

## Core Concepts

### 1. LangChain Architecture

**Three Key Components:**

1. **Models (LLMs)**: The language models you interact with
2. **Prompts**: Templates and formatting for inputs
3. **Chains**: Sequences of calls to models/tools

```
Input → Prompt → LLM → Output
```

### 2. PromptTemplate

Reusable prompt structures with variables:

```python
from langchain.prompts import PromptTemplate

# Basic template
template = PromptTemplate(
    input_variables=["product", "audience"],
    template="Write a marketing slogan for {product} targeting {audience}"
)

# Generate prompt
prompt = template.format(product="smartphone", audience="teenagers")
# "Write a marketing slogan for smartphone targeting teenagers"
```

**PromptTemplate Features:**
- Variable substitution
- Input validation
- Partial formatting
- Output parsing

**Advanced PromptTemplate:**
```python
from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["task", "context", "tone"],
    template=\"\"\"You are a {tone} assistant.

Context: {context}

Task: {task}

Response:\"\"\"
)
```

### 3. ChatPromptTemplate

For chat models (system/user/assistant):

```python
from langchain.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {role} assistant."),
    ("user", "Help me with: {request}")
])

messages = chat_template.format_messages(
    role="coding",
    request="debugging Python"
)
```

### 4. LLMChain

Combines a prompt template with an LLM:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize LLM
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

# Create prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms"
)

# Create chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run chain
result = chain.run(topic="quantum computing")
```

**LLMChain Benefits:**
- Automatic prompt formatting
- Consistent LLM configuration
- Easy to test and modify
- Reusable across application

### 5. Model Integration

LangChain supports multiple providers:

```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229")

# Switch providers easily - same interface!
```

### LangChain vs. Raw API

**Raw OpenAI API:**
```python
import openai

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "Explain AI"}
    ]
)
answer = response.choices[0].message.content
```

**LangChain:**
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful"),
    ("user", "Explain {topic}")
])
chain = LLMChain(llm=llm, prompt=prompt)
answer = chain.run(topic="AI")
```

**Advantages:**
- Cleaner separation of concerns
- Reusable templates
- Easier to test
- Provider-agnostic
- Built-in features (memory, agents, etc.)

## Your Task

Build a content generation system using LangChain PromptTemplates and LLMChains.
""",
    "starter_code": """import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain

# Initialize OpenAI LLM
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_content_generator():
    \"\"\"
    Build a content generation system using LangChain.

    Returns:
        dict: Generated content from different chains
    \"\"\"

    # TODO: Create a PromptTemplate for blog post titles
    # Variables: topic, tone (e.g., "professional", "casual")
    title_template = None  # PromptTemplate(...)

    # TODO: Create a PromptTemplate for social media posts
    # Variables: product, platform (e.g., "Twitter", "LinkedIn")
    social_template = None  # PromptTemplate(...)

    # TODO: Create a ChatPromptTemplate for product descriptions
    # System message: Define role
    # User message: Describe {product} for {audience}
    description_template = None  # ChatPromptTemplate.from_messages([...])

    # TODO: Create LLMChains for each template
    title_chain = None  # LLMChain(llm=llm, prompt=title_template)
    social_chain = None  # LLMChain(llm=llm, prompt=social_template)
    description_chain = None  # LLMChain(llm=llm, prompt=description_template)

    try:
        # TODO: Generate content using the chains
        blog_title = ""  # title_chain.run(...)
        social_post = ""  # social_chain.run(...)
        product_desc = ""  # description_chain.run(...)

        return {
            "blog_title": blog_title,
            "social_post": social_post,
            "product_description": product_desc,
            "chains_created": 3
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_content_generator()
    print("=== BLOG TITLE ===\")
    print(results.get("blog_title"))
    print("\\n=== SOCIAL MEDIA POST ===\")
    print(results.get("social_post"))
    print("\\n=== PRODUCT DESCRIPTION ===\")
    print(results.get("product_description"))
""",
    "solution_code": """import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain

# Initialize OpenAI LLM
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_content_generator():
    \"\"\"
    Build a content generation system using LangChain.

    Returns:
        dict: Generated content from different chains
    \"\"\"

    # Create PromptTemplate for blog post titles
    title_template = PromptTemplate(
        input_variables=["topic", "tone"],
        template=\"\"\"Generate a compelling blog post title about {topic}.
The tone should be {tone}.
Return only the title, nothing else.\"\"\"
    )

    # Create PromptTemplate for social media posts
    social_template = PromptTemplate(
        input_variables=["product", "platform"],
        template=\"\"\"Write a {platform} post promoting {product}.
Keep it concise and engaging for {platform}'s audience.
Include appropriate hashtags if relevant.\"\"\"
    )

    # Create ChatPromptTemplate for product descriptions
    description_template = ChatPromptTemplate.from_messages([
        ("system", "You are a creative marketing copywriter specializing in product descriptions."),
        ("user", "Write a compelling 2-3 sentence product description for {product} targeting {audience}. Focus on benefits, not just features.")
    ])

    # Create LLMChains
    title_chain = LLMChain(llm=llm, prompt=title_template)
    social_chain = LLMChain(llm=llm, prompt=social_template)
    description_chain = LLMChain(llm=llm, prompt=description_template)

    try:
        # Generate content using the chains
        blog_title = title_chain.run(
            topic="artificial intelligence in healthcare",
            tone="professional yet accessible"
        )

        social_post = social_chain.run(
            product="eco-friendly water bottle",
            platform="Instagram"
        )

        product_desc = description_chain.run(
            product="noise-canceling headphones",
            audience="remote workers"
        )

        return {
            "blog_title": blog_title.strip(),
            "social_post": social_post.strip(),
            "product_description": product_desc.strip(),
            "chains_created": 3,
            "framework": "LangChain"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_content_generator()
    print("=== CONTENT GENERATION WITH LANGCHAIN ===\")
    print(f"Framework: {results.get('framework')}")
    print(f"Chains created: {results.get('chains_created')}")
    print("\\n=== BLOG TITLE ===\")
    print(results.get("blog_title"))
    print("\\n=== SOCIAL MEDIA POST (Instagram) ===\")
    print(results.get("social_post"))
    print("\\n=== PRODUCT DESCRIPTION ===\")
    print(results.get("product_description"))
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:blog_title", "description": "Should generate blog title"},
        {"input": "", "expected_output": "contains:social_post", "description": "Should generate social media post"},
        {"input": "", "expected_output": "contains:product_description", "description": "Should generate product description"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
