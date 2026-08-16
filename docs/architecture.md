# Architecture Documentation
## GenAI Review Engine

### High-Level Architecture

Client Applications (Web, Mobile, Third-party)
                    │
                    ▼
            API Gateway Layer
         (FastAPI + Middleware)
    ┌──────────┬────────────┬───────────┐
    │ Rate     │ Auth       │ Logging   │
    │ Limiting │ Middleware │ Middleware│
    └──────────┴────────────┴───────────┘
                    │
                    ▼
              Router Layer
    (API Endpoints & Route Definitions)
    ┌────────────┬─────────────┬────────────┐
    │ Auth       │ Reviews     │ Search     │
    │ Routes     │ Routes      │ Routes     │
    └────────────┴─────────────┴────────────┘
                    │
                    ▼
              Service Layer
     (Business Logic & Use Cases)
    ┌────────────┬─────────────┬────────────┐
    │ Auth       │ Review      │ Search     │
    │ Service    │ Service     │ Service    │
    └────────────┴─────────────┴────────────┘
    ┌─────────────────────────────────────────┐
    │      LLM Service (Groq Integration)     │
    └─────────────────────────────────────────┘
                    │
                    ▼
            Repository Layer
      (Data Access & Persistence)
    ┌────────────┬─────────────┬────────────┐
    │ Review     │ User        │ Search     │
    │ Repository │ Repository  │ Repository │
    └────────────┴─────────────┴────────────┘
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐
│   PostgreSQL     │    │      Redis       │
│ ┌──────────────┐ │    │ ┌──────────────┐ │
│ │ Relational   │ │    │ │ Cache Layer  │ │
│ │ Data         │ │    │ └──────────────┘ │
│ └──────────────┘ │    │ ┌──────────────┐ │
│ ┌──────────────┐ │    │ │ Rate         │ │
│ │ pgvector     │ │    │ │ Limiting     │ │
│ │ (Vectors)    │ │    │ └──────────────┘ │
│ └──────────────┘ │    │ ┌──────────────┐ │
└──────────────────┘    │ │ Distributed  │ │
                        │ │ Locking      │ │
                        │ └──────────────┘ │
                        └──────────────────┘

### Layered Architecture Details

#### 1. API Gateway Layer
- FastAPI: Async web framework
- Middleware Chain:
  - CORS middleware
  - Request ID middleware
  - Logging middleware
  - Rate limiting middleware
  - Authentication middleware
  - Exception handling middleware

#### 2. Router Layer
- Endpoint Organization:
  - /auth - Authentication endpoints
  - /reviews - Review CRUD operations
  - /search - Semantic search endpoints
  - /rag - RAG query endpoints
  - /admin - Admin management endpoints
- Dependency Injection: FastAPI Depends() for service injection

#### 3. Service Layer
Core Services:
- AuthService: JWT management, password hashing, token generation
- ReviewService: Review CRUD, embedding generation
- SearchService: Semantic search, vector similarity
- RAGService: Retrieval + Generation pipeline
- LLMService: Groq API integration, prompt management
- CacheService: Redis operations, cache strategies

Service Responsibilities:
- Business logic implementation
- Transaction management
- Error handling and conversion
- Service-to-service communication
- Cache orchestration

#### 4. Repository Layer
Data Access Patterns:
- ReviewRepository: PostgreSQL operations for reviews
- UserRepository: User management operations
- VectorRepository: pgvector operations for embeddings
- CacheRepository: Redis operations abstraction

Repository Pattern Benefits:
- Separation of data access logic
- Easier testing (mocking)
- Database abstraction
- Consistent data access interfaces

### Database Architecture

#### PostgreSQL Schema
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Reviews Table
CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    product_id VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES users(id),
    title VARCHAR(200),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    embedding VECTOR(384),
    analysis JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_reviews_embedding ON reviews 
    USING ivfflat (embedding vector_cosine_ops);

#### Redis Data Structures
Cache Keys:
- review:{review_id}:analysis
- search:{query_hash}:results
- rag:{question_hash}:response
- user:{user_id}:session
- rate:{endpoint}:{identifier}

Redis Types:
- Strings: Cached responses
- Sorted Sets: Rate limiting counters
- Hashes: User session data
- Lists: Operation queues
- Sets: Active tokens

