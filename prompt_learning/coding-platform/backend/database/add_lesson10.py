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
    "title": "Prompt Chaining and Workflows",
    "slug": "prompt-chaining",
    "description": "Learn to build complex multi-step LLM workflows by chaining prompts together, where the output of one becomes the input of another.",
    "difficulty": "intermediate",
    "order": 10,
    "language": "python",
    "estimated_time": 55,
    "tags": ["prompt-engineering", "langchain", "chains", "workflows", "intermediate"],
    "content": """# Prompt Chaining and Workflows

## Learning Objectives
- Understand the concept of prompt chaining
- Learn when to use sequential workflows
- Use LangChain's SimpleSequentialChain
- Build custom multi-step chains
- Handle intermediate outputs in complex workflows

## Introduction

**Prompt chaining** is the technique of connecting multiple LLM calls where the output of one call becomes the input to the next. This enables complex, multi-step reasoning and processing that a single prompt cannot achieve.

**Simple Example:**
```
Step 1: Generate story idea → "A robot learning to cook"
Step 2: Write story from idea → "Once upon a time, a curious robot..."
Step 3: Summarize story → "A heartwarming tale about..."
```

**Why Chain Prompts?**

1. **Break complexity**: Divide complex tasks into manageable steps
2. **Better quality**: Each step focuses on one thing
3. **Intermediate validation**: Check outputs between steps
4. **Modularity**: Reuse steps in different workflows
5. **Debugging**: Identify which step failed

## Core Concepts

### What is Prompt Chaining?

```
Input → [Prompt 1] → LLM → Output 1 → [Prompt 2] → LLM → Output 2 → Final Result
```

**Example Workflow:**
```
User Query
    ↓
Extract Keywords (LLM 1)
    ↓
Search Database
    ↓
Summarize Results (LLM 2)
    ↓
Generate Answer (LLM 3)
```

### Types of Chains

**1. SimpleSequentialChain**
- Output of one chain → Input of next
- Single string passed between chains
- Simplest form

**2. SequentialChain**
- Multiple inputs/outputs
- Named variables
- More control

**3. Custom Chains**
- Full flexibility
- Conditional logic
- Error handling

### SimpleSequentialChain

Perfect for linear workflows with single inputs/outputs:

```python
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.7)

# Step 1: Generate idea
idea_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Generate a creative idea for a {topic}"
)
idea_chain = LLMChain(llm=llm, prompt=idea_prompt)

# Step 2: Expand idea
expand_prompt = PromptTemplate(
    input_variables=["idea"],
    template="Expand this idea into 3 sentences: {idea}"
)
expand_chain = LLMChain(llm=llm, prompt=expand_prompt)

# Create sequential chain
overall_chain = SimpleSequentialChain(
    chains=[idea_chain, expand_chain],
    verbose=True  # Shows intermediate outputs
)

result = overall_chain.run("mobile app")
```

### SequentialChain (Advanced)

For workflows with multiple variables:

```python
from langchain.chains import SequentialChain

# Chain 1: Extract info
extract_chain = LLMChain(
    llm=llm,
    prompt=extract_prompt,
    output_key="extracted_data"
)

# Chain 2: Analyze info
analyze_chain = LLMChain(
    llm=llm,
    prompt=analyze_prompt,
    output_key="analysis"
)

# Combine chains
workflow = SequentialChain(
    chains=[extract_chain, analyze_chain],
    input_variables=["text"],
    output_variables=["extracted_data", "analysis"],
    verbose=True
)

result = workflow({"text": "Some input text"})
# Returns: {"extracted_data": "...", "analysis": "..."}
```

### Real-World Workflow Examples

**Content Creation Pipeline:**
```
Topic → Outline → Draft → Edit → Format → Final Content
```

**Data Analysis Pipeline:**
```
Raw Data → Clean → Analyze → Visualize → Summarize → Report
```

**Customer Support Pipeline:**
```
Question → Classify → Extract Info → Search KB → Generate Answer → Format
```

### Building Custom Chains

Sometimes you need more control:

```python
def custom_chain_workflow(user_input):
    # Step 1: Classification
    classification = classify_chain.run(user_input)

    # Step 2: Conditional routing
    if classification == "technical":
        response = technical_chain.run(user_input)
    else:
        response = general_chain.run(user_input)

    # Step 3: Post-processing
    final = format_chain.run(response)

    return final
```

### Chain Design Patterns

**Pattern 1: Transform Pipeline**
```
Input → Transform 1 → Transform 2 → Transform 3 → Output
Example: Text → Translate → Summarize → Format → Final
```

**Pattern 2: Enrichment**
```
Input → Extract Entities → Lookup Info → Merge → Output
Example: "Call John" → Extract "John" → Get John's number → "Calling 555-1234"
```

**Pattern 3: Validation Loop**
```
Input → Generate → Validate → (if invalid) Regenerate → Output
Example: Code → Generate → Test → (if fails) Fix → Final Code
```

**Pattern 4: Map-Reduce**
```
Input → Split → Process Each → Combine → Output
Example: Long Doc → Chunks → Summarize Each → Merge Summaries
```

### Best Practices

**1. Keep chains focused**
- Each step should have one clear purpose
- Avoid trying to do too much in one chain

**2. Add visibility**
- Use `verbose=True` during development
- Log intermediate outputs

**3. Error handling**
- Validate outputs between steps
- Add fallbacks for failures

**4. Test incrementally**
- Test each chain individually first
- Then test the full workflow

**5. Consider cost**
- More chains = more API calls = higher cost
- Balance complexity vs. cost

## Your Task

Build a blog post creation workflow that chains multiple steps together.
""",
    "starter_code": """import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_blog_workflow():
    \"\"\"
    Build a multi-step blog post creation workflow using prompt chaining.

    Returns:
        dict: Outputs from each stage of the workflow
    \"\"\"

    topic = "The benefits of remote work"

    # TODO: Create Chain 1 - Generate outline
    # Input: topic
    # Output: A bullet-point outline
    outline_prompt = None  # PromptTemplate(...)
    outline_chain = None  # LLMChain(...)

    # TODO: Create Chain 2 - Write introduction
    # Input: outline (from Chain 1)
    # Output: Introduction paragraph
    intro_prompt = None  # PromptTemplate(...)
    intro_chain = None  # LLMChain(...)

    # TODO: Create Chain 3 - Add conclusion
    # Input: introduction (from Chain 2)
    # Output: Introduction + conclusion
    conclusion_prompt = None  # PromptTemplate(...)
    conclusion_chain = None  # LLMChain(...)

    # TODO: Create SimpleSequentialChain to connect all chains
    blog_workflow = None  # SimpleSequentialChain(...)

    try:
        # TODO: Run the workflow
        final_output = ""  # blog_workflow.run(topic)

        return {
            "topic": topic,
            "final_output": final_output,
            "chains_used": 3,
            "workflow_type": "SimpleSequentialChain"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_blog_workflow()
    print("=== BLOG POST WORKFLOW ===\")
    print(f"Topic: {results.get('topic')}")
    print(f"Workflow: {results.get('workflow_type')}")
    print(f"Chains: {results.get('chains_used')}")
    print("\\n=== FINAL OUTPUT ===\")
    print(results.get('final_output'))
""",
    "solution_code": """import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
)

def build_blog_workflow():
    \"\"\"
    Build a multi-step blog post creation workflow using prompt chaining.

    Returns:
        dict: Outputs from each stage of the workflow
    \"\"\"

    topic = "The benefits of remote work"

    # Chain 1: Generate outline
    outline_prompt = PromptTemplate(
        input_variables=["topic"],
        template=\"\"\"Create a brief 3-point outline for a blog post about: {topic}

Format as:
1. [Point 1]
2. [Point 2]
3. [Point 3]

Keep it concise.\"\"\"
    )
    outline_chain = LLMChain(llm=llm, prompt=outline_prompt)

    # Chain 2: Write introduction from outline
    intro_prompt = PromptTemplate(
        input_variables=["outline"],
        template=\"\"\"Based on this outline, write a compelling 2-3 sentence introduction:

{outline}

Make it engaging and set the context.\"\"\"
    )
    intro_chain = LLMChain(llm=llm, prompt=intro_prompt)

    # Chain 3: Add conclusion to introduction
    conclusion_prompt = PromptTemplate(
        input_variables=["introduction"],
        template=\"\"\"Here's a blog introduction:

{introduction}

Now write a 2-3 sentence conclusion that wraps up the topic and provides a call to action.

Format:
Introduction: [introduction text]

Conclusion: [conclusion text]\"\"\"
    )
    conclusion_chain = LLMChain(llm=llm, prompt=conclusion_prompt)

    # Create sequential workflow
    blog_workflow = SimpleSequentialChain(
        chains=[outline_chain, intro_chain, conclusion_chain],
        verbose=True  # Shows intermediate steps
    )

    try:
        # Run the complete workflow
        final_output = blog_workflow.run(topic)

        return {
            "topic": topic,
            "final_output": final_output,
            "chains_used": 3,
            "workflow_type": "SimpleSequentialChain",
            "stages": ["Outline → Introduction → Conclusion"]
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = build_blog_workflow()
    print("=== BLOG POST WORKFLOW ===\")
    print(f"Topic: {results.get('topic')}")
    print(f"Workflow: {results.get('workflow_type')}")
    print(f"Chains: {results.get('chains_used')}")
    print(f"Pipeline: {results.get('stages', ['N/A'])[0]}")
    print("\\n=== FINAL OUTPUT ===\")
    print(results.get('final_output'))

    if 'error' in results:
        print(f"\\nError: {results['error']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:final_output", "description": "Should return final output"},
        {"input": "", "expected_output": "contains:chains_used", "description": "Should use multiple chains"},
        {"input": "", "expected_output": "contains:workflow_type", "description": "Should specify workflow type"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
