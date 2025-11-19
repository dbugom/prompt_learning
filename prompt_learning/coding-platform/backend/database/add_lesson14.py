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
    "title": "Prompt Testing and Evaluation",
    "slug": "prompt-testing",
    "description": "Learn to systematically test and evaluate prompts using metrics, test cases, and A/B testing to ensure consistent, high-quality outputs.",
    "difficulty": "intermediate",
    "order": 14,
    "language": "python",
    "estimated_time": 60,
    "tags": ["prompt-engineering", "testing", "evaluation", "metrics", "qa", "intermediate"],
    "content": """# Prompt Testing and Evaluation

## Learning Objectives
- Understand why prompt testing is critical
- Create test suites for prompts
- Implement evaluation metrics
- Perform A/B testing on prompts
- Build automated testing pipelines

## Introduction

**The Problem:**
```python
# Works today
prompt = "Summarize this article"
result = llm(prompt)  # Good output

# Breaks tomorrow (LLM model updated, edge case found)
result = llm(prompt)  # Bad output!
```

LLM outputs are **non-deterministic** and can change with:
- Model updates
- Edge cases
- Prompt modifications
- Different providers

**The Solution:** Systematic testing and evaluation

Just like software testing, **prompt engineering needs testing** to ensure:
- Consistency across inputs
- Quality meets requirements
- Changes don't break existing functionality
- Performance is measurable

## Core Concepts

### Why Test Prompts?

**1. Catch Regressions**
- Prompt changes might break existing use cases
- Model updates can change behavior

**2. Measure Quality**
- Is output accurate, relevant, helpful?
- Does it meet business requirements?

**3. Compare Alternatives**
- Which prompt performs better?
- Which model is more suitable?

**4. Edge Cases**
- Handle unusual inputs gracefully
- Avoid harmful outputs

**5. Cost vs. Quality**
- Balance performance with API costs

### Test Case Structure

```python
test_cases = [
    {
        "input": "What is 2+2?",
        "expected_output": "4",
        "evaluation": "exact_match"
    },
    {
        "input": "Explain photosynthesis",
        "expected_keywords": ["sunlight", "plants", "oxygen", "carbon dioxide"],
        "evaluation": "keyword_presence"
    },
    {
        "input": "Translate 'Hello' to Spanish",
        "expected_output": "Hola",
        "evaluation": "contains"
    }
]
```

### Evaluation Metrics

**1. Exact Match**
```python
def exact_match(output, expected):
    return output.strip().lower() == expected.strip().lower()
```

**2. Contains Check**
```python
def contains_keywords(output, keywords):
    output_lower = output.lower()
    return all(keyword.lower() in output_lower for keyword in keywords)
```

**3. Length Check**
```python
def length_in_range(output, min_length, max_length):
    return min_length <= len(output) <= max_length
```

**4. Format Validation**
```python
import json

def is_valid_json(output):
    try:
        json.loads(output)
        return True
    except:
        return False
```

**5. Semantic Similarity**
```python
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(output, expected, threshold=0.8):
    embeddings = model.encode([output, expected])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return similarity >= threshold
```

**6. Custom Validators**
```python
def validate_sentiment(output, expected_sentiment):
    # Use another LLM to check sentiment
    check_prompt = f"Is this text {expected_sentiment}? Answer yes or no: {output}"
    response = llm(check_prompt)
    return "yes" in response.lower()
```

### Building a Test Suite

```python
class PromptTestSuite:
    def __init__(self, prompt_template):
        self.prompt_template = prompt_template
        self.test_cases = []
        self.results = []

    def add_test(self, input_data, expected, validator):
        self.test_cases.append({
            "input": input_data,
            "expected": expected,
            "validator": validator
        })

    def run_tests(self, llm):
        for test in self.test_cases:
            prompt = self.prompt_template.format(**test["input"])
            output = llm(prompt)

            passed = test["validator"](output, test["expected"])

            self.results.append({
                "input": test["input"],
                "output": output,
                "expected": test["expected"],
                "passed": passed
            })

        return self.generate_report()

    def generate_report(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])

        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "details": self.results
        }
```

### A/B Testing Prompts

Compare two prompt versions:

```python
def ab_test_prompts(prompt_a, prompt_b, test_inputs, llm):
    results = {
        "prompt_a": {"wins": 0, "outputs": []},
        "prompt_b": {"wins": 0, "outputs": []}
    }

    for input_text in test_inputs:
        output_a = llm(prompt_a.format(input=input_text))
        output_b = llm(prompt_b.format(input=input_text))

        # Human evaluation or automated scoring
        score_a = evaluate_output(output_a)
        score_b = evaluate_output(output_b)

        if score_a > score_b:
            results["prompt_a"]["wins"] += 1
        elif score_b > score_a:
            results["prompt_b"]["wins"] += 1

        results["prompt_a"]["outputs"].append(output_a)
        results["prompt_b"]["outputs"].append(output_b)

    return results
```

### Regression Testing

Prevent prompt changes from breaking existing functionality:

```python
import json

# Save baseline outputs
def create_baseline(prompt, test_inputs, llm):
    baseline = {}
    for input_text in test_inputs:
        output = llm(prompt.format(input=input_text))
        baseline[input_text] = output

    with open('baseline.json', 'w') as f:
        json.dump(baseline, f)

# Compare against baseline
def regression_test(prompt, llm):
    with open('baseline.json', 'r') as f:
        baseline = json.load(f)

    failures = []
    for input_text, expected_output in baseline.items():
        current_output = llm(prompt.format(input=input_text))

        if current_output != expected_output:
            failures.append({
                "input": input_text,
                "expected": expected_output,
                "actual": current_output
            })

    return failures
```

### Automated Evaluation with LLMs

Use an LLM to evaluate outputs:

```python
def llm_evaluate(output, criteria):
    eval_prompt = f\"\"\"Evaluate this output based on the following criteria:
{criteria}

Output to evaluate:
{output}

Provide a score from 1-10 and brief explanation.
Format: Score: X/10
Reason: ...\"\"\"

    evaluation = llm(eval_prompt)
    # Parse score
    score = extract_score(evaluation)
    return score

def extract_score(evaluation):
    import re
    match = re.search(r'Score: (\d+)/10', evaluation)
    return int(match.group(1)) if match else 0
```

### Performance Metrics

**Latency Testing**
```python
import time

def measure_latency(prompt, llm, iterations=10):
    latencies = []
    for _ in range(iterations):
        start = time.time()
        llm(prompt)
        latencies.append(time.time() - start)

    return {
        "avg_latency": sum(latencies) / len(latencies),
        "min_latency": min(latencies),
        "max_latency": max(latencies)
    }
```

**Token Usage Tracking**
```python
import tiktoken

def track_token_usage(prompt, llm):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    input_tokens = len(encoding.encode(prompt))

    response = llm(prompt)
    output_tokens = len(encoding.encode(response))

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }
```

### Best Practices

**1. Diverse Test Cases**
- Normal cases
- Edge cases
- Error cases
- Different lengths
- Various formats

**2. Automated Testing**
- Run tests in CI/CD
- Version control test cases
- Track metrics over time

**3. Human Evaluation**
- Sample random outputs
- Quality review process
- User feedback integration

**4. Continuous Monitoring**
- Log all inputs/outputs
- Track success rates
- Alert on quality degradation

**5. Iterative Improvement**
```python
# Test → Measure → Improve → Repeat
while quality < target:
    results = run_tests(prompt)
    if results["pass_rate"] < target:
        prompt = improve_prompt(prompt, results["failures"])
    else:
        break
```

## Your Task

Build a comprehensive prompt testing system with multiple evaluation strategies.
""",
    "starter_code": """import os
from openai import OpenAI
import time

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_prompt_testing_system():
    \"\"\"
    Build a testing system for evaluating prompt quality.

    Returns:
        dict: Test results with various metrics
    \"\"\"

    # Prompt to test
    test_prompt = "Translate '{text}' to {language}. Provide only the translation."

    # TODO: Create test cases
    test_cases = [
        # {"input": {"text": "Hello", "language": "Spanish"}, "expected": "Hola", "metric": "exact_match"},
        # Add more test cases
    ]

    # TODO: Implement evaluation functions
    def exact_match(output, expected):
        \"\"\"Check if output exactly matches expected.\"\"\"
        pass

    def contains_check(output, expected):
        \"\"\"Check if output contains expected string.\"\"\"
        pass

    def length_check(output, min_len, max_len):
        \"\"\"Check if output length is within range.\"\"\"
        pass

    # TODO: Run tests and collect results
    def run_test_suite():
        \"\"\"Run all test cases and return results.\"\"\"
        results = []
        # For each test case:
        #   1. Format prompt
        #   2. Call LLM
        #   3. Evaluate output
        #   4. Record result
        return results

    # TODO: Calculate metrics
    def calculate_metrics(results):
        \"\"\"Calculate pass rate and other metrics.\"\"\"
        total = len(results)
        passed = 0  # Count passed tests
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": 0.0
        }

    try:
        # TODO: Execute tests
        test_results = []  # run_test_suite()
        metrics = {}  # calculate_metrics(test_results)

        return {
            "tests_run": 0,
            "pass_rate": 0.0,
            "metrics": metrics,
            "sample_results": []
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_prompt_testing_system()
    print("=== PROMPT TESTING SYSTEM ===\")
    print(f"Tests run: {results.get('tests_run')}")
    print(f"Pass rate: {results.get('pass_rate'):.1%}")
    print(f"\\nMetrics: {results.get('metrics')}")
""",
    "solution_code": """import os
from openai import OpenAI
import time

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_prompt_testing_system():
    \"\"\"
    Build a testing system for evaluating prompt quality.

    Returns:
        dict: Test results with various metrics
    \"\"\"

    # Prompt to test
    test_prompt = "Translate '{text}' to {language}. Provide only the translation."

    # Create comprehensive test cases
    test_cases = [
        {
            "input": {"text": "Hello", "language": "Spanish"},
            "expected": "Hola",
            "metric": "exact_match"
        },
        {
            "input": {"text": "Goodbye", "language": "French"},
            "expected": "Au revoir",
            "metric": "contains"
        },
        {
            "input": {"text": "Thank you", "language": "German"},
            "expected": "Danke",
            "metric": "contains"
        },
        {
            "input": {"text": "Good morning", "language": "Italian"},
            "expected": None,  # Just check length
            "metric": "length",
            "min_len": 5,
            "max_len": 30
        }
    ]

    # Evaluation functions
    def exact_match(output, expected):
        \"\"\"Check if output exactly matches expected.\"\"\"
        return output.strip().lower() == expected.strip().lower()

    def contains_check(output, expected):
        \"\"\"Check if output contains expected string.\"\"\"
        return expected.lower() in output.lower()

    def length_check(output, min_len, max_len):
        \"\"\"Check if output length is within range.\"\"\"
        return min_len <= len(output.strip()) <= max_len

    # Run tests and collect results
    def run_test_suite():
        \"\"\"Run all test cases and return results.\"\"\"
        results = []

        for i, test in enumerate(test_cases):
            # Format prompt
            prompt = test_prompt.format(**test["input"])

            # Measure latency
            start_time = time.time()

            try:
                # Call LLM
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=50
                )
                output = response.choices[0].message.content.strip()
                latency = time.time() - start_time

                # Evaluate based on metric type
                if test["metric"] == "exact_match":
                    passed = exact_match(output, test["expected"])
                elif test["metric"] == "contains":
                    passed = contains_check(output, test["expected"])
                elif test["metric"] == "length":
                    passed = length_check(output, test["min_len"], test["max_len"])
                else:
                    passed = False

                results.append({
                    "test_id": i + 1,
                    "input": test["input"],
                    "output": output,
                    "expected": test.get("expected"),
                    "metric": test["metric"],
                    "passed": passed,
                    "latency": latency
                })

            except Exception as e:
                results.append({
                    "test_id": i + 1,
                    "input": test["input"],
                    "error": str(e),
                    "passed": False
                })

        return results

    # Calculate comprehensive metrics
    def calculate_metrics(results):
        \"\"\"Calculate pass rate and other metrics.\"\"\"
        total = len(results)
        passed = sum(1 for r in results if r.get("passed", False))
        failed = total - passed

        latencies = [r["latency"] for r in results if "latency" in r]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0,
            "avg_latency": avg_latency,
            "metrics_tracked": ["accuracy", "latency", "coverage"]
        }

    try:
        # Execute tests
        test_results = run_test_suite()
        metrics = calculate_metrics(test_results)

        # Get sample results (first 2)
        sample_results = [
            {
                "test": r["test_id"],
                "input": r["input"],
                "output": r.get("output", "ERROR"),
                "passed": r["passed"]
            }
            for r in test_results[:2]
        ]

        return {
            "tests_run": metrics["total"],
            "pass_rate": metrics["pass_rate"],
            "metrics": metrics,
            "sample_results": sample_results,
            "all_results": test_results
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_prompt_testing_system()
    print("=== PROMPT TESTING SYSTEM ===\")
    print(f"Tests run: {results.get('tests_run')}")
    print(f"Pass rate: {results.get('pass_rate', 0):.1%}")

    metrics = results.get('metrics', {})
    print(f"\\n=== METRICS ===\")
    print(f"Passed: {metrics.get('passed')}/{metrics.get('total')}")
    print(f"Failed: {metrics.get('failed')}")
    print(f"Avg latency: {metrics.get('avg_latency', 0):.3f}s")
    print(f"Metrics tracked: {', '.join(metrics.get('metrics_tracked', []))}")

    print(f"\\n=== SAMPLE RESULTS ===\")
    for sample in results.get('sample_results', []):
        status = "✓ PASS" if sample["passed"] else "✗ FAIL"
        print(f"Test {sample['test']}: {status}")
        print(f"  Input: {sample['input']}")
        print(f"  Output: {sample['output']}")

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:tests_run", "description": "Should run tests"},
        {"input": "", "expected_output": "contains:pass_rate", "description": "Should calculate pass rate"},
        {"input": "", "expected_output": "contains:metrics", "description": "Should provide metrics"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
