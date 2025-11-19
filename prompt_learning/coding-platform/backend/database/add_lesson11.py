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
    "title": "Error Handling and Retries",
    "slug": "error-handling-retries",
    "description": "Build reliable LLM applications with proper error handling, retry logic, and fallback strategies for production environments.",
    "difficulty": "intermediate",
    "order": 11,
    "language": "python",
    "estimated_time": 50,
    "tags": ["prompt-engineering", "error-handling", "retries", "tenacity", "reliability", "intermediate"],
    "content": """# Error Handling and Retries

## Learning Objectives
- Understand common LLM API errors
- Implement proper exception handling
- Use tenacity library for retry logic
- Design fallback strategies
- Build production-ready error handling

## Introduction

LLM APIs are network services that can fail for many reasons:
- Network timeouts
- Rate limits exceeded
- API server errors
- Invalid API keys
- Model overloaded

**Without error handling:**
```python
response = client.chat.completions.create(...)  # Crashes on error!
```

**With error handling:**
```python
try:
    response = client.chat.completions.create(...)
except RateLimitError:
    # Wait and retry
except APIError:
    # Use fallback
```

Building **resilient** applications means gracefully handling failures and recovering automatically when possible.

## Core Concepts

### Common API Errors

**1. RateLimitError**
- **Cause**: Too many requests in time window
- **Solution**: Exponential backoff, retry with delay

**2. APIConnectionError**
- **Cause**: Network issues, timeouts
- **Solution**: Retry with backoff

**3. AuthenticationError**
- **Cause**: Invalid API key
- **Solution**: Check credentials, don't retry

**4. APIError**
- **Cause**: Server-side error (500, 503)
- **Solution**: Retry, switch providers

**5. InvalidRequestError**
- **Cause**: Bad request (invalid parameters)
- **Solution**: Fix input, don't retry

**6. Timeout**
- **Cause**: Request took too long
- **Solution**: Retry with longer timeout

### Basic Error Handling

```python
from openai import OpenAI, RateLimitError, APIError
import time

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("Rate limit hit, waiting...")
    time.sleep(60)
    # Retry logic here
except APIError as e:
    print(f"API error: {e}")
    # Use fallback
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log and handle
```

### Retry Strategies

**1. Simple Retry (Fixed Delay)**
```python
max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.chat.completions.create(...)
        break  # Success
    except APIError:
        if attempt < max_retries - 1:
            time.sleep(5)  # Wait 5 seconds
        else:
            raise  # Give up
```

**2. Exponential Backoff**
```python
import time

def exponential_backoff(attempt):
    return min(2 ** attempt, 60)  # Max 60 seconds

for attempt in range(5):
    try:
        response = client.chat.completions.create(...)
        break
    except APIError:
        wait = exponential_backoff(attempt)
        time.sleep(wait)
```

**3. Exponential Backoff with Jitter**
```python
import random

def backoff_with_jitter(attempt):
    base_delay = 2 ** attempt
    jitter = random.uniform(0, 1)
    return min(base_delay + jitter, 60)
```

### Using Tenacity Library

**Tenacity** is a powerful retry library for Python:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import APIError, RateLimitError

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception_type((APIError, RateLimitError))
)
def call_llm_with_retry(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

**Tenacity Features:**
- `stop_after_attempt(n)`: Max retry count
- `wait_exponential()`: Exponential backoff
- `retry_if_exception_type()`: Only retry certain errors
- `before_sleep`: Log before each retry
- `after`: Callback after all attempts

**Advanced Tenacity:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True
)
def robust_llm_call(prompt):
    return client.chat.completions.create(...)
```

### Fallback Strategies

**Strategy 1: Model Fallback**
```python
def call_with_fallback(prompt):
    try:
        # Try GPT-4 first
        return call_gpt4(prompt)
    except Exception:
        # Fallback to GPT-3.5
        return call_gpt35(prompt)
```

**Strategy 2: Provider Fallback**
```python
def multi_provider_call(prompt):
    providers = [openai_call, anthropic_call, google_call]

    for provider in providers:
        try:
            return provider(prompt)
        except Exception as e:
            logger.warning(f"{provider.__name__} failed: {e}")
            continue

    raise Exception("All providers failed")
```

**Strategy 3: Cached Fallback**
```python
def call_with_cache(prompt):
    try:
        response = client.chat.completions.create(...)
        cache[prompt] = response
        return response
    except Exception:
        # Use cached response if available
        if prompt in cache:
            return cache[prompt]
        raise
```

**Strategy 4: Degraded Service**
```python
def call_with_degradation(prompt):
    try:
        # Try full response
        return get_detailed_response(prompt)
    except Exception:
        # Fallback to simple response
        return get_simple_response(prompt)
```

### Production Best Practices

**1. Timeout Configuration**
```python
from openai import OpenAI

client = OpenAI(timeout=30.0)  # 30 second timeout
```

**2. Circuit Breaker Pattern**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker open")

        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            self.state = "closed"
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

**3. Logging and Monitoring**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    response = client.chat.completions.create(...)
    logger.info("API call successful")
except Exception as e:
    logger.error(f"API call failed: {e}", exc_info=True)
    # Send to monitoring service (e.g., Sentry)
```

**4. Rate Limit Management**
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    def wait_if_needed(self):
        now = time.time()
        # Remove old requests
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()

        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            time.sleep(sleep_time)

        self.requests.append(now)
```

## Your Task

Build a robust LLM caller with comprehensive error handling and retry logic.
""",
    "starter_code": """import os
import time
from openai import OpenAI, APIError, RateLimitError
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_robust_llm_system():
    \"\"\"
    Build a robust LLM calling system with error handling and retries.

    Returns:
        dict: Results showing error handling capabilities
    \"\"\"

    test_prompt = "Explain the concept of error handling in one sentence."

    # TODO: Implement simple retry logic (manual)
    def simple_retry_call(prompt, max_retries=3):
        \"\"\"Call LLM with simple retry logic.\"\"\"
        # Implement retry with fixed delay
        pass

    # TODO: Implement exponential backoff retry
    def exponential_backoff_call(prompt, max_retries=5):
        \"\"\"Call LLM with exponential backoff.\"\"\"
        # Implement exponential backoff: 2^attempt seconds
        pass

    # TODO: Use tenacity decorator for automatic retries
    @retry(
        stop=None,  # stop_after_attempt(...)
        wait=None,  # wait_exponential(...)
    )
    def tenacity_call(prompt):
        \"\"\"Call LLM with tenacity retry decorator.\"\"\"
        # Implement LLM call
        pass

    # TODO: Implement fallback strategy
    def call_with_fallback(prompt):
        \"\"\"Call LLM with fallback to simpler model.\"\"\"
        try:
            # Try main approach
            pass
        except Exception:
            # Fallback approach
            pass

    try:
        # Test different strategies
        result = {
            "simple_retry": "Not implemented",
            "exponential_backoff": "Not implemented",
            "tenacity_retry": "Not implemented",
            "with_fallback": "Not implemented",
            "strategies_implemented": 0
        }

        return result

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_robust_llm_system()
    print("=== ROBUST LLM SYSTEM ===\")
    for strategy, result in results.items():
        print(f"{strategy}: {result}")
""",
    "solution_code": """import os
import time
from openai import OpenAI, APIError, RateLimitError, AuthenticationError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_robust_llm_system():
    \"\"\"
    Build a robust LLM calling system with error handling and retries.

    Returns:
        dict: Results showing error handling capabilities
    \"\"\"

    test_prompt = "Explain the concept of error handling in one sentence."

    # Simple retry logic (manual)
    def simple_retry_call(prompt, max_retries=3):
        \"\"\"Call LLM with simple retry logic.\"\"\"
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    timeout=10
                )
                return response.choices[0].message.content
            except (APIError, RateLimitError) as e:
                if attempt < max_retries - 1:
                    time.sleep(2)  # Fixed 2-second delay
                    continue
                else:
                    return f"Failed after {max_retries} attempts: {str(e)}"
            except AuthenticationError:
                return "Authentication error - check API key"
            except Exception as e:
                return f"Unexpected error: {str(e)}"

    # Exponential backoff retry
    def exponential_backoff_call(prompt, max_retries=5):
        \"\"\"Call LLM with exponential backoff.\"\"\"
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    timeout=10
                )
                return response.choices[0].message.content
            except (APIError, RateLimitError) as e:
                if attempt < max_retries - 1:
                    wait_time = min(2 ** attempt, 60)  # Cap at 60 seconds
                    time.sleep(wait_time)
                    continue
                else:
                    return f"Failed with exponential backoff: {str(e)}"
            except Exception as e:
                return f"Error: {str(e)}"

    # Tenacity decorator for automatic retries
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((APIError, RateLimitError)),
        reraise=True
    )
    def tenacity_call(prompt):
        \"\"\"Call LLM with tenacity retry decorator.\"\"\"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            timeout=10
        )
        return response.choices[0].message.content

    # Fallback strategy
    def call_with_fallback(prompt):
        \"\"\"Call LLM with fallback to simpler approach.\"\"\"
        try:
            # Try with temperature 0.7 first
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100,
                timeout=10
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback: simpler request with lower temperature
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=50,
                    timeout=15
                )
                return f"[Fallback] {response.choices[0].message.content}"
            except Exception as fallback_error:
                return f"Both attempts failed. Last error: {str(fallback_error)}"

    try:
        # Test different strategies
        simple_result = simple_retry_call(test_prompt)
        exponential_result = exponential_backoff_call(test_prompt)

        try:
            tenacity_result = tenacity_call(test_prompt)
        except Exception as e:
            tenacity_result = f"Tenacity failed: {str(e)}"

        fallback_result = call_with_fallback(test_prompt)

        result = {
            "simple_retry": simple_result[:100] + "..." if len(simple_result) > 100 else simple_result,
            "exponential_backoff": exponential_result[:100] + "..." if len(exponential_result) > 100 else exponential_result,
            "tenacity_retry": tenacity_result[:100] + "..." if len(tenacity_result) > 100 else tenacity_result,
            "with_fallback": fallback_result[:100] + "..." if len(fallback_result) > 100 else fallback_result,
            "strategies_implemented": 4,
            "best_practice": "Use tenacity with exponential backoff for production"
        }

        return result

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_robust_llm_system()
    print("=== ROBUST LLM SYSTEM ===\")
    print(f"Strategies implemented: {results.get('strategies_implemented', 0)}/4\\n")

    for strategy, result in results.items():
        if strategy not in ['strategies_implemented', 'best_practice', 'error']:
            print(f"\\n{strategy.replace('_', ' ').title()}:")
            print(f"  {result}")

    if 'best_practice' in results:
        print(f"\\nBest Practice: {results['best_practice']}")

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:simple_retry", "description": "Should implement simple retry"},
        {"input": "", "expected_output": "contains:tenacity_retry", "description": "Should implement tenacity retry"},
        {"input": "", "expected_output": "contains:strategies_implemented", "description": "Should count strategies"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
