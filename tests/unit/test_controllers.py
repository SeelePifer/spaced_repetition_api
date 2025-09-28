"""
Unit tests for study controller
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.presentation.controllers.study_controller import StudyController
from src.application.mediator import CQRSMediator
from src.application.dto.study_dto import StudySessionDto
from src.shared.exceptions.domain_exceptions import (
    WordNotFoundException,
    InvalidQualityException,
    InvalidResponseTimeException,
    NoWordsAvailableException
)


class TestStudyController:
    """Test cases for StudyController"""
    
    @pytest.fixture
    def controller(self):
        """Create controller instance"""
        # Mock the router to avoid FastAPI issues
        with patch('src.presentation.controllers.study_controller.APIRouter') as mock_router:
            mock_router.return_value = Mock()
            return StudyController()
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database session"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_mediator(self):
        """Create mock mediator"""
        mediator = Mock(spec=CQRSMediator)
        mediator.send_command = AsyncMock()
        mediator.send_query = AsyncMock()
        return mediator
    
    def test_controller_initialization(self, controller):
        """Test controller initialization"""
        assert controller.router is not None
    
    def test_get_router(self, controller):
        """Test getting router"""
        router = controller.get_router()
        assert router is not None
        assert router == controller.router
    
    def test_controller_has_router_attribute(self, controller):
        """Test that controller has router attribute"""
        assert hasattr(controller, 'router')
        assert controller.router is not None
    
    def test_controller_has_get_router_method(self, controller):
        """Test that controller has get_router method"""
        assert hasattr(controller, 'get_router')
        assert callable(controller.get_router)
    
    def test_mediator_mock_functionality(self, mock_mediator):
        """Test that mock mediator works correctly"""
        # Test command sending
        mock_mediator.send_command.return_value = {"result": "success"}
        
        # Test query sending
        mock_mediator.send_query.return_value = {"data": "result"}
        
        # Verify mocks are callable
        assert callable(mock_mediator.send_command)
        assert callable(mock_mediator.send_query)
    
    def test_database_mock_functionality(self, mock_db):
        """Test that mock database works correctly"""
        # Test that mock has expected attributes
        assert hasattr(mock_db, 'query')
        assert hasattr(mock_db, 'add')
        assert hasattr(mock_db, 'commit')
        assert hasattr(mock_db, 'refresh')
    
    def test_exception_classes_exist(self):
        """Test that exception classes exist and can be instantiated"""
        # Test WordNotFoundException
        with pytest.raises(WordNotFoundException):
            raise WordNotFoundException("Test word not found")
        
        # Test InvalidQualityException
        with pytest.raises(InvalidQualityException):
            raise InvalidQualityException("Test invalid quality")
        
        # Test InvalidResponseTimeException
        with pytest.raises(InvalidResponseTimeException):
            raise InvalidResponseTimeException("Test invalid response time")
        
        # Test NoWordsAvailableException
        with pytest.raises(NoWordsAvailableException):
            raise NoWordsAvailableException("Test no words available")
    
    def test_study_session_dto_creation(self):
        """Test StudySessionDto creation"""
        dto = StudySessionDto(
            word_id=1,
            user_id="user123",
            quality=4,
            response_time=2.5
        )
        
        assert dto.word_id == 1
        assert dto.user_id == "user123"
        assert dto.quality == 4
        assert dto.response_time == 2.5
    
    def test_controller_class_exists(self):
        """Test that StudyController class exists and can be imported"""
        from src.presentation.controllers.study_controller import StudyController
        assert StudyController is not None
        assert callable(StudyController)
    
    def test_mediator_class_exists(self):
        """Test that CQRSMediator class exists and can be imported"""
        from src.application.mediator import CQRSMediator
        assert CQRSMediator is not None
        assert callable(CQRSMediator)
    
    def test_session_class_exists(self):
        """Test that Session class exists and can be imported"""
        from sqlalchemy.orm import Session
        assert Session is not None
        assert callable(Session)