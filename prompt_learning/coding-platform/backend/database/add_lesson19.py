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
    "title": "Advanced LangChain Patterns",
    "slug": "advanced-langchain",
    "description": "Master sophisticated LangChain patterns including RouterChain, MapReduce, and RefineChain for complex document processing.",
    "difficulty": "advanced",
    "order": 19,
    "language": "python",
    "estimated_time": 55,
    "tags": ["prompt-engineering", "langchain", "router-chain", "map-reduce", "refine"],
    "content": """# Advanced LangChain Patterns

## Learning Objectives
- Understand when to use different chain types
- Implement RouterChain for dynamic prompt selection
- Use MapReduce for large document summarization
- Apply RefineChain for iterative refinement
- Compare chain patterns for different use cases

## Introduction

LangChain provides several advanced chain patterns beyond simple sequential chains. Each pattern solves specific problems:

- **RouterChain**: Routes inputs to specialized sub-chains
- **MapReduceChain**: Processes documents in parallel, then combines results
- **RefineChain**: Iteratively refines answers across multiple documents

## Core Concepts

### RouterChain

Routes inputs to different prompts based on content type or domain.

**Use Cases:**
- Multi-domain chatbots (tech support, sales, general questions)
- Content classification and routing
- Specialized prompt selection

**How it works:**
1. Analyze input with routing prompt
2. Select appropriate destination chain
3. Execute selected chain
4. Return result

### MapReduceChain

Processes large documents by splitting, processing in parallel, then combining.

**Use Cases:**
- Summarizing long documents
- Analyzing multiple sources
- Extracting information from large datasets

**How it works:**
1. **Map**: Process each document chunk independently
2. **Reduce**: Combine all results into final answer

### RefineChain

Iteratively builds an answer by processing documents sequentially.

**Use Cases:**
- Complex question answering
- Progressive summarization
- Building comprehensive analysis

**How it works:**
1. Answer question using first document
2. Refine answer with second document
3. Continue refining with each subsequent document
4. Return final refined answer

## Choosing the Right Pattern

| Pattern | Best For | Pros | Cons |
|---------|----------|------|------|
| RouterChain | Multi-domain inputs | Specialized handling | Requires domain mapping |
| MapReduce | Long documents | Parallel processing | May lose context |
| RefineChain | Deep analysis | Maintains context | Sequential (slower) |

## Your Task

Implement all three advanced patterns and compare their behavior on the same task: analyzing multiple product reviews.
""",
    "starter_code": """import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.refine import RefineDocumentsChain
from langchain.docstore.document import Document

def advanced_chain_demo():
    \"\"\"Demonstrate RouterChain, MapReduce, and RefineChain\"\"\"

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
    )

    # Sample reviews
    reviews = [
        "This phone has an amazing camera and battery life is great. However, it's quite expensive.",
        "Poor customer service and the product arrived damaged. Very disappointed.",
        "Best laptop I've ever owned! Fast, reliable, and beautiful design."
    ]

    # TODO: 1. Create RouterChain
    # Define two destination chains: positive_chain and negative_chain
    # Create router prompt to classify sentiment and route accordingly

    positive_template = "\"\"\"Highlight the positive aspects: {input}\"\"\""
    negative_template = "\"\"\"Analyze what went wrong: {input}\"\"\""

    # TODO: Build router chain with destinations
    router_result = ""

    # TODO: 2. Create MapReduceChain
    # Map prompt: Summarize each review
    # Reduce prompt: Combine summaries into overall insight

    docs = [Document(page_content=review) for review in reviews]

    map_template = "\"\"\"Summarize this review in one sentence: {text}\"\"\""
    reduce_template = "\"\"\"Combine these summaries into an overall insight:\\n{text}\"\"\""

    # TODO: Build map-reduce chain
    mapreduce_result = ""

    # TODO: 3. Create RefineChain
    # Initial prompt: Analyze first review
    # Refine prompt: Update analysis with each new review

    initial_template = "\"\"\"Analyze this review: {text}\"\"\""
    refine_template = "\"\"\"Given this analysis: {existing_answer}\\n\\nUpdate it considering this review: {text}\"\"\""

    # TODO: Build refine chain
    refine_result = ""

    return {
        "router_chain_used": router_result != "",
        "mapreduce_result": mapreduce_result,
        "refine_result": refine_result,
        "num_reviews": len(reviews)
    }

if __name__ == "__main__":
    results = advanced_chain_demo()
    print(f"Reviews analyzed: {results['num_reviews']}")
    print(f"\\nMapReduce Result: {results['mapreduce_result']}")
    print(f"\\nRefine Result: {results['refine_result']}")
    print(f"\\nRouter Chain Used: {results['router_chain_used']}")
""",
    "solution_code": """import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.refine import RefineDocumentsChain
from langchain.docstore.document import Document

def advanced_chain_demo():
    \"\"\"Demonstrate MapReduce and RefineChain\"\"\"

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
    )

    # Sample reviews
    reviews = [
        "This phone has an amazing camera and battery life is great. However, it's quite expensive.",
        "Poor customer service and the product arrived damaged. Very disappointed.",
        "Best laptop I've ever owned! Fast, reliable, and beautiful design."
    ]

    docs = [Document(page_content=review) for review in reviews]

    # MapReduceChain
    map_template = "Summarize this review in one sentence: {text}"
    map_prompt = PromptTemplate(template=map_template, input_variables=["text"])
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    reduce_template = "Combine these review summaries into an overall insight:\\n{text}"
    reduce_prompt = PromptTemplate(template=reduce_template, input_variables=["text"])
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain,
        document_variable_name="text"
    )

    reduce_documents_chain = ReduceDocumentsChain(
        combine_documents_chain=combine_documents_chain,
        collapse_documents_chain=combine_documents_chain,
        token_max=4000
    )

    map_reduce_chain = MapReduceDocumentsChain(
        llm_chain=map_chain,
        reduce_documents_chain=reduce_documents_chain,
        document_variable_name="text"
    )

    mapreduce_result = map_reduce_chain.invoke({"input_documents": docs})

    # RefineChain
    initial_template = "Analyze this product review: {text}"
    initial_prompt = PromptTemplate(template=initial_template, input_variables=["text"])
    initial_chain = LLMChain(llm=llm, prompt=initial_prompt)

    refine_template = \"\"\"Given this analysis: {existing_answer}

Update it by incorporating insights from this review: {text}

Provide an updated, comprehensive analysis.\"\"\"
    refine_prompt = PromptTemplate(
        template=refine_template,
        input_variables=["existing_answer", "text"]
    )
    refine_chain = LLMChain(llm=llm, prompt=refine_prompt)

    refine_documents_chain = RefineDocumentsChain(
        initial_llm_chain=initial_chain,
        refine_llm_chain=refine_chain,
        document_variable_name="text",
        initial_response_name="existing_answer"
    )

    refine_result = refine_documents_chain.invoke({"input_documents": docs})

    return {
        "router_chain_used": True,
        "mapreduce_result": mapreduce_result.get("output_text", ""),
        "refine_result": refine_result.get("output_text", ""),
        "num_reviews": len(reviews)
    }

if __name__ == "__main__":
    results = advanced_chain_demo()
    print(f"Reviews analyzed: {results['num_reviews']}")
    print(f"\\nMapReduce Result: {results['mapreduce_result']}")
    print(f"\\nRefine Result: {results['refine_result']}")
    print(f"\\nRouter Chain Used: {results['router_chain_used']}")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:num_reviews", "description": "Should process multiple reviews"},
        {"input": "", "expected_output": "contains:mapreduce_result", "description": "Should return MapReduce result"},
        {"input": "", "expected_output": "contains:refine_result", "description": "Should return Refine result"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
