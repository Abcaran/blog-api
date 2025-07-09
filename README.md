# Blog API

A modern, fast blog API built with FastAPI, SQLAlchemy, and SQLite. This API provides full CRUD operations for blog posts and comments with proper validation, relationships, and comprehensive testing.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - Powerful SQL toolkit and ORM
- **SQLite** - Lightweight, file-based database
- **Pydantic** - Data validation using Python type annotations
- **Docker** - Containerized deployment
- **Comprehensive Testing** - Unit tests with unittest framework
- **API Documentation** - Auto-generated with Swagger/OpenAPI

## Next Steps

- **API authentication and authorization**
- **Logging and monitoring**
- **Caching**
- **Rate limiting**
- **Production-ready Docker setup**
- **CI/CD pipeline**
- **More tests**
- **More documentation**

## 📋 API Endpoints

### Posts
- `POST /posts` - Create a new post
- `GET /posts` - Get all posts with content (paginated)
- `GET /posts/{post_id}` - Get a specific post with comments
- `PUT /posts/{post_id}` - Update a post
- `DELETE /posts/{post_id}` - Delete a post

### Comments
- `POST /posts/{post_id}/comments` - Create a comment for a post
- `GET /posts/{post_id}/comments` - Get all comments for a post
- `GET /comments/{comment_id}` - Get a specific comment
- `PUT /comments/{comment_id}` - Update a comment
- `DELETE /comments/{comment_id}` - Delete a comment

## 🛠️ Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.11+** (for local development)
- **Git**

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone git@github.com:Abcaran/blog-api.git
   ```

2. **Build and start the application**
   ```bash
   make install    # Build Docker image
   make init-db    # Initialize database with sample data
   make run        # Start the API server
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

### Option 2: Local Development

1. **Clone and setup**
   ```bash
   git clone git@github.com:Abcaran/blog-api.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r config/requirements.txt
   ```

3. **Initialize database**
   ```bash
   python init_database.py
   ```

4. **Start the server**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🐳 Docker Commands

```bash
# Build Docker image
make install

# Database operations
make init-db        # Initialize database with sample data
make reset-db       # Reset database (delete all data)

# Run application
make run           # Production mode (port 8000)
make dev           # Development mode with auto-reload (port 8001)

# Stop application
make docker-stop   # Stop containers
make docker-clean  # Stop and clean up containers/volumes
```

## 🧪 Testing

### Run All Tests
```bash
# Using Docker (recommended)
make test

# Locally (faster for development)
make test-local
```

## 🗄️ Database Management

### Initialize Database
```bash
# With Docker
make init-db

# Locally
python init_database.py
```

### Reset Database
```bash
# With Docker
make reset-db

# Locally
python reset_database.py
```

## 📖 API Usage Examples

### Create a Post
```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first blog post.",
    "author": "John Doe"
  }'
```

### Get All Posts
```bash
curl "http://localhost:8000/posts"
```

### Get Posts with Pagination
```bash
curl "http://localhost:8000/posts?skip=0&limit=5"
```

### Get Specific Post
```bash
curl "http://localhost:8000/posts/1"
```

### Create a Comment
```bash
curl -X POST "http://localhost:8000/posts/1/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great post!",
    "author": "Jane Smith"
  }'
```