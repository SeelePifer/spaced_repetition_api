"""
Unit tests for query handlers
"""
import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from src.application.handlers.query_handlers import (
    QueryHandler,
    GetUserProgressQueryHandler,
    GetWordStatsQueryHandler,
    GetGlobalStatsQueryHandler,
    GetWordByIdQueryHandler
)
from src.application.queries.study_queries import (
    GetUserProgressQuery,
    GetWordStatsQuery,
    GetGlobalStatsQuery,
    GetWordByIdQuery
)
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.value_objects.identifiers import UserId, WordId
from src.shared.exceptions.domain_exceptions import WordNotFoundException


class TestQueryHandler:
    """Test cases for QueryHandler base class"""
    
    def test_query_handler_is_abstract(self):
        """Test that QueryHandler is abstract"""
        with pytest.raises(TypeError):
            QueryHandler()


class TestGetUserProgressQueryHandler:
    """Test cases for GetUserProgressQueryHandler"""
    
    @pytest.fixture
    def mock_repositories(self):
        """Create mock repositories"""
        user_progress_repo = Mock()
        word_repo = Mock()
        return user_progress_repo, word_repo
    
    @pytest.fixture
    def handler(self, mock_repositories):
        """Create handler instance"""
        user_progress_repo, word_repo = mock_repositories
        return GetUserProgressQueryHandler(user_progress_repo, word_repo)
    
    @pytest.fixture
    def sample_word(self):
        """Create sample word"""
        return Word(
            id=1,
            word="test",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
    
    @pytest.fixture
    def sample_progress(self):
        """Create sample user progress"""
        return UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=1,
            ease_factor=2.5,
            interval=1,
            next_review=datetime.now(),
            last_review=datetime.now()
        )
    
    @pytest.mark.asyncio
    async def test_handle_valid_query(self, handler, mock_repositories, sample_word, sample_progress):
        """Test handling valid query"""
        user_progress_repo, word_repo = mock_repositories
        
        # Setup mocks
        user_progress_repo.find_by_user = AsyncMock(return_value=[sample_progress])
        word_repo.find_by_id = AsyncMock(return_value=sample_word)
        
        query = GetUserProgressQuery(user_id="user123")
        result = await handler.handle(query)
        
        # Verify result
        assert result.user_id == "user123"
        assert result.total_words_studied == 1
        assert len(result.progress) == 1
        assert result.progress[0].word == "test"
        assert result.progress[0].word_id == 1
    
    @pytest.mark.asyncio
    async def test_handle_invalid_query(self, handler):
        """Test handling invalid query"""
        query = GetWordStatsQuery(word_id=1)  # Wrong query type
        
        with pytest.raises(ValueError, match="Query inválida"):
            await handler.handle(query)
    
    @pytest.mark.asyncio
    async def test_handle_query_with_no_progress(self, handler, mock_repositories):
        """Test handling query when user has no progress"""
        user_progress_repo, word_repo = mock_repositories
        
        # Setup mocks
        user_progress_repo.find_by_user = AsyncMock(return_value=[])
        
        query = GetUserProgressQuery(user_id="user123")
        result = await handler.handle(query)
        
        # Verify result
        assert result.user_id == "user123"
        assert result.total_words_studied == 0
        assert result.words_due_for_review == 0
        assert len(result.progress) == 0
    
    @pytest.mark.asyncio
    async def test_handle_query_with_missing_word(self, handler, mock_repositories, sample_progress):
        """Test handling query when word is not found"""
        user_progress_repo, word_repo = mock_repositories
        
        # Setup mocks
        user_progress_repo.find_by_user = AsyncMock(return_value=[sample_progress])
        word_repo.find_by_id = AsyncMock(return_value=None)
        
        query = GetUserProgressQuery(user_id="user123")
        result = await handler.handle(query)
        
        # Verify result - should skip missing words
        assert result.user_id == "user123"
        assert result.total_words_studied == 0
        assert len(result.progress) == 0


