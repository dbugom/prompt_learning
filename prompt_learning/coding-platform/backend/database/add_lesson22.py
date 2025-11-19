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
    "title": "Production Best Practices and Deployment",
    "slug": "production-best-practices",
    "description": "Master production-ready LLM applications with API key management, rate limiting, monitoring, cost controls, and deployment strategies.",
    "difficulty": "advanced",
    "order": 22,
    "language": "python",
    "estimated_time": 70,
    "tags": ["prompt-engineering", "production", "deployment", "monitoring", "security", "cost-optimization"],
    "content": """# Production Best Practices and Deployment

## Learning Objectives
- Implement secure API key management
- Add rate limiting and request throttling
- Monitor LLM usage and costs
- Handle errors and implement retry logic
- Deploy LLM applications to production
- Optimize for cost and performance

## Introduction

Building a production-ready LLM application requires more than just good prompts. You need security, reliability, monitoring, and cost controls.

This lesson covers the essential practices for deploying LLM applications that are:
- **Secure**: Protected API keys and user data
- **Reliable**: Graceful error handling and retries
- **Observable**: Logging and monitoring
- **Cost-effective**: Budget controls and optimization
- **Scalable**: Handle growing user base

## Core Concepts

### 1. API Key Management

**Never hardcode API keys!**

Best practices:
- Use environment variables
- Store in secure vaults (AWS Secrets Manager, HashiCorp Vault)
- Rotate keys regularly
- Use separate keys for dev/staging/production
- Implement key usage monitoring

### 2. Rate Limiting

Protect your application from:
- Excessive costs from runaway usage
- API quota exhaustion
- Denial-of-service attacks

Implementation strategies:
- **Per-user limits**: Max requests per user per hour
- **Global limits**: Total requests per time window
- **Token budgets**: Limit total tokens per user/day
- **Queue systems**: Handle bursts gracefully

### 3. Error Handling and Retries

LLM APIs can fail due to:
- Network issues
- Rate limit errors (429)
- Server errors (500, 503)
- Timeout errors

Implement:
- Exponential backoff for retries
- Circuit breakers for persistent failures
- Fallback responses
- User-friendly error messages

### 4. Monitoring and Logging

Track these metrics:
- **Request volume**: Requests per minute/hour/day
- **Latency**: Response time (p50, p95, p99)
- **Error rates**: Failed requests percentage
- **Token usage**: Input/output tokens per request
- **Costs**: Daily/monthly spending
- **User patterns**: Most common queries

Tools:
- Application Performance Monitoring (APM): Datadog, New Relic
- Logging: ELK Stack, CloudWatch
- Custom dashboards: Grafana, Kibana

### 5. Cost Optimization

Strategies to reduce costs:
- **Caching**: Store and reuse common responses
- **Prompt compression**: Minimize token usage
- **Model selection**: Use cheaper models when appropriate
- **Smart routing**: Route simple queries to cheaper models
- **Streaming**: Improve perceived performance
- **Batch processing**: Combine similar requests

### 6. Security Best Practices

Protect your application:
- **Input validation**: Sanitize user inputs
- **Output filtering**: Check for sensitive data leaks
- **Prompt injection prevention**: Validate and escape inputs
- **User authentication**: Verify user identity
- **Content moderation**: Filter harmful content
- **Audit logging**: Track all LLM interactions

## Your Task

Build a production-ready LLM wrapper class that implements rate limiting, error handling, monitoring, and cost tracking.

### Implementation Checklist

- ✓ Environment-based configuration
- ✓ Rate limiting (per-user)
- ✓ Retry logic with exponential backoff
- ✓ Request/response logging
- ✓ Cost tracking
- ✓ Error handling
- ✓ Usage statistics
""",
    "starter_code": """import os
import time
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionLLMClient:
    \"\"\"Production-ready LLM client with monitoring and controls\"\"\"

    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))

        # TODO: Initialize tracking dictionaries
        self.request_counts = defaultdict(int)  # user_id -> count
        self.token_usage = defaultdict(int)     # user_id -> tokens
        self.costs = defaultdict(float)         # user_id -> cost
        self.last_request_time = {}             # user_id -> timestamp

        # Configuration
        self.max_requests_per_hour = 10
        self.max_tokens_per_day = 10000
        self.cost_per_1k_tokens = 0.002  # GPT-3.5-turbo pricing

    def check_rate_limit(self, user_id: str) -> bool:
        \"\"\"Check if user has exceeded rate limits\"\"\"
        # TODO: Implement rate limiting
        # Check requests per hour
        # Reset counter if hour has passed
        return True

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def make_request(self, user_id: str, prompt: str, **kwargs) -> Dict:
        \"\"\"Make LLM request with retry logic\"\"\"
        # TODO: Check rate limits
        # TODO: Make API call
        # TODO: Track usage and costs
        # TODO: Log request/response
        pass

    def get_usage_stats(self, user_id: str) -> Dict:
        \"\"\"Get usage statistics for a user\"\"\"
        # TODO: Return stats dictionary
        return {
            "requests": 0,
            "tokens_used": 0,
            "estimated_cost": 0.0
        }

    def log_request(self, user_id: str, prompt: str, response: str, tokens: int):
        \"\"\"Log request for monitoring\"\"\"
        # TODO: Log to file or monitoring service
        logger.info(f"User: {user_id} | Tokens: {tokens} | Prompt: {prompt[:50]}...")

def test_production_client():
    \"\"\"Test the production LLM client\"\"\"

    client = ProductionLLMClient()

    # Simulate multiple requests
    user_id = "user_123"

    try:
        # TODO: Make test requests
        result1 = None
        result2 = None

        # TODO: Get usage stats
        stats = client.get_usage_stats(user_id)

        return {
            "success": True,
            "requests_made": stats["requests"],
            "tokens_used": stats["tokens_used"],
            "estimated_cost": stats["estimated_cost"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    result = test_production_client()
    if result["success"]:
        print("✓ Production client test successful")
        print(f"Requests: {result['requests_made']}")
        print(f"Tokens: {result['tokens_used']}")
        print(f"Cost: ${result['estimated_cost']:.4f}")
    else:
        print(f"✗ Error: {result['error']}")
""",
    "solution_code": """import os
import time
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionLLMClient:
    \"\"\"Production-ready LLM client with monitoring and controls\"\"\"

    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY', 'test-key'))

        # Tracking
        self.request_counts = defaultdict(int)
        self.token_usage = defaultdict(int)
        self.costs = defaultdict(float)
        self.last_request_time = {}
        self.request_history = defaultdict(list)

        # Configuration
        self.max_requests_per_hour = 10
        self.max_tokens_per_day = 10000
        self.cost_per_1k_tokens = 0.002

    def check_rate_limit(self, user_id: str) -> bool:
        \"\"\"Check if user has exceeded rate limits\"\"\"
        now = time.time()

        # Clean old requests (older than 1 hour)
        if user_id in self.request_history:
            self.request_history[user_id] = [
                t for t in self.request_history[user_id]
                if now - t < 3600
            ]

        # Check hourly limit
        recent_requests = len(self.request_history[user_id])
        if recent_requests >= self.max_requests_per_hour:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return False

        return True

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def make_request(self, user_id: str, prompt: str, **kwargs) -> Dict:
        \"\"\"Make LLM request with retry logic\"\"\"

        # Check rate limits
        if not self.check_rate_limit(user_id):
            return {
                "error": "Rate limit exceeded. Please try again later.",
                "rate_limited": True
            }

        # Make API call
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 150),
                temperature=kwargs.get("temperature", 0.7)
            )

            # Extract data
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens

            # Track usage
            self.request_history[user_id].append(time.time())
            self.request_counts[user_id] += 1
            self.token_usage[user_id] += tokens
            cost = (tokens / 1000) * self.cost_per_1k_tokens
            self.costs[user_id] += cost

            # Log
            self.log_request(user_id, prompt, content, tokens)

            return {
                "response": content,
                "tokens": tokens,
                "cost": cost,
                "success": True
            }

        except Exception as e:
            logger.error(f"Request failed for user {user_id}: {str(e)}")
            return {"error": str(e), "success": False}

    def get_usage_stats(self, user_id: str) -> Dict:
        \"\"\"Get usage statistics for a user\"\"\"
        return {
            "requests": self.request_counts[user_id],
            "tokens_used": self.token_usage[user_id],
            "estimated_cost": self.costs[user_id]
        }

    def log_request(self, user_id: str, prompt: str, response: str, tokens: int):
        \"\"\"Log request for monitoring\"\"\"
        logger.info(
            f"User: {user_id} | Tokens: {tokens} | "
            f"Prompt: {prompt[:50]}... | Response: {response[:50]}..."
        )

def test_production_client():
    \"\"\"Test the production LLM client\"\"\"

    client = ProductionLLMClient()
    user_id = "user_123"

    try:
        # Make test requests
        result1 = client.make_request(
            user_id,
            "What is prompt engineering?",
            max_tokens=50
        )

        result2 = client.make_request(
            user_id,
            "Explain rate limiting in one sentence.",
            max_tokens=30
        )

        # Get usage stats
        stats = client.get_usage_stats(user_id)

        return {
            "success": True,
            "requests_made": stats["requests"],
            "tokens_used": stats["tokens_used"],
            "estimated_cost": stats["estimated_cost"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    result = test_production_client()
    if result["success"]:
        print("✓ Production client test successful")
        print(f"Requests: {result['requests_made']}")
        print(f"Tokens: {result['tokens_used']}")
        print(f"Cost: ${result['estimated_cost']:.4f}")
    else:
        print(f"✗ Error: {result['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:success", "description": "Should complete successfully"},
        {"input": "", "expected_output": "contains:requests_made", "description": "Should track requests"},
        {"input": "", "expected_output": "contains:tokens_used", "description": "Should track tokens"},
        {"input": "", "expected_output": "contains:estimated_cost", "description": "Should calculate costs"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
