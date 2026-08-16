# Architecture Decisions
## GenAI Review Engine

### Decision Records

## 1. Framework Selection: FastAPI vs Other Options

Context: Need a Python web framework for GenAI backend.

Decision: Use FastAPI

Options Considered:
- Django (too heavy, synchronous)
- Flask (no async support, less built-in features)
- Starlette (low-level, more boilerplate)

Rationale:
- Native async support for LLM calls
- Automatic OpenAPI documentation
- Pydantic validation for structured AI responses
- Dependency injection system
- High performance (on par with Node.js)
- Built-in WebSocket support for future features

Consequences:
- Faster development with automatic docs
- Better LLM integration with async
- Some learning curve for async patterns

## 2. Database Selection: PostgreSQL with pgvector

Context: Need both relational data and vector storage.

Decision: PostgreSQL + pgvector extension

Options Considered:
- Separate vector DB (Pinecone, Weaviate) + Relational DB
- MongoDB with vector support
- Single PostgreSQL with pgvector

Rationale:
- Single database for all data
- ACID compliance for transactional data
- pgvector provides production-ready vector search
- Reduced operational complexity
- Familiar SQL interface
- Lower cost (no additional vector DB)

Consequences:
- Vector search performance depends on indexing
- Need to manage vector dimensions
- Requires pgvector extension setup
- Some limitations vs specialized vector DBs

## 3. Caching Strategy: Redis

Context: Need high-performance caching for AI responses.

Decision: Redis for caching, rate limiting, and distributed locking

Options Considered:
- Memcached (simpler but no advanced features)
- In-memory cache (not distributed)
- Database-level caching
- CDN caching

Rationale:
- Advanced data structures (sorted sets for rate limiting)
- Distributed locking capability
- TTL and expiration support
- High performance
- Rich feature set for production needs
- Industry standard

Consequences:
- Additional infrastructure requirement
- Memory management considerations
- Need for cache invalidation strategies
- Redis expertise needed

## 4. LLM Provider: Groq vs OpenAI

Context: Need reliable LLM for review analysis and RAG.

Decision: Use Groq API

Options Considered:
- OpenAI API (more expensive)
- Anthropic Claude (high quality but costly)
- Open-source models (requires hosting)
- Groq (high performance + cost-effective)

Rationale:
- High inference speed
- Lower cost compared to alternatives
- Good performance for structured outputs
- API compatibility with OpenAI
- Growing ecosystem
- Cost-effective for production

Consequences:
- Vendor lock-in consideration
- Limited model selection compared to OpenAI
- Need fallback strategy
- API rate limits to manage

## 5. Authentication: JWT with Refresh Tokens

Context: Need secure, stateless authentication.

Decision: JWT with refresh token rotation

Options Considered:
- Session-based (requires state)
- OAuth2 (complex for internal API)
- API Keys (less secure)
- JWT with short-lived tokens (current)

Rationale:
- Stateless authentication
- No session storage needed
- Refresh tokens for security
- Easy scaling
- Industry standard
- Works well with FastAPI

Consequences:
- Token revocation challenges
- Need secure token storage
- Refresh token rotation complexity
- Base64 decoding overhead

## 6. Architecture Pattern: Clean Architecture

Context: Need maintainable, testable code.

Decision: Clean Architecture with Repository Pattern

Options Considered:
- MVC (tight coupling)
- Domain-Driven Design (complex for scale)
- Service-based (current choice)
- Functional approach

Rationale:
- Separation of concerns
- Easy testing with dependency injection
- Independent of frameworks
- Clear business logic isolation
- Maintainable at scale
- Technology agnostic

Consequences:
- More initial setup
- Learning curve for team
- More files to manage
- Potentially slower for simple projects

## 7. Data Modeling: Approach

Context: Need to store reviews and embeddings effectively.

Decision: Relational model with JSONB for flexible data

Options Considered:
- Document-store (MongoDB)
- Graph database (Neo4j)
- Traditional relational
- Hybrid (relational + JSONB)

Rationale:
- ACID compliance for business data
- JSONB for flexible AI analysis storage
- pgvector for embeddings in same DB
- Structured relations (users, reviews)
- Query flexibility

Consequences:
- Schema evolution challenges
- Migration management needed
- JSONB query performance considerations
- Complex relationships can impact performance

## 8. Rate Limiting Strategy

Context: Need to protect from abuse and ensure fair usage.

Decision: Redis-based rate limiting with sliding windows

Options Considered:
- Fixed window (burst issues)
- Token bucket (complex implementation)
- Sliding window (chosen)
- Application-level throttling

Rationale:
- Redis provides atomic operations
- Sliding window more accurate
- Distributed across instances
- Configurable per endpoint
- Prevention of abuse

Consequences:
- Redis dependency for critical path
- Slight latency overhead
- Need to choose proper limits
- Requires monitoring and adjustment

