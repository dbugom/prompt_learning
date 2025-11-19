# Prompt Engineering Learning Platform - Project Progress

**Last Updated:** 2025-11-19 (ALL LESSONS COMPLETE - 22/22)
**Repository:** https://github.com/dbugom/prompt_learning
**Purpose:** Transform the coding education platform into a Prompt Engineering teaching platform

---

## Project Vision

Transform this interactive coding platform from teaching Python programming to teaching **Prompt Engineering**. Students will learn how to craft effective prompts, interact with LLMs, and build LLM-powered applications using Python.

---

## Current Status

### Completed

1. **Git Repository Setup**
   - Initialized git repository in `/Users/mohammadrazavi/claude_project/Prompt_engineering`
   - Resolved embedded git repository issue (removed `.git` from `prompt_learning/`)
   - Connected to GitHub: `https://github.com/dbugom/prompt_learning.git`
   - Successfully pushed initial codebase
   - All updates committed and pushed regularly

2. **Prompt Engineering Libraries Installation**
   - Added comprehensive LLM and prompt engineering libraries to `backend/requirements.txt`
   - **Core LLM SDKs:**
     - `openai>=1.54.0` - OpenAI API (GPT-4, GPT-3.5)
     - `anthropic>=0.39.0` - Anthropic API (Claude)
     - `google-generativeai>=0.8.3` - Google Gemini API

   - **Frameworks:**
     - `langchain>=0.3.7` - LLM application framework
     - `langchain-openai>=0.2.9` - LangChain + OpenAI integration
     - `langchain-anthropic>=0.3.3` - LangChain + Anthropic integration
     - `langchain-community>=0.3.5` - Community integrations
     - `langchain-core>=0.3.15` - Core LangChain components
     - `llama-index>=0.12.0` - Data framework for LLMs
     - `guidance>=0.1.16` - Microsoft's prompt engineering library
     - `dspy-ai>=2.5.36` - Prompt optimization framework

   - **Utilities:**
     - `tiktoken>=0.8.0` - Token counting for OpenAI
     - `prompttools>=0.4.0` - Testing and experimentation
     - `tenacity>=9.0.0` - Retry logic for API calls

3. **Lesson Management Tools**
   - Created `backend/database/add_lesson.py` script for easy lesson addition
   - Script includes:
     - Duplicate checking (prevents slug conflicts)
     - Example prompt engineering lesson template
     - Simple command-line execution
   - Usage: `cd prompt_learning/coding-platform/backend && python -m database.add_lesson`

4. **Curriculum Design - COMPLETED**
   - Finalized comprehensive 22-lesson curriculum across 3 difficulty levels
   - **Module 1 (Beginner)**: 7 lessons - LLM basics, prompt fundamentals
   - **Module 2 (Intermediate)**: 7 lessons - Advanced techniques, LangChain
   - **Module 3 (Advanced)**: 8 lessons - Specialized patterns, production deployment

5. **First 4 Lessons Created and Deployed**

   **Lesson 1: Introduction to LLMs and Prompt Engineering**
   - Slug: `intro-to-llms`
   - Topics: LLM basics, tokens, temperature, max_tokens, model selection
   - Starter code: Simple `ask_llm()` function using OpenAI API
   - File: `backend/database/add_lesson.py`

   **Lesson 2: Writing Clear and Specific Instructions**
   - Slug: `clear-instructions`
   - Topics: Vague vs specific prompts, 6 elements of effective prompts
   - Starter code: Comparison function demonstrating quality differences
   - File: `backend/database/add_lesson_lesson2.py`

   **Lesson 3: Role Prompting and System Messages**
   - Slug: `role-prompting`
   - Topics: System/user/assistant roles, persona techniques
   - Starter code: Three specialist assistants (code explainer, security auditor, performance optimizer)
   - File: `backend/database/add_lesson3.py`

   **Lesson 4: Few-Shot Learning with Examples**
   - Slug: `few-shot-learning`
   - Topics: Zero-shot, one-shot, few-shot paradigms, in-context learning
   - Starter code: Sentiment classifier comparing zero-shot vs few-shot
   - File: `backend/database/add_lesson4.py`

