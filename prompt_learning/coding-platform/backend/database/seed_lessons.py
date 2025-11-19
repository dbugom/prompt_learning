"""
Seed script to populate the database with sample Python lessons
Run this after the application is deployed
"""

import asyncio
import sys
from sqlalchemy import select
from database.connection import AsyncSessionLocal, init_db
from models.lesson import Lesson
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample lessons data
SAMPLE_LESSONS = [
    {
        "title": "Hello World and Variables",
        "slug": "hello-world-variables",
        "description": "Learn Python basics with your first program and variables",
        "difficulty": "beginner",
        "order": 1,
        "language": "python",
        "estimated_time": 15,
        "tags": ["basics", "variables", "print"],
        "content": """# Hello World and Variables

Welcome to your first Python lesson! In this lesson, you'll learn:
- How to print output
- What variables are
- Basic data types

## Printing Output

In Python, you can display text using the `print()` function:

```python
print("Hello, World!")
```

## Variables

Variables are containers for storing data. You can create a variable by giving it a name and a value:

```python
name = "Alice"
age = 25
```

## Your Task

Create three variables:
1. `name` - your name (string)
2. `age` - your age (number)
3. `greeting` - a greeting message that includes your name

Then print the greeting message.

**Example Output:**
```
Hello, my name is Alice and I am 25 years old!
```
""",
        "starter_code": """# Create your variables here
name = "Your Name"
age = 0
greeting = ""

# Print your greeting
print(greeting)
""",
        "solution_code": """name = "Alice"
age = 25
greeting = f"Hello, my name is {name} and I am {age} years old!"
print(greeting)
""",
        "test_cases": [
            {
                "input": "",
                "expected_output": "Hello, my name is Alice and I am 25 years old!",
                "description": "Print greeting message with name and age"
            }
        ]
    },
    {
        "title": "Functions and Control Flow",
        "slug": "functions-control-flow",
        "description": "Master functions and conditional statements in Python",
        "difficulty": "beginner",
        "order": 2,
        "language": "python",
        "estimated_time": 25,
        "tags": ["functions", "if-else", "control-flow"],
        "content": """# Functions and Control Flow

In this lesson, you'll learn:
- How to create and use functions
- Conditional statements (if/else)
- How to make decisions in your code

## Functions

Functions are reusable blocks of code. You define them with `def`:

```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")
print(result)  # Output: Hello, Alice!
```

## Conditional Statements

Use `if`, `elif`, and `else` to make decisions:

```python
age = 18
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

## Your Task

Create a function called `check_number(n)` that:
- Takes a number as input
- Returns "Positive" if the number is greater than 0
- Returns "Negative" if the number is less than 0
- Returns "Zero" if the number is exactly 0

**Example:**
```python
print(check_number(5))   # Output: Positive
print(check_number(-3))  # Output: Negative
print(check_number(0))   # Output: Zero
```
""",
        "starter_code": """def check_number(n):
    # Write your code here
    pass

# Test your function
print(check_number(5))
print(check_number(-3))
print(check_number(0))
""",
        "solution_code": """def check_number(n):
    if n > 0:
        return "Positive"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"

print(check_number(5))
print(check_number(-3))
print(check_number(0))
""",
        "test_cases": [
            {
                "input": "",
                "expected_output": "Positive\nNegative\nZero",
                "description": "Check positive, negative, and zero numbers"
            }
        ]
    },
    {
        "title": "Working with Lists",
        "slug": "working-with-lists",
        "description": "Learn to manipulate and iterate through Python lists",
        "difficulty": "beginner",
        "order": 3,
        "language": "python",
        "estimated_time": 30,
        "tags": ["lists", "loops", "data-structures"],
        "content": """# Working with Lists

In this lesson, you'll learn:
- What lists are and how to use them
- How to add and remove items
- How to loop through lists
- Common list operations

## Creating Lists

Lists are ordered collections of items:

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
```

## Accessing List Items

Use index numbers to access items (starting from 0):

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])  # Output: apple
print(fruits[1])  # Output: banana
```

## Looping Through Lists

Use a `for` loop to iterate through items:

```python
for fruit in fruits:
    print(fruit)
```

## List Operations

Common operations:
- `append()` - add item to end
- `len()` - get length
- `sum()` - sum all numbers

## Your Task

Create a function called `process_numbers(numbers)` that:
- Takes a list of numbers as input
- Returns the sum of all numbers in the list
- Should work with any list of numbers

**Example:**
```python
print(process_numbers([1, 2, 3, 4, 5]))  # Output: 15
print(process_numbers([10, 20, 30]))     # Output: 60
```
""",
        "starter_code": """def process_numbers(numbers):
    # Write your code here
    pass

# Test your function
print(process_numbers([1, 2, 3, 4, 5]))
print(process_numbers([10, 20, 30]))
""",
        "solution_code": """def process_numbers(numbers):
    total = sum(numbers)
    return total

print(process_numbers([1, 2, 3, 4, 5]))
print(process_numbers([10, 20, 30]))
""",
        "test_cases": [
            {
                "input": "",
                "expected_output": "15\n60",
                "description": "Sum lists of numbers"
            }
        ]
    },
    {
        "title": "String Manipulation",
        "slug": "string-manipulation",
        "description": "Master string operations and formatting in Python",
        "difficulty": "intermediate",
        "order": 4,
        "language": "python",
        "estimated_time": 30,
        "tags": ["strings", "text-processing"],
        "content": """# String Manipulation

In this lesson, you'll learn:
- String methods and operations
- String formatting
- Working with text data

## String Methods

Python strings have many useful methods:

```python
text = "Hello World"
print(text.upper())      # HELLO WORLD
print(text.lower())      # hello world
print(text.replace("World", "Python"))  # Hello Python
```

## Your Task

Create a function called `format_name(first, last)` that:
- Takes first name and last name as inputs
- Returns the full name in format: "Last, First"
- Both names should be capitalized

**Example:**
```python
print(format_name("john", "doe"))  # Output: Doe, John
```
""",
        "starter_code": """def format_name(first, last):
    # Write your code here
    pass

print(format_name("john", "doe"))
""",
        "solution_code": """def format_name(first, last):
    return f"{last.capitalize()}, {first.capitalize()}"

print(format_name("john", "doe"))
""",
        "test_cases": [
            {
                "input": "",
                "expected_output": "Doe, John",
                "description": "Format name correctly"
            }
        ]
    },
    {
        "title": "Dictionaries and Data Structures",
        "slug": "dictionaries-data-structures",
        "description": "Learn to work with dictionaries and nested data structures",
        "difficulty": "intermediate",
        "order": 5,
        "language": "python",
        "estimated_time": 35,
        "tags": ["dictionaries", "data-structures"],
        "content": """# Dictionaries and Data Structures

In this lesson, you'll learn:
- What dictionaries are
- How to access and modify dictionary data
- Working with nested structures

## Dictionaries

Dictionaries store key-value pairs:

```python
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

print(person["name"])  # Output: Alice
```

## Your Task

Create a function called `get_student_info(student)` that:
- Takes a dictionary with student data
- Returns a formatted string with their info

**Example:**
```python
student = {"name": "Alice", "grade": "A", "age": 20}
print(get_student_info(student))
# Output: Alice (age 20) - Grade: A
```
""",
        "starter_code": """def get_student_info(student):
    # Write your code here
    pass

student = {"name": "Alice", "grade": "A", "age": 20}
print(get_student_info(student))
""",
        "solution_code": """def get_student_info(student):
    return f"{student['name']} (age {student['age']}) - Grade: {student['grade']}"

student = {"name": "Alice", "grade": "A", "age": 20}
print(get_student_info(student))
""",
        "test_cases": [
            {
                "input": "",
                "expected_output": "Alice (age 20) - Grade: A",
                "description": "Format student info"
            }
        ]
    }
]

