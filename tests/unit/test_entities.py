"""
Unit tests for domain entities
"""
import pytest
from datetime import datetime, timedelta
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.events.study_events import StudySessionCompleted, WordLearned


class TestWord:
    """Test cases for Word entity"""
    
    def test_valid_word_creation(self):
        """Test creating a valid word"""
        word = Word(
            id=1,
            word="hello",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
        
        assert word.id == 1
        assert word.word == "hello"
        assert word.frequency_rank.value == 100
        assert word.difficulty_level.value == 1
    
    def test_empty_word_raises_error(self):
        """Test that empty word raises ValueError"""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            Word(
                id=1,
                word="",
                frequency_rank=FrequencyRank(100),
                difficulty_level=DifficultyLevel(1)
            )
        
        with pytest.raises(ValueError, match="Word cannot be empty"):
            Word(
                id=1,
                word="   ",
                frequency_rank=FrequencyRank(100),
                difficulty_level=DifficultyLevel(1)
            )
    
    def test_is_difficult(self):
        """Test is_difficult method"""
        easy_word = Word(
            id=1,
            word="hello",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(2)
        )
        assert easy_word.is_difficult() is False
        
        hard_word = Word(
            id=2,
            word="complex",
            frequency_rank=FrequencyRank(2000),
            difficulty_level=DifficultyLevel(4)
        )
        assert hard_word.is_difficult() is True
    
    def test_is_common(self):
        """Test is_common method"""
        common_word = Word(
            id=1,
            word="hello",
            frequency_rank=FrequencyRank(100),
            difficulty_level=DifficultyLevel(1)
        )
        assert common_word.is_common() is True
        
        uncommon_word = Word(
            id=2,
            word="esoteric",
            frequency_rank=FrequencyRank(2000),
            difficulty_level=DifficultyLevel(3)
        )
        assert uncommon_word.is_common() is False


class TestUserProgress:
    """Test cases for UserProgress entity"""
    
    def test_valid_user_progress_creation(self):
        """Test creating valid user progress"""
        progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=0,
            ease_factor=2.5,
            interval=1
        )
        
        assert progress.id == 1
        assert progress.user_id == "user123"
        assert progress.word_id == 1
        assert progress.repetitions == 0
        assert progress.ease_factor == 2.5
        assert progress.interval == 1
    
    def test_empty_user_id_raises_error(self):
        """Test that empty user ID raises ValueError"""
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            UserProgress(
                id=1,
                user_id="",
                word_id=1
            )
    
    def test_invalid_word_id_raises_error(self):
        """Test that invalid word ID raises ValueError"""
        with pytest.raises(ValueError, match="Word ID must be positive"):
            UserProgress(
                id=1,
                user_id="user123",
                word_id=0
            )
    
    def test_invalid_ease_factor_raises_error(self):
        """Test that invalid ease factor raises ValueError"""
        with pytest.raises(ValueError, match="Ease factor cannot be less than 1.3"):
            UserProgress(
                id=1,
                user_id="user123",
                word_id=1,
                ease_factor=1.2
            )
    
    def test_update_progress_correct_answer_first_time(self):
        """Test updating progress with correct answer for first time"""
        progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=0,
            ease_factor=2.5,
            interval=1
        )
        
        quality = Quality(4)
        events = progress.update_progress(quality)
        
        assert progress.repetitions == 1
        assert progress.interval == 1
        assert progress.next_review is not None
        assert progress.last_review is not None
        
        # Check events
        assert len(events) == 2
        assert isinstance(events[0], StudySessionCompleted)
        assert isinstance(events[1], WordLearned)
        assert events[0].user_id == "user123"
        assert events[0].word_id == 1
        assert events[0].quality == 4
    
    def test_update_progress_correct_answer_second_time(self):
        """Test updating progress with correct answer for second time"""
        progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=1,
            ease_factor=2.5,
            interval=1
        )
        
        quality = Quality(4)
        events = progress.update_progress(quality)
        
        assert progress.repetitions == 2
        assert progress.interval == 6
        assert progress.next_review is not None
        assert progress.last_review is not None
        
        # Check events
        assert len(events) == 1
        assert isinstance(events[0], StudySessionCompleted)
    
    def test_update_progress_correct_answer_third_time(self):
        """Test updating progress with correct answer for third time"""
        progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=2,
            ease_factor=2.5,
            interval=6
        )
        
        quality = Quality(4)
        events = progress.update_progress(quality)
        
        assert progress.repetitions == 3
        assert progress.interval == 15  # 6 * 2.5
        assert progress.next_review is not None
        assert progress.last_review is not None
        
        # Check events
        assert len(events) == 1
        assert isinstance(events[0], StudySessionCompleted)
    
    def test_update_progress_incorrect_answer(self):
        """Test updating progress with incorrect answer"""
        progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=3,
            ease_factor=2.5,
            interval=15
        )
        
        quality = Quality(2)
        events = progress.update_progress(quality)
        
        assert progress.repetitions == 0
        assert progress.interval == 1
        assert progress.next_review is not None
        assert progress.last_review is not None
        
        # Check events
        assert len(events) == 1
        assert isinstance(events[0], StudySessionCompleted)
    
    def test_update_progress_ease_factor_adjustment(self):
        """Test that ease factor adjusts based on quality"""
        progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            repetitions=2,
            ease_factor=2.5,
            interval=6
        )
        
        # Perfect answer should increase ease factor
        quality = Quality(5)
        events = progress.update_progress(quality)
        
        assert progress.ease_factor > 2.5
        
        # Poor answer should decrease ease factor
        progress2 = UserProgress(
            id=2,
            user_id="user123",
            word_id=2,
            repetitions=2,
            ease_factor=2.5,
            interval=6
        )
        
        quality2 = Quality(3)
        events2 = progress2.update_progress(quality2)
        
        assert progress2.ease_factor < 2.5
    
    def test_is_due_for_review(self):
        """Test is_due_for_review method"""
        progress = UserProgress(
            id=1,
            user_id="user123",
            word_id=1,
            next_review=None
        )
        assert progress.is_due_for_review() is True
        
        # Past due
        past_due = UserProgress(
            id=2,
            user_id="user123",
            word_id=2,
            next_review=datetime.now() - timedelta(days=1)
        )
        assert past_due.is_due_for_review() is True
        
        # Not due yet
        not_due = UserProgress(
            id=3,
            user_id="user123",
            word_id=3,
            next_review=datetime.now() + timedelta(days=1)
        )
        assert not_due.is_due_for_review() is False


