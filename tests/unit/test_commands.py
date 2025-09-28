"""
Unit tests for application commands
"""
import pytest
from src.application.commands.study_commands import (
    Command,
    SubmitAnswerCommand,
    GenerateStudyBlockCommand,
    CreateWordCommand,
    UpdateUserProgressCommand
)
from src.application.dto.study_dto import StudySessionDto


class TestCommand:
    """Test cases for Command base class"""
    
    def test_command_is_abstract(self):
        """Test that Command cannot be instantiated directly"""
        with pytest.raises(TypeError):
            Command()


class TestSubmitAnswerCommand:
    """Test cases for SubmitAnswerCommand"""
    
    def test_submit_answer_command_creation(self):
        """Test creating SubmitAnswerCommand"""
        session_data = StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        )
        
        command = SubmitAnswerCommand(session_data=session_data)
        
        assert command.session_data == session_data
        assert isinstance(command, Command)
    
    def test_submit_answer_command_with_session_data(self):
        """Test SubmitAnswerCommand with different session data"""
        session_data = StudySessionDto(
            word_id=2,
            user_id="user456",
            quality=3,
            response_time=1.8
        )
        
        command = SubmitAnswerCommand(session_data=session_data)
        
        assert command.session_data.word_id == 2
        assert command.session_data.user_id == "user456"
        assert command.session_data.quality == 3
        assert command.session_data.response_time == 1.8


class TestGenerateStudyBlockCommand:
    """Test cases for GenerateStudyBlockCommand"""
    
    def test_generate_study_block_command_creation(self):
        """Test creating GenerateStudyBlockCommand with default limit"""
        command = GenerateStudyBlockCommand(user_id="user123")
        
        assert command.user_id == "user123"
        assert command.limit == 20
        assert isinstance(command, Command)
    
    def test_generate_study_block_command_with_custom_limit(self):
        """Test GenerateStudyBlockCommand with custom limit"""
        command = GenerateStudyBlockCommand(user_id="user123", limit=50)
        
        assert command.user_id == "user123"
        assert command.limit == 50
    
    def test_generate_study_block_command_with_zero_limit(self):
        """Test GenerateStudyBlockCommand with zero limit"""
        command = GenerateStudyBlockCommand(user_id="user123", limit=0)
        
        assert command.user_id == "user123"
        assert command.limit == 0


class TestCreateWordCommand:
    """Test cases for CreateWordCommand"""
    
    def test_create_word_command_creation(self):
        """Test creating CreateWordCommand"""
        command = CreateWordCommand(
            word="hello",
            frequency_rank=100,
            difficulty_level=1
        )
        
        assert command.word == "hello"
        assert command.frequency_rank == 100
        assert command.difficulty_level == 1
        assert isinstance(command, Command)
    
    def test_create_word_command_with_different_values(self):
        """Test CreateWordCommand with different values"""
        command = CreateWordCommand(
            word="complex",
            frequency_rank=2000,
            difficulty_level=5
        )
        
        assert command.word == "complex"
        assert command.frequency_rank == 2000
        assert command.difficulty_level == 5


class TestUpdateUserProgressCommand:
    """Test cases for UpdateUserProgressCommand"""
    
    def test_update_user_progress_command_creation(self):
        """Test creating UpdateUserProgressCommand"""
        command = UpdateUserProgressCommand(
            user_id="user123",
            word_id=1,
            quality=4,
            response_time=2.5
        )
        
        assert command.user_id == "user123"
        assert command.word_id == 1
        assert command.quality == 4
        assert command.response_time == 2.5
        assert isinstance(command, Command)
    
    def test_update_user_progress_command_with_different_values(self):
        """Test UpdateUserProgressCommand with different values"""
        command = UpdateUserProgressCommand(
            user_id="user456",
            word_id=2,
            quality=2,
            response_time=5.0
        )
        
        assert command.user_id == "user456"
        assert command.word_id == 2
        assert command.quality == 2
        assert command.response_time == 5.0
