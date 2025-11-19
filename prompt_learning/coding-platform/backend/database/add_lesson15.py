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
    "title": "ReAct: Reasoning + Acting",
    "slug": "react-pattern",
    "description": "Learn the ReAct pattern that combines reasoning and action, enabling LLMs to use tools and solve complex problems through iterative thought-action-observation loops.",
    "difficulty": "advanced",
    "order": 15,
    "language": "python",
    "estimated_time": 65,
    "tags": ["prompt-engineering", "react", "agents", "reasoning", "tools", "advanced"],
    "content": """# ReAct: Reasoning + Acting

## Learning Objectives
- Understand the ReAct (Reasoning + Acting) framework
- Learn the Thought-Action-Observation loop
- Implement tool-using agents
- Build systems that combine reasoning with external actions
- Apply ReAct to complex problem-solving tasks

## Introduction

**ReAct** is a powerful paradigm that combines:
- **Reasoning**: Thinking through problems step-by-step
- **Acting**: Taking actions (using tools, APIs, searches)

**Traditional LLM (No Tools):**
```
User: "What's the current temperature in Tokyo?"
LLM: "I don't have access to real-time data..." ❌
```

**ReAct LLM (With Tools):**
```
Thought: I need to look up current weather data
Action: search("Tokyo weather")
Observation: Tokyo is currently 18°C, partly cloudy
Thought: I have the information needed
Response: "It's currently 18°C in Tokyo with partly cloudy skies" ✓
```

ReAct enables LLMs to:
- Access real-time information
- Perform calculations
- Interact with databases
- Use external APIs
- Solve multi-step problems

## Core Concepts

### The ReAct Loop

```
┌─────────────────────────────────────┐
│         User Question               │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │   Thought    │ ← "I need to search for X"
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   Action     │ ← search("X")
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │ Observation  │ ← "Found: ..."
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   Thought    │ ← "Now I know..."
        └──────┬───────┘
               │
               ▼
          (Repeat or Answer)
```

### ReAct Components

**1. Thought**
- Internal reasoning
- Planning next steps
- Analyzing observations

**2. Action**
- Tool invocation
- API calls
- External interactions

**3. Observation**
- Results from actions
- New information acquired
- Environmental feedback

### Basic ReAct Example

```python
def react_agent(question):
    max_iterations = 5

    for i in range(max_iterations):
        # Thought
        thought = llm(f"Think about how to answer: {question}")

        # Decide action
        action = llm(f"Based on this thought: {thought}, what action should I take?")

        if "FINAL ANSWER" in action:
            return extract_answer(action)

        # Execute action
        observation = execute_action(action)

        # Continue loop with new observation
        question = f"{question}\\nObservation: {observation}"

    return "Could not solve in max iterations"
```

### Tool Definition

Tools are functions the LLM can call:

```python
tools = {
    "calculator": {
        "description": "Perform mathematical calculations",
        "function": lambda expr: eval(expr)
    },
    "search": {
        "description": "Search the web for information",
        "function": lambda query: web_search(query)
    },
    "weather": {
        "description": "Get current weather for a location",
        "function": lambda location: get_weather(location)
    }
}
```

### ReAct Prompt Template

```python
REACT_PROMPT = \"\"\"Answer the following question by reasoning and using tools.

Available tools:
{tool_descriptions}

Use this format:
Thought: [your reasoning]
Action: [tool_name: input]
Observation: [tool output]
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: [your answer]

Question: {question}

Begin!
\"\"\"
```

### Example: ReAct in Action

**Question:** "What's 15% of the population of Tokyo?"

```
Thought: I need to find Tokyo's population first
Action: search: Tokyo population
Observation: Tokyo has approximately 14 million people

Thought: Now I need to calculate 15% of 14 million
Action: calculator: 14000000 * 0.15
Observation: 2100000

Thought: I now have the final answer
Final Answer: 15% of Tokyo's population is approximately 2.1 million people
```

### Implementing ReAct

**Simple ReAct Agent:**
```python
def simple_react_agent(question, tools, max_steps=5):
    context = f"Question: {question}\\n"

    for step in range(max_steps):
        # Generate thought and action
        prompt = f\"\"\"{context}
Think about the next step and choose an action.
Available tools: {list(tools.keys())}

Thought:\"\"\"

        response = llm(prompt)

        # Check if final answer
        if "Final Answer:" in response:
            return extract_final_answer(response)

        # Parse action
        if "Action:" in response:
            action_line = extract_action(response)
            tool_name, tool_input = parse_action(action_line)

            # Execute tool
            if tool_name in tools:
                observation = tools[tool_name](tool_input)
                context += f"{response}\\nObservation: {observation}\\n"
            else:
                context += f"{response}\\nObservation: Tool not found\\n"
        else:
            context += f"{response}\\n"

    return "Could not find answer within step limit"
```

### Advanced ReAct Features

**1. Error Handling**
```python
try:
    observation = execute_tool(action)
except Exception as e:
    observation = f"Error: {str(e)}"
    # Agent can reason about errors and try alternative approach
```

**2. Tool Selection**
```python
def select_tool(thought, available_tools):
    prompt = f\"\"\"Given this thought: {thought}
    Which tool should I use?
    Tools: {available_tools}
    Answer with just the tool name.\"\"\"
    return llm(prompt)
```

**3. Multi-Step Reasoning**
```python
# Agent can chain multiple tools
Thought: Need to convert currency then calculate tax
Action: currency_converter: 100 USD to EUR
Observation: 92 EUR
Thought: Now calculate 20% tax
Action: calculator: 92 * 0.20
Observation: 18.4
Final Answer: 18.4 EUR tax on 100 USD
```

### LangChain ReAct Agent

LangChain provides built-in ReAct support:

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub

# Define tools
def calculator(expression):
    return eval(expression)

def search(query):
    return f"Search results for: {query}"

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations"
    ),
    Tool(
        name="Search",
        func=search,
        description="Useful for finding information"
    )
]

# Create ReAct agent
llm = ChatOpenAI(temperature=0)
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Use agent
result = agent_executor.invoke({
    "input": "What's 25% of 841?"
})
```

### ReAct vs. Other Patterns

| Pattern | Reasoning | Actions | Use Case |
|---------|-----------|---------|----------|
| **Direct** | No | No | Simple Q&A |
| **Chain-of-Thought** | Yes | No | Complex reasoning |
| **ReAct** | Yes | Yes | Tool use, multi-step |
| **Plan-and-Execute** | Yes (upfront) | Yes | Complex workflows |

### Best Practices

**1. Clear Tool Descriptions**
```python
{
    "name": "weather_api",
    "description": "Gets current weather. Input should be a city name like 'London' or 'Tokyo'"
}
```

**2. Limit Iterations**
```python
max_iterations = 10  # Prevent infinite loops
```

**3. Validate Tool Inputs**
```python
def safe_calculator(expr):
    # Validate before eval
    if not is_safe_expression(expr):
        return "Invalid expression"
    return eval(expr)
```

**4. Log Reasoning Trace**
```python
trace = []
for step in agent_steps:
    trace.append({
        "thought": step.thought,
        "action": step.action,
        "observation": step.observation
    })
```

**5. Handle Failures Gracefully**
```python
if iterations >= max_iterations:
    return "Could not complete task. Last state: ..."
```

## Your Task

Build a ReAct agent that can use multiple tools to solve complex problems.
""",
    "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_react_agent():
    \"\"\"
    Build a ReAct agent that combines reasoning with tool use.

    Returns:
        dict: Results from ReAct agent solving problems
    \"\"\"

    # TODO: Define tools
    def calculator(expression):
        \"\"\"Evaluate a mathematical expression.\"\"\"
        try:
            # Safe evaluation (in production, use ast.literal_eval or safer methods)
            result = eval(expression)
            return str(result)
        except:
            return "Error in calculation"

    def search_simulator(query):
        \"\"\"Simulate a search engine (returns mock data).\"\"\"
        # Mock search results
        mock_data = {
            "python": "Python is a programming language created in 1991",
            "tokyo": "Tokyo is the capital of Japan with 14 million people",
            "weather": "The weather API returns current conditions"
        }
        for key in mock_data:
            if key in query.lower():
                return mock_data[key]
        return "No results found"

    tools = {
        "calculator": calculator,
        "search": search_simulator
    }

    # TODO: Create ReAct prompt template
    def create_react_prompt(question, tools_desc):
        \"\"\"Create a ReAct-style prompt.\"\"\"
        prompt = f\"\"\"Answer this question using reasoning and tools.

