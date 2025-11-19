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
    "title": "Conversation Memory and Context",
    "slug": "conversation-memory",
    "description": "Learn to build stateful chatbots that remember conversation history using LangChain memory components and context management techniques.",
    "difficulty": "intermediate",
    "order": 13,
    "language": "python",
    "estimated_time": 55,
    "tags": ["prompt-engineering", "langchain", "memory", "chatbots", "context", "intermediate"],
    "content": """# Conversation Memory and Context

## Learning Objectives
- Understand why conversation memory is essential
- Learn LangChain memory types (Buffer, Summary, Window)
- Implement conversation history management
- Handle context window limits
- Build stateful chatbots with memory

## Introduction

LLMs are **stateless** by default - each API call is independent. They don't remember previous messages unless you explicitly send the conversation history.

**Without Memory:**
```
User: "My name is Alice"
Bot: "Nice to meet you!"

User: "What's my name?"
Bot: "I don't know your name."  # Forgot!
```

**With Memory:**
```
User: "My name is Alice"
Bot: "Nice to meet you, Alice!"

User: "What's my name?"
Bot: "Your name is Alice!"  # Remembered!
```

**Conversation memory** enables chatbots to maintain context across multiple exchanges, creating natural, coherent conversations.

## Core Concepts

### The Memory Problem

**Challenge:**
- LLMs have no inherent memory
- Each API call is isolated
- Need to pass full conversation history each time
- Context windows have token limits

**Solutions:**
1. Manual history management
2. LangChain Memory components
3. Context summarization
4. Message pruning

### Manual Conversation History

```python
from openai import OpenAI

client = OpenAI()
messages = []  # Store conversation history

def chat(user_input):
    # Add user message
    messages.append({"role": "user", "content": user_input})

    # Get response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Add assistant response
    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})

    return assistant_message

# Conversation
chat("My name is Alice")
chat("What's my name?")  # Works because we pass full history
```

### LangChain Memory Types

**1. ConversationBufferMemory**
- Stores all messages
- Simple and complete
- Can exceed token limits on long conversations

```python
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
llm = ChatOpenAI(temperature=0.7)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

conversation.predict(input="Hi, I'm Alice")
conversation.predict(input="What's my name?")
# Output: "Your name is Alice"
```

**2. ConversationBufferWindowMemory**
- Keeps only last K messages
- Prevents token overflow
- Loses older context

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=5)  # Keep last 5 exchanges
conversation = ConversationChain(llm=llm, memory=memory)
```

**3. ConversationSummaryMemory**
- Summarizes old messages
- Keeps recent messages in full
- Good for long conversations

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(llm=llm)
conversation = ConversationChain(llm=llm, memory=memory)
```

**4. ConversationSummaryBufferMemory**
- Hybrid: summary + recent messages
- Best of both worlds
- Token-efficient for long conversations

```python
from langchain.memory import ConversationSummaryBufferMemory

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=200
)
```

### Memory in Chains

**Basic Chain with Memory:**
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

template = \"\"\"You are a helpful assistant.

{history}
Human: {input}
Assistant:\"\"\"

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

memory = ConversationBufferMemory(memory_key="history")

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

chain.run("My name is Alice")
chain.run("What's my name?")
```

### Context Window Management

**Problem:** Models have token limits
- GPT-3.5: 4K tokens
- GPT-4: 8K tokens
- Claude: 200K tokens

**Strategies:**

**1. Sliding Window**
```python
def keep_recent_messages(messages, max_messages=10):
    return messages[-max_messages:]
```

**2. Token Counting and Pruning**
```python
import tiktoken

def prune_to_token_limit(messages, max_tokens=3000):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    total_tokens = 0
    pruned = []

    # Work backwards from most recent
    for msg in reversed(messages):
        msg_tokens = len(encoding.encode(msg["content"]))
        if total_tokens + msg_tokens > max_tokens:
            break
        pruned.insert(0, msg)
        total_tokens += msg_tokens

    return pruned
```

**3. Summarization**
```python
def summarize_old_messages(messages, keep_recent=5):
    if len(messages) <= keep_recent:
        return messages

    old_messages = messages[:-keep_recent]
    recent_messages = messages[-keep_recent:]

    # Summarize old messages
    summary = llm.invoke(f"Summarize this conversation: {old_messages}")

    return [
        {"role": "system", "content": f"Previous summary: {summary}"}
    ] + recent_messages
```

### Practical Patterns

**Pattern 1: Chat with Context**
```python
class ChatBot:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=ChatOpenAI(),
            memory=self.memory
        )

    def chat(self, message):
        return self.conversation.predict(input=message)

    def clear_memory(self):
        self.memory.clear()
```

**Pattern 2: Persistent Memory**
```python
# Save conversation to database/file
def save_conversation(user_id, messages):
    # Save to database
    db.save(user_id, messages)

def load_conversation(user_id):
    # Load from database
    return db.load(user_id)
```

**Pattern 3: Multi-User Memory**
```python
class MultiUserChatBot:
    def __init__(self):
        self.memories = {}  # user_id -> memory

    def get_or_create_memory(self, user_id):
        if user_id not in self.memories:
            self.memories[user_id] = ConversationBufferMemory()
        return self.memories[user_id]

    def chat(self, user_id, message):
        memory = self.get_or_create_memory(user_id)
        conversation = ConversationChain(llm=llm, memory=memory)
        return conversation.predict(input=message)
```

### Memory Variables

LangChain memory uses variables:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",  # Variable name
    return_messages=True  # Return as message objects
)

# Access history
history = memory.load_memory_variables({})
print(history["chat_history"])
```

### Best Practices

**1. Choose Right Memory Type**
- Short conversations: ConversationBufferMemory
- Long conversations: ConversationSummaryBufferMemory
- Token-limited: ConversationBufferWindowMemory

**2. Monitor Token Usage**
```python
def get_conversation_tokens(memory):
    history = memory.load_memory_variables({})
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(str(history)))
```

**3. System Messages for Context**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant. Remember user preferences."},
    # ... conversation history ...
]
```

**4. Clear Memory When Needed**
```python
# New topic, clear history
memory.clear()

# Or reset specific user
def reset_user_conversation(user_id):
    memories[user_id] = ConversationBufferMemory()
```

## Your Task

Build a multi-turn chatbot with conversation memory and context management.
""",
    "starter_code": """import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_chatbot_with_memory():
    \"\"\"
    Build chatbots with different memory strategies.

    Returns:
        dict: Conversation results from different memory types
    \"\"\"

    # TODO: Create chatbot with full buffer memory
    buffer_memory = None  # ConversationBufferMemory()
    buffer_chat = None  # ConversationChain(...)

    # TODO: Create chatbot with window memory (keep last 3 exchanges)
    window_memory = None  # ConversationBufferWindowMemory(k=3)
    window_chat = None  # ConversationChain(...)

    # TODO: Simulate a conversation with buffer memory
    # Message 1: "My favorite color is blue"
    # Message 2: "I love pizza"
    # Message 3: "What's my favorite color?"
    buffer_response_1 = ""
    buffer_response_2 = ""
    buffer_response_3 = ""

    # TODO: Simulate same conversation with window memory
    window_response_1 = ""
    window_response_2 = ""
    window_response_3 = ""

    # TODO: Create a function to inspect memory
    def inspect_memory(memory):
        \"\"\"Return conversation history from memory.\"\"\"
        # Load and return memory variables
        pass

    try:
        return {
            "buffer_final_response": buffer_response_3,
            "window_final_response": window_response_3,
            "buffer_memory_size": 0,
            "window_memory_size": 0,
            "memory_types_tested": 2
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_chatbot_with_memory()
    print("=== CHATBOT MEMORY SYSTEM ===\")
    print(f"Memory types tested: {results.get('memory_types_tested')}")
    print(f"\\n=== BUFFER MEMORY (Full History) ===\")
    print(f"Final response: {results.get('buffer_final_response')}")
    print(f"Memory size: {results.get('buffer_memory_size')} messages")
    print(f"\\n=== WINDOW MEMORY (Last 3) ===\")
    print(f"Final response: {results.get('window_final_response')}")
    print(f"Memory size: {results.get('window_memory_size')} messages")
""",
    "solution_code": """import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_chatbot_with_memory():
    \"\"\"
    Build chatbots with different memory strategies.

    Returns:
        dict: Conversation results from different memory types
    \"\"\"

    # Create chatbot with full buffer memory
    buffer_memory = ConversationBufferMemory()
    buffer_chat = ConversationChain(
        llm=llm,
        memory=buffer_memory,
        verbose=False
    )

    # Create chatbot with window memory (keep last 3 exchanges only)
    window_memory = ConversationBufferWindowMemory(k=3)
    window_chat = ConversationChain(
        llm=llm,
        memory=window_memory,
        verbose=False
    )

    # Function to inspect memory
    def inspect_memory(memory):
        \"\"\"Return conversation history from memory.\"\"\"
        history = memory.load_memory_variables({})
        return history.get("history", "")

    try:
        # Simulate conversation with buffer memory (remembers everything)
        buffer_response_1 = buffer_chat.predict(input="My favorite color is blue")
        buffer_response_2 = buffer_chat.predict(input="I love pizza")
        buffer_response_3 = buffer_chat.predict(input="What's my favorite color?")

        # Simulate same conversation with window memory (forgets older messages)
        window_response_1 = window_chat.predict(input="My favorite color is blue")
        window_response_2 = window_chat.predict(input="I love pizza")
        window_response_3 = window_chat.predict(input="What's my favorite color?")

        # Inspect memories
        buffer_history = inspect_memory(buffer_memory)
        window_history = inspect_memory(window_memory)

        # Count messages
        buffer_msg_count = buffer_history.count("Human:") + buffer_history.count("AI:")
        window_msg_count = window_history.count("Human:") + window_history.count("AI:")

        return {
            "buffer_final_response": buffer_response_3,
            "window_final_response": window_response_3,
            "buffer_memory_size": buffer_msg_count,
            "window_memory_size": window_msg_count,
            "memory_types_tested": 2,
            "buffer_history_preview": buffer_history[:200] + "...",
            "window_history_preview": window_history[:200] + "...",
            "observation": "Buffer memory remembers all, window memory only last 3 exchanges"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_chatbot_with_memory()
    print("=== CHATBOT MEMORY SYSTEM ===\")
    print(f"Memory types tested: {results.get('memory_types_tested')}")

    print(f"\\n=== BUFFER MEMORY (Full History) ===\")
    print(f"Final response: {results.get('buffer_final_response')}")
    print(f"Memory entries: {results.get('buffer_memory_size')}")
    print(f"History preview: {results.get('buffer_history_preview')}")

    print(f"\\n=== WINDOW MEMORY (Last 3 Exchanges) ===\")
    print(f"Final response: {results.get('window_final_response')}")
    print(f"Memory entries: {results.get('window_memory_size')}")
    print(f"History preview: {results.get('window_history_preview')}")

    print(f"\\n=== OBSERVATION ===\")
    print(results.get('observation'))

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:buffer_final_response", "description": "Should return buffer memory response"},
        {"input": "", "expected_output": "contains:window_final_response", "description": "Should return window memory response"},
        {"input": "", "expected_output": "contains:memory_types_tested", "description": "Should test multiple memory types"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