6. **Database Cleanup**
   - Removed 5 old Python programming lessons from database
   - SQL: `DELETE FROM lessons WHERE slug IN ('hello-world', 'variables-types', 'lists-loops', 'functions', 'classes-oop');`

7. **Lesson Generation Progress - 22/22 COMPLETED** (100%) ✓

   **Module 1 (Beginner): 7/7 ✓ COMPLETE**
   - Lesson 1-7: All beginner lessons completed and deployed

   **Module 2 (Intermediate): 7/7 ✓ COMPLETE**
   - Lesson 8-14: All intermediate lessons completed and deployed

   **Module 3 (Advanced): 8/8 ✓ COMPLETE**
   - ✓ Lesson 15: ReAct Pattern
   - ✓ Lesson 16: Function Calling and Tool Use
   - ✓ Lesson 17: LangChain Agents
   - ✓ Lesson 18: Retrieval-Augmented Generation (RAG)
   - ✓ Lesson 19: Advanced LangChain Patterns
   - ✓ Lesson 20: Prompt Optimization with DSPy
   - ✓ Lesson 21: Tree of Thoughts
   - ✓ Lesson 22: Production Best Practices and Deployment

### Completed - All Lessons Generated! ✓

All 22 lessons have been successfully created and are ready for deployment.

### Pending (Optional Enhancements)

- Configure environment variables for LLM API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
- Test lesson flow end-to-end with actual students
- Deploy lessons to database (run add_lesson scripts)
- Update deployment documentation to reflect Prompt Engineering focus
- Consider frontend modifications for better prompt testing experience

---

## Platform Architecture

### Current Platform (Prompt Engineering Education)
The platform is a full-stack interactive prompt engineering education system:

**Frontend:**
- Next.js 14 with React
- CodeMirror 6 for code editing (Python + LLM API code)
- Real-time code execution feedback
- Progress tracking UI
- Auto-save functionality
- Keyboard shortcuts (Cmd/Ctrl+Enter to run, Shift+Alt+F to format)
- WCAG 2.1 AA accessibility compliance

**Backend:**
- FastAPI (Python)
- PostgreSQL for data persistence
- Redis for caching
- Celery for async tasks
- Piston for secure code execution (runs Python with LLM API calls)

**Features:**
- JWT authentication
- RESTful API with OpenAPI docs
- Docker-based deployment
- Secure sandboxed code execution
- Format button (whitespace cleanup)

### Key Files & Locations

```
prompt_learning/coding-platform/
├── backend/
│   ├── requirements.txt           # Updated with prompt engineering libs
│   ├── database/
│   │   ├── seed_lessons.py        # Seeds initial lessons (deprecated)
│   │   ├── add_lesson.py          # Lesson 1
│   │   ├── add_lesson_lesson2.py  # Lesson 2
│   │   ├── add_lesson3.py         # Lesson 3
│   │   ├── add_lesson4.py         # Lesson 4
│   │   ├── add_lesson5-17.py      # Lessons 5-17 (completed)
│   │   ├── add_lesson18.py        # Lesson 18: RAG
│   │   ├── add_lesson19.py        # Lesson 19: Advanced LangChain
│   │   ├── add_lesson20.py        # Lesson 20: DSPy Optimization
│   │   ├── add_lesson21.py        # Lesson 21: Tree of Thoughts
│   │   ├── add_lesson22.py        # Lesson 22: Production Best Practices
│   │   ├── connection.py          # Database connection
│   │   └── init.sql               # Database initialization
│   ├── models/
│   │   └── lesson.py              # Lesson database model
│   ├── api/
│   │   ├── lessons.py             # Lesson CRUD endpoints
│   │   ├── auth.py                # Authentication
│   │   ├── code_execution.py      # Code execution (works with LLM APIs)
│   │   └── progress.py            # Progress tracking
│   └── main.py                     # FastAPI entry point
├── frontend/
│   ├── pages/
│   │   ├── lessons/
│   │   │   ├── index.js           # Lesson list
│   │   │   └── [slug].js          # Individual lesson page
│   │   ├── login.js
│   │   └── register.js
│   └── components/
│       ├── CodeEditor.js           # CodeMirror editor
│       └── OutputConsole.js        # Display execution results
├── docker-compose.yml              # Service orchestration
├── README.md                       # Main documentation (to be updated)
└── CLAUDE.md                       # This file - session context
```

