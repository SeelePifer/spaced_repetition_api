"""
Unit tests for domain events
"""
import pytest
from datetime import datetime
from src.domain.events.study_events import DomainEvent, StudySessionCompleted, WordLearned


class TestDomainEvent:
    """Test cases for DomainEvent base class"""
    
    def test_domain_event_is_abstract(self):
        """Test that DomainEvent cannot be instantiated directly"""
        with pytest.raises(TypeError):
            DomainEvent()


class TestStudySessionCompleted:
    """Test cases for StudySessionCompleted event"""
    
    def test_study_session_completed_creation(self):
        """Test creating StudySessionCompleted event"""
        event = StudySessionCompleted(
            user_id="user123",
            word_id=1,
            quality=4,
            repetitions=2,
            ease_factor=2.5
        )
        
        assert event.user_id == "user123"
        assert event.word_id == 1
        assert event.quality == 4
        assert event.repetitions == 2
        assert event.ease_factor == 2.5
        assert isinstance(event, DomainEvent)
    
    def test_study_session_completed_with_timestamp(self):
        """Test StudySessionCompleted event with custom timestamp"""
        timestamp = datetime.now()
        event = StudySessionCompleted(
            user_id="user123",
            word_id=1,
            quality=4,
            repetitions=2,
            ease_factor=2.5,
            timestamp=timestamp
        )
        
        assert event.timestamp == timestamp


class TestWordLearned:
    """Test cases for WordLearned event"""
    
    def test_word_learned_creation(self):
        """Test creating WordLearned event"""
        event = WordLearned(
            user_id="user123",
            word_id=1
        )
        
        assert event.user_id == "user123"
        assert event.word_id == 1
        assert isinstance(event, DomainEvent)
    
    def test_word_learned_with_timestamp(self):
        """Test WordLearned event with custom timestamp"""
        timestamp = datetime.now()
        event = WordLearned(
            user_id="user123",
            word_id=1,
            timestamp=timestamp
        )
        
        assert event.timestamp == timestamp
