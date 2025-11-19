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
    "title": "Output Formatting and Structured Responses",
    "slug": "output-formatting",
    "description": "Master techniques for getting structured, parseable outputs from LLMs using JSON, delimiters, and formatting instructions.",
    "difficulty": "beginner",
    "order": 6,
    "language": "python",
    "estimated_time": 45,
    "tags": ["prompt-engineering", "json", "formatting", "parsing", "structured-output"],
    "content": """# Output Formatting and Structured Responses

## Learning Objectives
- Understand why structured outputs matter
- Learn to request JSON and other formats from LLMs
- Master delimiter techniques for clean parsing
- Handle and validate LLM-generated structured data
- Build robust parsing logic for LLM responses

## Introduction

One of the biggest challenges in LLM applications is getting **consistent, parseable output**. LLMs naturally produce free-form text, but real applications need structured data like JSON, CSV, or XML that can be programmatically processed.

**The Problem:**
```python
# Unpredictable output
response = "The sentiment is positive and the confidence is high..."
# How do you extract "positive" and "high" reliably?
```

**The Solution:**
```python
# Structured output
response = '{"sentiment": "positive", "confidence": "high"}'
data = json.loads(response)  # Easy to parse!
```

This lesson teaches you how to engineer prompts that produce consistent, machine-readable outputs.

## Core Concepts

### Why Structured Output Matters

**Use Cases:**
- **Data extraction**: Pull specific fields from LLM analysis
- **API integration**: Return data that other systems can consume
- **Validation**: Verify the response contains required information
- **Error handling**: Detect when LLM didn't follow instructions
- **Chaining**: Use output from one LLM call as input to another

### Technique 1: JSON Output

**Basic JSON Request:**
```python
prompt = \"\"\"Analyze this review and return JSON with this exact structure:
{
  "sentiment": "positive/negative/neutral",
  "score": 1-10,
  "keywords": ["keyword1", "keyword2"]
}

Review: "Great product but expensive"
\"\"\"
```

**Key Tips:**
- Provide exact JSON structure as example
- Specify data types (string, number, array)
- Use triple quotes for multi-line prompts
- Request "valid JSON only, no other text"

### Technique 2: Delimiters

Delimiters help separate different parts of the output:

```python
prompt = \"\"\"Analyze this text and format your response as:

SUMMARY: <one-line summary>
---
KEYWORDS: <comma-separated keywords>
---
SENTIMENT: <positive/negative/neutral>

Text: "..."
\"\"\"
```

**Common Delimiters:**
- `---` (three dashes)
- `###` (three hashes)
- `===` (three equals)
- XML-style tags: `<summary>...</summary>`

### Technique 3: Explicit Format Instructions

Be very specific about format requirements:

```python
prompt = \"\"\"Extract person names from this text.

IMPORTANT FORMAT RULES:
- Return ONLY a Python list
- Format: ["Name1", "Name2"]
- No explanations or other text
- If no names found, return []

Text: "John met Sarah at the park"
\"\"\"
```

### Parsing LLM Outputs

**Parsing JSON:**
```python
import json

try:
    data = json.loads(response)
    sentiment = data["sentiment"]
except json.JSONDecodeError:
    # Handle invalid JSON
    print("LLM didn't return valid JSON")
except KeyError:
    # Handle missing fields
    print("JSON missing required field")
```

**Parsing Delimited Text:**
```python
sections = response.split("---")
summary = sections[0].replace("SUMMARY:", "").strip()
keywords = sections[1].replace("KEYWORDS:", "").strip()
```

**Cleaning LLM Output:**
```python
# Remove markdown code blocks
response = response.replace("```json", "").replace("```", "")

# Extract JSON from text
import re
json_match = re.search(r'\\{.*\\}', response, re.DOTALL)
if json_match:
    json_str = json_match.group()
```

## Your Task

Build a product review analyzer that returns structured data in multiple formats.
""",
    "starter_code": """import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def analyze_review_structured():
    \"\"\"
    Analyze a product review and return structured outputs in different formats.

    Returns:
        dict: Contains JSON analysis, delimited analysis, and parsing success status
    \"\"\"

    review = \"\"\"I bought this laptop last month. The performance is amazing -
    it handles video editing smoothly. However, the battery life is disappointing,
    lasting only 4 hours. The build quality feels premium and the keyboard is
    comfortable. Customer service was helpful when I had questions. Overall,
    it's a good laptop but overpriced at $2000.\"\"\"

    # TODO: Create a prompt that requests JSON output
    # Should extract: overall_sentiment, pros (list), cons (list),
    # score (1-10), would_recommend (boolean)
    json_prompt = \"\"\"
    # Your JSON prompt here
    \"\"\"

    # TODO: Create a prompt that uses delimiters
    # Should separate: SUMMARY, PROS, CONS, RATING
    delimited_prompt = \"\"\"
    # Your delimited prompt here
    \"\"\"

    try:
        # TODO: Get JSON response
        json_response = ""  # Get completion for json_prompt

        # TODO: Get delimited response
        delimited_response = ""  # Get completion for delimited_prompt

        # TODO: Parse JSON response
        try:
            json_data = {}  # Parse json_response
            json_valid = True
        except:
            json_data = {}
            json_valid = False

        # TODO: Parse delimited response
        # Extract sections between delimiters
        parsed_delimited = {
            "summary": "",
            "pros": "",
            "cons": "",
            "rating": ""
        }

        return {
            "json_output": json_data,
            "json_valid": json_valid,
            "delimited_output": parsed_delimited,
            "review_analyzed": review[:50] + "..."
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = analyze_review_structured()
    print("=== JSON OUTPUT ===\")
    print(f"Valid: {results.get('json_valid')}")
    print(json.dumps(results.get('json_output', {}), indent=2))
    print("\\n=== DELIMITED OUTPUT ===\")
    for key, value in results.get('delimited_output', {}).items():
        print(f"{key.upper()}: {value}")
""",
    "solution_code": """import os
import json
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def analyze_review_structured():
    \"\"\"
    Analyze a product review and return structured outputs in different formats.

    Returns:
        dict: Contains JSON analysis, delimited analysis, and parsing success status
    \"\"\"

    review = \"\"\"I bought this laptop last month. The performance is amazing -
    it handles video editing smoothly. However, the battery life is disappointing,
    lasting only 4 hours. The build quality feels premium and the keyboard is
    comfortable. Customer service was helpful when I had questions. Overall,
    it's a good laptop but overpriced at $2000.\"\"\"

    json_prompt = f\"\"\"Analyze this product review and return your response as valid JSON ONLY.
Use this exact structure:

{{
  "overall_sentiment": "positive/negative/mixed",
  "pros": ["pro1", "pro2", "pro3"],
  "cons": ["con1", "con2"],
  "score": <number 1-10>,
  "would_recommend": true/false
}}

IMPORTANT: Return ONLY the JSON object, no other text or explanations.

Review: {review}
\"\"\"

    delimited_prompt = f\"\"\"Analyze this product review using the following format:

SUMMARY: <Write a one-sentence summary>
---
PROS: <List positive aspects, comma-separated>
---
CONS: <List negative aspects, comma-separated>
---
RATING: <Number from 1-10>

Review: {review}
\"\"\"

    try:
        # Get JSON response
        json_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": json_prompt}],
            temperature=0.3,
            max_tokens=300
        )
        json_response = json_completion.choices[0].message.content.strip()

        # Get delimited response
        delimited_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": delimited_prompt}],
            temperature=0.3,
            max_tokens=300
        )
        delimited_response = delimited_completion.choices[0].message.content.strip()

        # Parse JSON response (with cleanup)
        try:
            # Remove markdown code blocks if present
            cleaned_json = json_response.replace("```json", "").replace("```", "").strip()

            # Try to extract JSON object if embedded in text
            json_match = re.search(r'\\{.*\\}', cleaned_json, re.DOTALL)
            if json_match:
                cleaned_json = json_match.group()

            json_data = json.loads(cleaned_json)
            json_valid = True
        except json.JSONDecodeError as e:
            json_data = {"error": f"Invalid JSON: {str(e)}", "raw": json_response}
            json_valid = False

        # Parse delimited response
        sections = delimited_response.split("---")
        parsed_delimited = {}

        for section in sections:
            section = section.strip()
            if "SUMMARY:" in section:
                parsed_delimited["summary"] = section.replace("SUMMARY:", "").strip()
            elif "PROS:" in section:
                parsed_delimited["pros"] = section.replace("PROS:", "").strip()
            elif "CONS:" in section:
                parsed_delimited["cons"] = section.replace("CONS:", "").strip()
            elif "RATING:" in section:
                parsed_delimited["rating"] = section.replace("RATING:", "").strip()

        return {
            "json_output": json_data,
            "json_valid": json_valid,
            "delimited_output": parsed_delimited,
            "review_analyzed": review[:50] + "..."
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = analyze_review_structured()
    print("=== JSON OUTPUT ===\")
    print(f"Valid: {results.get('json_valid')}")
    print(json.dumps(results.get('json_output', {}), indent=2))
    print("\\n=== DELIMITED OUTPUT ===\")
    for key, value in results.get('delimited_output', {}).items():
        print(f"{key.upper()}: {value}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:json_output", "description": "Should return JSON output"},
        {"input": "", "expected_output": "contains:json_valid", "description": "Should validate JSON"},
        {"input": "", "expected_output": "contains:delimited_output", "description": "Should return delimited output"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
