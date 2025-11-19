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
    "title": "LangChain Agents",
    "slug": "langchain-agents",
    "description": "Learn to build autonomous agents using LangChain that can reason, plan, and use tools to accomplish complex tasks.",
    "difficulty": "advanced",
    "order": 17,
    "language": "python",
    "estimated_time": 70,
    "tags": ["prompt-engineering", "langchain", "agents", "autonomous", "tools", "advanced"],
    "content": """# LangChain Agents

## Learning Objectives
- Understand LangChain agent architecture
- Learn different agent types (ReAct, OpenAI Functions, Structured Chat)
- Build custom agents with tools
- Implement agent executors with memory
- Create autonomous problem-solving systems

## Introduction

**LangChain Agents** are autonomous systems that use LLMs to determine which actions to take and in what order. Unlike chains (pre-defined sequences), agents make decisions dynamically.

**Chain (Fixed):**
```
Input → Step 1 → Step 2 → Step 3 → Output
```

**Agent (Dynamic):**
```
Input → Agent decides → Tool A → Agent decides → Tool C → Output
                    ↓                        ↓
                  Tool B                   Done
```

**Key Characteristics:**
- **Autonomous**: Makes own decisions
- **Tool-using**: Can call external functions
- **Iterative**: Repeats until task complete
- **Reasoning**: Thinks through problems

## Core Concepts

### Agent Components

**1. LLM (Brain)**
- Makes decisions
- Reasons about next steps
- Interprets tool outputs

**2. Tools (Hands)**
- Functions agent can call
- Search, calculate, API calls, etc.
- Defined with descriptions

**3. Agent Executor**
- Manages execution loop
- Handles errors
- Enforces iteration limits

**4. Memory (Optional)**
- Remembers conversation
- Maintains context
- Learns from interactions

### LangChain Agent Types

**1. ReAct Agent**
- Uses Thought-Action-Observation pattern
- Most versatile
- Good for complex tasks

**2. OpenAI Functions Agent**
- Uses native function calling
- More reliable
- Requires OpenAI models

**3. Structured Chat Agent**
- For chat models
- Handles multi-turn conversations

**4. Self-Ask with Search**
- Breaks down questions
- Uses search for facts

### Basic Agent Example

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub

# Define tools
def calculator(expression):
    return str(eval(expression))

def search(query):
    return f"Search results for: {query}"

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math. Input: mathematical expression"
    ),
    Tool(
        name="Search",
        func=search,
        description="Useful for finding information. Input: search query"
    )
]

# Create agent
llm = ChatOpenAI(temperature=0)
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# Run agent
result = agent_executor.invoke({
    "input": "What's 25% of 400?"
})

print(result["output"])
```

### OpenAI Functions Agent

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor

# Create agent with function calling
agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

result = agent_executor.invoke({
    "input": "Search for Python tutorials and summarize the top result"
})
```

### Custom Tools

**Simple Tool:**
```python
from langchain.tools import tool

@tool
def get_word_length(word: str) -> int:
    \"\"\"Returns the length of a word.\"\"\"
    return len(word)

# Automatically creates tool with description from docstring
```

**Structured Tool:**
```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="City name")
    unit: str = Field(description="Temperature unit", default="celsius")

def get_weather(location: str, unit: str = "celsius") -> str:
    return f"Weather in {location}: 20°{unit[0].upper()}"

weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="GetWeather",
    description="Get current weather for a location",
    args_schema=WeatherInput
)
```

### Agent with Memory

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Multi-turn conversation
agent_executor.invoke({"input": "My name is Alice"})
agent_executor.invoke({"input": "What's my name?"})  # Remembers!
```

### Agent Execution Flow

```python
1. Receive input
2. Agent thinks (LLM reasoning)
3. Agent decides on action
   ├─→ Use tool
   │   ├─→ Execute tool
   │   └─→ Get observation
   └─→ Or provide final answer
4. Repeat from step 2 until done
5. Return final output
```

### Error Handling in Agents

**Max Iterations:**
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=10,  # Prevent infinite loops
    early_stopping_method="generate"  # Generate answer if max reached
)
```

**Tool Error Handling:**
```python
from langchain.tools import Tool

def safe_calculator(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

calculator_tool = Tool(
    name="Calculator",
    func=safe_calculator,
    description="Safe calculator",
    handle_tool_error=True  # Continue on error
)
```

**Custom Error Handler:**
```python
def handle_parsing_error(error):
    return f"Could not parse output. Please try again. Error: {error}"

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=handle_parsing_error
)
```

### Agent Customization

**Custom Prompt:**
```python
from langchain.prompts import PromptTemplate

custom_prompt = PromptTemplate(
    template=\"\"\"You are a helpful assistant with access to tools.

Tools:
{tools}

History:
{chat_history}

Question: {input}

Think step by step and use tools as needed.
{agent_scratchpad}
\"\"\",
    input_variables=["tools", "chat_history", "input", "agent_scratchpad"]
)
```

**Agent Callbacks:**
```python
from langchain.callbacks import StdOutCallbackHandler

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[StdOutCallbackHandler()],
    verbose=True
)
```

### Multi-Agent Systems

**Specialized Agents:**
```python
# Research agent
research_tools = [search_tool, wikipedia_tool]
research_agent = create_react_agent(llm, research_tools, prompt)

# Math agent
math_tools = [calculator_tool]
math_agent = create_react_agent(llm, math_tools, prompt)

# Coordinator
def route_to_agent(task):
    if "calculate" in task.lower():
        return math_agent
    else:
        return research_agent
```

### Best Practices

**1. Clear Tool Descriptions**
```python
Tool(
    name="WebSearch",
    func=search,
    description="Search the web for current information. "
                "Input should be a search query string. "
                "Useful for facts, news, recent events."
)
```

**2. Limit Iterations**
```python
max_iterations=5  # Reasonable for most tasks
```

**3. Verbose Mode During Development**
```python
verbose=True  # See agent reasoning
```

**4. Handle Tool Failures**
```python
handle_tool_error=True
```

**5. Type Hints for Tools**
```python
def get_weather(location: str, unit: str = "celsius") -> dict:
    \"\"\"
    Get current weather.

    Args:
        location: City name
        unit: Temperature unit (celsius or fahrenheit)

    Returns:
        Dictionary with weather data
    \"\"\"
    ...
```

### Agent Use Cases

**Customer Support:**
- Search knowledge base
- Check order status
- Process refunds
- Update account info

**Research Assistant:**
- Search web
- Summarize articles
- Cite sources
- Answer questions

**Data Analysis:**
- Query databases
- Perform calculations
- Generate visualizations
- Write reports

**Personal Assistant:**
- Check calendar
- Send emails
- Set reminders
- Search documents

## Your Task

Build a LangChain agent system with multiple tools and memory.
""",
    "starter_code": """import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_langchain_agent():
    \"\"\"
    Build a LangChain agent with multiple tools.

    Returns:
        dict: Results from agent execution
    \"\"\"

    # TODO: Define tool functions
    def calculator(expression):
        \"\"\"Perform calculations.\"\"\"
        try:
            return str(eval(expression))
        except:
            return "Error in calculation"

    def text_analyzer(text):
        \"\"\"Analyze text and return word count and character count.\"\"\"
        words = len(text.split())
        chars = len(text)
        return f"Words: {words}, Characters: {chars}"

    # TODO: Create Tool objects
    tools = [
        # Tool(name="...", func=..., description="...")
    ]

    # TODO: Create agent prompt
    prompt = PromptTemplate(
        template=\"\"\"Answer the following question using available tools.

Tools:
{tools}

Tool Names: {tool_names}

Question: {input}

Thought: {agent_scratchpad}
\"\"\",
        input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
    )

    # TODO: Create agent
    agent = None  # create_react_agent(...)

    # TODO: Create agent executor
    agent_executor = None  # AgentExecutor(...)

    try:
        # TODO: Test the agent
        test_query = "What is 15 * 23?"

        result = {}  # agent_executor.invoke(...)

        return {
            "query": test_query,
            "answer": result.get("output", "Not implemented"),
            "tools_used": len(tools),
            "agent_type": "LangChain ReAct Agent"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_langchain_agent()
    print("=== LANGCHAIN AGENT ===\")
    print(f"Agent type: {results.get('agent_type')}")
    print(f"Tools: {results.get('tools_used')}")
    print(f"\\nQuery: {results.get('query')}")
    print(f"Answer: {results.get('answer')}")
""",
    "solution_code": """import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_langchain_agent():
    \"\"\"
    Build a LangChain agent with multiple tools.

    Returns:
        dict: Results from agent execution
    \"\"\"

    # Define tool functions
    def calculator(expression):
        \"\"\"Perform mathematical calculations.\"\"\"
        try:
            result = eval(str(expression))
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

    def text_analyzer(text):
        \"\"\"Analyze text and return statistics.\"\"\"
        words = len(str(text).split())
        chars = len(str(text))
        return f"Analysis: {words} words, {chars} characters"

    def string_reverser(text):
        \"\"\"Reverse a string.\"\"\"
        return str(text)[::-1]

    # Create Tool objects with clear descriptions
    tools = [
        Tool(
            name="Calculator",
            func=calculator,
            description="Useful for performing mathematical calculations. "
                       "Input should be a valid mathematical expression like '15 * 23' or '100 / 4'."
        ),
        Tool(
            name="TextAnalyzer",
            func=text_analyzer,
            description="Analyzes text and returns word count and character count. "
                       "Input should be a text string to analyze."
        ),
        Tool(
            name="StringReverser",
            func=string_reverser,
            description="Reverses a string. Input should be text to reverse."
        )
    ]

    # Create ReAct prompt template
    prompt = PromptTemplate.from_template(\"\"\"Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}\"\"\")

    # Create ReAct agent
    agent = create_react_agent(llm, tools, prompt)

    # Create agent executor with settings
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )

    try:
        # Test the agent with a calculation
        test_query = "What is 15 * 23?"

        result = agent_executor.invoke({"input": test_query})

        return {
            "query": test_query,
            "answer": result.get("output"),
            "tools_used": len(tools),
            "agent_type": "LangChain ReAct Agent",
            "max_iterations": 5,
            "tools_available": [t.name for t in tools]
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_langchain_agent()
    print("=== LANGCHAIN AGENT SYSTEM ===\")
    print(f"Agent type: {results.get('agent_type')}")
    print(f"Tools available: {results.get('tools_available')}")
    print(f"Max iterations: {results.get('max_iterations')}")

    print(f"\\n=== EXECUTION ===\")
    print(f"Query: {results.get('query')}")
    print(f"Answer: {results.get('answer')}")

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:answer", "description": "Should return an answer"},
        {"input": "", "expected_output": "contains:tools_used", "description": "Should use tools"},
        {"input": "", "expected_output": "contains:agent_type", "description": "Should identify as LangChain agent"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
