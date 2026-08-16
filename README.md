# GenAI Review Engine

A production-oriented GenAI backend built with **Python and FastAPI** for AI-powered review analysis, semantic search, and Retrieval-Augmented Generation (RAG).

The project focuses on building a production-ready GenAI backend incrementally, combining modern backend architecture with LLM integration, Redis, embeddings, vector search, and RAG.

---

## 🚀 Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* AsyncIO
* REST APIs
* Clean Architecture
* Dependency Injection
* Repository Pattern
* Service Layer

### Database

* PostgreSQL
* SQLAlchemy
* Alembic
* pgvector

### Redis

* Redis
* Caching
* TTL
* Cache Invalidation
* Rate Limiting
* Sorted Sets
* Distributed Locking
* Cache Stampede Protection

### GenAI

* Groq API
* LLM Integration
* Prompt Engineering
* Structured AI Responses
* Pydantic Validation
* Embeddings
* Vector Search
* Semantic Search
* Retrieval-Augmented Generation (RAG)

### Authentication & Security

* JWT Authentication
* Access Tokens
* Refresh Tokens
* RBAC
* Password Hashing
* Rate Limiting

### Engineering

* Centralized Exception Handling
* Custom Exceptions
* Middleware
* Structured Logging
* Request/Correlation IDs
* API Testing with Postman
* Unit Testing
* Integration Testing

---

## 🎯 Project Goal

The goal of this project is to build a **production-oriented GenAI backend** while applying real-world backend engineering principles.

The project combines:

```text
Client
   ↓
FastAPI
   ↓
Authentication / Authorization
   ↓
Service Layer
   ↓
Repository Layer
   ↓
PostgreSQL
```

with GenAI capabilities:

```text
Review
   ↓
LLM Analysis
   ↓
Structured Response
   ↓
PostgreSQL
```

and semantic retrieval:

```text
User Query
    ↓
Embedding
    ↓
Vector Search
    ↓
Relevant Reviews
    ↓
Context Construction
    ↓
LLM
    ↓
RAG Response
```

---

## 🧠 GenAI Capabilities

### LLM Integration

Integrated Groq-hosted LLMs for AI-powered review analysis with structured responses validated using Pydantic.

### Embeddings

Reviews and user queries are converted into numerical vector representations to enable semantic similarity search.

### Vector Search

Implemented vector storage and similarity search using **PostgreSQL + pgvector**.

The system retrieves semantically relevant reviews instead of relying only on keyword matching.

### RAG

Implemented a Retrieval-Augmented Generation pipeline:

```text
Question
   ↓
Query Embedding
   ↓
Vector Similarity Search
   ↓
Relevant Reviews
   ↓
Context
   ↓
LLM
   ↓
Generated Response
```

The RAG pipeline includes retrieval, similarity thresholds, Top-K results, context construction, and LLM response generation.

---

## ⚡ Redis & Performance

Redis is used for production-oriented backend capabilities including:

* AI response caching
* TTL-based expiration
* Cache invalidation
* Rate limiting
* Redis sorted sets
* Distributed locking
* Cache stampede protection

Distributed locking prevents multiple concurrent requests from unnecessarily executing the same expensive AI operation.

---

## 🔐 Authentication & Authorization

The backend implements:

* JWT authentication
* Access tokens
* Refresh tokens
* Password hashing
* Role-Based Access Control (RBAC)
* Current-user dependencies
* Role-based authorization

---

## 🏗️ Architecture

The application follows a clean layered architecture:

```text
Router
   ↓
Dependencies
   ↓
Service
   ↓
Repository
   ↓
Database
```

Infrastructure concerns such as:

```text
Redis
LLM Provider
Embeddings
Vector Search
Logging
```

are separated from the core business logic.

The project uses Dependency Injection and the Repository Pattern to keep components testable and maintainable.

---

## 🧪 Testing

The project includes testing across backend and GenAI functionality.

Testing covers:

* API testing
* Unit testing
* Service testing
* Dependency overrides
* Mocking
* Integration testing
* Database-related testing
* Redis-related testing
* RAG workflow testing

Postman is used for manual API validation and end-to-end API testing.

---

## 📊 Current Status

### Completed

* ✅ FastAPI backend
* ✅ Clean Architecture
* ✅ Dependency Injection
* ✅ Repository Pattern
* ✅ Async backend
* ✅ PostgreSQL
* ✅ SQLAlchemy
* ✅ Alembic
* ✅ JWT Authentication
* ✅ Refresh Tokens
* ✅ RBAC
* ✅ Logging
* ✅ Exception Handling
* ✅ Middleware
* ✅ Redis Caching
* ✅ TTL
* ✅ Cache Invalidation
* ✅ Redis Rate Limiting
* ✅ Distributed Locking
* ✅ Cache Stampede Protection
* ✅ Groq LLM Integration
* ✅ Structured AI Responses
* ✅ Embeddings
* ✅ pgvector
* ✅ Semantic Search
* ✅ Vector Search
* ✅ RAG
* ✅ API Testing
* ✅ RAG Testing

### 🔄 Next

The project will continue evolving toward a more complete production GenAI backend with:

* LangChain
* LangGraph
* Agentic workflows
* Tool Calling
* Production GenAI reliability patterns
* Docker
* CI/CD
* Cloud deployment
* Production infrastructure

---

## 🔗 Project

GitHub:

https://github.com/varadrajkamath1804/genai-review-engine

---

## 📌 Why This Project?

This project is designed to demonstrate practical **Backend + GenAI Engineering**, rather than simply calling an LLM API.

It focuses on:

* Scalable backend architecture
* Asynchronous processing
* Database design
* Caching
* Rate limiting
* Distributed locking
* Authentication
* LLM integration
* Embeddings
* Vector search
* RAG
* Testing
* Production-oriented reliability

The project is continuously evolving as new GenAI and backend engineering capabilities are implemented.
