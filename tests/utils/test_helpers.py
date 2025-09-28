"""
Test utilities and helpers
"""
import pytest
from typing import Dict, Any, List
from datetime import datetime, timedelta
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.value_objects.identifiers import UserId, WordId


class TestDataFactory:
    """Factory class for creating test data"""
    
    @staticmethod
    def create_word(
        word_id: int = 1,
        word: str = "hello",
        frequency_rank: int = 100,
        difficulty_level: int = 1
    ) -> Word:
        """Create a Word entity for testing"""
        # Ensure positive values
        if word_id <= 0:
            word_id = 1
        if frequency_rank <= 0:
            frequency_rank = 100
        if difficulty_level <= 0:
            difficulty_level = 1
            
        return Word(
            id=word_id,
            word=word,
            frequency_rank=FrequencyRank(frequency_rank),
            difficulty_level=DifficultyLevel(difficulty_level)
        )
    
    @staticmethod
    def create_user_progress(
        progress_id: int = 1,
        user_id: str = "user123",
        word_id: int = 1,
        repetitions: int = 0,
        ease_factor: float = 2.5,
        interval: int = 1,
        next_review: datetime = None,
        last_review: datetime = None
    ) -> UserProgress:
        """Create a UserProgress entity for testing"""
        # Ensure positive values
        if progress_id <= 0:
            progress_id = 1
        if word_id <= 0:
            word_id = 1
            
        return UserProgress(
            id=progress_id,
            user_id=user_id,
            word_id=word_id,
            repetitions=repetitions,
            ease_factor=ease_factor,
            interval=interval,
            next_review=next_review,
            last_review=last_review
        )
    
    @staticmethod
    def create_study_session(
        session_id: int = 1,
        word_id: int = 1,
        user_id: str = "user123",
        correct: bool = True,
        response_time: float = 2.5,
        timestamp: datetime = None,
        quality: int = 4
    ) -> StudySession:
        """Create a StudySession entity for testing"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Ensure positive values
        if session_id <= 0:
            session_id = 1
        if word_id <= 0:
            word_id = 1
            
        return StudySession(
            id=session_id,
            word_id=word_id,
            user_id=user_id,
            correct=correct,
            response_time=response_time,
            timestamp=timestamp,
            quality=Quality(quality)
        )
    
    @staticmethod
    def create_quality(value: int) -> Quality:
        """Create a Quality value object for testing"""
        return Quality(value)
    
    @staticmethod
    def create_difficulty_level(value: int) -> DifficultyLevel:
        """Create a DifficultyLevel value object for testing"""
        return DifficultyLevel(value)
    
    @staticmethod
    def create_frequency_rank(value: int) -> FrequencyRank:
        """Create a FrequencyRank value object for testing"""
        return FrequencyRank(value)
    
    @staticmethod
    def create_user_id(value: str) -> UserId:
        """Create a UserId value object for testing"""
        return UserId(value)
    
    @staticmethod
    def create_word_id(value: int) -> WordId:
        """Create a WordId value object for testing"""
        return WordId(value)


class TestAssertions:
    """Custom assertions for testing"""
    
    @staticmethod
    def assert_word_equal(actual: Word, expected: Word):
        """Assert that two Word entities are equal"""
        assert actual.id == expected.id
        assert actual.word == expected.word
        assert actual.frequency_rank.value == expected.frequency_rank.value
        assert actual.difficulty_level.value == expected.difficulty_level.value
    
    @staticmethod
    def assert_user_progress_equal(actual: UserProgress, expected: UserProgress):
        """Assert that two UserProgress entities are equal"""
        assert actual.id == expected.id
        assert actual.user_id == expected.user_id
        assert actual.word_id == expected.word_id
        assert actual.repetitions == expected.repetitions
        assert actual.ease_factor == expected.ease_factor
        assert actual.interval == expected.interval
        assert actual.next_review == expected.next_review
        assert actual.last_review == expected.last_review
    
    @staticmethod
    def assert_study_session_equal(actual: StudySession, expected: StudySession):
        """Assert that two StudySession entities are equal"""
        assert actual.id == expected.id
        assert actual.word_id == expected.word_id
        assert actual.user_id == expected.user_id
        assert actual.correct == expected.correct
        assert actual.response_time == expected.response_time
        assert actual.timestamp == expected.timestamp
        assert actual.quality.value == expected.quality.value
    
    @staticmethod
    def assert_datetime_close(actual: datetime, expected: datetime, delta_seconds: int = 5):
        """Assert that two datetimes are close to each other"""
        time_diff = abs((actual - expected).total_seconds())
        assert time_diff <= delta_seconds, f"Time difference {time_diff}s exceeds {delta_seconds}s"


class MockRepository:
    """Base mock repository for testing"""
    
    def __init__(self):
        self._data: Dict[Any, Any] = {}
        self._next_id = 1
    
    def _get_next_id(self) -> int:
        """Get next available ID"""
        id = self._next_id
        self._next_id += 1
        return id
    
    def clear(self):
        """Clear all data"""
        self._data.clear()
        self._next_id = 1


class MockWordRepository(MockRepository):
    """Mock word repository for testing"""
    
    async def find_by_id(self, word_id: WordId) -> Word:
        """Find word by ID"""
        return self._data.get(word_id.value)
    
    async def save(self, word: Word) -> Word:
        """Save word"""
        if not word.id:
            word.id = self._get_next_id()
        self._data[word.id] = word
        return word
    
    async def find_unstudied_words(self, user_id: UserId, limit: int) -> List[Word]:
        """Find unstudied words"""
        return list(self._data.values())[:limit]


class MockUserProgressRepository(MockRepository):
    """Mock user progress repository for testing"""
    
    async def find_by_user_and_word(self, user_id: UserId, word_id: WordId) -> UserProgress:
        """Find user progress by user and word"""
        key = f"{user_id.value}_{word_id.value}"
        return self._data.get(key)
    
    async def save(self, progress: UserProgress) -> UserProgress:
        """Save user progress"""
        if not progress.id:
            progress.id = self._get_next_id()
        key = f"{progress.user_id}_{progress.word_id}"
        self._data[key] = progress
        return progress
    
    async def find_words_due_for_review(self, user_id: UserId, limit: int) -> List[Word]:
        """Find words due for review"""
        return []


class MockStudySessionRepository(MockRepository):
    """Mock study session repository for testing"""
    
    async def save(self, session: StudySession) -> StudySession:
        """Save study session"""
        if not session.id:
            session.id = self._get_next_id()
        self._data[session.id] = session
        return session
    
    async def find_by_user(self, user_id: UserId) -> List[StudySession]:
        """Find study sessions by user"""
        return [s for s in self._data.values() if s.user_id == user_id.value]


@pytest.fixture
def test_data_factory():
    """Provide TestDataFactory instance"""
    return TestDataFactory()


@pytest.fixture
def test_assertions():
    """Provide TestAssertions instance"""
    return TestAssertions()


@pytest.fixture
def mock_word_repository():
    """Provide MockWordRepository instance"""
    return MockWordRepository()


@pytest.fixture
def mock_user_progress_repository():
    """Provide MockUserProgressRepository instance"""
    return MockUserProgressRepository()


@pytest.fixture
def mock_study_session_repository():
    """Provide MockStudySessionRepository instance"""
    return MockStudySessionRepository()
