"""
Test configuration and fixtures for the Spaced Repetition API
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import os
import tempfile

# Set test database URL
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from src.infrastructure.database.models import Base, get_db
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.value_objects.identifiers import UserId, WordId
from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_db() -> Generator[Session, None, None]:
    """Create a test database session"""
    # Create in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_word() -> Word:
    """Create a sample word entity"""
    return Word(
        id=1,
        word="hello",
        frequency_rank=FrequencyRank(100),
        difficulty_level=DifficultyLevel(1)
    )


@pytest.fixture
def sample_user_progress() -> UserProgress:
    """Create a sample user progress entity"""
    return UserProgress(
        id=1,
        user_id="user123",
        word_id=1,
        repetitions=0,
        ease_factor=2.5,
        interval=1,
        next_review=None,
        last_review=None
    )


@pytest.fixture
def sample_study_session() -> StudySession:
    """Create a sample study session entity"""
    return StudySession(
        id=1,
        word_id=1,
        user_id="user123",
        correct=True,
        response_time=2.5,
        timestamp=datetime.now(),
        quality=Quality(4)
    )


@pytest.fixture
def sample_quality_values():
    """Sample quality values for testing"""
    return {
        "perfect": Quality(5),
        "good": Quality(4),
        "correct": Quality(3),
        "poor": Quality(2),
        "incorrect": Quality(1),
        "very_poor": Quality(0)
    }


@pytest.fixture
def sample_difficulty_levels():
    """Sample difficulty levels for testing"""
    return {
        "beginner": DifficultyLevel(1),
        "easy": DifficultyLevel(2),
        "intermediate": DifficultyLevel(3),
        "hard": DifficultyLevel(4),
        "expert": DifficultyLevel(5)
    }


@pytest.fixture
def sample_frequency_ranks():
    """Sample frequency ranks for testing"""
    return {
        "very_common": FrequencyRank(50),
        "common": FrequencyRank(500),
        "uncommon": FrequencyRank(2000)
    }


@pytest.fixture
def sample_user_ids():
    """Sample user IDs for testing"""
    return {
        "valid": UserId("user123"),
        "short": UserId("ab"),
        "empty": UserId("")
    }


@pytest.fixture
def sample_word_ids():
    """Sample word IDs for testing"""
    return {
        "valid": WordId(1),
        "zero": WordId(0),
        "negative": WordId(-1)
    }


@pytest.fixture
def mock_word_repository():
    """Mock word repository for testing"""
    class MockWordRepository:
        def __init__(self):
            self.words = {}
        
        async def find_by_id(self, word_id: WordId) -> Word:
            return self.words.get(word_id.value)
        
        async def save(self, word: Word) -> Word:
            if not word.id:
                word.id = len(self.words) + 1
            self.words[word.id] = word
            return word
        
        async def find_unstudied_words(self, user_id: UserId, limit: int) -> list[Word]:
            return list(self.words.values())[:limit]
    
    return MockWordRepository()


@pytest.fixture
def mock_user_progress_repository():
    """Mock user progress repository for testing"""
    class MockUserProgressRepository:
        def __init__(self):
            self.progress = {}
        
        async def find_by_user_and_word(self, user_id: UserId, word_id: WordId) -> UserProgress:
            key = f"{user_id.value}_{word_id.value}"
            return self.progress.get(key)
        
        async def save(self, progress: UserProgress) -> UserProgress:
            if not progress.id:
                progress.id = len(self.progress) + 1
            key = f"{progress.user_id}_{progress.word_id}"
            self.progress[key] = progress
            return progress
        
        async def find_words_due_for_review(self, user_id: UserId, limit: int) -> list[Word]:
            return []
    
    return MockUserProgressRepository()


@pytest.fixture
def mock_study_session_repository():
    """Mock study session repository for testing"""
    class MockStudySessionRepository:
        def __init__(self):
            self.sessions = {}
        
        async def save(self, session: StudySession) -> StudySession:
            if not session.id:
                session.id = len(self.sessions) + 1
            self.sessions[session.id] = session
            return session
    
    return MockStudySessionRepository()
