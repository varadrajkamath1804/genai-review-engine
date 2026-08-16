# API Flow Documentation
## GenAI Review Engine

### Overview
The API flow follows a clean layered architecture with authentication, business logic, and data access layers.

### Authentication Flow

#### 1. User Registration
POST /api/v1/auth/register
├── Request: { email, password, name, role? }
├── Validation: Pydantic schema validation
├── Service: UserService.register()
│   ├── Check existing user
│   ├── Hash password (bcrypt)
│   └── Create user in PostgreSQL
└── Response: { user_id, email, name, role }

#### 2. User Login
POST /api/v1/auth/login
├── Request: { email, password }
├── Validation: Credentials validation
├── Service: AuthService.login()
│   ├── Verify user exists
│   ├── Verify password
│   ├── Generate Access Token (JWT, 15min)
│   └── Generate Refresh Token (JWT, 7days)
└── Response: { access_token, refresh_token, token_type }

#### 3. Token Refresh
POST /api/v1/auth/refresh
├── Request: { refresh_token }
├── Validation: Token validation
├── Service: AuthService.refresh_token()
│   ├── Validate refresh token
│   ├── Generate new access token
│   └── Optional: Rotate refresh token
└── Response: { access_token }

### Core Business Flows

#### 4. Create Review
POST /api/v1/reviews
├── Authentication: JWT Bearer Token
├── Authorization: RBAC (User/Admin)
├── Request: { product_id, rating, comment, title? }
├── Middleware: Rate Limiting (Redis)
├── Service: ReviewService.create_review()
│   ├── Validate input
│   ├── Check product exists
│   ├── Save to PostgreSQL
│   ├── Generate embedding (Groq/Embeddings)
│   └── Store vector in pgvector
├── Cache: Invalidate product review cache
└── Response: { review_id, ...review_data }

#### 5. AI Review Analysis
POST /api/v1/reviews/{review_id}/analyze
├── Authentication: JWT Bearer Token
├── Authorization: User owns review or Admin
├── Request: None (uses review data)
├── Cache Check: Redis cache hit?
│   ├── If yes → Return cached analysis
│   └── If no → Proceed to LLM
├── Service: ReviewAnalysisService.analyze()
│   ├── Fetch review from DB
│   ├── Construct prompt with review context
│   ├── Call Groq LLM with structured output
│   ├── Validate LLM response with Pydantic
│   ├── Store analysis in PostgreSQL
│   └── Cache result in Redis (TTL: 1 hour)
├── Distributed Locking: Prevent duplicate AI calls
└── Response: { sentiment, key_points, summary, rating }

#### 6. Semantic Search
GET /api/v1/reviews/search?q={query}&limit={n}&threshold={t}
├── Authentication: Optional (public or protected)
├── Request: Query parameters
├── Service: SearchService.semantic_search()
│   ├── Generate embedding for query
│   ├── Perform pgvector similarity search
│   │   ├── Calculate cosine similarity
│   │   ├── Apply threshold filter
│   │   └── Return top-k results
│   └── Fetch full review data
├── Cache: Search results cached (TTL: 5min)
└── Response: { results: [{ review, similarity_score }] }

#### 7. RAG (Retrieval-Augmented Generation)
POST /api/v1/rag/query
├── Authentication: JWT Bearer Token
├── Request: { question, top_k?, threshold? }
├── Service: RAGService.query()
│   ├── Generate query embedding
│   ├── Vector similarity search (pgvector)
│   │   └── Retrieve top_k relevant reviews
│   ├── Construct context from retrieved reviews
│   ├── Build prompt with context + question
│   ├── Call Groq LLM
│   ├── Validate structured response
│   └── Cache RAG response (TTL: 15min)
├── Distributed Locking: Prevent duplicate RAG calls
└── Response: { answer, sources: [review_ids], confidence }

### Admin Flows

#### 8. Admin Review Management
GET /api/v1/admin/reviews
├── Authentication: JWT Bearer Token
├── Authorization: Admin role required
├── Service: AdminService.get_all_reviews()
│   ├── Apply filters (date, rating, product)
│   ├── Pagination support
│   └── Include analysis data
└── Response: { reviews: [], total, page, limit }

DELETE /api/v1/admin/reviews/{review_id}
├── Authentication: JWT Bearer Token
├── Authorization: Admin role required
├── Service: AdminService.delete_review()
│   ├── Delete from PostgreSQL
│   ├── Delete embedding from pgvector
│   └── Invalidate caches
└── Response: { success: true }

### Error Handling Flow

Any API Endpoint
├── Middleware: Exception Handler
├── Custom Exceptions:
│   ├── AuthenticationError → 401
│   ├── AuthorizationError → 403
│   ├── ValidationError → 400
│   ├── NotFoundError → 404
│   ├── RateLimitError → 429
│   └── LLMError → 503
└── Response: { error: { code, message, details } }

### Caching Strategy

Read Operations:
├── Check Redis cache (key: endpoint + params)
├── If hit → Return cached response
└── If miss → Execute operation → Cache result

Write Operations:
├── Execute operation
├── Update database
├── Invalidate relevant cache keys
└── Optional: Update cache proactively

Cache Stampede Protection:
├── Multiple concurrent requests for same expensive operation
├── Distributed lock acquired (Redis lock)
├── First request executes operation
├── Others wait for result
└── Result cached for subsequent requests

### Rate Limiting

Rate Limiting Flow:
├── Extract client identifier (IP or user_id)
├── Check Redis for request count
├── Apply configured limits:
│   ├── Public endpoints: 100 requests/hour
│   ├── Authenticated endpoints: 1000 requests/hour
│   └── Admin endpoints: 2000 requests/hour
└── If exceeded → Return 429 Too Many Requests

### Response Formats

#### Success Response
{
  "status": "success",
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO8601",
    "version": "1.0.0"
  }
}

#### Error Response
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... }
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO8601"
  }
}

### API Versioning
/api/v1/ - Current stable version
/api/v2/ - Future version (preparation)

### Monitoring & Logging
Each Request:
├── Correlation ID generated
├── Structured logging (JSON format)
├── Request/Response logging (excluding sensitive data)
├── Performance metrics (response time)
└── Error tracking with stack traces