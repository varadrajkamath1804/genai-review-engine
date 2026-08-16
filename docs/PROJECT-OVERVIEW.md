
                    GENAI REVIEW ENGINE - PROJECT OVERVIEW


1. PROJECT OVERVIEW


1.1 Purpose
-----------
The GenAI Review Engine is a production-oriented backend system designed to 
demonstrate practical GenAI engineering principles. It combines modern backend 
architecture with LLM capabilities to provide AI-powered review analysis, 
semantic search, and Retrieval-Augmented Generation (RAG).

1.2 Key Features
----------------
- LLM Integration: Groq-hosted AI models for review analysis
- Semantic Search: Vector-based similarity search using pgvector
- RAG Pipeline: Retrieval-augmented generation for contextual answers
- Authentication: JWT-based auth with refresh tokens and RBAC
- Caching: Redis with TTL, invalidation, and distributed locking
- Rate Limiting: Protection against abuse
- Clean Architecture: Separation of concerns, testable code

1.3 Target Audience
-------------------
- Backend developers learning GenAI
- Engineering teams building AI-powered applications
- Technical evaluators of GenAI solutions
- Students in AI/ML engineering


2. TECHNICAL STACK


2.1 Core Backend
----------------
| Component   | Technology   | Version |
|-------------|--------------|---------|
| Language    | Python       | 3.10+   |
| Framework   | FastAPI      | 0.100+  |
| Async       | AsyncIO      | Built-in|
| ORM         | SQLAlchemy   | 2.0+    |
| Migration   | Alembic      | 1.11+   |

2.2 Database
------------
| Component        | Technology      | Purpose                |
|------------------|-----------------|------------------------|
| Primary DB       | PostgreSQL 15+  | Relational data        |
| Vector Extension | pgvector        | Vector storage & search|
| Cache            | Redis 7+        | Caching, rate limiting |

2.3 GenAI
---------
| Component      | Technology      | Purpose               |
|----------------|-----------------|-----------------------|
| LLM Provider   | Groq API        | AI inference          |
| Embeddings     | Groq Embeddings | Text vectorization    |
| Vector Index   | pgvector        | Similarity search     |

2.4 Security
------------
- JWT for authentication
- bcrypt for password hashing
- RBAC for authorization
- CORS protection
- Rate limiting

2.5 Development Tools
---------------------
- Docker & Docker Compose
- Postman for API testing
- Pytest for unit/integration tests
- Black & Flake8 for code quality


3. PROJECT STRUCTURE


genai-review-engine/
├── alembic/                     # Database migrations
│   ├── versions/               # Migration files
│   └── env.py
├── app/                         # Main application
│   ├── api/                    # API endpoints
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
│   ├── core/                   # Core functionality
│   │   ├── config.py           # Configuration
│   │   ├── security/           # Security utilities
│   │   └── exceptions/         # Custom exceptions
│   ├── models/                 # Data models
│   │   ├── db/                # SQLAlchemy models
│   │   └── schemas/           # Pydantic schemas
│   ├── services/               # Business logic
│   ├── repositories/           # Data access
│   ├── utils/                  # Utilities
│   └── middleware/             # Custom middleware
├── tests/                      # Test suites
├── docker/                     # Docker configuration
└── scripts/                    # Utility scripts


4. CORE COMPONENTS


4.1 Authentication System
-------------------------
- JWT-based authentication with access and refresh tokens
- Role-Based Access Control (RBAC)
- Password hashing with bcrypt
- Token validation middleware
- Session management

4.2 Review Management
---------------------
- CRUD operations for reviews
- Product-based organization
- Rating system (1-5 stars)
- Optional title and comment fields
- User ownership validation

4.3 AI Analysis Pipeline
------------------------
- Review text analysis using Groq LLM
- Structured output with Pydantic validation
- Sentiment analysis
- Key points extraction
- Summary generation
- Cached results with Redis

4.4 Semantic Search
-------------------
- Text embedding generation
- Vector similarity search using pgvector
- Cosine similarity scoring
- Configurable threshold and top-k results
- Cached search results

