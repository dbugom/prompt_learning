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
    "title": "Working with Multiple LLM Providers",
    "slug": "multiple-providers",
    "description": "Learn to work with different LLM providers (OpenAI, Anthropic, Google) and implement provider-agnostic applications with smart routing.",
    "difficulty": "intermediate",
    "order": 12,
    "language": "python",
    "estimated_time": 55,
    "tags": ["prompt-engineering", "openai", "anthropic", "google", "multi-provider", "intermediate"],
    "content": """# Working with Multiple LLM Providers

## Learning Objectives
- Understand major LLM providers and their offerings
- Learn to use OpenAI, Anthropic, and Google APIs
- Build provider-agnostic applications with LangChain
- Implement smart provider routing
- Optimize for cost, performance, and quality

## Introduction

The LLM landscape has multiple providers, each with unique strengths:

- **OpenAI**: GPT-4, GPT-3.5 - General purpose, widely adopted
- **Anthropic**: Claude - Strong reasoning, safety-focused
- **Google**: Gemini - Multimodal, large context windows

**Why use multiple providers?**

1. **Redundancy**: If one provider is down, use another
2. **Cost optimization**: Route to cheapest suitable model
3. **Performance**: Different models excel at different tasks
4. **Avoid vendor lock-in**: Easy migration if needed
5. **Feature access**: Use best features from each

## Core Concepts

### Provider Comparison

**OpenAI (GPT Models)**
- **Strengths**: Widely used, excellent general performance, function calling
- **Models**: GPT-4, GPT-4-turbo, GPT-3.5-turbo
- **Context**: 4K - 128K tokens
- **Pricing**: $0.0005 - $0.06 per 1K tokens
- **Best for**: General tasks, coding, analysis

**Anthropic (Claude)**
- **Strengths**: Long context (200K), strong reasoning, safety-focused
- **Models**: Claude 3 Opus, Sonnet, Haiku
- **Context**: Up to 200K tokens
- **Pricing**: $0.00025 - $0.015 per 1K tokens (Haiku very cheap)
- **Best for**: Long documents, detailed analysis, ethical AI

**Google (Gemini)**
- **Strengths**: Multimodal (text, images, video), large context
- **Models**: Gemini Pro, Gemini Ultra
- **Context**: Up to 1M tokens
- **Pricing**: Competitive, free tier available
- **Best for**: Multimodal tasks, large context needs

### Using OpenAI

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "Explain AI"}
    ],
    temperature=0.7,
    max_tokens=150
)

answer = response.choices[0].message.content
```

### Using Anthropic

```python
from anthropic import Anthropic

client = Anthropic(api_key="sk-ant-...")

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=150,
    messages=[
        {"role": "user", "content": "Explain AI"}
    ],
    system="You are helpful"  # Note: system is separate parameter
)

answer = response.content[0].text
```

### Using Google Gemini

```python
import google.generativeai as genai

genai.configure(api_key="...")

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Explain AI")

answer = response.text
```

### Provider-Agnostic with LangChain

LangChain provides a unified interface:

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# All use the same interface!
openai_llm = ChatOpenAI(model="gpt-3.5-turbo")
anthropic_llm = ChatAnthropic(model="claude-3-sonnet-20240229")
google_llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Same invoke method for all
response = openai_llm.invoke("Explain AI")
response = anthropic_llm.invoke("Explain AI")
response = google_llm.invoke("Explain AI")
```

### Smart Provider Routing

**Route by Task Type:**
```python
def get_llm_for_task(task_type):
    if task_type == "coding":
        return ChatOpenAI(model="gpt-4")
    elif task_type == "long_document":
        return ChatAnthropic(model="claude-3-sonnet-20240229")
    elif task_type == "multimodal":
        return ChatGoogleGenerativeAI(model="gemini-pro")
    else:
        return ChatOpenAI(model="gpt-3.5-turbo")  # Default
```

**Route by Cost:**
```python
def get_cheapest_llm():
    # Use cheapest suitable model
    return ChatAnthropic(model="claude-3-haiku-20240307")  # Very cheap
```

**Route by Load Balancing:**
```python
import random

def load_balanced_llm():
    providers = [
        ChatOpenAI(model="gpt-3.5-turbo"),
        ChatAnthropic(model="claude-3-haiku-20240307")
    ]
    return random.choice(providers)
```

### Cost Comparison Example

**Same task, different costs:**

```python
# GPT-4: $0.03/1K input, $0.06/1K output
# 1000 tokens in, 500 tokens out = $0.06

# GPT-3.5: $0.0005/1K input, $0.0015/1K output
# 1000 tokens in, 500 tokens out = $0.00125

# Claude Haiku: $0.00025/1K input, $0.00125/1K output
# 1000 tokens in, 500 tokens out = $0.000875

# Savings: Haiku is 68x cheaper than GPT-4!
```

### Unified Prompt Interface

```python
class UnifiedLLM:
    def __init__(self, provider="openai"):
        if provider == "openai":
            self.llm = ChatOpenAI(model="gpt-3.5-turbo")
        elif provider == "anthropic":
            self.llm = ChatAnthropic(model="claude-3-sonnet-20240229")
        elif provider == "google":
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro")

    def generate(self, prompt):
        return self.llm.invoke(prompt)

# Easy switching
llm = UnifiedLLM(provider="anthropic")
response = llm.generate("Explain AI")
```

### Fallback Chain

```python
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

def multi_provider_chain(prompt):
    providers = [
        ("OpenAI GPT-4", ChatOpenAI(model="gpt-4")),
        ("Anthropic Claude", ChatAnthropic(model="claude-3-sonnet-20240229")),
        ("OpenAI GPT-3.5", ChatOpenAI(model="gpt-3.5-turbo"))
    ]

    for name, llm in providers:
        try:
            chain = LLMChain(llm=llm, prompt=prompt)
            result = chain.run(prompt)
            print(f"Success with {name}")
            return result
        except Exception as e:
            print(f"{name} failed: {e}")
            continue

    raise Exception("All providers failed")
```

### When to Use Which Provider

**Use OpenAI when:**
- Need function calling
- Building production apps (reliability)
- Need established ecosystem
- Doing code generation

**Use Anthropic when:**
- Processing long documents
- Need strong reasoning
- Want ethical/safe outputs
- Cost-conscious (Haiku)

**Use Google when:**
- Working with multimodal content
- Need massive context (1M tokens)
- Want free tier for testing
- Experimenting with latest features

### Best Practices

**1. Environment Variable Configuration**
```python
import os

PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
```

**2. Cost Tracking**
```python
def track_cost(provider, input_tokens, output_tokens):
    costs = {
        "openai-gpt4": {"input": 0.03, "output": 0.06},
        "openai-gpt35": {"input": 0.0005, "output": 0.0015},
        "anthropic-haiku": {"input": 0.00025, "output": 0.00125}
    }
    rate = costs.get(provider)
    total = (input_tokens/1000 * rate["input"]) + (output_tokens/1000 * rate["output"])
    return total
```

**3. Provider Abstraction**
```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        # OpenAI implementation
        pass

class AnthropicProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        # Anthropic implementation
        pass
```

## Your Task

Build a multi-provider LLM system with smart routing and cost tracking.
""",
    "starter_code": """import os
from langchain_openai import ChatOpenAI
# Note: For this exercise, we'll simulate Anthropic/Google if keys aren't available

def build_multi_provider_system():
    \"\"\"
    Build a system that works with multiple LLM providers.

    Returns:
        dict: Results from different providers with cost comparison
    \"\"\"

    test_prompt = "Explain quantum computing in 2 sentences."

    # TODO: Initialize OpenAI LLM
    openai_llm = None  # ChatOpenAI(...)

    # TODO: Create a provider router function
    def route_to_provider(task_type):
        \"\"\"Route request to best provider based on task type.\"\"\"
        # Return appropriate LLM based on task_type
        # Options: "simple", "complex", "long_document", "cost_optimized"
        pass

    # TODO: Create a fallback chain
    def call_with_fallback(prompt):
        \"\"\"Try multiple providers in order until one succeeds.\"\"\"
        providers = []  # List of (name, llm) tuples

        # Try each provider
        pass

    # TODO: Calculate cost comparison
    def compare_costs(input_tokens=100, output_tokens=50):
        \"\"\"Compare costs across providers.\"\"\"
        costs = {
            # Provider: cost calculation
        }
        return costs

    try:
        # TODO: Test different routing strategies
        simple_result = ""  # route_to_provider("simple")
        complex_result = ""  # route_to_provider("complex")

        # TODO: Get cost comparison
        cost_comparison = {}  # compare_costs()

        return {
            "simple_task_provider": "Not implemented",
            "complex_task_provider": "Not implemented",
            "cost_comparison": cost_comparison,
            "providers_configured": 1
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_multi_provider_system()
    print("=== MULTI-PROVIDER SYSTEM ===\")
    print(f"Providers configured: {results.get('providers_configured')}")
    print(f"\\nSimple task routed to: {results.get('simple_task_provider')}")
    print(f"Complex task routed to: {results.get('complex_task_provider')}")
    print(f"\\nCost comparison: {results.get('cost_comparison')}")
""",
    "solution_code": """import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

def build_multi_provider_system():
    \"\"\"
    Build a system that works with multiple LLM providers.

    Returns:
        dict: Results from different providers with cost comparison
    \"\"\"

    test_prompt = "Explain quantum computing in 2 sentences."

    # Initialize OpenAI LLM (primary provider for this exercise)
    openai_gpt35 = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
    )

    openai_gpt4 = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
    )

    # Provider router function
    def route_to_provider(task_type):
        \"\"\"Route request to best provider based on task type.\"\"\"
        routing_map = {
            "simple": ("GPT-3.5-turbo", openai_gpt35),
            "complex": ("GPT-4", openai_gpt4),
            "long_document": ("GPT-4", openai_gpt4),  # Would use Claude in production
            "cost_optimized": ("GPT-3.5-turbo", openai_gpt35)
        }
        return routing_map.get(task_type, ("GPT-3.5-turbo", openai_gpt35))

    # Fallback chain
    def call_with_fallback(prompt):
        \"\"\"Try multiple providers in order until one succeeds.\"\"\"
        providers = [
            ("OpenAI GPT-4", openai_gpt4),
            ("OpenAI GPT-3.5", openai_gpt35)
        ]

        for name, llm in providers:
            try:
                response = llm.invoke(prompt)
                return {
                    "provider": name,
                    "response": response.content,
                    "success": True
                }
            except Exception as e:
                print(f"{name} failed: {e}")
                continue

        return {"success": False, "error": "All providers failed"}

    # Calculate cost comparison
    def compare_costs(input_tokens=100, output_tokens=50):
        \"\"\"Compare costs across providers.\"\"\"
        pricing = {
            "GPT-4": {
                "input_rate": 0.03,
                "output_rate": 0.06
            },
            "GPT-3.5-turbo": {
                "input_rate": 0.0005,
                "output_rate": 0.0015
            },
            "Claude-Haiku": {
                "input_rate": 0.00025,
                "output_rate": 0.00125
            },
            "Claude-Sonnet": {
                "input_rate": 0.003,
                "output_rate": 0.015
            }
        }

        costs = {}
        for provider, rates in pricing.items():
            input_cost = (input_tokens / 1000) * rates["input_rate"]
            output_cost = (output_tokens / 1000) * rates["output_rate"]
            total = input_cost + output_cost
            costs[provider] = f"${total:.6f}"

        return costs

    try:
        # Test different routing strategies
        simple_provider, simple_llm = route_to_provider("simple")
        complex_provider, complex_llm = route_to_provider("complex")

        # Test simple task
        simple_response = simple_llm.invoke(test_prompt)

        # Test fallback
        fallback_result = call_with_fallback(test_prompt)

        # Get cost comparison
        cost_comparison = compare_costs(input_tokens=100, output_tokens=50)

        return {
            "simple_task_provider": simple_provider,
            "complex_task_provider": complex_provider,
            "simple_response": simple_response.content[:100] + "...",
            "fallback_provider": fallback_result.get("provider"),
            "cost_comparison": cost_comparison,
            "providers_configured": 2,
            "routing_strategy": "Task-based routing with fallback",
            "cheapest_provider": "Claude-Haiku",
            "most_expensive_provider": "GPT-4"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_multi_provider_system()
    print("=== MULTI-PROVIDER SYSTEM ===\")
    print(f"Providers configured: {results.get('providers_configured')}")
    print(f"Routing strategy: {results.get('routing_strategy')}")

    print(f"\\n=== TASK ROUTING ===\")
    print(f"Simple task → {results.get('simple_task_provider')}")
    print(f"Complex task → {results.get('complex_task_provider')}")

    if 'simple_response' in results:
        print(f"\\nSample response: {results.get('simple_response')}")

    print(f"\\n=== COST COMPARISON (100 input + 50 output tokens) ===\")
    for provider, cost in results.get('cost_comparison', {}).items():
        print(f"{provider}: {cost}")

    print(f"\\nCheapest: {results.get('cheapest_provider')}")
    print(f"Most expensive: {results.get('most_expensive_provider')}")

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:providers_configured", "description": "Should configure multiple providers"},
        {"input": "", "expected_output": "contains:cost_comparison", "description": "Should compare costs"},
        {"input": "", "expected_output": "contains:simple_task_provider", "description": "Should route simple tasks"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
