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
    "title": "Token Management and Cost Optimization",
    "slug": "token-management",
    "description": "Learn to count tokens, calculate API costs, and optimize your prompts for efficiency without sacrificing quality.",
    "difficulty": "beginner",
    "order": 7,
    "language": "python",
    "estimated_time": 50,
    "tags": ["prompt-engineering", "tokens", "cost-optimization", "tiktoken", "efficiency"],
    "content": """# Token Management and Cost Optimization

## Learning Objectives
- Understand what tokens are and how they're counted
- Use tiktoken to count tokens accurately
- Calculate API costs for different models
- Learn optimization techniques to reduce token usage
- Balance cost, quality, and performance

## Introduction

LLM APIs charge based on **tokens** - the fundamental units that models process. Understanding token management is crucial for:

- **Cost Control**: Prevent unexpected bills
- **Performance**: Shorter prompts = faster responses
- **Reliability**: Stay within model token limits
- **Efficiency**: Get more done with your API budget

**Real-world scenario:**
A chatbot processing 1,000 requests/day:
- Poorly optimized: 500 tokens/request = 500,000 tokens/day
- Well optimized: 200 tokens/request = 200,000 tokens/day
- **Savings**: 60% reduction in costs!

## Core Concepts

### What Are Tokens?

Tokens are pieces of words that LLMs process. Tokenization varies by model, but generally:

**English text (rough estimates):**
- 1 token ≈ 4 characters
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words

**Examples:**
- "Hello" = 1 token
- "Hello, world!" = 4 tokens ["Hello", ",", " world", "!"]
- "ChatGPT" = 2 tokens ["Chat", "GPT"]
- "unprecedented" = 3 tokens ["un", "pre", "cedented"]

**Special cases:**
- Numbers: "1234" = 1-4 tokens (varies)
- Code: More tokens than natural language
- Non-English: Can be 2-3x more tokens

### Token Limits by Model

| Model | Max Tokens | Input + Output |
|-------|-----------|----------------|
| gpt-3.5-turbo | 4,096 | Combined |
| gpt-3.5-turbo-16k | 16,384 | Combined |
| gpt-4 | 8,192 | Combined |
| gpt-4-32k | 32,768 | Combined |
| gpt-4-turbo | 128,000 | Combined |

**Important**: `max_tokens` parameter limits OUTPUT only, but the model considers INPUT + OUTPUT together.

### Pricing (as of 2024)

**GPT-3.5-turbo:**
- Input: $0.0005 per 1K tokens
- Output: $0.0015 per 1K tokens

**GPT-4:**
- Input: $0.03 per 1K tokens
- Output: $0.06 per 1K tokens

**GPT-4-turbo:**
- Input: $0.01 per 1K tokens
- Output: $0.03 per 1K tokens

### Using tiktoken for Token Counting

```python
import tiktoken

# Get encoding for specific model
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

# Count tokens in text
text = "Hello, how are you?"
tokens = encoding.encode(text)
token_count = len(tokens)  # Returns: 6

# Count tokens in messages (for chat models)
def count_message_tokens(messages, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    tokens_per_message = 3  # Format overhead
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3  # Reply priming
    return num_tokens
```

### Cost Calculation

```python
def calculate_cost(input_tokens, output_tokens, model="gpt-3.5-turbo"):
    pricing = {
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03}
    }

    rates = pricing.get(model, pricing["gpt-3.5-turbo"])
    input_cost = (input_tokens / 1000) * rates["input"]
    output_cost = (output_tokens / 1000) * rates["output"]

    return input_cost + output_cost
```

### Optimization Techniques

**1. Be Concise**
```python
# Verbose (28 tokens)
prompt = "I would like you to please analyze the following text and provide me with a summary"

# Concise (11 tokens)
prompt = "Summarize this text"
```

**2. Use Shorter Examples**
```python
# Long examples (100+ tokens)
examples = "Review: 'This product exceeded all of my expectations...'"

# Short examples (30 tokens)
examples = "Review: 'Amazing!' → Positive"
```

**3. Limit max_tokens**
```python
# Unlimited (expensive)
response = openai.chat.completions.create(max_tokens=4096)

# Limited (cost-effective)
response = openai.chat.completions.create(max_tokens=150)
```

**4. Choose the Right Model**
- Use GPT-3.5-turbo for simple tasks
- Reserve GPT-4 for complex reasoning
- Test if GPT-3.5 meets your needs first

**5. Avoid Redundancy**
```python
# Redundant system + user message
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "You are helpful. Answer this: ..."}
]

# Streamlined
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Answer this: ..."}
]
```

## Your Task

Build a token analyzer that counts tokens, estimates costs, and suggests optimizations.
""",
    "starter_code": """import os
import tiktoken
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def token_cost_analyzer():
    \"\"\"
    Analyze token usage and costs for different prompting strategies.

    Returns:
        dict: Token counts, costs, and optimization recommendations
    \"\"\"

    # Sample task: Summarize a product review
    review = \"\"\"I purchased this wireless mouse three weeks ago and have been using it daily.
    The ergonomic design is comfortable for long work sessions. The battery life is impressive -
    I haven't needed to replace batteries yet. However, the scroll wheel feels a bit loose and
    sometimes skips. The price point of $45 seems reasonable for the quality. Connection is
    reliable with no dropouts. Overall, I'd rate it 4 out of 5 stars and would recommend it
    to others looking for a budget-friendly wireless mouse.\"\"\"

    # TODO: Create a verbose prompt (inefficient)
    verbose_prompt = \"\"\"
    # Create a long-winded prompt with unnecessary details
    \"\"\"

    # TODO: Create an optimized prompt (efficient)
    optimized_prompt = \"\"\"
    # Create a concise, effective prompt
    \"\"\"

    # TODO: Count tokens using tiktoken
    # Get encoding for gpt-3.5-turbo
    encoding = None  # tiktoken.encoding_for_model("gpt-3.5-turbo")

    # TODO: Count tokens for both prompts
    verbose_tokens = 0
    optimized_tokens = 0

    # TODO: Calculate estimated costs
    # Assume 50 output tokens for each
    # Use GPT-3.5-turbo pricing: input $0.0005/1K, output $0.0015/1K
    verbose_cost = 0.0
    optimized_cost = 0.0

    # TODO: Calculate savings
    token_savings = 0  # verbose_tokens - optimized_tokens
    cost_savings_percent = 0.0

    try:
        # Optional: Get actual response to measure real token usage
        # response = client.chat.completions.create(...)

        return {
            "verbose_tokens": verbose_tokens,
            "optimized_tokens": optimized_tokens,
            "token_savings": token_savings,
            "verbose_cost": verbose_cost,
            "optimized_cost": optimized_cost,
            "cost_savings_percent": cost_savings_percent,
            "recommendation": "Use optimized prompts to save tokens and costs"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = token_cost_analyzer()
    print("=== TOKEN ANALYSIS ===\")
    print(f"Verbose prompt: {results.get('verbose_tokens')} tokens")
    print(f"Optimized prompt: {results.get('optimized_tokens')} tokens")
    print(f"Token savings: {results.get('token_savings')} tokens")
    print(f"\\n=== COST ANALYSIS ===\")
    print(f"Verbose cost: ${results.get('verbose_cost'):.6f}")
    print(f"Optimized cost: ${results.get('optimized_cost'):.6f}")
    print(f"Savings: {results.get('cost_savings_percent'):.1f}%")
    print(f"\\nRecommendation: {results.get('recommendation')}")
""",
    "solution_code": """import os
import tiktoken
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def token_cost_analyzer():
    \"\"\"
    Analyze token usage and costs for different prompting strategies.

    Returns:
        dict: Token counts, costs, and optimization recommendations
    \"\"\"

    review = \"\"\"I purchased this wireless mouse three weeks ago and have been using it daily.
    The ergonomic design is comfortable for long work sessions. The battery life is impressive -
    I haven't needed to replace batteries yet. However, the scroll wheel feels a bit loose and
    sometimes skips. The price point of $45 seems reasonable for the quality. Connection is
    reliable with no dropouts. Overall, I'd rate it 4 out of 5 stars and would recommend it
    to others looking for a budget-friendly wireless mouse.\"\"\"

    # Verbose prompt (inefficient)
    verbose_prompt = f\"\"\"I would like you to carefully read through the following product review
    and then provide me with a comprehensive summary of the main points. Please make sure to
    include both the positive aspects and negative aspects that the reviewer mentioned.
    I would also appreciate it if you could mention the overall rating they gave.
    Here is the review for your consideration:

    {review}

    Please provide your detailed summary below:\"\"\"

    # Optimized prompt (efficient)
    optimized_prompt = f\"\"\"Summarize this review, including pros, cons, and rating:

    {review}\"\"\"

    # Count tokens using tiktoken
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    verbose_tokens = len(encoding.encode(verbose_prompt))
    optimized_tokens = len(encoding.encode(optimized_prompt))

    # Calculate estimated costs
    # Assume 50 output tokens for each response
    output_tokens = 50

    # GPT-3.5-turbo pricing (per 1K tokens)
    input_rate = 0.0005
    output_rate = 0.0015

    verbose_cost = ((verbose_tokens / 1000) * input_rate) + ((output_tokens / 1000) * output_rate)
    optimized_cost = ((optimized_tokens / 1000) * input_rate) + ((output_tokens / 1000) * output_rate)

    # Calculate savings
    token_savings = verbose_tokens - optimized_tokens
    cost_savings = verbose_cost - optimized_cost
    cost_savings_percent = (cost_savings / verbose_cost) * 100 if verbose_cost > 0 else 0

    try:
        # Get actual response to measure real usage
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": optimized_prompt}],
            max_tokens=50,
            temperature=0.5
        )

        actual_output_tokens = response.usage.completion_tokens
        actual_input_tokens = response.usage.prompt_tokens

        return {
            "verbose_tokens": verbose_tokens,
            "optimized_tokens": optimized_tokens,
            "token_savings": token_savings,
            "verbose_cost": verbose_cost,
            "optimized_cost": optimized_cost,
            "cost_savings_percent": cost_savings_percent,
            "actual_input_tokens": actual_input_tokens,
            "actual_output_tokens": actual_output_tokens,
            "recommendation": f"Optimized prompt saves {token_savings} tokens ({cost_savings_percent:.1f}% cost reduction)"
        }
    except Exception as e:
        return {
            "verbose_tokens": verbose_tokens,
            "optimized_tokens": optimized_tokens,
            "token_savings": token_savings,
            "verbose_cost": verbose_cost,
            "optimized_cost": optimized_cost,
            "cost_savings_percent": cost_savings_percent,
            "error": str(e)
        }

if __name__ == "__main__":
    results = token_cost_analyzer()
    print("=== TOKEN ANALYSIS ===\")
    print(f"Verbose prompt: {results.get('verbose_tokens')} tokens")
    print(f"Optimized prompt: {results.get('optimized_tokens')} tokens")
    print(f"Token savings: {results.get('token_savings')} tokens")
    print(f"\\n=== COST ANALYSIS ===\")
    print(f"Verbose cost: ${results.get('verbose_cost'):.6f}")
    print(f"Optimized cost: ${results.get('optimized_cost'):.6f}")
    print(f"Savings: {results.get('cost_savings_percent'):.1f}%")
    if 'actual_input_tokens' in results:
        print(f"\\n=== ACTUAL USAGE ===\")
        print(f"Input tokens: {results.get('actual_input_tokens')}")
        print(f"Output tokens: {results.get('actual_output_tokens')}")
    print(f"\\nRecommendation: {results.get('recommendation')}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:verbose_tokens", "description": "Should count verbose prompt tokens"},
        {"input": "", "expected_output": "contains:optimized_tokens", "description": "Should count optimized prompt tokens"},
        {"input": "", "expected_output": "contains:token_savings", "description": "Should calculate token savings"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