class TestGetWordStatsQueryHandler:
    """Test cases for GetWordStatsQueryHandler"""
    
    @pytest.fixture
    def mock_repositories(self):
        """Create mock repositories"""
        word_repo = Mock()
        study_session_repo = Mock()
        return word_repo, study_session_repo
    
    @pytest.fixture
    def handler(self, mock_repositories):
        """Create handler instance"""
        word_repo, study_session_repo = mock_repositories
        return GetWordStatsQueryHandler(word_repo, study_session_repo)
    
    @pytest.fixture
    def sample_word(self):
        """Create sample word"""
        return Word(
            id=1,
            word="test",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
    
    @pytest.fixture
    def sample_sessions(self):
        """Create sample study sessions"""
        return [
            StudySession(
                id=1,
                word_id=1,
                user_id="user123",
                correct=True,
                response_time=2.5,
                timestamp=datetime.now(),
                quality=Quality(4)
            ),
            StudySession(
                id=2,
                word_id=1,
                user_id="user123",
                correct=False,
                response_time=5.0,
                timestamp=datetime.now(),
                quality=Quality(2)
            )
        ]
    
    @pytest.mark.asyncio
    async def test_handle_valid_query(self, handler, mock_repositories, sample_word, sample_sessions):
        """Test handling valid query"""
        word_repo, study_session_repo = mock_repositories
        
        # Setup mocks
        word_repo.find_by_id = AsyncMock(return_value=sample_word)
        study_session_repo.find_by_word = AsyncMock(return_value=sample_sessions)
        study_session_repo.count_correct_sessions = AsyncMock(return_value=1)
        
        query = GetWordStatsQuery(word_id=1)
        result = await handler.handle(query)
        
        # Verify result
        assert result.word.id == 1
        assert result.word.word == "test"
        assert result.total_attempts == 2
        assert result.correct_attempts == 1
        assert result.accuracy_percentage == 50.0
        assert result.average_response_time == 3.75
    
    @pytest.mark.asyncio
    async def test_handle_invalid_query(self, handler):
        """Test handling invalid query"""
        query = GetUserProgressQuery(user_id="user123")  # Wrong query type
        
        with pytest.raises(ValueError, match="Query inválida"):
            await handler.handle(query)
    
    @pytest.mark.asyncio
    async def test_handle_word_not_found(self, handler, mock_repositories):
        """Test handling query when word is not found"""
        word_repo, study_session_repo = mock_repositories
        
        # Setup mocks
        word_repo.find_by_id = AsyncMock(return_value=None)
        
        query = GetWordStatsQuery(word_id=999)
        
        with pytest.raises(WordNotFoundException):
            await handler.handle(query)
    
    @pytest.mark.asyncio
    async def test_handle_query_with_no_sessions(self, handler, mock_repositories, sample_word):
        """Test handling query when word has no sessions"""
        word_repo, study_session_repo = mock_repositories
        
        # Setup mocks
        word_repo.find_by_id = AsyncMock(return_value=sample_word)
        study_session_repo.find_by_word = AsyncMock(return_value=[])
        study_session_repo.count_correct_sessions = AsyncMock(return_value=0)
        
        query = GetWordStatsQuery(word_id=1)
        result = await handler.handle(query)
        
        # Verify result
        assert result.total_attempts == 0
        assert result.correct_attempts == 0
        assert result.accuracy_percentage == 0
        assert result.average_response_time == 0


class TestGetGlobalStatsQueryHandler:
    """Test cases for GetGlobalStatsQueryHandler"""
    
    @pytest.fixture
    def mock_repositories(self):
        """Create mock repositories"""
        word_repo = Mock()
        study_session_repo = Mock()
        user_progress_repo = Mock()
        return word_repo, study_session_repo, user_progress_repo
    
    @pytest.fixture
    def handler(self, mock_repositories):
        """Create handler instance"""
        word_repo, study_session_repo, user_progress_repo = mock_repositories
        return GetGlobalStatsQueryHandler(word_repo, study_session_repo, user_progress_repo)
    
    @pytest.fixture
    def sample_words(self):
        """Create sample words"""
        return [
            Word(
                id=1,
                word="test1",
                frequency_rank=FrequencyRank(100),
                difficulty_level=DifficultyLevel(1)
            ),
            Word(
                id=2,
                word="test2",
                frequency_rank=FrequencyRank(200),
                difficulty_level=DifficultyLevel(2)
            )
        ]
    
    @pytest.mark.asyncio
    async def test_handle_valid_query(self, handler, mock_repositories, sample_words):
        """Test handling valid query"""
        word_repo, study_session_repo, user_progress_repo = mock_repositories
        
        # Setup mocks
        word_repo.find_all = AsyncMock(return_value=sample_words)
        study_session_repo.count_total_sessions = AsyncMock(return_value=10)
        
        query = GetGlobalStatsQuery()
        result = await handler.handle(query)
        
        # Verify result
        assert result.total_words == 2
        assert result.total_study_sessions == 10
        assert result.total_users == 0  # Not implemented yet
        assert result.difficulty_distribution == {1: 1, 2: 1}
        assert result.average_sessions_per_word == 5.0
    
    @pytest.mark.asyncio
    async def test_handle_invalid_query(self, handler):
        """Test handling invalid query"""
        query = GetUserProgressQuery(user_id="user123")  # Wrong query type
        
        with pytest.raises(ValueError, match="Query inválida"):
            await handler.handle(query)
    
    @pytest.mark.asyncio
    async def test_handle_query_with_no_words(self, handler, mock_repositories):
        """Test handling query when there are no words"""
        word_repo, study_session_repo, user_progress_repo = mock_repositories
        
        # Setup mocks
        word_repo.find_all = AsyncMock(return_value=[])
        study_session_repo.count_total_sessions = AsyncMock(return_value=0)
        
        query = GetGlobalStatsQuery()
        result = await handler.handle(query)
        
        # Verify result
        assert result.total_words == 0
        assert result.total_study_sessions == 0
        assert result.difficulty_distribution == {}
        assert result.average_sessions_per_word == 0


class TestGetWordByIdQueryHandler:
    """Test cases for GetWordByIdQueryHandler"""
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository"""
        return Mock()
    
    @pytest.fixture
    def handler(self, mock_repository):
        """Create handler instance"""
        return GetWordByIdQueryHandler(mock_repository)
    
    @pytest.fixture
    def sample_word(self):
        """Create sample word"""
        return Word(
            id=1,
            word="test",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
    
    @pytest.mark.asyncio
    async def test_handle_valid_query(self, handler, mock_repository, sample_word):
        """Test handling valid query"""
        # Setup mock
        mock_repository.find_by_id = AsyncMock(return_value=sample_word)
        
        query = GetWordByIdQuery(word_id=1)
        result = await handler.handle(query)
        
        # Verify result
        assert result.id == 1
        assert result.word == "test"
        assert result.frequency_rank == 100
        assert result.difficulty_level == 1
    
    @pytest.mark.asyncio
    async def test_handle_invalid_query(self, handler):
        """Test handling invalid query"""
        query = GetUserProgressQuery(user_id="user123")  # Wrong query type
        
        with pytest.raises(ValueError, match="Query inválida"):
            await handler.handle(query)
    
    @pytest.mark.asyncio
    async def test_handle_word_not_found(self, handler, mock_repository):
        """Test handling query when word is not found"""
        # Setup mock
        mock_repository.find_by_id = AsyncMock(return_value=None)
        
        query = GetWordByIdQuery(word_id=999)
        
        with pytest.raises(WordNotFoundException):
            await handler.handle(query)
