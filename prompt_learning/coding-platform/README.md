# Prompt Engineering Learning Platform

A complete, production-ready interactive **Prompt Engineering** education platform with secure code execution, real-time LLM interaction, and progress tracking. Learn to craft effective prompts, interact with LLMs, and build AI-powered applications through hands-on Python coding exercises.

## Features

### Core Features
- **Interactive Code Editor**: CodeMirror 6 with Python syntax highlighting for LLM API code
- **Secure Code Execution**: Sandboxed execution via Piston engine with resource limits and all LLM libraries installed
- **Real-Time LLM Interaction**: Execute Python code that calls OpenAI, Anthropic, and Google APIs
- **Comprehensive Curriculum**: 22 complete lessons from beginner to advanced prompt engineering
- **Practical Exercises**: 2 hands-on exercises per lesson with hints to reinforce learning
- **Exercise Validation**: Automatic checking of solutions with helpful feedback
- **Progress Tracking**: Track student progress through lessons and exercises with detailed analytics
- **User Authentication**: JWT-based authentication with secure password hashing
- **Responsive Design**: Mobile-friendly UI that works on all devices
- **RESTful API**: Comprehensive API with OpenAPI/Swagger documentation
- **Production Ready**: Docker-based deployment with security hardening

### Enhanced UX Features

#### Accessibility & Inclusivity
- **WCAG 2.1 AA Compliant**: Improved color contrast for better readability
- **Full Keyboard Navigation**: Complete keyboard support with intuitive shortcuts
- **Screen Reader Compatible**: Proper ARIA labels and semantic HTML throughout
- **Focus Management**: Advanced focus trapping in modals and dialogs
- **Reduced Motion Support**: Respects user's motion preferences
- **High Contrast Mode**: Enhanced visibility for users with visual impairments

#### User Experience Enhancements
- **Auto-Save Functionality**: Never lose your work - code is automatically saved to local storage
- **Visual Save Status**: Real-time feedback showing save status (Saving/Saved/Error)
- **Smart Error Messages**: Contextual, helpful error messages with retry mechanisms
- **Loading Skeletons**: Professional loading states that match content structure
- **Session Management**: Automatic session timeout warnings with extension option
- **Password Strength Indicator**: Real-time password strength visualization
- **Show/Hide Password**: Toggle password visibility for easier input
- **Real-Time Form Validation**: Instant feedback on form fields with helpful error messages
- **Code Formatting**: One-click code formatting to clean up spacing and indentation

