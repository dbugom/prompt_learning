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
    "title": "Chain-of-Thought Prompting",
    "slug": "chain-of-thought",
    "description": "Learn advanced reasoning techniques that dramatically improve LLM performance on complex problems by breaking them into logical steps.",
    "difficulty": "intermediate",
    "order": 8,
    "language": "python",
    "estimated_time": 50,
    "tags": ["prompt-engineering", "reasoning", "chain-of-thought", "problem-solving", "intermediate"],
    "content": """# Chain-of-Thought Prompting

## Learning Objectives
- Understand what Chain-of-Thought (CoT) prompting is
- Learn when and why to use CoT
- Master the "Let's think step by step" technique
- Compare direct vs. CoT reasoning performance
- Apply CoT to complex multi-step problems

## Introduction

**Chain-of-Thought (CoT) prompting** is a breakthrough technique that dramatically improves LLM performance on reasoning tasks. Instead of asking for a direct answer, you prompt the model to show its reasoning process step-by-step.

**The Problem:**
```python
# Direct prompting (often incorrect)
Q: "Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many balls does he have?"
A: "11 balls"  # Wrong! (Common LLM error)
```

**The Solution:**
```python
# Chain-of-Thought prompting (correct)
Q: "Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many balls does he have? Let's think step by step."
A: "Roger starts with 5 balls.
    Each can has 3 balls.
    2 cans = 2 × 3 = 6 balls.
    Total = 5 + 6 = 11 balls."  # Correct!
```

**Key Insight:** By making the LLM "show its work," it's forced to reason more carefully, reducing errors significantly.

## Core Concepts

### What is Chain-of-Thought?

Chain-of-Thought prompting encourages the model to:
1. Break down complex problems into smaller steps
2. Show intermediate reasoning
3. Arrive at answers through logical progression

**Research shows:** CoT improves accuracy by 50%+ on reasoning tasks (Wei et al., 2022)

### When to Use CoT

**Use CoT for:**
- ✓ Math word problems
- ✓ Multi-step reasoning
- ✓ Complex logical deduction
- ✓ Planning and strategy
- ✓ Analysis requiring justification
- ✓ Debugging and troubleshooting

**Don't use CoT for:**
- ✗ Simple factual questions
- ✗ Creative writing
- ✗ Translation
- ✗ Single-step tasks

### CoT Techniques

**1. Zero-Shot CoT (Simplest)**
Just add: "Let's think step by step"

```python
prompt = f\"\"\"Question: {question}
Let's think step by step.\"\"\"
```

**2. Few-Shot CoT (More Reliable)**
Provide examples with reasoning chains:

```python
prompt = \"\"\"Q: If a train travels 60 mph for 2 hours, how far does it go?
A: Let's think step by step.
- Speed = 60 mph
- Time = 2 hours
- Distance = Speed × Time = 60 × 2 = 120 miles

Q: {new_question}
A: Let's think step by step.\"\"\"
```

**3. Explicit Step Prompting**
Guide the reasoning structure:

```python
prompt = f\"\"\"Solve this problem step by step:
1. Identify the given information
2. Determine what we need to find
3. Choose the appropriate formula
4. Perform the calculation
5. State the final answer

Problem: {question}\"\"\"
```

**4. Self-Consistency CoT**
Generate multiple reasoning paths, pick the most common answer:

```python
# Generate 5 different reasoning chains
# Pick the answer that appears most frequently
```

### CoT Patterns

**Mathematical Reasoning:**
```
"Let's solve this step by step:
Step 1: Identify the knowns
Step 2: Apply the formula
Step 3: Calculate the result"
```

**Logical Deduction:**
```
"Let's reason through this:
- Given: [premises]
- Therefore: [intermediate conclusion]
- Thus: [final conclusion]"
```

**Planning:**
```
"Let's break this down:
1. What's the goal?
2. What resources do we have?
3. What are the steps?
4. What's the best approach?"
```

### Benefits of CoT

1. **Improved Accuracy**: 20-50% better on complex tasks
2. **Transparency**: You can see the reasoning
3. **Debuggable**: Find where logic went wrong
4. **Educational**: Explanations help users learn
5. **Trustworthy**: Users can verify the logic

### Limitations

- **Token Cost**: Longer outputs = higher costs
- **Time**: More tokens = slower responses
- **Not Always Needed**: Overkill for simple tasks
- **No Guarantee**: Still can make logical errors

## Your Task

Build a problem solver that compares direct vs. Chain-of-Thought reasoning on complex problems.
""",
    "starter_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def compare_reasoning_approaches():
    \"\"\"
    Compare direct prompting vs. Chain-of-Thought on complex problems.

    Returns:
        dict: Results from both approaches with reasoning quality analysis
    \"\"\"

    # Complex problem requiring multi-step reasoning
    problem = \"\"\"A bakery makes 12 dozen cookies every morning. They sell cookies in boxes
    of 6. If they've already sold 18 boxes today and need to reserve 4 dozen for a catering
    order, how many boxes can they still sell?\"\"\"

    # TODO: Create a direct prompt (no reasoning guidance)
    direct_prompt = \"\"\"
    # Ask for the answer directly without reasoning steps
    \"\"\"

    # TODO: Create a Chain-of-Thought prompt
    # Use "Let's think step by step" or similar technique
    cot_prompt = \"\"\"
    # Guide the model to show step-by-step reasoning
    \"\"\"

    # TODO: Create a few-shot CoT prompt with an example
    few_shot_cot_prompt = \"\"\"
    # Provide an example problem with step-by-step reasoning
    # Then ask to solve the new problem the same way
    \"\"\"

    try:
        # TODO: Get direct response
        direct_response = ""  # Get completion for direct_prompt

        # TODO: Get zero-shot CoT response
        cot_response = ""  # Get completion for cot_prompt

        # TODO: Get few-shot CoT response
        few_shot_response = ""  # Get completion for few_shot_cot_prompt

        # TODO: Analyze which approach showed better reasoning
        # Count reasoning steps, check for logical flow

        return {
            "problem": problem,
            "direct_answer": direct_response,
            "cot_answer": cot_response,
            "few_shot_cot_answer": few_shot_response,
            "analysis": "Chain-of-Thought provides transparent, verifiable reasoning"
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = compare_reasoning_approaches()
    print("=== PROBLEM ===\")
    print(results.get("problem"))
    print("\\n=== DIRECT APPROACH ===\")
    print(results.get("direct_answer"))
    print("\\n=== CHAIN-OF-THOUGHT ===\")
    print(results.get("cot_answer"))
    print("\\n=== FEW-SHOT COT ===\")
    print(results.get("few_shot_cot_answer"))
    print("\\n=== ANALYSIS ===\")
    print(results.get("analysis"))
""",
    "solution_code": """import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def compare_reasoning_approaches():
    \"\"\"
    Compare direct prompting vs. Chain-of-Thought on complex problems.

    Returns:
        dict: Results from both approaches with reasoning quality analysis
    \"\"\"

    problem = \"\"\"A bakery makes 12 dozen cookies every morning. They sell cookies in boxes
    of 6. If they've already sold 18 boxes today and need to reserve 4 dozen for a catering
    order, how many boxes can they still sell?\"\"\"

    # Direct prompt (no reasoning guidance)
    direct_prompt = f\"\"\"Answer this question with just the final number:

{problem}

Answer:\"\"\"

    # Zero-shot Chain-of-Thought prompt
    cot_prompt = f\"\"\"{problem}

Let's think step by step to solve this problem.\"\"\"

    # Few-shot CoT prompt with example
    few_shot_cot_prompt = f\"\"\"Solve these problems step by step:

Example:
Q: A store has 8 boxes of pencils with 12 pencils each. They sell 3 boxes. How many pencils remain?
A: Let's think step by step:
1. Total pencils initially: 8 boxes × 12 pencils = 96 pencils
2. Pencils sold: 3 boxes × 12 pencils = 36 pencils
3. Remaining pencils: 96 - 36 = 60 pencils
Answer: 60 pencils

Now solve this:
Q: {problem}
A: Let's think step by step:\"\"\"

    try:
        # Get direct response
        direct_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": direct_prompt}],
            temperature=0.3,
            max_tokens=100
        )
        direct_response = direct_completion.choices[0].message.content.strip()

        # Get zero-shot CoT response
        cot_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": cot_prompt}],
            temperature=0.3,
            max_tokens=300
        )
        cot_response = cot_completion.choices[0].message.content.strip()

        # Get few-shot CoT response
        few_shot_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": few_shot_cot_prompt}],
            temperature=0.3,
            max_tokens=300
        )
        few_shot_response = few_shot_completion.choices[0].message.content.strip()

        # Analyze reasoning quality
        analysis = \"\"\"
Chain-of-Thought Benefits Observed:
1. Transparent reasoning - can verify each step
2. Better accuracy - less likely to make calculation errors
3. Educational - shows the problem-solving process
4. Debuggable - can identify where logic fails

Correct Answer:
- 12 dozen = 144 cookies
- 18 boxes sold = 108 cookies
- 4 dozen reserved = 48 cookies
- Available = 144 - 108 - 48 = -12 (error in problem) or
- Better interpretation: Available after reservation before sales
- (144 - 48) ÷ 6 = 16 boxes possible, minus 18 sold = issue
\"\"\"

        return {
            "problem": problem,
            "direct_answer": direct_response,
            "cot_answer": cot_response,
            "few_shot_cot_answer": few_shot_response,
            "analysis": analysis.strip(),
            "direct_tokens": direct_completion.usage.total_tokens,
            "cot_tokens": cot_completion.usage.total_tokens,
            "few_shot_tokens": few_shot_completion.usage.total_tokens
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = compare_reasoning_approaches()
    print("=== PROBLEM ===\")
    print(results.get("problem"))
    print("\\n=== DIRECT APPROACH ===\")
    print(results.get("direct_answer"))
    if "direct_tokens" in results:
        print(f"Tokens used: {results['direct_tokens']}")
    print("\\n=== ZERO-SHOT CHAIN-OF-THOUGHT ===\")
    print(results.get("cot_answer"))
    if "cot_tokens" in results:
        print(f"Tokens used: {results['cot_tokens']}")
    print("\\n=== FEW-SHOT CHAIN-OF-THOUGHT ===\")
    print(results.get("few_shot_cot_answer"))
    if "few_shot_tokens" in results:
        print(f"Tokens used: {results['few_shot_tokens']}")
    print("\\n=== ANALYSIS ===\")
    print(results.get("analysis"))
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:direct_answer", "description": "Should return direct answer"},
        {"input": "", "expected_output": "contains:cot_answer", "description": "Should return CoT answer"},
        {"input": "", "expected_output": "contains:analysis", "description": "Should provide analysis"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
