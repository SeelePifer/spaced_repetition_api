from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List
from ..value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from ..events.study_events import DomainEvent, StudySessionCompleted, WordLearned


@dataclass
class Word:
    """Word Entity - represents a word in the system"""
    id: Optional[int]
    word: str
    frequency_rank: FrequencyRank
    difficulty_level: DifficultyLevel
    
    def __post_init__(self):
        if not self.word or not self.word.strip():
            raise ValueError("Word cannot be empty")
    
    def is_difficult(self) -> bool:
        """Determines if the word is difficult based on its level"""
        return self.difficulty_level.value > 3
    
    def is_common(self) -> bool:
        """Determines if the word is common based on its frequency"""
        return self.frequency_rank.value <= 1000


@dataclass
class UserProgress:
    """UserProgress Entity - represents user progress with a word"""
    id: Optional[int]
    user_id: str
    word_id: int
    repetitions: int = 0
    ease_factor: float = 2.5
    interval: int = 1  # days
    next_review: Optional[datetime] = None
    last_review: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.user_id or not self.user_id.strip():
            raise ValueError("User ID cannot be empty")
        if self.word_id <= 0:
            raise ValueError("Word ID must be positive")
        if self.ease_factor < 1.3:
            raise ValueError("Ease factor cannot be less than 1.3")
    
    def update_progress(self, quality: Quality) -> List[DomainEvent]:
        """Updates progress using SM-2 algorithm and returns domain events"""
        events = []
        
        if quality.value < 3:
            # Incorrect answer - reset
            self.repetitions = 0
            self.interval = 1
        else:
            # Correct answer
            self.repetitions += 1
            
            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            # Update ease_factor based on quality
            self.ease_factor = max(1.3,
                                   self.ease_factor + (0.1 - (5 - quality.value) * (0.08 + (5 - quality.value) * 0.02)))
        
        # Update dates
        self.next_review = datetime.now() + timedelta(days=self.interval)
        self.last_review = datetime.now()
        
        # Generate events
        events.append(StudySessionCompleted(
            user_id=self.user_id,
            word_id=self.word_id,
            quality=quality.value,
            repetitions=self.repetitions,
            ease_factor=self.ease_factor
        ))
        
        # If it's the first time learning correctly
        if self.repetitions == 1 and quality.value >= 3:
            events.append(WordLearned(
                user_id=self.user_id,
                word_id=self.word_id
            ))
        
        return events
    
    def is_due_for_review(self) -> bool:
        """Checks if the word is ready for review"""
        if not self.next_review:
            return True
        return datetime.now() >= self.next_review


@dataclass
class StudySession:
    """StudySession Entity - represents a study session"""
    id: Optional[int]
    word_id: int
    user_id: str
    correct: bool
    response_time: float
    timestamp: datetime
    quality: Quality
    
    def __post_init__(self):
        if not self.user_id or not self.user_id.strip():
            raise ValueError("User ID cannot be empty")
        if self.word_id <= 0:
            raise ValueError("Word ID must be positive")
        if self.response_time < 0:
            raise ValueError("Response time cannot be negative")
    
    def is_fast_response(self) -> bool:
        """Determines if the response was fast (< 2 seconds)"""
        return self.response_time < 2.0
    
    def is_slow_response(self) -> bool:
        """Determines if the response was slow (> 10 seconds)"""
        return self.response_time > 10.0
