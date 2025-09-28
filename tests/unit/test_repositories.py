"""
Unit tests for SQLAlchemy repositories
"""
import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from sqlalchemy.orm import Session

from src.infrastructure.repositories.sqlalchemy_repositories import (
    SQLAlchemyWordRepository,
    SQLAlchemyUserProgressRepository,
    SQLAlchemyStudySessionRepository
)
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.value_objects.identifiers import UserId, WordId
from src.infrastructure.database.models import WordModel, UserProgressModel, StudySessionModel


class TestSQLAlchemyWordRepository:
    """Test cases for SQLAlchemyWordRepository"""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database session"""
        db = Mock(spec=Session)
        
        # Create a mock query object
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_query.all.return_value = []
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 0
        
        # Configure the db.query to return our mock query
        db.query.return_value = mock_query
        db.add.return_value = None
        db.commit.return_value = None
        db.refresh.return_value = None
        
        return db
    
    @pytest.fixture
    def repository(self, mock_db):
        """Create repository instance"""
        return SQLAlchemyWordRepository(mock_db)
    
    def test_repository_initialization(self, repository, mock_db):
        """Test repository initialization"""
        assert repository is not None
        assert repository.db == mock_db
        assert isinstance(repository, SQLAlchemyWordRepository)
    
    def test_repository_has_required_methods(self, repository):
        """Test that repository has all required methods"""
        required_methods = [
            'find_by_id', 'find_all', 'find_by_difficulty',
            'find_unstudied_words', 'save', '_to_domain_entity'
        ]
        
        for method in required_methods:
            assert hasattr(repository, method), f"Repository missing method: {method}"
            assert callable(getattr(repository, method)), f"Method {method} is not callable"
    
    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self, repository, mock_db):
        """Test finding word by ID when not found"""
        # Setup mock to return None
        mock_query = mock_db.query.return_value
        mock_query.first.return_value = None
        
        result = await repository.find_by_id(WordId(999))
        
        assert result is None
        mock_db.query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_find_all_empty(self, repository, mock_db):
        """Test finding all words when none exist"""
        # Setup mock to return empty list
        mock_query = mock_db.query.return_value
        mock_query.all.return_value = []
        
        result = await repository.find_all()
        
        assert result == []
        mock_db.query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_save_new_word(self, repository, mock_db):
        """Test saving new word"""
        word = Word(
            id=None,  # New word
            word="new_word",
            frequency_rank=FrequencyRank(200),
            difficulty_level=DifficultyLevel(2)
        )
        
        # Mock the refresh to return a model
        mock_model = Mock()
        mock_model.id = 1
        mock_model.word = "new_word"
        mock_model.frequency_rank = 200
        mock_model.difficulty_level = 2
        mock_db.refresh.return_value = mock_model
        
        result = await repository.save(word)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


class TestSQLAlchemyUserProgressRepository:
    """Test cases for SQLAlchemyUserProgressRepository"""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database session"""
        db = Mock(spec=Session)
        
        # Create a mock query object
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_query.all.return_value = []
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 0
        
        # Configure the db.query to return our mock query
        db.query.return_value = mock_query
        db.add.return_value = None
        db.commit.return_value = None
        db.refresh.return_value = None
        
        return db
    
    @pytest.fixture
    def repository(self, mock_db):
        """Create repository instance"""
        return SQLAlchemyUserProgressRepository(mock_db)
    
    def test_repository_initialization(self, repository, mock_db):
        """Test repository initialization"""
        assert repository is not None
        assert repository.db == mock_db
        assert isinstance(repository, SQLAlchemyUserProgressRepository)
    
    def test_repository_has_required_methods(self, repository):
        """Test that repository has all required methods"""
        required_methods = [
            'find_by_user_and_word', 'find_by_user', 'find_words_due_for_review',
            'save', 'count_words_studied', 'count_words_due_for_review', '_to_domain_entity'
        ]
        
        for method in required_methods:
            assert hasattr(repository, method), f"Repository missing method: {method}"
            assert callable(getattr(repository, method)), f"Method {method} is not callable"
    
    @pytest.mark.asyncio
    async def test_find_by_user_and_word_not_found(self, repository, mock_db):
        """Test finding progress by user and word when not found"""
        # Setup mock to return None
        mock_query = mock_db.query.return_value
        mock_query.first.return_value = None
        
        result = await repository.find_by_user_and_word(UserId("user123"), WordId(999))
        
        assert result is None
        mock_db.query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_save_new_progress(self, repository, mock_db):
        """Test saving new progress"""
        progress = UserProgress(
            id=None,  # New progress
            user_id="user123",
            word_id=1,
            repetitions=1,
            ease_factor=2.5,
            interval=1,
            next_review=datetime.now(),
            last_review=datetime.now()
        )
        
        # Mock the refresh to return a model
        mock_model = Mock()
        mock_model.id = 1
        mock_model.user_id = "user123"
        mock_model.word_id = 1
        mock_model.repetitions = 1
        mock_model.ease_factor = 2.5
        mock_model.interval = 1
        mock_db.refresh.return_value = mock_model
        
        result = await repository.save(progress)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


class TestSQLAlchemyStudySessionRepository:
    """Test cases for SQLAlchemyStudySessionRepository"""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database session"""
        db = Mock(spec=Session)
        
        # Create a mock query object
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_query.all.return_value = []
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 0
        
        # Configure the db.query to return our mock query
        db.query.return_value = mock_query
        db.add.return_value = None
        db.commit.return_value = None
        db.refresh.return_value = None
        
        return db
    
    @pytest.fixture
    def repository(self, mock_db):
        """Create repository instance"""
        return SQLAlchemyStudySessionRepository(mock_db)
    
    def test_repository_initialization(self, repository, mock_db):
        """Test repository initialization"""
        assert repository is not None
        assert repository.db == mock_db
        assert isinstance(repository, SQLAlchemyStudySessionRepository)
    
    def test_repository_has_required_methods(self, repository):
        """Test that repository has all required methods"""
        required_methods = [
            'save', 'find_by_user', 'find_by_word',
            'count_total_sessions', 'count_correct_sessions', '_to_domain_entity'
        ]
        
        for method in required_methods:
            assert hasattr(repository, method), f"Repository missing method: {method}"
            assert callable(getattr(repository, method)), f"Method {method} is not callable"
    
    @pytest.mark.asyncio
    async def test_save_session(self, repository, mock_db):
        """Test saving study session"""
        session = StudySession(
            id=None,  # New session
            word_id=1,
            user_id="user123",
            correct=True,
            response_time=2.5,
            timestamp=datetime.now(),
            quality=Quality(4)
        )
        
        # Mock the refresh to return a model
        mock_model = Mock()
        mock_model.id = 1
        mock_model.word_id = 1
        mock_model.user_id = "user123"
        mock_model.correct = True
        mock_model.response_time = 2.5
        mock_model.timestamp = datetime.now()
        mock_model.quality = 4
        mock_db.refresh.return_value = mock_model
        
        result = await repository.save(session)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_count_total_sessions(self, repository, mock_db):
        """Test counting total sessions"""
        # Setup mock to return count
        mock_query = mock_db.query.return_value
        mock_query.count.return_value = 100
        
        result = await repository.count_total_sessions()
        
        assert result == 100
        mock_db.query.assert_called_once()