## 9. Distributed Locking Implementation

Context: Prevent duplicate expensive AI operations.

Decision: Redis distributed locking for cache stampede protection

Options Considered:
- Database locks (performance hit)
- Application-level semaphores (not distributed)
- Redis distributed locking (chosen)
- No locking (higher cost)

Rationale:
- Prevents duplicate AI calls
- Works across multiple instances
- Simple implementation with Redis
- Essential for cost control
- Improves user experience

Consequences:
- Additional Redis calls
- Lock timeout considerations
- Potential deadlock scenarios
- Complexity in error handling

## 10. Testing Strategy

Context: Ensure reliability of GenAI features.

Decision: Multi-level testing approach

Options Considered:
- Only unit tests (insufficient)
- Only integration tests (slow)
- End-to-end only (fragile)
- Mixed approach (chosen)

Rationale:
- Unit tests for business logic
- Integration tests for database
- Mocking for LLM services
- Special RAG testing pipeline
- Postman for manual testing
- CI/CD automation ready

Consequences:
- Higher initial investment
- Longer test execution time
- Mock complexity for AI features
- Need test data management

## 11. Error Handling Strategy

Context: Need consistent error responses.

Decision: Centralized exception handling with custom hierarchy

Options Considered:
- Decorator-based handling
- Middleware approach (chosen)
- Try-except everywhere (messy)
- Custom exception classes

Rationale:
- Consistent error responses
- Logging built-in
- Request ID correlation
- Clean separation of error logic
- Easy to extend

Consequences:
- Global handler catches all exceptions
- Need to maintain hierarchy
- Potential overhead
- Must avoid catching system errors

## 12. Configuration Management

Context: Need manage environment-specific configurations.

Decision: Pydantic Settings with environment variables

Options Considered:
- YAML/JSON config files
- Environment variables (chosen)
- Config service (consul, etcd)
- Python config module

Rationale:
- 12-factor app compliant
- Easy Docker integration
- No file system dependency
- Type-safe with Pydantic
- Secrets management support

Consequences:
- Many environment variables needed
- Secrets handling in CI/CD
- Validation overhead at startup
- Limited hierarchy support

## 13. Vector Indexing Strategy

Context: Need efficient vector similarity search.

Decision: IVFFlat index with cosine similarity

Options Considered:
- No index (full scan)
- IVFFlat (chosen for production)
- HNSW (higher memory, faster)
- Product Quantization

Rationale:
- Good balance of speed and memory
- Built into pgvector
- Works well for production
- Support for incremental updates
- Lower memory footprint

Consequences:
- Build time for index
- Need to tune parameters
- Version migration complexity
- Backup/restore considerations

## 14. Caching Expiration Strategy

Context: Need balance freshness and performance.

Decision: Multi-tier TTL strategy

Options Considered:
- Fixed TTL all endpoints (too rigid)
- Adaptive TTL based on data (chosen)
- No expiration (stale data)
- Event-based invalidation

Rationale:
- AI analysis: 1-hour TTL
- Search results: 5-minute TTL
- RAG responses: 15-minute TTL
- User data: 30-minute TTL
- Configuration: 1-hour TTL

Consequences:
- Increased complexity
- Need monitoring of cache hit rates
- Potential stale data window
- Memory management implications

## 15. API Response Structure

Context: Need consistent, useful API responses.

Decision: Standardized response envelope

Options Considered:
- Direct data (less structured)
- Envelope with metadata (chosen)
- HAL JSON (too complex)
- JSON API (compliance heavy)

Rationale:
- Consistent across endpoints
- Easy to add metadata
- Clear success/error differentiation
- Request ID for debugging
- Version information included

Consequences:
- Slightly larger payloads
- Need to parse envelope
- More boilerplate code
- Client must understand structure

### Decision Summary Table

| Decision Area | Chosen Option | Key Rationale |
|--------------|---------------|---------------|
| Web Framework | FastAPI | Async, Pydantic, OpenAPI |
| Database | PostgreSQL + pgvector | Single DB, ACID, vector support |
| Caching | Redis | Performance, distributed features |
| LLM Provider | Groq | Speed, cost-effectiveness |
| Auth | JWT + Refresh Tokens | Stateless, scalable |
| Architecture | Clean + Repository | Testability, maintainability |
| Data Model | Relational + JSONB | ACID, flexibility |
| Rate Limiting | Redis Sliding Window | Accuracy, distributed |
| Distributed Lock | Redis Locks | Multi-instance support |
| Testing | Multi-level | Reliability, automation |
| Error Handling | Centralized Middleware | Consistency, logging |
| Config | Pydantic Settings | 12-factor, type safety |
| Vector Indexing | IVFFlat | Speed, memory balance |
| Cache TTL | Multi-tier | Performance vs freshness |
| API Response | Envelope | Consistency, metadata |