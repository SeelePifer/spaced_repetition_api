"""
Integration tests for database operations
"""
import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.infrastructure.database.models import WordModel, UserProgressModel, StudySessionModel
from src.domain.entities.word import Word, UserProgress, StudySession
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank


@pytest.mark.integration
class TestDatabaseOperations:
    """Integration tests for database operations"""
    
    def test_create_word_model(self, test_db: Session):
        """Test creating a word in the database"""
        word = WordModel(
            word="hello",
            frequency_rank=100,
            difficulty_level=1
        )
        
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        assert word.id is not None
        assert word.word == "hello"
        assert word.frequency_rank == 100
        assert word.difficulty_level == 1
    
    def test_create_user_progress_model(self, test_db: Session):
        """Test creating user progress in the database"""
        # First create a word
        word = WordModel(
            word="hello",
            frequency_rank=100,
            difficulty_level=1
        )
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        # Then create user progress
        progress = UserProgressModel(
            user_id="user123",
            word_id=word.id,
            repetitions=0,
            ease_factor=2.5,
            interval=1,
            next_review=datetime.now() + timedelta(days=1)
        )
        
        test_db.add(progress)
        test_db.commit()
        test_db.refresh(progress)
        
        assert progress.id is not None
        assert progress.user_id == "user123"
        assert progress.word_id == word.id
        assert progress.repetitions == 0
        assert progress.ease_factor == 2.5
        assert progress.interval == 1
    
    def test_create_study_session_model(self, test_db: Session):
        """Test creating study session in the database"""
        # First create a word
        word = WordModel(
            word="hello",
            frequency_rank=100,
            difficulty_level=1
        )
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        # Then create study session
        session = StudySessionModel(
            word_id=word.id,
            user_id="user123",
            correct=True,
            response_time=2.5,
            timestamp=datetime.now(),
            quality=4
        )
        
        test_db.add(session)
        test_db.commit()
        test_db.refresh(session)
        
        assert session.id is not None
        assert session.word_id == word.id
        assert session.user_id == "user123"
        assert session.correct is True
        assert session.response_time == 2.5
        assert session.quality == 4
    
    def test_word_user_progress_relationship(self, test_db: Session):
        """Test relationship between word and user progress"""
        # Create word
        word = WordModel(
            word="hello",
            frequency_rank=100,
            difficulty_level=1
        )
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        # Create user progress
        progress = UserProgressModel(
            user_id="user123",
            word_id=word.id,
            repetitions=2,
            ease_factor=2.5,
            interval=6
        )
        test_db.add(progress)
        test_db.commit()
        test_db.refresh(progress)
        
        # Test relationship
        assert progress.word.id == word.id
        assert progress.word.word == "hello"
        assert len(word.user_progress) == 1
        assert word.user_progress[0].user_id == "user123"
    
    def test_query_words_by_difficulty(self, test_db: Session):
        """Test querying words by difficulty level"""
        # Create words with different difficulty levels
        words = [
            WordModel(word="easy1", frequency_rank=100, difficulty_level=1),
            WordModel(word="easy2", frequency_rank=200, difficulty_level=1),
            WordModel(word="hard1", frequency_rank=1000, difficulty_level=4),
            WordModel(word="hard2", frequency_rank=2000, difficulty_level=5)
        ]
        
        for word in words:
            test_db.add(word)
        test_db.commit()
        
        # Query easy words
        easy_words = test_db.query(WordModel).filter(
            WordModel.difficulty_level == 1
        ).all()
        
        assert len(easy_words) == 2
        assert all(word.difficulty_level == 1 for word in easy_words)
        
        # Query hard words
        hard_words = test_db.query(WordModel).filter(
            WordModel.difficulty_level >= 4
        ).all()
        
        assert len(hard_words) == 2
        assert all(word.difficulty_level >= 4 for word in hard_words)
    
    def test_query_user_progress_by_user(self, test_db: Session):
        """Test querying user progress by user ID"""
        # Create words
        words = [
            WordModel(word="word1", frequency_rank=100, difficulty_level=1),
            WordModel(word="word2", frequency_rank=200, difficulty_level=2)
        ]
        
        for word in words:
            test_db.add(word)
        test_db.commit()
        
        # Create user progress for different users
        progress_data = [
            UserProgressModel(user_id="user123", word_id=words[0].id, repetitions=1),
            UserProgressModel(user_id="user123", word_id=words[1].id, repetitions=2),
            UserProgressModel(user_id="user456", word_id=words[0].id, repetitions=3)
        ]
        
        for progress in progress_data:
            test_db.add(progress)
        test_db.commit()
        
        # Query progress for user123
        user123_progress = test_db.query(UserProgressModel).filter(
            UserProgressModel.user_id == "user123"
        ).all()
        
        assert len(user123_progress) == 2
        assert all(p.user_id == "user123" for p in user123_progress)
        
        # Query progress for user456
        user456_progress = test_db.query(UserProgressModel).filter(
            UserProgressModel.user_id == "user456"
        ).all()
        
        assert len(user456_progress) == 1
        assert user456_progress[0].user_id == "user456"
    
    def test_query_study_sessions_by_user(self, test_db: Session):
        """Test querying study sessions by user ID"""
        # Create word
        word = WordModel(word="hello", frequency_rank=100, difficulty_level=1)
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        # Create study sessions for different users
        sessions = [
            StudySessionModel(
                word_id=word.id,
                user_id="user123",
                correct=True,
                response_time=2.0,
                quality=4
            ),
            StudySessionModel(
                word_id=word.id,
                user_id="user123",
                correct=False,
                response_time=5.0,
                quality=2
            ),
            StudySessionModel(
                word_id=word.id,
                user_id="user456",
                correct=True,
                response_time=1.5,
                quality=5
            )
        ]
        
        for session in sessions:
            test_db.add(session)
        test_db.commit()
        
        # Query sessions for user123
        user123_sessions = test_db.query(StudySessionModel).filter(
            StudySessionModel.user_id == "user123"
        ).all()
        
        assert len(user123_sessions) == 2
        assert all(s.user_id == "user123" for s in user123_sessions)
        
        # Query correct sessions for user123
        correct_sessions = test_db.query(StudySessionModel).filter(
            StudySessionModel.user_id == "user123",
            StudySessionModel.correct == True
        ).all()
        
        assert len(correct_sessions) == 1
        assert correct_sessions[0].correct is True
    
    def test_update_user_progress(self, test_db: Session):
        """Test updating user progress"""
        # Create word
        word = WordModel(word="hello", frequency_rank=100, difficulty_level=1)
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        # Create initial progress
        progress = UserProgressModel(
            user_id="user123",
            word_id=word.id,
            repetitions=0,
            ease_factor=2.5,
            interval=1
        )
        test_db.add(progress)
        test_db.commit()
        test_db.refresh(progress)
        
        # Update progress
        progress.repetitions = 2
        progress.ease_factor = 2.7
        progress.interval = 6
        progress.next_review = datetime.now() + timedelta(days=6)
        
        test_db.commit()
        test_db.refresh(progress)
        
        assert progress.repetitions == 2
        assert progress.ease_factor == 2.7
        assert progress.interval == 6
        assert progress.next_review is not None
    
    def test_delete_user_progress(self, test_db: Session):
        """Test deleting user progress"""
        # Create word
        word = WordModel(word="hello", frequency_rank=100, difficulty_level=1)
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        # Create progress
        progress = UserProgressModel(
            user_id="user123",
            word_id=word.id,
            repetitions=2,
            ease_factor=2.5,
            interval=6
        )
        test_db.add(progress)
        test_db.commit()
        test_db.refresh(progress)
        
        progress_id = progress.id
        
        # Delete progress
        test_db.delete(progress)
        test_db.commit()
        
        # Verify deletion
        deleted_progress = test_db.query(UserProgressModel).filter(
            UserProgressModel.id == progress_id
        ).first()
        
        assert deleted_progress is None
    
    def test_transaction_rollback(self, test_db: Session):
        """Test transaction rollback on error"""
        # Create word
        word = WordModel(word="hello", frequency_rank=100, difficulty_level=1)
        test_db.add(word)
        test_db.commit()
        test_db.refresh(word)
        
        # Start transaction
        progress = UserProgressModel(
            user_id="user123",
            word_id=word.id,
            repetitions=1,
            ease_factor=2.5,
            interval=1
        )
        test_db.add(progress)
        
        # Simulate error and rollback
        try:
            # This should cause an error
            invalid_progress = UserProgressModel(
                user_id="",  # Invalid empty user_id
                word_id=word.id,
                repetitions=1,
                ease_factor=2.5,
                interval=1
            )
            test_db.add(invalid_progress)
            test_db.commit()
        except Exception:
            test_db.rollback()
        
        # Verify that the first progress was saved (it was committed before the error)
        saved_progress = test_db.query(UserProgressModel).filter(
            UserProgressModel.user_id == "user123"
        ).first()
        
        assert saved_progress is not None
        assert saved_progress.user_id == "user123"
