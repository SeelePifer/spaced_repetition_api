"""
Unit tests for dependencies
"""
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from src.infrastructure.dependencies import (
    get_word_repository,
    get_user_progress_repository,
    get_study_session_repository,
    get_mediator
)
from src.infrastructure.repositories.sqlalchemy_repositories import (
    SQLAlchemyWordRepository,
    SQLAlchemyUserProgressRepository,
    SQLAlchemyStudySessionRepository
)
from src.application.mediator import CQRSMediator


class TestDependencies:
    """Test cases for dependency injection functions"""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database session"""
        return Mock(spec=Session)
    
    def test_get_word_repository_with_db(self, mock_db):
        """Test getting word repository with provided db"""
        repository = get_word_repository(mock_db)
        
        assert isinstance(repository, SQLAlchemyWordRepository)
        assert repository.db == mock_db
    
    @patch('src.infrastructure.dependencies.get_db')
    def test_get_word_repository_without_db(self, mock_get_db, mock_db):
        """Test getting word repository without provided db"""
        mock_get_db.return_value = iter([mock_db])
        
        repository = get_word_repository()
        
        assert isinstance(repository, SQLAlchemyWordRepository)
        assert repository.db == mock_db
    
    def test_get_user_progress_repository_with_db(self, mock_db):
        """Test getting user progress repository with provided db"""
        repository = get_user_progress_repository(mock_db)
        
        assert isinstance(repository, SQLAlchemyUserProgressRepository)
        assert repository.db == mock_db
    
    @patch('src.infrastructure.dependencies.get_db')
    def test_get_user_progress_repository_without_db(self, mock_get_db, mock_db):
        """Test getting user progress repository without provided db"""
        mock_get_db.return_value = iter([mock_db])
        
        repository = get_user_progress_repository()
        
        assert isinstance(repository, SQLAlchemyUserProgressRepository)
        assert repository.db == mock_db
    
    def test_get_study_session_repository_with_db(self, mock_db):
        """Test getting study session repository with provided db"""
        repository = get_study_session_repository(mock_db)
        
        assert isinstance(repository, SQLAlchemyStudySessionRepository)
        assert repository.db == mock_db
    
    @patch('src.infrastructure.dependencies.get_db')
    def test_get_study_session_repository_without_db(self, mock_get_db, mock_db):
        """Test getting study session repository without provided db"""
        mock_get_db.return_value = iter([mock_db])
        
        repository = get_study_session_repository()
        
        assert isinstance(repository, SQLAlchemyStudySessionRepository)
        assert repository.db == mock_db
    
    @patch('src.infrastructure.dependencies.get_word_repository')
    @patch('src.infrastructure.dependencies.get_user_progress_repository')
    @patch('src.infrastructure.dependencies.get_study_session_repository')
    def test_get_mediator_with_db(self, mock_session_repo, mock_progress_repo, mock_word_repo, mock_db):
        """Test getting mediator with provided db"""
        # Setup mock repositories
        mock_word_repo.return_value = Mock()
        mock_progress_repo.return_value = Mock()
        mock_session_repo.return_value = Mock()
        
        mediator = get_mediator(mock_db)
        
        assert isinstance(mediator, CQRSMediator)
        
        # Verify repositories were created with correct db
        mock_word_repo.assert_called_once_with(mock_db)
        mock_progress_repo.assert_called_once_with(mock_db)
        mock_session_repo.assert_called_once_with(mock_db)
    
    @patch('src.infrastructure.dependencies.get_db')
    @patch('src.infrastructure.dependencies.get_word_repository')
    @patch('src.infrastructure.dependencies.get_user_progress_repository')
    @patch('src.infrastructure.dependencies.get_study_session_repository')
    def test_get_mediator_without_db(self, mock_session_repo, mock_progress_repo, mock_word_repo, mock_get_db, mock_db):
        """Test getting mediator without provided db"""
        # Setup mocks
        mock_get_db.return_value = iter([mock_db])
        mock_word_repo.return_value = Mock()
        mock_progress_repo.return_value = Mock()
        mock_session_repo.return_value = Mock()
        
        mediator = get_mediator()
        
        assert isinstance(mediator, CQRSMediator)
        
        # Verify repositories were created with db from get_db()
        mock_word_repo.assert_called_once_with(mock_db)
        mock_progress_repo.assert_called_once_with(mock_db)
        mock_session_repo.assert_called_once_with(mock_db)
    
    def test_get_mediator_registers_handlers(self, mock_db):
        """Test that mediator registers all handlers correctly"""
        mediator = get_mediator(mock_db)
        
        # Verify mediator has registered handlers
        assert len(mediator._command_handlers) == 2  # SubmitAnswerCommand, GenerateStudyBlockCommand
        assert len(mediator._query_handlers) == 4   # GetUserProgressQuery, GetWordStatsQuery, GetGlobalStatsQuery, GetWordByIdQuery
    
    def test_repository_caching(self, mock_db):
        """Test that repositories are cached"""
        # Clear cache first
        get_word_repository.cache_clear()
        get_user_progress_repository.cache_clear()
        get_study_session_repository.cache_clear()
        
        # Get repositories twice
        repo1 = get_word_repository(mock_db)
        repo2 = get_word_repository(mock_db)
        
        # Should be the same instance due to caching
        assert repo1 is repo2
        
        # Test other repositories
        progress_repo1 = get_user_progress_repository(mock_db)
        progress_repo2 = get_user_progress_repository(mock_db)
        assert progress_repo1 is progress_repo2
        
        session_repo1 = get_study_session_repository(mock_db)
        session_repo2 = get_study_session_repository(mock_db)
        assert session_repo1 is session_repo2
    
    def test_mediator_caching(self, mock_db):
        """Test that mediator is cached"""
        # Clear cache first
        get_mediator.cache_clear()
        
        # Get mediator twice
        mediator1 = get_mediator(mock_db)
        mediator2 = get_mediator(mock_db)
        
        # Should be the same instance due to caching
        assert mediator1 is mediator2