Available tools:
{tools_desc}

Format:
Thought: [your reasoning]
Action: [tool_name: input]
Observation: [wait for result]

Question: {question}

Begin!
Thought:\"\"\"
        return prompt

    # TODO: Implement ReAct loop
    def react_solve(question, max_steps=5):
        \"\"\"Solve a question using ReAct pattern.\"\"\"
        context = ""
        tool_descriptions = "calculator - for math\\nsearch - for information"

        for step in range(max_steps):
            # TODO: Generate thought and action
            # TODO: Parse and execute action
            # TODO: Add observation to context
            # TODO: Check for final answer
            pass

        return "Not implemented"

    # Test questions
    test_question = "What is 15% of 200?"

    try:
        # TODO: Solve using ReAct
        result = react_solve(test_question)

        return {
            "question": test_question,
            "answer": result,
            "tools_available": list(tools.keys()),
            "pattern": "ReAct"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_react_agent()
    print("=== ReAct AGENT ===\")
    print(f"Pattern: {results.get('pattern')}")
    print(f"Tools: {results.get('tools_available')}")
    print(f"\\nQuestion: {results.get('question')}")
    print(f"Answer: {results.get('answer')}")
""",
    "solution_code": """import os
from openai import OpenAI
import re

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def build_react_agent():
    \"\"\"
    Build a ReAct agent that combines reasoning with tool use.

    Returns:
        dict: Results from ReAct agent solving problems
    \"\"\"

    # Define tools
    def calculator(expression):
        \"\"\"Evaluate a mathematical expression.\"\"\"
        try:
            # Clean expression
            expression = expression.strip()
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

    def search_simulator(query):
        \"\"\"Simulate a search engine (returns mock data).\"\"\"
        mock_data = {
            "python": "Python is a programming language created in 1991",
            "tokyo": "Tokyo is the capital of Japan with 14 million people",
            "weather": "Current weather APIs provide real-time conditions"
        }
        query_lower = query.lower()
        for key in mock_data:
            if key in query_lower:
                return mock_data[key]
        return "No specific results found"

    tools = {
        "calculator": calculator,
        "search": search_simulator
    }

    def create_react_prompt(question, context=""):
        \"\"\"Create a ReAct-style prompt.\"\"\"
        tools_desc = "- calculator: for mathematical calculations (e.g., calculator: 100 * 0.15)\\n- search: for finding information"

        prompt = f\"\"\"You are a helpful assistant that uses tools to answer questions.

Available tools:
{tools_desc}

Format:
Thought: [reasoning about what to do]
Action: [tool_name: input]
Observation: [result will be provided]
... (repeat as needed)
Thought: I now have the final answer
Final Answer: [your answer]

{context}
Question: {question}
Thought:\"\"\"
        return prompt

    def parse_action(text):
        \"\"\"Extract tool name and input from action.\"\"\"
        match = re.search(r'Action:\\s*([^:]+):\\s*(.+)', text)
        if match:
            tool_name = match.group(1).strip().lower()
            tool_input = match.group(2).strip()
            return tool_name, tool_input
        return None, None

    def react_solve(question, max_steps=5):
        \"\"\"Solve a question using ReAct pattern.\"\"\"
        context = ""
        trace = []

        for step in range(max_steps):
            # Generate thought and action
            prompt = create_react_prompt(question, context)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )

            agent_response = response.choices[0].message.content.strip()

            # Check for final answer
            if "Final Answer:" in agent_response:
                match = re.search(r'Final Answer:\\s*(.+)', agent_response, re.DOTALL)
                if match:
                    final_answer = match.group(1).strip()
                    trace.append({"step": step + 1, "type": "final", "content": agent_response})
                    return final_answer, trace

            # Parse and execute action
            tool_name, tool_input = parse_action(agent_response)

            if tool_name and tool_input:
                if tool_name in tools:
                    observation = tools[tool_name](tool_input)
                    trace.append({
                        "step": step + 1,
                        "thought": agent_response,
                        "action": f"{tool_name}: {tool_input}",
                        "observation": observation
                    })
                    context += f"{agent_response}\\nObservation: {observation}\\n"
                else:
                    observation = f"Tool '{tool_name}' not found"
                    context += f"{agent_response}\\nObservation: {observation}\\n"
            else:
                # No valid action, just thought
                context += f"{agent_response}\\n"

        return "Could not solve within step limit", trace

    # Test questions
    test_question = "What is 15% of 200?"

    try:
        # Solve using ReAct
        answer, trace = react_solve(test_question)

        return {
            "question": test_question,
            "answer": answer,
            "tools_available": list(tools.keys()),
            "pattern": "ReAct (Reasoning + Acting)",
            "steps_taken": len(trace),
            "trace": trace[:3]  # First 3 steps
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_react_agent()
    print("=== ReAct AGENT ===\")
    print(f"Pattern: {results.get('pattern')}")
    print(f"Tools: {results.get('tools_available')}")
    print(f"Steps: {results.get('steps_taken')}")

    print(f"\\nQuestion: {results.get('question')}")
    print(f"Answer: {results.get('answer')}")

    print(f"\\n=== REASONING TRACE ===\")
    for step in results.get('trace', []):
        if 'thought' in step:
            print(f"\\nStep {step['step']}:")
            print(f"Action: {step['action']}")
            print(f"Observation: {step['observation']}")

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:answer", "description": "Should return an answer"},
        {"input": "", "expected_output": "contains:tools_available", "description": "Should list available tools"},
        {"input": "", "expected_output": "contains:pattern", "description": "Should identify as ReAct pattern"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