4.5 RAG Pipeline
----------------
- Query embedding generation
- Vector similarity search
- Context construction from relevant reviews
- Prompt engineering with context
- LLM response generation
- Source attribution

4.6 Caching System
------------------
- Redis-based caching
- TTL management
- Cache invalidation strategies
- Cache stampede protection
- Distributed locking

4.7 Rate Limiting
-----------------
- Redis-based sliding window
- Per-endpoint limits
- Per-user/IP limits
- 429 response handling


5. API ENDPOINTS


5.1 Authentication
------------------
- POST /api/v1/auth/register - User registration
- POST /api/v1/auth/login - User login
- POST /api/v1/auth/refresh - Refresh token
- POST /api/v1/auth/logout - User logout

5.2 Reviews
-----------
- POST /api/v1/reviews - Create review
- GET /api/v1/reviews/{review_id} - Get review
- PUT /api/v1/reviews/{review_id} - Update review
- DELETE /api/v1/reviews/{review_id} - Delete review
- GET /api/v1/reviews/product/{product_id} - Get product reviews
- POST /api/v1/reviews/{review_id}/analyze - Analyze review

5.3 Search
----------
- GET /api/v1/reviews/search - Semantic search
- GET /api/v1/reviews/search/keyword - Keyword search

5.4 RAG
-------
- POST /api/v1/rag/query - RAG query
- GET /api/v1/rag/feedback - Get RAG feedback

5.5 Admin
---------
- GET /api/v1/admin/reviews - List all reviews
- DELETE /api/v1/admin/reviews/{review_id} - Delete review


6. DATA MODELS


6.1 User Model
--------------
- id: UUID (Primary Key)
- email: String (Unique)
- password_hash: String
- name: String
- role: String (user/admin)
- created_at: DateTime
- updated_at: DateTime

6.2 Review Model
----------------
- id: UUID (Primary Key)
- product_id: String
- user_id: UUID (Foreign Key)
- title: String (Optional)
- rating: Integer (1-5)
- comment: Text
- embedding: Vector(384)
- analysis: JSONB
- created_at: DateTime
- updated_at: DateTime

6.3 Analysis Schema
-------------------
- sentiment: String (positive/negative/neutral)
- sentiment_score: Float
- key_points: List[String]
- summary: String
- suggested_rating: Integer
- topics: List[String]


7. CURRENT STATUS & ROADMAP


7.1 Completed Features
-----------------------
✅ FastAPI backend with clean architecture
✅ PostgreSQL with pgvector integration
✅ Redis caching and rate limiting
✅ JWT authentication with refresh tokens
✅ Groq LLM integration
✅ Structured AI responses with Pydantic
✅ Semantic search with embeddings
✅ RAG pipeline
✅ Distributed locking for cache stampede
✅ RBAC implementation
✅ Centralized exception handling
✅ Structured logging
✅ API testing with Postman

7.2 Planned Features
---------------------
🔲 LangChain integration
🔲 LangGraph workflows
🔲 Agentic workflows
🔲 Tool calling
🔲 Production GenAI reliability patterns
🔲 Docker containerization
🔲 CI/CD pipeline
🔲 Cloud deployment
🔲 Production infrastructure
🔲 Advanced monitoring and observability


8. GETTING STARTED


8.1 Prerequisites
------------------
- Python 3.10+
- PostgreSQL 15+ with pgvector
- Redis 7+
- Groq API key

8.2 Installation
-----------------
1. Clone the repository
2. Create virtual environment
3. Install dependencies: pip install -r requirements.txt
4. Configure environment variables
5. Run migrations: alembic upgrade head
6. Start the server: uvicorn app.main:app --reload

8.3 Configuration
------------------
Required environment variables:
- DATABASE_URL: PostgreSQL connection string
- REDIS_URL: Redis connection string
- GROQ_API_KEY: Groq API key
- SECRET_KEY: JWT secret key
- ACCESS_TOKEN_EXPIRE_MINUTES: Access token expiry
- REFRESH_TOKEN_EXPIRE_DAYS: Refresh token expiry


                            END OF DOCUMENTATION
