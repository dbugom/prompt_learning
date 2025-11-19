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
    "title": "Retrieval-Augmented Generation (RAG)",
    "slug": "rag-basics",
    "description": "Learn how to combine document retrieval with LLMs to create AI systems that answer questions using your own data.",
    "difficulty": "advanced",
    "order": 18,
    "language": "python",
    "estimated_time": 60,
    "tags": ["prompt-engineering", "rag", "embeddings", "vector-db", "langchain"],
    "content": """# Retrieval-Augmented Generation (RAG)

## Learning Objectives
- Understand the RAG architecture and why it's essential
- Learn about embeddings and semantic search
- Build a simple document Q&A system
- Implement vector-based retrieval with LangChain

## Introduction

**Retrieval-Augmented Generation (RAG)** is a technique that enhances LLM responses by retrieving relevant information from a knowledge base before generating answers.

### Why RAG?

LLMs have limitations:
- **Knowledge cutoff**: No information after training date
- **Hallucinations**: May fabricate plausible-sounding answers
- **No access to private data**: Can't answer questions about your documents

RAG solves these problems by:
1. **Retrieving** relevant documents based on the query
2. **Augmenting** the prompt with retrieved context
3. **Generating** an answer grounded in actual data

## Core Concepts

### The RAG Pipeline

1. **Document Ingestion**
   - Split documents into chunks
   - Convert chunks to embeddings (vector representations)
   - Store in vector database

2. **Query Processing**
   - Convert user question to embedding
   - Find most similar document chunks (semantic search)
   - Retrieve top-k relevant chunks

3. **Answer Generation**
   - Combine retrieved chunks with user question
   - Send to LLM with instruction to answer based on context
   - Generate grounded, factual response

### Embeddings

Embeddings are numerical representations of text that capture semantic meaning. Similar concepts have similar embeddings, enabling semantic search.

### Vector Databases

Store embeddings for efficient similarity search:
- **Chroma**: Lightweight, open-source
- **Pinecone**: Managed, scalable
- **Weaviate**: Production-ready
- **FAISS**: Facebook's similarity search library

## Your Task

Build a simple RAG system that answers questions about provided documents using LangChain and Chroma.

### Implementation Tips

1. **Chunk size matters**: 500-1000 characters is typical
2. **Overlap chunks**: Prevents losing context at boundaries
3. **Retrieve enough context**: 3-5 chunks usually sufficient
4. **Cite sources**: Include which documents were used
""",
    "starter_code": """import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

def build_rag_system():
    \"\"\"Build a simple RAG system for document Q&A\"\"\"

    # Sample documents about prompt engineering
    documents = [
        "Prompt engineering is the process of designing effective prompts for LLMs. It involves understanding model capabilities, crafting clear instructions, and iterating based on outputs.",
        "Few-shot learning allows LLMs to learn from examples in the prompt. By providing 2-5 examples, you can teach the model new patterns without fine-tuning.",
        "Chain-of-thought prompting improves reasoning by asking the LLM to think step-by-step. This technique is especially effective for math and logic problems.",
        "Temperature controls randomness in LLM outputs. Low temperature (0.1-0.3) gives deterministic results, while high temperature (0.7-1.0) increases creativity.",
        "RAG systems combine retrieval with generation. They find relevant documents, then use them as context for the LLM to generate accurate answers."
    ]

    # TODO: Create Document objects
    docs = []

    # TODO: Split documents into chunks (use RecursiveCharacterTextSplitter)
    # Recommended: chunk_size=200, chunk_overlap=50
    text_splitter = None
    chunks = []

    # TODO: Create embeddings and vector store
    # Use OpenAIEmbeddings and Chroma
    embeddings = None
    vectorstore = None

    # TODO: Create RetrievalQA chain
    # Use ChatOpenAI with temperature=0 for consistency
    llm = None
    qa_chain = None

    # Test the system
    question = "What is few-shot learning?"

    try:
        # TODO: Get answer using qa_chain
        result = None

        return {
            "question": question,
            "answer": result.get("result", "") if result else "",
            "num_documents": len(documents),
            "num_chunks": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = build_rag_system()
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Question: {result['question']}")
        print(f"\\nAnswer: {result['answer']}")
        print(f"\\nProcessed {result['num_documents']} documents into {result['num_chunks']} chunks")
""",
    "solution_code": """import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

def build_rag_system():
    \"\"\"Build a simple RAG system for document Q&A\"\"\"

    # Sample documents about prompt engineering
    documents = [
        "Prompt engineering is the process of designing effective prompts for LLMs. It involves understanding model capabilities, crafting clear instructions, and iterating based on outputs.",
        "Few-shot learning allows LLMs to learn from examples in the prompt. By providing 2-5 examples, you can teach the model new patterns without fine-tuning.",
        "Chain-of-thought prompting improves reasoning by asking the LLM to think step-by-step. This technique is especially effective for math and logic problems.",
        "Temperature controls randomness in LLM outputs. Low temperature (0.1-0.3) gives deterministic results, while high temperature (0.7-1.0) increases creativity.",
        "RAG systems combine retrieval with generation. They find relevant documents, then use them as context for the LLM to generate accurate answers."
    ]

    # Create Document objects
    docs = [Document(page_content=doc) for doc in documents]

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_documents(docs)

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="prompt_engineering_docs"
    )

    # Create RetrievalQA chain
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv('OPENAI_API_KEY', 'test-key')
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=False
    )

    # Test the system
    question = "What is few-shot learning?"

    try:
        result = qa_chain.invoke({"query": question})

        return {
            "question": question,
            "answer": result.get("result", ""),
            "num_documents": len(documents),
            "num_chunks": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = build_rag_system()
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Question: {result['question']}")
        print(f"\\nAnswer: {result['answer']}")
        print(f"\\nProcessed {result['num_documents']} documents into {result['num_chunks']} chunks")
""",
    "test_cases": [
        {"input": "", "expected_output": "contains:question", "description": "Should return the question"},
        {"input": "", "expected_output": "contains:answer", "description": "Should return an answer"},
        {"input": "", "expected_output": "contains:num_chunks", "description": "Should process documents into chunks"}
    ]
}

if __name__ == "__main__":
    asyncio.run(add_lesson(NEW_LESSON))
