"""
Unit tests for CQRS mediator
"""
import pytest
from unittest.mock import Mock, AsyncMock

from src.application.mediator import Mediator, CQRSMediator
from src.application.commands.study_commands import SubmitAnswerCommand, GenerateStudyBlockCommand
from src.application.queries.study_queries import GetUserProgressQuery, GetWordStatsQuery
from src.application.handlers.command_handlers import CommandHandler
from src.application.handlers.query_handlers import QueryHandler
from src.application.dto.study_dto import StudySessionDto


class TestMediator:
    """Test cases for Mediator base class"""
    
    def test_mediator_is_abstract(self):
        """Test that Mediator is abstract"""
        with pytest.raises(TypeError):
            Mediator()


class TestCQRSMediator:
    """Test cases for CQRSMediator"""
    
    @pytest.fixture
    def mediator(self):
        """Create mediator instance"""
        return CQRSMediator()
    
    @pytest.fixture
    def mock_command_handler(self):
        """Create mock command handler"""
        handler = Mock(spec=CommandHandler)
        handler.handle = AsyncMock(return_value={"message": "success"})
        return handler
    
    @pytest.fixture
    def mock_query_handler(self):
        """Create mock query handler"""
        handler = Mock(spec=QueryHandler)
        handler.handle = AsyncMock(return_value={"data": "result"})
        return handler
    
    def test_register_command_handler(self, mediator, mock_command_handler):
        """Test registering command handler"""
        command = SubmitAnswerCommand(session_data=StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        ))
        
        mediator.register_command_handler(type(command), mock_command_handler)
        
        # Verify handler is registered
        assert type(command) in mediator._command_handlers
        assert mediator._command_handlers[type(command)] == mock_command_handler
    
    def test_register_query_handler(self, mediator, mock_query_handler):
        """Test registering query handler"""
        query = GetUserProgressQuery(user_id="user123")
        
        mediator.register_query_handler(type(query), mock_query_handler)
        
        # Verify handler is registered
        assert type(query) in mediator._query_handlers
        assert mediator._query_handlers[type(query)] == mock_query_handler
    
    @pytest.mark.asyncio
    async def test_send_command_success(self, mediator, mock_command_handler):
        """Test sending command successfully"""
        command = SubmitAnswerCommand(session_data=StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        ))
        
        mediator.register_command_handler(type(command), mock_command_handler)
        
        result = await mediator.send_command(command)
        
        # Verify result
        assert result == {"message": "success"}
        mock_command_handler.handle.assert_called_once_with(command)
    
    @pytest.mark.asyncio
    async def test_send_command_no_handler(self, mediator):
        """Test sending command with no registered handler"""
        command = SubmitAnswerCommand(session_data=StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        ))
        
        with pytest.raises(ValueError, match="No handler registered for command SubmitAnswerCommand"):
            await mediator.send_command(command)
    
    @pytest.mark.asyncio
    async def test_send_query_success(self, mediator, mock_query_handler):
        """Test sending query successfully"""
        query = GetUserProgressQuery(user_id="user123")
        
        mediator.register_query_handler(type(query), mock_query_handler)
        
        result = await mediator.send_query(query)
        
        # Verify result
        assert result == {"data": "result"}
        mock_query_handler.handle.assert_called_once_with(query)
    
    @pytest.mark.asyncio
    async def test_send_query_no_handler(self, mediator):
        """Test sending query with no registered handler"""
        query = GetUserProgressQuery(user_id="user123")
        
        with pytest.raises(ValueError, match="No handler registered for query GetUserProgressQuery"):
            await mediator.send_query(query)
    
    @pytest.mark.asyncio
    async def test_send_command_handler_error(self, mediator):
        """Test sending command when handler raises error"""
        command = SubmitAnswerCommand(session_data=StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        ))
        
        # Create handler that raises error
        handler = Mock(spec=CommandHandler)
        handler.handle = AsyncMock(side_effect=ValueError("Handler error"))
        
        mediator.register_command_handler(type(command), handler)
        
        with pytest.raises(ValueError, match="Handler error"):
            await mediator.send_command(command)
    
    @pytest.mark.asyncio
    async def test_send_query_handler_error(self, mediator):
        """Test sending query when handler raises error"""
        query = GetUserProgressQuery(user_id="user123")
        
        # Create handler that raises error
        handler = Mock(spec=QueryHandler)
        handler.handle = AsyncMock(side_effect=ValueError("Handler error"))
        
        mediator.register_query_handler(type(query), handler)
        
        with pytest.raises(ValueError, match="Handler error"):
            await mediator.send_query(query)
    
    def test_multiple_command_handlers(self, mediator):
        """Test registering multiple command handlers"""
        submit_handler = Mock(spec=CommandHandler)
        generate_handler = Mock(spec=CommandHandler)
        
        submit_command = SubmitAnswerCommand(session_data=StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        ))
        generate_command = GenerateStudyBlockCommand(user_id="user123", limit=10)
        
        mediator.register_command_handler(type(submit_command), submit_handler)
        mediator.register_command_handler(type(generate_command), generate_handler)
        
        # Verify both handlers are registered
        assert len(mediator._command_handlers) == 2
        assert mediator._command_handlers[type(submit_command)] == submit_handler
        assert mediator._command_handlers[type(generate_command)] == generate_handler
    
    def test_multiple_query_handlers(self, mediator):
        """Test registering multiple query handlers"""
        progress_handler = Mock(spec=QueryHandler)
        stats_handler = Mock(spec=QueryHandler)
        
        progress_query = GetUserProgressQuery(user_id="user123")
        stats_query = GetWordStatsQuery(word_id=1)
        
        mediator.register_query_handler(type(progress_query), progress_handler)
        mediator.register_query_handler(type(stats_query), stats_handler)
        
        # Verify both handlers are registered
        assert len(mediator._query_handlers) == 2
        assert mediator._query_handlers[type(progress_query)] == progress_handler
        assert mediator._query_handlers[type(stats_query)] == stats_handler
    
    def test_handler_replacement(self, mediator):
        """Test replacing existing handler"""
        command = SubmitAnswerCommand(session_data=StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        ))
        
        handler1 = Mock(spec=CommandHandler)
        handler2 = Mock(spec=CommandHandler)
        
        # Register first handler
        mediator.register_command_handler(type(command), handler1)
        assert mediator._command_handlers[type(command)] == handler1
        
        # Replace with second handler
        mediator.register_command_handler(type(command), handler2)
        assert mediator._command_handlers[type(command)] == handler2
        assert len(mediator._command_handlers) == 1  # Still only one entry