### GenAI Architecture

#### Embedding Pipeline
Review Text → Preprocessing → Embedding Model → Vector Storage
     │                              │                │
     └─ Clean text                 └─ Groq API      └─ pgvector

#### RAG Pipeline
User Query → Query Embedding → Vector Search → Context Retrieval
     │                                            │
     └─ Preprocessing            └─ Top-k relevant reviews
                                         │
                                         ▼
                    LLM Generation ← Prompt Engineering ← Context Construction
                           │
                           ▼
                    Structured Response (Pydantic)

#### LLM Integration
Service → Prompt Template → Groq API → Response Parsing → Validation
   │              │             │            │               │
   └─ Context    └─ System    └─ LLM Call   └─ Pydantic    └─ Schema
                 + User Prompt                Model          Validation

### Caching Architecture

#### Multi-Level Caching
Level 1 (Application): In-memory cache (TTL: seconds)
Level 2 (Redis): Distributed cache (TTL: minutes)
Level 3 (Database): Persistent storage (indefinite)

#### Cache Strategies
- Cache-Aside: Lazy loading
- Write-Through: Update cache on write
- Cache Invalidation: On data changes
- Cache Stampede Protection: Distributed locking

### Security Architecture

#### Authentication Flow
Request → JWT Validation → User Context → Authorization Check
   │           │                │               │
   └─ Bearer   └─ Token         └─ Current      └─ RBAC
     Token       Verification     User           Rules

#### Authorization Levels
Roles:
- User: Read own, Create, Update own
- Admin: Read all, Update all, Delete all
- System: Internal operations

#### Security Measures
- Password hashing (bcrypt)
- JWT with short-lived access tokens
- Refresh token rotation
- Rate limiting per endpoint
- CORS configuration
- Input validation (Pydantic)
- SQL injection prevention (ORM)

### Performance Architecture

#### Optimization Strategies
Database:
- Connection pooling
- Query optimization
- Indexing (including vector indexes)
- Read replicas (planned)

Caching:
- Redis cache layer
- TTL optimization
- Cache warming
- Cache invalidation strategies

Async Processing:
- AsyncIO for I/O operations
- Background tasks for heavy operations
- Queue for batch processing

Scalability:
- Horizontal scaling ready
- Stateless application design
- Distributed locking
- Service decoupling

### Development Architecture

#### Project Structure
genai-review-engine/
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   └── env.py
├── app/                     # Main application
│   ├── api/                # API endpoints
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── reviews.py
│   │   │   │   ├── search.py
│   │   │   │   ├── rag.py
│   │   │   │   └── admin.py
│   │   │   └── dependencies/
│   │   │       ├── auth.py
│   │   │       └── database.py
│   │   └── deps.py
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration
│   │   ├── security/       # Security utilities
│   │   └── exceptions/     # Custom exceptions
│   ├── models/             # Data models
│   │   ├── db/            # SQLAlchemy models
│   │   └── schemas/       # Pydantic schemas
│   ├── services/           # Business logic
│   ├── repositories/       # Data access
│   ├── utils/              # Utilities
│   └── middleware/         # Custom middleware
├── tests/                  # Test suites
├── docker/                 # Docker configuration
└── scripts/               # Utility scripts

#### Design Patterns
- Clean Architecture: Separation of concerns
- Repository Pattern: Data access abstraction
- Service Layer: Business logic encapsulation
- Dependency Injection: Loose coupling
- Factory Pattern: Object creation
- Strategy Pattern: Algorithm selection
- Observer Pattern: Event handling

### Error Handling Architecture

#### Exception Hierarchy
BaseException
├── AppException
│   ├── BusinessException
│   │   ├── ValidationError
│   │   ├── BusinessRuleError
│   │   └── ResourceNotFoundError
│   ├── SystemException
│   │   ├── DatabaseError
│   │   ├── LLMServiceError
│   │   └── CacheError
│   └── SecurityException
│       ├── AuthenticationError
│       ├── AuthorizationError
│       └── TokenError
└── HTTPException

#### Error Response Strategy
Error Response = {
    status: "error",
    error: {
        code: "UNIQUE_ERROR_CODE",
        message: "Human-readable message",
        details: "Additional context"
    },
    meta: {
        request_id: "uuid",
        timestamp: "ISO8601"
    }
}