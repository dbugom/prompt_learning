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
    "title": "Function Calling and Tool Use",
    "slug": "function-calling",
    "description": "Master OpenAI's function calling feature to enable LLMs to reliably call external functions, APIs, and tools with structured outputs.",
    "difficulty": "advanced",
    "order": 16,
    "language": "python",
    "estimated_time": 65,
    "tags": ["prompt-engineering", "function-calling", "tools", "openai", "apis", "advanced"],
    "content": """# Function Calling and Tool Use

## Learning Objectives
- Understand OpenAI's function calling feature
- Define function schemas with JSON Schema
- Implement function execution pipelines
- Build reliable tool-using systems
- Handle parallel function calls

## Introduction

**Function calling** allows LLMs to generate structured function calls instead of natural language responses. This enables reliable integration with external systems.

**Without Function Calling:**
```
User: "What's the weather in Tokyo?"
LLM: "I should use get_weather(location='Tokyo')"  # Just text!
```

**With Function Calling:**
```
User: "What's the weather in Tokyo?"
LLM: {
    "name": "get_weather",
    "arguments": {"location": "Tokyo"}
}  # Structured, executable!
```

**Benefits:**
- Reliable structured output
- Type-safe function calls
- Automatic parameter extraction
- Multi-tool orchestration
- Better than prompt engineering for tool use

## Core Concepts

### How Function Calling Works

```
1. User asks question
       ↓
2. LLM receives question + function definitions
       ↓
3. LLM decides: answer directly OR call function
       ↓
4. If function call → returns function name + arguments
       ↓
5. Your code executes the function
       ↓
6. Return result to LLM
       ↓
7. LLM generates final answer
```

### Function Schema Format

Functions are defined using JSON Schema:

```python
function_definition = {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name, e.g., 'Tokyo'"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    }
}
```

### Basic Function Calling Example

```python
from openai import OpenAI

client = OpenAI()

# Define function
def get_weather(location, unit="celsius"):
    # Your implementation
    return f"Weather in {location}: 20°{unit[0].upper()}"

# Function schema
functions = [{
    "name": "get_weather",
    "description": "Get current weather",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        },
        "required": ["location"]
    }
}]

# Make API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    functions=functions,
    function_call="auto"  # Let model decide
)

# Check if function was called
message = response.choices[0].message

if message.function_call:
    function_name = message.function_call.name
    function_args = json.loads(message.function_call.arguments)

    # Execute function
    if function_name == "get_weather":
        result = get_weather(**function_args)

        # Send result back to model
        messages = [
            {"role": "user", "content": "What's the weather in Tokyo?"},
            message,
            {"role": "function", "name": function_name, "content": result}
        ]

        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        print(final_response.choices[0].message.content)
```

### Function Call Control

**auto** - Model decides:
```python
function_call="auto"
```

**none** - Never call functions:
```python
function_call="none"
```

**Force specific function**:
```python
function_call={"name": "get_weather"}
```

### Multiple Functions

Define multiple tools:

```python
functions = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {...}
    },
    {
        "name": "get_stock_price",
        "description": "Get stock price for a symbol",
        "parameters": {...}
    },
    {
        "name": "calculator",
        "description": "Perform calculations",
        "parameters": {...}
    }
]

# Model will choose appropriate function
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's Apple's stock price?"}],
    functions=functions,
    function_call="auto"
)
```

### Parallel Function Calls

GPT-4 can call multiple functions in parallel:

```python
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{
        "role": "user",
        "content": "Get weather in Tokyo and stock price for AAPL"
    }],
    tools=tools  # New format
)

# Response may contain multiple tool calls
for tool_call in response.choices[0].message.tool_calls:
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    # Execute each function
```

### Building a Function Execution Framework

```python
import json

class FunctionExecutor:
    def __init__(self):
        self.functions = {}

    def register(self, name, func, schema):
        \"\"\"Register a function with its schema.\"\"\"
        self.functions[name] = {
            "function": func,
            "schema": schema
        }

    def get_schemas(self):
        \"\"\"Get all function schemas for API call.\"\"\"
        return [f["schema"] for f in self.functions.values()]

    def execute(self, function_name, arguments):
        \"\"\"Execute a function by name with arguments.\"\"\"
        if function_name not in self.functions:
            return {"error": f"Function {function_name} not found"}

        func = self.functions[function_name]["function"]

        try:
            result = func(**arguments)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

# Usage
executor = FunctionExecutor()

executor.register(
    "get_weather",
    get_weather,
    {
        "name": "get_weather",
        "description": "Get weather",
        "parameters": {...}
    }
)

# Execute
result = executor.execute("get_weather", {"location": "Tokyo"})
```

### Error Handling

**Invalid Arguments:**
```python
try:
    args = json.loads(function_call.arguments)
    result = function(**args)
except json.JSONDecodeError:
    result = "Error: Invalid JSON arguments"
except TypeError as e:
    result = f"Error: Invalid arguments - {e}"
```

**Function Errors:**
```python
def safe_execute(func, args):
    try:
        return {"success": True, "result": func(**args)}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Real-World Tools

**Database Query:**
```python
{
    "name": "query_database",
    "description": "Query the customer database",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "SQL query"},
            "limit": {"type": "integer", "description": "Max results"}
        },
        "required": ["query"]
    }
}
```

**API Call:**
```python
{
    "name": "send_email",
    "description": "Send an email",
    "parameters": {
        "type": "object",
        "properties": {
            "to": {"type": "string", "description": "Recipient email"},
            "subject": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["to", "subject", "body"]
    }
}
```

**File Operations:**
```python
{
    "name": "read_file",
    "description": "Read contents of a file",
    "parameters": {
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Path to file"}
        },
        "required": ["filepath"]
    }
}
```

### Best Practices

**1. Clear Descriptions**
```python
# Bad
"description": "Gets data"

# Good
"description": "Gets current weather data for a specific city. Returns temperature, conditions, and humidity."
```

**2. Parameter Validation**
```python
def get_weather(location, unit="celsius"):
    if unit not in ["celsius", "fahrenheit"]:
        raise ValueError(f"Invalid unit: {unit}")
    if not location:
        raise ValueError("Location is required")
    # ...
```

**3. Type Hints**
```python
from typing import Literal

def get_weather(
    location: str,
    unit: Literal["celsius", "fahrenheit"] = "celsius"
) -> dict:
    ...
```

**4. Structured Returns**
```python
def get_weather(location):
    return {
        "location": location,
        "temperature": 20,
        "conditions": "sunny",
        "unit": "celsius"
    }
```

**5. Logging**
```python
import logging

logger = logging.getLogger(__name__)

def execute_function(name, args):
    logger.info(f"Executing {name} with {args}")
    result = functions[name](**args)
    logger.info(f"Result: {result}")
    return result
```

### Function Calling vs. ReAct

| Feature | Function Calling | ReAct |
|---------|-----------------|-------|
| **Structure** | Strict schema | Text-based |
| **Reliability** | High | Medium |
| **Flexibility** | Lower | Higher |
| **Implementation** | Native API | Custom prompting |
| **Use Case** | Structured tools | Exploratory tasks |

## Your Task

Build a multi-tool system using OpenAI function calling with proper execution and error handling.
""",
    "starter_code": """import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_function_calling_system():
    \"\"\"
    Build a system that uses OpenAI function calling with multiple tools.

    Returns:
        dict: Results from function calling execution
    \"\"\"

    # TODO: Define tool functions
    def calculator(expression):
        \"\"\"Evaluate a math expression.\"\"\"
        try:
            return str(eval(expression))
        except:
            return "Error in calculation"

    def get_word_count(text):
        \"\"\"Count words in text.\"\"\"
        return str(len(text.split()))

    def reverse_text(text):
        \"\"\"Reverse a string.\"\"\"
        return text[::-1]

    # TODO: Define function schemas
    functions = [
        # {
        #     "name": "calculator",
        #     "description": "...",
        #     "parameters": {...}
        # },
    ]

    # TODO: Create a function to execute functions
    def execute_function(function_name, arguments):
        \"\"\"Execute a function by name.\"\"\"
        # Map function names to actual functions
        # Execute and return result
        pass

    # TODO: Implement function calling flow
    def call_with_functions(user_message):
        \"\"\"Call LLM with function calling capability.\"\"\"
        # 1. Make API call with functions
        # 2. Check if function_call in response
        # 3. Execute function
        # 4. Send result back to LLM
        # 5. Get final response
        pass

    try:
        # Test with a query that requires function calling
        test_query = "What is 25 * 17?"

        result = call_with_functions(test_query)

        return {
            "query": test_query,
            "result": result,
            "functions_available": 3,
            "pattern": "OpenAI Function Calling"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_function_calling_system()
    print("=== FUNCTION CALLING SYSTEM ===\")
    print(f"Pattern: {results.get('pattern')}")
    print(f"Functions: {results.get('functions_available')}")
    print(f"\\nQuery: {results.get('query')}")
    print(f"Result: {results.get('result')}")
""",
    "solution_code": """import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_function_calling_system():
    \"\"\"
    Build a system that uses OpenAI function calling with multiple tools.

    Returns:
        dict: Results from function calling execution
    \"\"\"

    # Define tool functions
    def calculator(expression):
        \"\"\"Evaluate a math expression.\"\"\"
        try:
            # Clean and evaluate
            result = eval(str(expression))
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

    def get_word_count(text):
        \"\"\"Count words in text.\"\"\"
        words = str(text).split()
        return str(len(words))

    def reverse_text(text):
        \"\"\"Reverse a string.\"\"\"
        return str(text)[::-1]

    # Define function schemas
    functions = [
        {
            "name": "calculator",
            "description": "Perform mathematical calculations. Input should be a valid Python expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate, e.g., '25 * 17'"
                    }
                },
                "required": ["expression"]
            }
        },
        {
            "name": "get_word_count",
            "description": "Count the number of words in a text string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to count words in"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "reverse_text",
            "description": "Reverse a string of text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to reverse"
                    }
                },
                "required": ["text"]
            }
        }
    ]

    # Map function names to implementations
    available_functions = {
        "calculator": calculator,
        "get_word_count": get_word_count,
        "reverse_text": reverse_text
    }

    def execute_function(function_name, arguments):
        \"\"\"Execute a function by name with arguments.\"\"\"
        if function_name not in available_functions:
            return f"Error: Function {function_name} not found"

        func = available_functions[function_name]
        try:
            result = func(**arguments)
            return result
        except Exception as e:
            return f"Error executing {function_name}: {str(e)}"

    def call_with_functions(user_message):
        \"\"\"Call LLM with function calling capability.\"\"\"
        messages = [{"role": "user", "content": user_message}]

        # Make initial API call with functions
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto"
        )

        response_message = response.choices[0].message

        # Check if model wants to call a function
        if response_message.function_call:
            function_name = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)

            # Execute the function
            function_result = execute_function(function_name, function_args)

            # Add messages to conversation
            messages.append(response_message)
            messages.append({
                "role": "function",
                "name": function_name,
                "content": function_result
            })

            # Get final response from model
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            return {
                "answer": second_response.choices[0].message.content,
                "function_called": function_name,
                "function_args": function_args,
                "function_result": function_result
            }
        else:
            # No function call needed
            return {
                "answer": response_message.content,
                "function_called": None
            }

    try:
        # Test with different queries
        test_query = "What is 25 * 17?"

        result = call_with_functions(test_query)

        return {
            "query": test_query,
            "answer": result.get("answer"),
            "function_called": result.get("function_called"),
            "function_args": result.get("function_args"),
            "function_result": result.get("function_result"),
            "functions_available": len(functions),
            "pattern": "OpenAI Function Calling"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_function_calling_system()
    print("=== FUNCTION CALLING SYSTEM ===\")
    print(f"Pattern: {results.get('pattern')}")
    print(f"Functions available: {results.get('functions_available')}")

    print(f"\\nQuery: {results.get('query')}")
    print(f"Answer: {results.get('answer')}")

    if results.get('function_called'):
        print(f"\\n=== FUNCTION EXECUTION ===\")
        print(f"Function: {results.get('function_called')}")
        print(f"Arguments: {results.get('function_args')}")
        print(f"Result: {results.get('function_result')}")

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:answer", "description": "Should return an answer"},
        {"input": "", "expected_output": "contains:functions_available", "description": "Should list available functions"},
        {"input": "", "expected_output": "contains:pattern", "description": "Should use function calling pattern"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
