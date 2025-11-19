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
    "title": "Tree of Thoughts",
    "slug": "tree-of-thoughts",
    "description": "Explore advanced reasoning with Tree of Thoughts - a technique that explores multiple reasoning paths, evaluates them, and selects the best solution.",
    "difficulty": "advanced",
    "order": 21,
    "language": "python",
    "estimated_time": 65,
    "tags": ["prompt-engineering", "tree-of-thoughts", "reasoning", "search", "evaluation"],
    "content": """# Tree of Thoughts

## Learning Objectives
- Understand the Tree of Thoughts (ToT) framework
- Learn how ToT differs from Chain-of-Thought
- Implement thought generation, evaluation, and search
- Build a ToT solver for complex problems
- Compare ToT with linear reasoning approaches

## Introduction

**Tree of Thoughts (ToT)** is an advanced prompting technique that extends Chain-of-Thought by exploring multiple reasoning paths simultaneously, evaluating each path, and using search algorithms to find the best solution.

### The Evolution of Reasoning

1. **Direct Prompting**: Single answer, no reasoning
2. **Chain-of-Thought**: Linear step-by-step reasoning
3. **Tree of Thoughts**: Branching multi-path exploration

### Why Tree of Thoughts?

CoT has limitations:
- **Linear path**: Commits to early decisions
- **No backtracking**: Can't recover from wrong steps
- **No exploration**: Misses alternative solutions

ToT solves these by:
- **Exploring multiple paths** simultaneously
- **Evaluating each step** before proceeding
- **Backtracking** when paths lead to dead ends
- **Finding optimal solutions** through search

## Core Concepts

### The ToT Framework

ToT consists of four key components:

1. **Thought Decomposition**
   - Break problem into intermediate steps
   - Each step is a "thought" (partial solution)

2. **Thought Generation**
   - Generate multiple candidate thoughts at each step
   - Use sampling or propose multiple options

3. **State Evaluation**
   - Assess how promising each thought is
   - Use LLM to evaluate or heuristic scoring

4. **Search Algorithm**
   - **Breadth-First Search (BFS)**: Explore all options level by level
   - **Depth-First Search (DFS)**: Explore one path fully before backtracking
   - **Beam Search**: Keep top-k best paths

### The ToT Process

```
Problem
  ↓
Generate 3 initial thoughts
  ↓
Evaluate each (score: good/medium/bad)
  ↓
Keep best 2 thoughts
  ↓
For each thought, generate 3 next steps
  ↓
Evaluate and prune
  ↓
Continue until solution found
```

### When to Use ToT

**Good for:**
- Complex puzzles (Game of 24, Sudoku)
- Creative writing with constraints
- Strategic planning
- Problems requiring exploration

**Overkill for:**
- Simple classification
- Straightforward Q&A
- Tasks with obvious single path

## Your Task

Implement a simplified Tree of Thoughts solver for a creative writing task: generate a short story that must include specific elements.

### Implementation Strategy

1. **Decompose**: Story into intro → conflict → resolution
2. **Generate**: 3 options for each part
3. **Evaluate**: Rate coherence and constraint satisfaction
4. **Select**: Best path through the tree
5. **Combine**: Selected thoughts into final story
""",
    "starter_code": """import os
from openai import OpenAI
from typing import List, Dict

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def generate_thoughts(prompt: str, num_thoughts: int = 3) -> List[str]:
    \"\"\"Generate multiple candidate thoughts\"\"\"
    # TODO: Use OpenAI to generate num_thoughts different options
    # Use temperature=0.8 for diversity
    thoughts = []
    return thoughts

def evaluate_thought(thought: str, criteria: str) -> float:
    \"\"\"Evaluate a thought on a scale of 0-10\"\"\"
    # TODO: Use OpenAI to evaluate the thought
    # Ask it to rate the thought based on criteria
    # Parse the numeric score from response
    score = 0.0
    return score

def tree_of_thoughts_story():
    \"\"\"Generate a story using Tree of Thoughts approach\"\"\"

    # Constraints: Story must include a robot, a garden, and a secret
    constraints = "robot, garden, secret"

    # Step 1: Generate story openings
    opening_prompt = f\"\"\"Generate a story opening (2-3 sentences) that introduces: {constraints}
Give me one creative opening.\"\"\"

    # TODO: Generate 3 different openings
    openings = []

    # TODO: Evaluate each opening
    # Criteria: "creativity and inclusion of required elements: robot, garden, secret"
    opening_scores = []

    # TODO: Select best opening
    best_opening = ""

    # Step 2: Generate conflict/middle
    conflict_prompt = f\"\"\"Given this story opening: '{best_opening}'
Generate a conflict or middle section (2-3 sentences) that develops the plot.\"\"\"

    # TODO: Generate 3 different conflicts
    conflicts = []

    # TODO: Evaluate and select best conflict
    best_conflict = ""

    # Step 3: Generate resolution
    resolution_prompt = f\"\"\"Given this story so far:
Opening: {best_opening}
Conflict: {best_conflict}

Generate a satisfying resolution (2-3 sentences).\"\"\"

    # TODO: Generate 3 different resolutions
    resolutions = []

    # TODO: Evaluate and select best resolution
    best_resolution = ""

    # Combine final story
    final_story = f\"{best_opening}\\n\\n{best_conflict}\\n\\n{best_resolution}\"

    return {
        "story": final_story,
        "constraints": constraints,
        "thoughts_generated": 9,  # 3 per stage
        "stages": 3
    }

if __name__ == "__main__":
    result = tree_of_thoughts_story()
    print(f"Required elements: {result['constraints']}")
    print(f"\\nThoughts generated: {result['thoughts_generated']} across {result['stages']} stages")
    print(f"\\nFinal Story:\\n{result['story']}")
""",
    "solution_code": """import os
from openai import OpenAI
from typing import List, Dict

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'test-key'))

def generate_thoughts(prompt: str, num_thoughts: int = 3) -> List[str]:
    \"\"\"Generate multiple candidate thoughts\"\"\"
    thoughts = []
    for i in range(num_thoughts):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=100
        )
        thoughts.append(response.choices[0].message.content.strip())
    return thoughts

def evaluate_thought(thought: str, criteria: str) -> float:
    \"\"\"Evaluate a thought on a scale of 0-10\"\"\"
    eval_prompt = f\"\"\"Evaluate this text based on {criteria}.
Rate it from 0-10 where 10 is excellent.
Respond with ONLY a number.

Text: {thought}

Rating:\"\"\"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0,
        max_tokens=10
    )

    try:
        score = float(response.choices[0].message.content.strip())
        return min(10.0, max(0.0, score))
    except:
        return 5.0

def tree_of_thoughts_story():
    \"\"\"Generate a story using Tree of Thoughts approach\"\"\"

    constraints = "robot, garden, secret"

    # Step 1: Generate and evaluate story openings
    opening_prompt = f\"\"\"Generate a story opening (2-3 sentences) that introduces: {constraints}
Give me one creative opening.\"\"\"

    openings = generate_thoughts(opening_prompt, num_thoughts=3)
    opening_scores = [
        evaluate_thought(opening, "creativity and inclusion of required elements: robot, garden, secret")
        for opening in openings
    ]

    best_opening_idx = opening_scores.index(max(opening_scores))
    best_opening = openings[best_opening_idx]

    # Step 2: Generate and evaluate conflicts
    conflict_prompt = f\"\"\"Given this story opening: '{best_opening}'
Generate a conflict or middle section (2-3 sentences) that develops the plot.\"\"\"

    conflicts = generate_thoughts(conflict_prompt, num_thoughts=3)
    conflict_scores = [
        evaluate_thought(conflict, "plot development and tension")
        for conflict in conflicts
    ]

    best_conflict_idx = conflict_scores.index(max(conflict_scores))
    best_conflict = conflicts[best_conflict_idx]

    # Step 3: Generate and evaluate resolutions
    resolution_prompt = f\"\"\"Given this story so far:
Opening: {best_opening}
Conflict: {best_conflict}

Generate a satisfying resolution (2-3 sentences).\"\"\"

    resolutions = generate_thoughts(resolution_prompt, num_thoughts=3)
    resolution_scores = [
        evaluate_thought(resolution, "satisfying conclusion and coherence")
        for resolution in resolutions
    ]

    best_resolution_idx = resolution_scores.index(max(resolution_scores))
    best_resolution = resolutions[best_resolution_idx]

    # Combine final story
    final_story = f"{best_opening}\\n\\n{best_conflict}\\n\\n{best_resolution}"

    return {
        "story": final_story,
        "constraints": constraints,
        "thoughts_generated": 9,
        "stages": 3
    }

if __name__ == "__main__":
    result = tree_of_thoughts_story()
    print(f"Required elements: {result['constraints']}")
    print(f"\\nThoughts generated: {result['thoughts_generated']} across {result['stages']} stages")
    print(f"\\nFinal Story:\\n{result['story']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:story", "description": "Should return a complete story"},
        {"input": "", "expected_output": "contains:thoughts_generated", "description": "Should show number of thoughts generated"},
        {"input": "", "expected_output": "contains:stages", "description": "Should show number of stages"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