---

## Lesson Structure

Each lesson in the database has the following schema:

```python
{
    "title": str,                    # Lesson title
    "slug": str,                     # URL-friendly unique identifier
    "description": str,              # Brief description
    "difficulty": str,               # "beginner", "intermediate", "advanced"
    "order": int,                    # Display order
    "language": str,                 # "python" (kept for compatibility)
    "estimated_time": int,           # Minutes
    "tags": List[str],              # Categorization tags
    "content": str,                  # Markdown lesson content
    "starter_code": str,             # Initial code template
    "solution_code": str,            # Model solution (hidden from students)
    "test_cases": List[Dict],       # Validation test cases
    "is_published": bool             # Visibility flag (defaults True)
}
```

### How to Add Lessons

**Method 1: Individual Script (CURRENT METHOD)**
1. Create a new file: `backend/database/add_lesson_N.py` (where N is lesson number)
2. Copy structure from existing lesson file
3. Modify the `NEW_LESSON` dictionary with lesson content
4. Run: `cd prompt_learning/coding-platform/backend && python -m database.add_lesson_N`
5. Or via Docker: `docker exec -it coding_platform_backend python -m database.add_lesson_N`

**Method 2: API Endpoint (Admin Required)**
- POST request to `/api/lessons`
- Requires admin JWT authentication
- See `backend/api/lessons.py:160-204` for details

**Method 3: Bulk Seeding (Only works on empty DB)**
- Edit `backend/database/seed_lessons.py`
- Add lessons to `SAMPLE_LESSONS` array
- Run: `docker exec -it coding_platform_backend python database/seed_lessons.py`

---

## Full Curriculum (22 Lessons)

### Module 1: Beginner (7 lessons)

1. **Introduction to LLMs and Prompt Engineering** - COMPLETED
   - LLM basics, tokens, temperature, API parameters
   - First API call with OpenAI

2. **Writing Clear and Specific Instructions** - COMPLETED
   - Vague vs specific prompts
   - 6 elements of effective prompts

3. **Role Prompting and System Messages** - COMPLETED
   - System/user/assistant message types
   - Creating personas and specialists

4. **Few-Shot Learning with Examples** - COMPLETED
   - Zero-shot, one-shot, few-shot
   - In-context learning techniques

5. **Prompt Templates and Variables** - COMPLETED
   - Reusable prompt templates
   - Variable substitution
   - String formatting best practices

6. **Output Formatting and Structured Responses** - COMPLETED
   - JSON/XML output formats
   - Delimiter usage
   - Parsing structured LLM responses

7. **Token Management and Cost Optimization** - COMPLETED
   - Token counting with tiktoken
   - Cost calculation
   - Optimization strategies

### Module 2: Intermediate (7 lessons)

8. **Chain-of-Thought Prompting** - COMPLETED
   - Step-by-step reasoning
   - "Let's think step by step"
   - Complex problem solving

9. **Introduction to LangChain** - COMPLETED
   - LangChain basics
   - PromptTemplates
   - LLMChain

10. **Prompt Chaining and Workflows** - COMPLETED
    - Sequential chains
    - SimpleSequentialChain
    - Multi-step workflows

11. **Error Handling and Retries** - COMPLETED
    - Exception handling for APIs
    - Retry logic with tenacity
    - Fallback strategies

12. **Working with Multiple LLM Providers** - COMPLETED
    - OpenAI vs Anthropic vs Google
    - Provider switching
    - Cost/performance tradeoffs

13. **Conversation Memory and Context** - COMPLETED
    - Managing conversation history
    - ConversationBufferMemory
    - Context window management

14. **Prompt Testing and Evaluation** - COMPLETED
    - Unit testing prompts
    - Evaluation metrics
    - A/B testing approaches

### Module 3: Advanced (8 lessons)

15. **ReAct Pattern: Reasoning + Acting** - COMPLETED
    - ReAct framework
    - Thought-Action-Observation loops
    - Tool-using agents

16. **Function Calling and Tool Use** - COMPLETED
    - OpenAI function calling
    - Tool selection
    - Building custom tools

17. **LangChain Agents** - COMPLETED
    - Agent types (ReAct, Plan-and-Execute)
    - Custom agent creation
    - Agent executor patterns

