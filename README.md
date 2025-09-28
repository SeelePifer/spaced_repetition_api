# Spaced Repetition Language Learning API

API for language learning using spaced repetition implemented with **layered architecture** and **CQRS (Command Query Responsibility Segregation)**.

## 🏗️ Architecture

The application is structured in the following layers:

### 📁 Project Structure

```
src/
├── domain/                    # Domain Layer
│   ├── entities/             # Business entities
│   ├── value_objects/        # Value objects
│   ├── events/              # Domain events
│   └── repositories.py      # Repository interfaces
├── application/              # Application Layer (CQRS)
│   ├── commands/            # Commands (write operations)
│   ├── queries/             # Queries (read operations)
│   ├── handlers/            # Command and query handlers
│   ├── dto/                 # Data Transfer Objects
│   └── mediator.py          # CQRS Mediator
├── infrastructure/          # Infrastructure Layer
│   ├── database/           # Database models
│   ├── repositories/       # Repository implementations
│   └── dependencies.py    # Dependency injection
├── presentation/           # Presentation Layer
│   ├── controllers/        # REST controllers
│   ├── dto/               # Presentation DTOs
│   └── app.py            # FastAPI configuration
└── shared/                # Shared components
    ├── exceptions/        # Custom exceptions
    └── config.py         # Configuration
```

## 🔄 CQRS Pattern

### Commands (Commands)

- **SubmitAnswerCommand**: Records a study answer
- **GenerateStudyBlockCommand**: Generates a study block

### Queries (Queries)

- **GetUserProgressQuery**: Gets user progress
- **GetWordStatsQuery**: Gets word statistics
- **GetGlobalStatsQuery**: Gets global statistics

### Handlers

- **Command Handlers**: Process commands and modify state
- **Query Handlers**: Process queries and return data

## 🚀 Features

- ✅ **Layered Architecture**: Clear separation of responsibilities
- ✅ **CQRS**: Separation of commands and queries
- ✅ **Domain-Driven Design**: Entities, value objects and domain events
- ✅ **Dependency Injection**: Automatic dependency configuration
- ✅ **Repository Pattern**: Data access abstraction
- ✅ **Event Sourcing**: Domain events for auditing
- ✅ **Validation**: Robust validation with Pydantic
- ✅ **Documentation**: Automatic Swagger/OpenAPI

## 🛠️ Technologies

- **FastAPI**: Modern and fast web framework
- **SQLAlchemy**: Python ORM
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## 📋 Endpoints

### Study

- `GET /api/v1/study-block/{user_id}` - Generates study block
- `POST /api/v1/submit-answer` - Submits study answer

### Progress

- `GET /api/v1/progress/{user_id}` - Gets user progress

### Statistics

- `GET /api/v1/word/{word_id}` - Word statistics
- `GET /api/v1/stats` - Global statistics

### System

- `GET /` - API information
- `GET /health` - Health check

## 🚀 Installation and Usage

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Configure database**:

```bash
# Use Docker Compose
docker-compose up -d
```

3. **Run the application**:

```bash
python main.py
```

4. **Access documentation**:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Configuration

Available environment variables:

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/spaced_repetition_db
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=info
```

## 📊 SM-2 Algorithm

The application implements the SM-2 algorithm for spaced repetition:

- **Quality 0-2**: Resets interval (incorrect answer)
- **Quality 3-5**: Increases interval (correct answer)
- **Ease factor**: Adjusts based on answer quality
- **Intervals**: 1 day → 6 days → interval × ease factor

## 🎯 Architecture Benefits

1. **Maintainability**: Organized and easy to maintain code
2. **Scalability**: Clear separation allows independent component scaling
3. **Testability**: Each layer can be tested in isolation
4. **Flexibility**: Easy to change implementations (e.g., switch from SQLAlchemy to another ORM)
5. **Auditability**: Domain events allow tracking changes
6. **Performance**: CQRS allows optimizing reads and writes separately

## 🔍 Usage Example

```python
# Generate study block
GET /api/v1/study-block/user123?limit=20

# Submit answer
POST /api/v1/submit-answer
{
    "user_id": "user123",
    "word_id": 1,
    "quality": 4,
    "response_time": 2.5
}

# Get progress
GET /api/v1/progress/user123
```

## 📈 Next Improvements

- [ ] Implement Event Store
- [ ] Add optimized read projections
- [ ] Implement Redis cache
- [ ] Add metrics and monitoring
- [ ] Implement authentication and authorization
- [x] Add unit and integration tests