#### Keyboard Shortcuts
- **⌘/Ctrl + Enter**: Run code and execute tests
- **⌘/Ctrl + R**: Reset code to starter template
- **Shift + Alt + F**: Format code automatically
- **Esc**: Clear output console
- **⌘/Ctrl + /**: Display keyboard shortcuts help

## Tech Stack

### Frontend
- **Next.js 14**: React framework with SSR/SSG
- **CodeMirror 6**: Advanced code editor with Python syntax highlighting
- **Axios**: HTTP client for API communication with centralized error handling
- **React Hot Toast**: Beautiful, accessible notifications

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database for user data and lessons
- **Redis**: Caching and session management
- **Celery**: Asynchronous task queue
- **SQLAlchemy**: ORM for database operations
- **Piston**: Secure code execution engine (Python 3.10.0)

### Prompt Engineering & LLM Libraries

#### Core LLM SDKs
- **openai>=1.54.0**: OpenAI API (GPT-4, GPT-3.5)
- **anthropic>=0.39.0**: Anthropic API (Claude)
- **google-generativeai>=0.8.3**: Google Gemini API

#### Frameworks
- **langchain>=0.3.7**: LLM application framework
- **langchain-openai>=0.2.9**: LangChain + OpenAI integration
- **langchain-anthropic>=0.3.3**: LangChain + Anthropic integration
- **langchain-community>=0.3.5**: Community integrations
- **langchain-core>=0.3.15**: Core LangChain components
- **llama-index>=0.12.0**: Data framework for LLMs
- **guidance>=0.1.16**: Microsoft's prompt engineering library
- **dspy-ai>=2.5.36**: Prompt optimization framework

#### Utilities
- **tiktoken>=0.8.0**: Token counting for OpenAI models
- **prompttools>=0.4.0**: Testing and experimentation
- **tenacity>=9.0.0**: Retry logic for API calls

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **Nginx**: Reverse proxy with SSL/TLS termination
- **Ubuntu 22.04 LTS**: Server operating system
- **Let's Encrypt**: Free SSL certificates

## Curriculum

**Progress: 22 out of 22 lessons completed (100%)** ✓
- Module 1 (Beginner): 7/7 ✓ Complete
- Module 2 (Intermediate): 7/7 ✓ Complete
- Module 3 (Advanced): 8/8 ✓ Complete

### Module 1: Beginner (7 lessons) ✓ COMPLETE

1. **Introduction to LLMs and Prompt Engineering**
   - LLM basics, tokens, temperature, API parameters
   - First API call with OpenAI

2. **Writing Clear and Specific Instructions**
   - Vague vs specific prompts
   - 6 elements of effective prompts

3. **Role Prompting and System Messages**
   - System/user/assistant message types
   - Creating personas and specialists

4. **Few-Shot Learning with Examples**
   - Zero-shot, one-shot, few-shot paradigms
   - In-context learning techniques

5. **Prompt Templates and Variables**
   - Reusable prompt templates
   - Variable substitution

6. **Output Formatting and Structured Responses**
   - JSON/XML output formats
   - Parsing structured LLM responses

7. **Token Management and Cost Optimization**
   - Token counting with tiktoken
   - Cost calculation strategies

### Module 2: Intermediate (7 lessons) ✓ COMPLETE

8. **Chain-of-Thought Prompting**
   - Step-by-step reasoning
   - Complex problem solving

9. **Introduction to LangChain**
   - LangChain basics
   - PromptTemplates and LLMChain

10. **Prompt Chaining and Workflows**
    - Sequential chains
    - Multi-step workflows

11. **Error Handling and Retries**
    - Exception handling for APIs
    - Retry logic with tenacity

12. **Working with Multiple LLM Providers**
    - OpenAI vs Anthropic vs Google
    - Cost/performance tradeoffs

13. **Conversation Memory and Context**
    - Managing conversation history
    - Context window management

14. **Prompt Testing and Evaluation**
    - Unit testing prompts
    - Evaluation metrics

### Module 3: Advanced (8 lessons) ✓ COMPLETE

15. **ReAct Pattern: Reasoning + Acting** ✓
    - ReAct framework
    - Tool-using agents

16. **Function Calling and Tool Use** ✓
    - OpenAI function calling
    - Building custom tools

17. **LangChain Agents** ✓
    - Agent types
    - Custom agent creation

18. **Retrieval-Augmented Generation (RAG)** ✓
    - Vector databases
    - Embeddings and semantic search
    - Question answering over documents

19. **Advanced LangChain Patterns** ✓
    - RouterChain, MapReduce, RefineChain
    - Complex document processing

20. **Prompt Optimization with DSPy** ✓
    - Automatic prompt optimization
    - Evaluation and tuning

21. **Tree of Thoughts** ✓
    - Multi-path reasoning
    - Self-evaluation strategies
    - Search algorithms

22. **Production Best Practices and Deployment** ✓
    - API key management
    - Rate limiting and cost controls
    - Monitoring and logging

## Practical Exercises

Each lesson includes **2 hands-on exercises** to reinforce learning:

### Exercise Features
- **Clear Objectives**: Each exercise has specific learning goals
- **Starter Code**: Template to get students started quickly
- **Hint System**: Short, precise hints available on request
- **Automatic Validation**: Real-time feedback on solutions
- **Progress Tracking**: Must complete exercises to unlock next lesson
- **Solution Access**: Full solutions available with confirmation

### Example Exercises (Lesson 1)
1. **Deterministic Responses**: Control temperature for consistent outputs
2. **Response Length Control**: Use max_tokens to limit response size

### Educational Benefits
- ✓ **Reinforces Concepts**: Practice immediately after learning
- ✓ **Builds Confidence**: Guided practice with hints
- ✓ **Progressive Learning**: Must master basics before advancing
- ✓ **Real-World Skills**: Exercises mirror actual use cases

## System Requirements

### Development
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### Production (Hetzner CX32 or similar)
- 4 vCPUs
- 8GB RAM
- 80GB SSD
- Ubuntu 22.04 LTS
- Public IP address

## Quick Start (Development)

### 1. Clone the Repository

```bash
git clone https://github.com/dbugom/prompt_learning.git
cd prompt_learning/coding-platform
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

**Important:** Add your LLM API keys to `.env`:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Verify Services

```bash
docker-compose ps
```

### 5. Access the Platform

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

### Default Admin Credentials

- **Username**: admin
- **Password**: admin123
- **Change immediately in production!**

## Project Structure

```
coding-platform/
├── docker-compose.yml           # Docker services configuration
├── .env                        # Environment variables
├── CLAUDE.md                   # Session context (for development)
├── frontend/                   # Next.js frontend application
│   ├── pages/                 # Next.js pages
│   │   ├── lessons/
│   │   │   ├── index.js       # Lesson list
│   │   │   └── [slug].js      # Individual lesson page
│   │   ├── login.js
│   │   └── register.js
│   ├── components/            # React components
│   │   ├── CodeEditor.js      # CodeMirror editor
│   │   └── OutputConsole.js   # Execution results
│   ├── styles/               # CSS modules
│   └── utils/                # Utility functions
├── backend/                   # FastAPI backend application
│   ├── main.py               # FastAPI entry point
│   ├── requirements.txt      # Python dependencies (including LLM libs)
│   ├── api/                  # API endpoints
│   │   ├── lessons.py        # Lesson CRUD
│   │   ├── auth.py           # Authentication
│   │   ├── code_execution.py # Code execution
│   │   └── progress.py       # Progress tracking
│   ├── models/               # Database models
│   │   └── lesson.py         # Lesson model
│   ├── database/             # Database configuration
│   │   ├── connection.py     # Database connection
│   │   ├── add_lesson.py     # Lesson 1
│   │   ├── add_lesson_lesson2.py  # Lesson 2
│   │   ├── add_lesson3.py    # Lesson 3
│   │   └── add_lesson4.py    # Lesson 4
│   ├── queue/                # Celery tasks
│   └── tests/                # API tests
├── nginx/                    # Nginx configuration
│   └── nginx.conf           # Reverse proxy config
└── deployment/              # Deployment scripts
    ├── setup.sh            # System setup script
    ├── security-hardening.sh  # Security configuration
    └── hetzner-deploy.sh      # Automated deployment
```

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user info |
| GET | `/api/auth/verify` | Verify token validity |

### Lessons Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/lessons` | Get all lessons |
| GET | `/api/lessons/{id}` | Get lesson by ID |
| GET | `/api/lessons/slug/{slug}` | Get lesson by slug |
| POST | `/api/lessons` | Create lesson (admin) |
| PUT | `/api/lessons/{id}` | Update lesson (admin) |
| DELETE | `/api/lessons/{id}` | Delete lesson (admin) |

### Code Execution Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/code/execute` | Execute Python code (including LLM API calls) |
| GET | `/api/code/runtimes` | Get available runtimes |
| GET | `/api/code/submissions` | Get user submissions |
| GET | `/api/code/submissions/{id}` | Get submission by ID |

### Progress Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/progress/overview` | Get progress overview |
| GET | `/api/progress/lessons` | Get lessons with progress |
| GET | `/api/progress/lesson/{id}` | Get lesson progress |
| POST | `/api/progress/lesson/{id}` | Update lesson progress |
| DELETE | `/api/progress/lesson/{id}` | Reset lesson progress |

## Database Operations

### Add Lessons

```bash
# Add individual lesson via Docker
docker exec -it coding_platform_backend python -m database.add_lesson4

# Or without Docker (from backend directory)
cd backend
python -m database.add_lesson4
```

### Verify Lessons

```bash
# View all lessons
docker exec coding_platform_db psql -U platform_user -d coding_platform -c \
  "SELECT title, slug, difficulty, \"order\", estimated_time FROM lessons ORDER BY \"order\";"
```

### Backup Database

```bash
# Create backup
docker exec coding_platform_db pg_dump -U platform_user coding_platform > backup.sql

# Restore backup
docker exec -i coding_platform_db psql -U platform_user coding_platform < backup.sql
```

## Testing

### Backend Tests

```bash
# Run all tests
docker exec -it coding_platform_backend pytest

# Run with coverage
docker exec -it coding_platform_backend pytest --cov

# Run specific test file
docker exec -it coding_platform_backend pytest tests/test_api.py
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f backend/tests/load_test.py --host=http://localhost:8000

# Open browser to http://localhost:8089 for UI
```

## Security Features

- **Authentication**: JWT tokens with secure password hashing (bcrypt)
- **Code Execution**: Sandboxed containers with resource limits
- **Rate Limiting**: API rate limiting (10 req/min by default)
- **CORS**: Configured Cross-Origin Resource Sharing
- **Security Headers**: X-Frame-Options, CSP, HSTS
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: ORM with parameterized queries
- **XSS Protection**: Content sanitization
- **API Key Management**: Secure environment variable storage

## Monitoring

### Health Checks

```bash
# Check all services
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost:3000
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# View recent logs
docker-compose logs --tail=100 backend
```

### Resource Usage

```bash
# Monitor container resources
docker stats

# Monitor from within server
htop
iotop
```

## Troubleshooting

### Services Won't Start

```bash
# Check Docker is running
sudo systemctl status docker

# Check logs for errors
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection
docker exec coding_platform_backend python -c "from database.connection import init_db; import asyncio; asyncio.run(init_db())"
```

### Code Execution Fails

```bash
# Check Piston is running
docker-compose ps piston

# Check Piston health
curl http://localhost:2000/runtimes

# Restart Piston
docker-compose restart piston
```

### LLM API Errors

```bash
# Verify environment variables
docker exec coding_platform_backend env | grep API_KEY

# Test OpenAI connection
docker exec coding_platform_backend python -c "import openai; print(openai.__version__)"
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000
sudo lsof -i :3000

# Kill process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
```

## Performance Optimization

### Database
- Indexes are automatically created on frequently queried fields
- Connection pooling via SQLAlchemy
- Query optimization with async operations

### Frontend
- Next.js automatic code splitting
- Static asset caching
- Image optimization
- Local storage for code persistence

### Backend
- Async/await for non-blocking operations
- Redis caching for frequently accessed data
- Rate limiting to prevent abuse
- Efficient LLM API call management

## Deployment

See `DEPLOYMENT.md` for detailed production deployment instructions including:
- SSL/TLS configuration
- Security hardening
- Automated backups
- Monitoring setup
- Domain configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub: https://github.com/dbugom/prompt_learning/issues
- Contact: admin@example.com

## Acknowledgments

- [Piston](https://github.com/engineer-man/piston) - Code execution engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Next.js](https://nextjs.org/) - React framework
- [CodeMirror](https://codemirror.net/) - Code editor component
- [LangChain](https://python.langchain.com/) - LLM application framework
- [OpenAI](https://openai.com/) - GPT models and API
- [Anthropic](https://anthropic.com/) - Claude models and API

## Additional Resources

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com)
- [LangChain Documentation](https://python.langchain.com/docs)
- [DSPy Documentation](https://dspy-docs.vercel.app/)

---

**Built with love for the prompt engineering community**

For development context and session recovery, see `CLAUDE.md` in the root directory.