18. **Retrieval-Augmented Generation (RAG)** - COMPLETED
    - Vector databases
    - Embeddings
    - Question answering over documents

19. **Advanced LangChain Patterns** - COMPLETED
    - RouterChain
    - MapReduce
    - RefineChain

20. **Prompt Optimization with DSPy** - COMPLETED
    - DSPy introduction
    - Automatic prompt optimization
    - Evaluation and tuning

21. **Tree of Thoughts** - COMPLETED
    - Multi-path reasoning
    - Self-evaluation
    - Backtracking strategies

22. **Production Best Practices and Deployment** - COMPLETED
    - API key management
    - Rate limiting
    - Monitoring and logging
    - Cost controls

---

## Environment Setup

### Required Environment Variables (For LLM APIs)

Create/update `.env` file in `prompt_learning/coding-platform/`:

```bash
# Existing variables (database, etc.)
# ... keep existing config ...

# LLM API Keys (REQUIRED FOR LESSONS TO WORK)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# LLM Configuration
DEFAULT_LLM_PROVIDER=openai  # or anthropic, google
DEFAULT_MODEL=gpt-3.5-turbo  # or gpt-4, claude-3-sonnet, gemini-pro
MAX_TOKENS=2000
TEMPERATURE=0.7
```

**Note:** Students will need to provide their own API keys or use platform-provided keys (to be implemented)

---

## Quick Start Commands

### Development Setup
```bash
# Navigate to project
cd /Users/mohammadrazavi/claude_project/Prompt_engineering/prompt_learning/coding-platform

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Database Operations
```bash
# Add individual lesson
cd backend
python -m database.add_lesson_N  # where N is lesson number

# Or via Docker
docker exec -it coding_platform_backend python -m database.add_lesson4

# Verify lessons in database
docker exec coding_platform_db psql -U platform_user -d coding_platform -c \
  "SELECT title, slug, difficulty, \"order\", estimated_time FROM lessons ORDER BY \"order\";"

# Backup database
docker exec coding_platform_db pg_dump -U platform_user coding_platform > backup.sql

# Delete specific lesson
docker exec coding_platform_db psql -U platform_user -d coding_platform -c \
  "DELETE FROM lessons WHERE slug = 'lesson-slug';"
```

### Access Points
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **API ReDoc:** http://localhost:8000/redoc

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123` (change in production!)

---

## Next Steps

1. **Deploy Lessons to Database** ✓ Ready
   - Run deployment scripts for lessons 18-22
   - `cd prompt_learning/coding-platform/backend`
   - `python -m database.add_lesson18`
   - `python -m database.add_lesson19`
   - `python -m database.add_lesson20`
   - `python -m database.add_lesson21`
   - `python -m database.add_lesson22`

2. **Environment Configuration**
   - Add OPENAI_API_KEY to .env file
   - Test API connectivity
   - Consider rate limiting for student usage

3. **Testing & Validation**
   - Test each lesson end-to-end
   - Verify code execution works with LLM APIs
   - Check auto-save and format features
   - Validate progress tracking

4. **Optional Frontend Enhancements**
   - Add token counter display
   - Show API cost estimator
   - Add prompt template helpers
   - Improve LLM response formatting

5. **Documentation Updates**
   - Update README.md with Prompt Engineering focus
   - Update deployment guides
   - Create student onboarding guide

---

## Key Decisions Made

1. **Keep Python Execution Environment**
   - Students write Python code that interacts with LLMs
   - Allows teaching both prompting AND programmatic LLM usage
   - More practical for real-world applications
   - Piston engine supports OpenAI/Anthropic SDK calls

2. **Library Selection**
   - Chose comprehensive suite (OpenAI, Anthropic, LangChain, DSPy)
   - Enables teaching multiple approaches and frameworks
   - Industry-standard tools
   - Future-proof curriculum

3. **Lesson Addition Method**
   - Preferred: Individual script files (`add_lesson_N.py`)
   - Allows incremental lesson creation and testing
   - No need to rebuild entire database
   - Easy to version control and review

4. **Curriculum Structure**
   - 22 lessons across 3 modules (Beginner, Intermediate, Advanced)
   - Progressive difficulty with clear learning path
   - Covers fundamentals through production deployment
   - Includes modern frameworks (LangChain, DSPy)

