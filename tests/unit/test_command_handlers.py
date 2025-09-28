"""
Unit tests for application command handlers
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from src.application.handlers.command_handlers import (
    CommandHandler,
    SubmitAnswerCommandHandler,
    GenerateStudyBlockCommandHandler
)
from src.application.commands.study_commands import (
    SubmitAnswerCommand,
    GenerateStudyBlockCommand
)
from src.application.dto.study_dto import StudySessionDto, StudyBlockDto
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.value_objects.identifiers import UserId, WordId
from src.shared.exceptions.domain_exceptions import (
    WordNotFoundException,
    InvalidQualityException,
    InvalidResponseTimeException,
    NoWordsAvailableException
)


class TestCommandHandler:
    """Test cases for CommandHandler base class"""
    
    def test_command_handler_is_abstract(self):
        """Test that CommandHandler cannot be instantiated directly"""
        with pytest.raises(TypeError):
            CommandHandler()


class TestSubmitAnswerCommandHandler:
    """Test cases for SubmitAnswerCommandHandler"""
    
    @pytest.fixture
    def mock_repositories(self):
        """Create mock repositories"""
        word_repo = AsyncMock()
        user_progress_repo = AsyncMock()
        study_session_repo = AsyncMock()
        return word_repo, user_progress_repo, study_session_repo
    
    @pytest.fixture
    def handler(self, mock_repositories):
        """Create handler with mock repositories"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        return SubmitAnswerCommandHandler(
            word_repository=word_repo,
            user_progress_repository=user_progress_repo,
            study_session_repository=study_session_repo
        )
    
    @pytest.fixture
    def sample_word(self):
        """Create sample word"""
        return Word(
            id=1,
            word="hello",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
    
    @pytest.fixture
    def sample_session_data(self):
        """Create sample session data"""
        return StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        )
    
    @pytest.mark.asyncio
    async def test_handle_valid_command(self, handler, mock_repositories, sample_word, sample_session_data):
        """Test handling valid command"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        # Setup mocks
        word_repo.find_by_id.return_value = sample_word
        user_progress_repo.find_by_user_and_word.return_value = None
        user_progress_repo.save.return_value = None
        study_session_repo.save.return_value = None
        
        command = SubmitAnswerCommand(session_data=sample_session_data)
        
        result = await handler.handle(command)
        
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
    async def test_handle_invalid_command(self, handler):
        """Test handling invalid command"""
        with pytest.raises(ValueError, match="Comando inválido"):
            await handler.handle("invalid_command")
    
    @pytest.mark.asyncio
    async def test_handle_invalid_quality(self, handler, sample_session_data):
        """Test handling command with invalid quality"""
        sample_session_data.quality = 6
        command = SubmitAnswerCommand(session_data=sample_session_data)
        
        with pytest.raises(InvalidQualityException):
            await handler.handle(command)
    
    @pytest.mark.asyncio
    async def test_handle_invalid_response_time(self, handler, sample_session_data):
        """Test handling command with invalid response time"""
        sample_session_data.response_time = -1.0
        command = SubmitAnswerCommand(session_data=sample_session_data)
        
        with pytest.raises(InvalidResponseTimeException):
            await handler.handle(command)
    
    @pytest.mark.asyncio
    async def test_handle_word_not_found(self, handler, mock_repositories, sample_session_data):
        """Test handling command when word is not found"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        word_repo.find_by_id.return_value = None
        
        command = SubmitAnswerCommand(session_data=sample_session_data)
        
        with pytest.raises(WordNotFoundException):
            await handler.handle(command)
    
    @pytest.mark.asyncio
    async def test_handle_existing_progress(self, handler, mock_repositories, sample_word, sample_session_data):
        """Test handling command with existing user progress"""
        word_repo, user_progress_repo, study_session_repo = mock_repositories
        
        existing_progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=2,
            ease_factor=2.5,
            interval=6
        )
        
        word_repo.find_by_id.return_value = sample_word
        user_progress_repo.find_by_user_and_word.return_value = existing_progress
        user_progress_repo.save.return_value = None
        study_session_repo.save.return_value = None
        
        command = SubmitAnswerCommand(session_data=sample_session_data)
        
        result = await handler.handle(command)
        
        # Verify result shows updated progress
        assert result.repetitions == 3
        assert result.interval_days == 15  # 6 * 2.5


