# Low Level Design (LLD)

# AI Interview Preparation Copilot

Version: 1.0

---

# 1. Design Principles

The project follows:

- Clean Architecture
- SOLID Principles
- Dependency Injection
- Repository Pattern
- Service Pattern
- DTO-Based Communication

Goals:

- Maintainability
- Testability
- Scalability
- Separation of Concerns

---

# 2. Project Structure

app/

```text id="ktk9nm"
app
│
├── core
│   ├── config
│   ├── security
│   ├── database
│   ├── exceptions
│   └── dependencies
│
├── infrastructure
│   ├── ai
│   ├── storage
│   ├── cache
│   └── background_jobs
│
├── shared
│   ├── enums
│   ├── constants
│   ├── utils
│   └── schemas
│
├── modules
│
│   ├── auth
│   ├── resume
│   ├── jd
│   ├── matching
│   ├── interview
│   ├── evaluation
│   ├── recommendation
│   └── rag
│
└── main.py
```

---

# 3. Module Internal Structure

Every module follows the same pattern.

Example:

auth/

```text id="k67j80"
auth
│
├── api
│   └── auth_router.py
│
├── service
│   └── auth_service.py
│
├── repository
│   └── auth_repository.py
│
├── models
│   └── user_model.py
│
├── schemas
│   ├── request.py
│   └── response.py
│
└── dependencies
```

All modules follow this structure.

---

# 4. Layer Responsibilities

## API Layer

Responsibilities:

- Receive Requests
- Validate DTOs
- Call Services
- Return Responses

No business logic allowed.

---

## Service Layer

Responsibilities:

- Business Rules
- Workflow Orchestration
- AI Calls
- Validation Logic

Most business logic lives here.

---

## Repository Layer

Responsibilities:

- Database Queries
- CRUD Operations
- Data Persistence

No business logic.

---

## Database Layer

Responsibilities:

- Data Storage
- Indexing
- Relationships

---

# 5. Dependency Flow

```text id="0teq8g"
API Layer
     ↓
Service Layer
     ↓
Repository Layer
     ↓
Database
```

Never:

```text id="5ks8uj"
API → Database
```

Direct access is forbidden.

---

# 6. Authentication Design

Components:

```text id="87iz80"
Auth Router

Auth Service

User Repository

JWT Service

Password Service
```

Flow:

```text id="2kn11r"
Login
 ↓
Auth Service
 ↓
Verify Password
 ↓
Generate Tokens
 ↓
Return Response
```

---

# 7. Resume Module Design

Components:

```text id="5g3b36"
Resume Router

Resume Service

Resume Repository

Resume Parser

Storage Provider
```

Flow:

```text id="mcbn6v"
Upload Resume
       ↓
Validate File
       ↓
Store File
       ↓
Extract Text
       ↓
Save Metadata
```

---

# 8. JD Module Design

Components:

```text id="cx8k8r"
JD Router

JD Service

JD Repository
```

Flow:

```text id="njgcl3"
Upload JD
      ↓
Store JD
      ↓
Save Metadata
```

---

# 9. Matching Module Design

Components:

```text id="x35cwk"
Matching Router

Matching Service

AI Provider

Matching Repository
```

Flow:

```text id="w4nttw"
Resume
    +
JD
    ↓
Prompt Builder
    ↓
LLM Provider
    ↓
Structured Result
```

Output:

```text id="zq1or4"
Match Score
Missing Skills
Recommendations
```

---

# 10. Interview Module Design

Components:

```text id="3nn2he"
Interview Router

Question Service

Question Repository

Session Repository
```

Flow:

```text id="vtt6be"
Resume
JD
Count
 ↓
Generate Questions
 ↓
Save Optional
```

Supports:

- Generate Only
- Generate and Save

---

# 11. Evaluation Module Design

Components:

```text id="chc8sx"
Evaluation Router

Evaluation Service

AI Provider

Evaluation Repository
```

Flow:

```text id="em6e64"
Question
Answer
 ↓
Prompt Builder
 ↓
AI Provider
 ↓
Evaluation Result
```

---

# 12. Recommendation Module Design

Components:

```text id="7rt0z6"
Recommendation Router

Recommendation Service

Recommendation Repository
```

Flow:

```text id="hnxq7q"
Match Analysis
Evaluation
 ↓
Generate Roadmap
 ↓
Save Recommendations
```

---

# 13. RAG Module Design

Components:

```text id="8ybe4o"
Embedding Service

Vector Repository

Retriever

Knowledge Service
```

Flow:

```text id="5q5e13"
Question
 ↓
Embedding
 ↓
Vector Search
 ↓
Context Retrieval
 ↓
LLM
```

---

# 14. AI Layer Design

Provider Abstraction:

```text id="d6ovvx"
LLMProvider
```

Implementations:

```text id="h3ppqg"
OpenAIProvider

GeminiProvider

ClaudeProvider
```

Business services never directly call OpenAI.

---

# 15. Storage Design

Interface:

```text id="mgl8bi"
StorageProvider
```

Implementations:

```text id="zpn4bw"
LocalStorageProvider

R2StorageProvider
```

Services use interface only.

---

# 16. Cache Design

Redis will cache:

- Match Results
- Generated Questions
- Recommendations

Benefits:

- Reduced AI Cost
- Faster Responses

---

# 17. Background Job Design

Celery Tasks:

```text id="66x4cf"
Resume Parsing

Embedding Generation

Recommendation Generation
```

Heavy tasks run asynchronously.

---

# 18. Error Handling Design

Global Exception Handler.

Categories:

```text id="70r9jf"
Validation Errors

Authentication Errors

Authorization Errors

Business Errors

External Service Errors
```

Standard Response:

```json id="2mjlwm"
{
  "success": false,
  "message": "Error message",
  "code": "ERROR_CODE"
}
```

---

# 19. Logging Design

Log Levels:

```text id="zcljmv"
INFO
WARNING
ERROR
CRITICAL
```

Log:

- Requests
- Responses
- AI Calls
- Failures

---

# 20. Testing Strategy

Unit Tests

```text id="m5vj6t"
Services
Repositories
Utilities
```

Integration Tests

```text id="3iq58o"
API
Database
Redis
```

---

# 21. Future Expansion

The architecture supports:

- Multiple AI Providers
- Voice Interviews
- Video Interviews
- Multi-Tenant SaaS
- Team Accounts
- Enterprise Plans