---

## Reference Documentation

### Platform Documentation
- Main README: `prompt_learning/coding-platform/README.md` (to be updated)
- Deployment Guide: `prompt_learning/coding-platform/DEPLOYMENT.md`
- Setup Fixes: `prompt_learning/coding-platform/SETUP_FIXES.md`
- Project Criteria: `prompt_learning/coding-platform/project_criteria.md`
- This Document: `CLAUDE.md` (session context recovery)

### API Documentation
- Interactive Docs: http://localhost:8000/docs (when running)
- ReDoc: http://localhost:8000/redoc (when running)

### External Resources
- OpenAI API: https://platform.openai.com/docs
- Anthropic API: https://docs.anthropic.com
- LangChain: https://python.langchain.com/docs
- Prompt Engineering Guide: https://www.promptingguide.ai/
- DSPy: https://dspy-docs.vercel.app/

---

## Git Information

- **Local Path:** `/Users/mohammadrazavi/claude_project/Prompt_engineering`
- **Remote:** `https://github.com/dbugom/prompt_learning.git`
- **Branch:** `main`
- **Recent Commits:**
  - Initial commit with full codebase
  - Added prompt engineering libraries
  - Created lesson addition scripts
  - Added lessons 1-4
  - Removed old Python lessons
  - Updated CLAUDE.md and README.md

### Common Git Commands
```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Description"

# Push to GitHub
git push origin main

# View history
git log --oneline
git log --oneline -10  # last 10 commits
```

---

## Troubleshooting

### If Context is Lost
1. Read this file: `CLAUDE.md` (you are here!)
2. Check recent git commits: `git log --oneline -10`
3. Review lesson structure: `backend/models/lesson.py`
4. Check installed libraries: `backend/requirements.txt`
5. Verify lessons in database: Use SQL query above

### Common Issues

**Database empty or wrong lessons:**
- Check: `docker exec coding_platform_db psql -U platform_user -d coding_platform -c "SELECT title, slug FROM lessons ORDER BY \"order\";"`
- Re-run lesson scripts if needed

**Services not starting:**
- Check: `docker-compose ps`
- View logs: `docker-compose logs`
- Restart: `docker-compose restart`

**Port conflicts:**
- Ensure 3000, 8000, 5432, 6379 are free
- Check: `lsof -i :3000` / `lsof -i :8000`

**LLM API errors:**
- Verify OPENAI_API_KEY is set in .env
- Check API key validity
- Review rate limits

**Code execution fails:**
- Check Piston is running: `docker-compose ps piston`
- Check Piston health: `curl http://localhost:2000/runtimes`
- Restart: `docker-compose restart piston`

---

## Session Context

**Completed Work:**
- Git repository setup and GitHub connection
- Prompt engineering libraries installation
- Lesson management tools created
- Curriculum designed (22 lessons)
- **ALL 22 LESSONS COMPLETED (100%)** ✓
  - Module 1 (Beginner): 7/7 ✓
  - Module 2 (Intermediate): 7/7 ✓
  - Module 3 (Advanced): 8/8 ✓
- Old Python lessons removed
- Documentation updated (README.md and CLAUDE.md)
- Lesson files created:
  - add_lesson18.py (RAG)
  - add_lesson19.py (Advanced LangChain Patterns)
  - add_lesson20.py (DSPy Optimization)
  - add_lesson21.py (Tree of Thoughts)
  - add_lesson22.py (Production Best Practices)

**Current State:**
- All 22 lesson scripts created and ready for deployment
- Lessons 1-17 already deployed to database
- Lessons 18-22 ready to be added to database
- Last completed: Lesson 22 - Production Best Practices and Deployment
- CLAUDE.md and README.md updated with 100% completion status

**Next Action Required:**
- Deploy lessons 18-22 to database using the add_lesson scripts
- Configure OPENAI_API_KEY in environment (when ready for production)
- Test all lessons end-to-end with actual students

**User Preferences:**
- Lesson addition method: Individual scripts (Option 2)
- Teaching focus: Prompt Engineering (not Python basics)
- Curriculum: 22-lesson comprehensive program

---

*This document should be read at the start of each session to restore context and continue work efficiently.*
- to memorize