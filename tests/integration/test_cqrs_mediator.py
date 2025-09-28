"""
Integration tests for CQRS mediator and handlers
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.mediator import CQRSMediator
from src.application.commands.study_commands import (
    SubmitAnswerCommand,
    GenerateStudyBlockCommand
)
from src.application.queries.study_queries import (
    GetUserProgressQuery,
    GetWordStatsQuery,
    GetGlobalStatsQuery
)
from src.application.dto.study_dto import StudySessionDto
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.value_objects.identifiers import UserId, WordId


@pytest.mark.integration
class TestCQRSMediator:
    """Integration tests for CQRS mediator"""
    
    @pytest.fixture
    def mock_repositories(self):
        """Create mock repositories"""
        word_repo = AsyncMock()
        user_progress_repo = AsyncMock()
        study_session_repo = AsyncMock()
        return word_repo, user_progress_repo, study_session_repo
    
    @pytest.fixture
    def mediator(self, mock_repositories):
        """Create mediator with mock repositories"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        mediator = CQRSMediator()
        
        # Register command handlers
        from src.application.handlers.command_handlers import (
            SubmitAnswerCommandHandler,
            GenerateStudyBlockCommandHandler
        )
        
        submit_handler = SubmitAnswerCommandHandler(
            word_repository=word_repo,
            user_progress_repository=user_progress_repo,
            study_session_repository=study_session_repo
        )
        
        generate_handler = GenerateStudyBlockCommandHandler(
            word_repository=word_repo,
            user_progress_repository=user_progress_repo
        )
        
        mediator.register_command_handler(SubmitAnswerCommand, submit_handler)
        mediator.register_command_handler(GenerateStudyBlockCommand, generate_handler)
        
        return mediator
    
    @pytest.mark.asyncio
    async def test_send_command_submit_answer(self, mediator, mock_repositories):
        """Test sending SubmitAnswerCommand through mediator"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        # Setup mocks
        sample_word = Word(
            id=1,
            word="hello",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
        
        word_repo.find_by_id.return_value = sample_word
        user_progress_repo.find_by_user_and_word.return_value = None
        user_progress_repo.save.return_value = None
        study_session_repo.save.return_value = None
        
        # Create command
        session_data = StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        )
        command = SubmitAnswerCommand(session_data=session_data)
        
        # Send command through mediator
        result = await mediator.send_command(command)
        
        # Verify result
        assert result.message == "Respuesta registrada exitosamente"
        assert result.word_id == 1
        assert result.quality == 4
        assert result.next_review is not None
        assert result.repetitions == 1
        assert result.ease_factor == 2.5
        assert result.interval_days == 1
        
        # Verify repository calls
        word_repo.find_by_id.assert_called_once()
        user_progress_repo.find_by_user_and_word.assert_called_once()
        user_progress_repo.save.assert_called_once()
        study_session_repo.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_command_generate_study_block(self, mediator, mock_repositories):
        """Test sending GenerateStudyBlockCommand through mediator"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        # Setup mocks
        sample_words = [
            Word(
                id=1,
                word="hello",
                frequency_rank=FrequencyRank(100),
                difficulty_level=DifficultyLevel(1)
            ),
            Word(
                id=2,
                word="world",
                frequency_rank=FrequencyRank(200),
                difficulty_level=DifficultyLevel(2)
            )
        ]
        
        user_progress_repo.find_words_due_for_review.return_value = sample_words
        
        # Create command
        command = GenerateStudyBlockCommand(user_id="user123", limit=20)
        
        # Send command through mediator
        result = await mediator.send_command(command)
        
        # Verify result
        assert result.block_id.startswith("user123_")
        assert len(result.words) == 2
        assert result.total_words == 2
        assert result.difficulty_distribution == {1: 1, 2: 1}
        
        # Verify repository calls
        user_progress_repo.find_words_due_for_review.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_command_unregistered_handler(self, mediator):
        """Test sending command with unregistered handler"""
        from src.application.commands.study_commands import CreateWordCommand
        
        command = CreateWordCommand(
            word="test",
            frequency_rank=100,
            difficulty_level=1
        )
        
        with pytest.raises(ValueError, match="No handler registered for command"):
            await mediator.send_command(command)
    
    @pytest.mark.asyncio
    async def test_send_query_unregistered_handler(self, mediator):
        """Test sending query with unregistered handler"""
        query = GetUserProgressQuery(user_id="user123")
        
        with pytest.raises(ValueError, match="No handler registered for query"):
            await mediator.send_query(query)
    
    @pytest.mark.asyncio
    async def test_register_multiple_handlers_same_command(self, mediator, mock_repositories):
        """Test registering multiple handlers for the same command type"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        # Create another handler
        from src.application.handlers.command_handlers import SubmitAnswerCommandHandler
        
        another_handler = SubmitAnswerCommandHandler(
            word_repository=word_repo,
            user_progress_repository=user_progress_repo,
            study_session_repository=study_session_repo
        )
        
        # Registering the same command type should replace the previous handler
        mediator.register_command_handler(SubmitAnswerCommand, another_handler)
        
        # Should not raise an error
        assert True
    
    @pytest.mark.asyncio
    async def test_command_handler_error_propagation(self, mediator, mock_repositories):
        """Test that errors from command handlers are properly propagated"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        # Setup mock to raise an error
        word_repo.find_by_id.side_effect = Exception("Database error")
        
        # Create command
        session_data = StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        )
        command = SubmitAnswerCommand(session_data=session_data)
        
        # Send command through mediator should raise the error
        with pytest.raises(Exception, match="Database error"):
            await mediator.send_command(command)
    
    @pytest.mark.asyncio
    async def test_mediator_with_real_handlers(self):
        """Test mediator with real handlers and mock repositories"""
        # Create mock repositories
        word_repo = AsyncMock()
        user_progress_repo = AsyncMock()
        study_session_repo = AsyncMock()
        
        # Create mediator
        mediator = CQRSMediator()
        
        # Register real handlers
        from src.application.handlers.command_handlers import (
            SubmitAnswerCommandHandler,
            GenerateStudyBlockCommandHandler
        )
        
        submit_handler = SubmitAnswerCommandHandler(
            word_repository=word_repo,
            user_progress_repository=user_progress_repo,
            study_session_repository=study_session_repo
        )
        
        generate_handler = GenerateStudyBlockCommandHandler(
            word_repository=word_repo,
            user_progress_repository=user_progress_repo
        )
        
        mediator.register_command_handler(SubmitAnswerCommand, submit_handler)
        mediator.register_command_handler(GenerateStudyBlockCommand, generate_handler)
        
        # Test with SubmitAnswerCommand
        sample_word = Word(
            id=1,
            word="hello",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
        
        word_repo.find_by_id.return_value = sample_word
        user_progress_repo.find_by_user_and_word.return_value = None
        user_progress_repo.save.return_value = None
        study_session_repo.save.return_value = None
        
        session_data = StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        )
        command = SubmitAnswerCommand(session_data=session_data)
        
        result = await mediator.send_command(command)
        
        assert result.message == "Respuesta registrada exitosamente"
        assert result.word_id == 1
        assert result.quality == 4
        
        # Test with GenerateStudyBlockCommand
        sample_words = [
            Word(
                id=1,
                word="hello",
                frequency_rank=FrequencyRank(100),
                difficulty_level=DifficultyLevel(1)
            )
        ]
        
        user_progress_repo.find_words_due_for_review.return_value = sample_words
        
        command = GenerateStudyBlockCommand(user_id="user123", limit=20)
        
        result = await mediator.send_command(command)
        
        assert result.block_id.startswith("user123_")
        assert len(result.words) == 1
        assert result.total_words == 1