class TestStudySession:
    """Test cases for StudySession entity"""
    
    def test_valid_study_session_creation(self):
        """Test creating valid study session"""
        session = StudySession(
            id=1,
            word_id=1,
            user_id="user123",
            correct=True,
            response_time=2.5,
            timestamp=datetime.now(),
            quality=Quality(4)
        )
        
        assert session.id == 1
        assert session.word_id == 1
        assert session.user_id == "user123"
        assert session.correct is True
        assert session.response_time == 2.5
        assert session.quality.value == 4
    
    def test_empty_user_id_raises_error(self):
        """Test that empty user ID raises ValueError"""
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            StudySession(
                id=1,
                word_id=1,
                user_id="",
                correct=True,
                response_time=2.5,
                timestamp=datetime.now(),
                quality=Quality(4)
            )
    
    def test_invalid_word_id_raises_error(self):
        """Test that invalid word ID raises ValueError"""
        with pytest.raises(ValueError, match="Word ID must be positive"):
            StudySession(
                id=1,
                word_id=0,
                user_id="user123",
                correct=True,
                response_time=2.5,
                timestamp=datetime.now(),
                quality=Quality(4)
            )
    
    def test_negative_response_time_raises_error(self):
        """Test that negative response time raises ValueError"""
        with pytest.raises(ValueError, match="Response time cannot be negative"):
            StudySession(
                id=1,
                word_id=1,
                user_id="user123",
                correct=True,
                response_time=-1.0,
                timestamp=datetime.now(),
                quality=Quality(4)
            )
    
    def test_is_fast_response(self):
        """Test is_fast_response method"""
        fast_session = StudySession(
            id=1,
            word_id=1,
            user_id="user123",
            correct=True,
            response_time=1.5,
            timestamp=datetime.now(),
            quality=Quality(4)
        )
        assert fast_session.is_fast_response() is True
        
        slow_session = StudySession(
            id=2,
            word_id=2,
            user_id="user123",
            correct=True,
            response_time=3.0,
            timestamp=datetime.now(),
            quality=Quality(4)
        )
        assert slow_session.is_fast_response() is False
    
    def test_is_slow_response(self):
        """Test is_slow_response method"""
        slow_session = StudySession(
            id=1,
            word_id=1,
            user_id="user123",
            correct=True,
            response_time=15.0,
            timestamp=datetime.now(),
            quality=Quality(4)
        )
        assert slow_session.is_slow_response() is True
        
        fast_session = StudySession(
            id=2,
            word_id=2,
            user_id="user123",
            correct=True,
            response_time=5.0,
            timestamp=datetime.now(),
            quality=Quality(4)
        )
        assert fast_session.is_slow_response() is False