async def create_admin_user(session):
    """Create an admin user if not exists"""
    result = await session.execute(
        select(User).where(User.username == "admin")
    )
    admin = result.scalar_one_or_none()

    if not admin:
        admin = User(
            email="admin@example.com",
            username="admin",
            hashed_password=pwd_context.hash("admin123"),
            full_name="Administrator",
            is_admin=True
        )
        session.add(admin)
        await session.commit()
        print("✓ Admin user created (username: admin, password: admin123)")
    else:
        print("✓ Admin user already exists")

    return admin

async def seed_lessons():
    """Seed the database with sample lessons"""
    print("Initializing database...")
    await init_db()

    async with AsyncSessionLocal() as session:
        # Create admin user
        await create_admin_user(session)

        # Check if lessons already exist
        result = await session.execute(select(Lesson))
        existing_lessons = result.scalars().all()

        if existing_lessons:
            print(f"✓ Database already contains {len(existing_lessons)} lessons")
            print("Skipping lesson creation...")
            return

        # Create sample lessons
        print(f"\nCreating {len(SAMPLE_LESSONS)} sample lessons...")

        for lesson_data in SAMPLE_LESSONS:
            lesson = Lesson(**lesson_data)
            session.add(lesson)
            print(f"  ✓ Created: {lesson_data['title']}")

        await session.commit()

        print(f"\n✓ Successfully created {len(SAMPLE_LESSONS)} lessons!")
        print("\nYou can now access the platform and start learning!")

if __name__ == "__main__":
    try:
        asyncio.run(seed_lessons())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
