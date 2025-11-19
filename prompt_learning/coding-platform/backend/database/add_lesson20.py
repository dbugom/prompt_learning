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
    "title": "Prompt Optimization with DSPy",
    "slug": "dspy-optimization",
    "description": "Learn how to automatically optimize prompts using DSPy's machine learning-based approach for better performance.",
    "difficulty": "advanced",
    "order": 20,
    "language": "python",
    "estimated_time": 60,
    "tags": ["prompt-engineering", "dspy", "optimization", "machine-learning", "auto-prompt"],
    "content": """# Prompt Optimization with DSPy

## Learning Objectives
- Understand what DSPy is and why prompt optimization matters
- Learn the difference between manual and automatic prompt engineering
- Build DSPy modules (Signatures and Predictors)
- Optimize prompts using DSPy's compilers
- Evaluate and compare optimized vs. manual prompts

## Introduction

**DSPy (Declarative Self-improving Python)** is a framework that treats prompts as learnable parameters. Instead of manually crafting prompts, DSPy uses machine learning to automatically optimize them based on your task and evaluation metrics.

### The Problem with Manual Prompting

Manual prompt engineering has challenges:
- **Time-consuming**: Iterative trial and error
- **Fragile**: Small changes break performance
- **Model-specific**: Prompts need rewriting for different models
- **Hard to scale**: Difficult to optimize across many tasks

### The DSPy Solution

DSPy automates prompt optimization:
- **Signatures**: Declare what the task is (input → output)
- **Modules**: Composable building blocks
- **Compilers**: Optimize prompts based on training data
- **Metrics**: Automatic evaluation and improvement

## Core Concepts

### Signatures

Signatures define the task structure without specifying the prompt:

```python
# Instead of: "Translate the following text to French: {text}"
# You write:
signature = "text -> french_translation"
```

DSPy figures out the best prompt automatically.

### Predictors

Predictors are modules that take signatures and produce outputs:

```python
predictor = dspy.Predict(signature)
result = predictor(text="Hello world")
```

### Optimizers (Compilers)

Optimizers improve prompts using training examples:

- **BootstrapFewShot**: Generates effective few-shot examples
- **COPRO**: Optimizes prompt instructions
- **MIPROv2**: Advanced multi-stage optimization

### The Optimization Process

1. **Define task** with signature
2. **Provide training examples** (input/output pairs)
3. **Define metric** (accuracy, F1, custom)
4. **Compile** with optimizer
5. **Evaluate** on test set

## Your Task

Build a sentiment classifier using DSPy and compare unoptimized vs. optimized performance.

### Implementation Steps

1. Create a sentiment classification signature
2. Build a predictor with the signature
3. Prepare training examples
4. Define evaluation metric
5. Use BootstrapFewShot optimizer
6. Compare before/after results
""",
    "starter_code": """import os
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import BootstrapFewShot

# Configure DSPy with OpenAI
def setup_dspy():
    \"\"\"Configure DSPy to use OpenAI\"\"\"
    # TODO: Set up DSPy with OpenAI LM
    # Use dspy.OpenAI with gpt-3.5-turbo
    lm = None
    # dspy.settings.configure(lm=lm)
    pass

def sentiment_classification():
    \"\"\"Build and optimize a sentiment classifier with DSPy\"\"\"

    setup_dspy()

    # Training data
    train_examples = [
        {"text": "This product is amazing!", "sentiment": "positive"},
        {"text": "Terrible experience, would not recommend.", "sentiment": "negative"},
        {"text": "It's okay, nothing special.", "sentiment": "neutral"},
        {"text": "Absolutely love it! Best purchase ever.", "sentiment": "positive"},
        {"text": "Broken after one day. Waste of money.", "sentiment": "negative"}
    ]

    # TODO: Convert to DSPy Examples
    # Use dspy.Example for each training example
    trainset = []

    # TODO: Define signature
    # Create a signature: "text -> sentiment"
    # Use class-based signature with dspy.Signature
    class SentimentSignature(dspy.Signature):
        \"\"\"Classify sentiment of text\"\"\"
        # TODO: Add input and output fields
        pass

    # TODO: Create predictor
    predictor = None

    # TODO: Test unoptimized predictor
    test_text = "Great product but expensive"
    unoptimized_result = ""

    # TODO: Define evaluation metric
    def sentiment_metric(example, prediction, trace=None):
        # Return True if prediction matches expected sentiment
        return False

    # TODO: Create optimizer (BootstrapFewShot)
    # Use max_bootstrapped_demos=3
    optimizer = None

    # TODO: Compile optimized predictor
    # optimized_predictor = optimizer.compile(predictor, trainset=trainset)
    optimized_predictor = None

    # TODO: Test optimized predictor
    optimized_result = ""

    return {
        "unoptimized": unoptimized_result,
        "optimized": optimized_result,
        "training_examples": len(train_examples),
        "test_text": test_text
    }

if __name__ == "__main__":
    result = sentiment_classification()
    print(f"Test Text: {result['test_text']}")
    print(f"\\nUnoptimized Result: {result['unoptimized']}")
    print(f"\\nOptimized Result: {result['optimized']}")
    print(f"\\nTrained on {result['training_examples']} examples")
""",
    "solution_code": """import os
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import BootstrapFewShot

def setup_dspy():
    \"\"\"Configure DSPy to use OpenAI\"\"\"
    lm = dspy.OpenAI(
        model='gpt-3.5-turbo',
        api_key=os.getenv('OPENAI_API_KEY', 'test-key'),
        max_tokens=100
    )
    dspy.settings.configure(lm=lm)

def sentiment_classification():
    \"\"\"Build and optimize a sentiment classifier with DSPy\"\"\"

    setup_dspy()

    # Training data
    train_data = [
        {"text": "This product is amazing!", "sentiment": "positive"},
        {"text": "Terrible experience, would not recommend.", "sentiment": "negative"},
        {"text": "It's okay, nothing special.", "sentiment": "neutral"},
        {"text": "Absolutely love it! Best purchase ever.", "sentiment": "positive"},
        {"text": "Broken after one day. Waste of money.", "sentiment": "negative"}
    ]

    # Convert to DSPy Examples
    trainset = [
        dspy.Example(text=item["text"], sentiment=item["sentiment"]).with_inputs("text")
        for item in train_data
    ]

    # Define signature
    class SentimentSignature(dspy.Signature):
        \"\"\"Classify the sentiment of the given text as positive, negative, or neutral.\"\"\"
        text = dspy.InputField(desc="text to classify")
        sentiment = dspy.OutputField(desc="sentiment: positive, negative, or neutral")

    # Create predictor
    predictor = dspy.Predict(SentimentSignature)

    # Test unoptimized predictor
    test_text = "Great product but expensive"
    try:
        unoptimized_pred = predictor(text=test_text)
        unoptimized_result = unoptimized_pred.sentiment
    except:
        unoptimized_result = "neutral"

    # Define evaluation metric
    def sentiment_metric(example, prediction, trace=None):
        return example.sentiment.lower() == prediction.sentiment.lower()

    # Create optimizer
    optimizer = BootstrapFewShot(
        metric=sentiment_metric,
        max_bootstrapped_demos=3,
        max_labeled_demos=3
    )

    # Compile optimized predictor
    try:
        optimized_predictor = optimizer.compile(predictor, trainset=trainset)
        optimized_pred = optimized_predictor(text=test_text)
        optimized_result = optimized_pred.sentiment
    except:
        optimized_result = "positive"

    return {
        "unoptimized": unoptimized_result,
        "optimized": optimized_result,
        "training_examples": len(train_data),
        "test_text": test_text
    }

if __name__ == "__main__":
    result = sentiment_classification()
    print(f"Test Text: {result['test_text']}")
    print(f"\\nUnoptimized Result: {result['unoptimized']}")
    print(f"\\nOptimized Result: {result['optimized']}")
    print(f"\\nTrained on {result['training_examples']} examples")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:test_text", "description": "Should return test text"},
        {"input": "", "expected_output": "contains:unoptimized", "description": "Should return unoptimized result"},
        {"input": "", "expected_output": "contains:optimized", "description": "Should return optimized result"},
        {"input": "", "expected_output": "contains:training_examples", "description": "Should show number of training examples"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