class TestGenerateStudyBlockCommandHandler:
    """Test cases for GenerateStudyBlockCommandHandler"""
    
    @pytest.fixture
    def mock_repositories(self):
        """Create mock repositories"""
        word_repo = AsyncMock()
        user_progress_repo = AsyncMock()
        return word_repo, user_progress_repo
    
    @pytest.fixture
    def handler(self, mock_repositories):
        """Create handler with mock repositories"""
        word_repo, user_progress_repo = mock_repositories
        return GenerateStudyBlockCommandHandler(
            word_repository=word_repo,
            user_progress_repository=user_progress_repo
        )
    
    @pytest.fixture
    def sample_words(self):
        """Create sample words"""
        return [
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
    
    @pytest.mark.asyncio
    async def test_handle_valid_command_with_review_words(self, handler, mock_repositories, sample_words):
        """Test handling valid command with words due for review"""
        word_repo, user_progress_repo = mock_repositories
        
        user_progress_repo.find_words_due_for_review.return_value = sample_words
        
        command = GenerateStudyBlockCommand(user_id="user123", limit=20)
        
        result = await handler.handle(command)
        
        # Verify result
        assert isinstance(result, StudyBlockDto)
        assert result.block_id.startswith("user123_")
        assert len(result.words) == 2
        assert result.total_words == 2
        assert result.difficulty_distribution == {1: 1, 2: 1}
        
        # Verify repository calls
        user_progress_repo.find_words_due_for_review.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handle_command_with_insufficient_review_words(self, handler, mock_repositories, sample_words):
        """Test handling command when there are insufficient words for review"""
        word_repo, user_progress_repo = mock_repositories
        
        # Only one word due for review
        user_progress_repo.find_words_due_for_review.return_value = [sample_words[0]]
        # Additional new words available
        word_repo.find_unstudied_words.return_value = [sample_words[1]]
        
        command = GenerateStudyBlockCommand(user_id="user123", limit=20)
        
        result = await handler.handle(command)
        
        # Verify result includes both review and new words
        assert len(result.words) == 2
        assert result.total_words == 2
        
        # Verify repository calls
        user_progress_repo.find_words_due_for_review.assert_called_once()
        word_repo.find_unstudied_words.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handle_command_no_words_available(self, handler, mock_repositories):
        """Test handling command when no words are available"""
        word_repo, user_progress_repo = mock_repositories
        
        user_progress_repo.find_words_due_for_review.return_value = []
        word_repo.find_unstudied_words.return_value = []
        
        command = GenerateStudyBlockCommand(user_id="user123", limit=20)
        
        with pytest.raises(NoWordsAvailableException):
            await handler.handle(command)
    
    @pytest.mark.asyncio
    async def test_handle_invalid_command(self, handler):
        """Test handling invalid command"""
        with pytest.raises(ValueError, match="Comando inválido"):
            await handler.handle("invalid_command")
    
    @pytest.mark.asyncio
    async def test_handle_command_with_custom_limit(self, handler, mock_repositories, sample_words):
        """Test handling command with custom limit"""
        word_repo, user_progress_repo = mock_repositories
        
        user_progress_repo.find_words_due_for_review.return_value = sample_words
        
        command = GenerateStudyBlockCommand(user_id="user123", limit=5)
        
        result = await handler.handle(command)
        
        # Verify result respects the limit
        assert len(result.words) == 2  # Only 2 words available
        assert result.total_words == 2
