from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


class DomainEvent(ABC):
    """Base class for all domain events"""
    
    @abstractmethod
    def occurred_on(self) -> datetime:
        """Returns when the event occurred"""
        pass
    
    @abstractmethod
    def event_data(self) -> Dict[str, Any]:
        """Returns event data"""
        pass


@dataclass
class StudySessionCompleted(DomainEvent):
    """Event fired when a study session is completed"""
    user_id: str
    word_id: int
    quality: int
    repetitions: int
    ease_factor: float
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def occurred_on(self) -> datetime:
        return self.timestamp
    
    def event_data(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "word_id": self.word_id,
            "quality": self.quality,
            "repetitions": self.repetitions,
            "ease_factor": self.ease_factor,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class WordLearned(DomainEvent):
    """Event fired when a user learns a word for the first time"""
    user_id: str
    word_id: int
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def occurred_on(self) -> datetime:
        return self.timestamp
    
    def event_data(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "word_id": self.word_id,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class StudyBlockGenerated(DomainEvent):
    """Event fired when a study block is generated"""
    user_id: str
    block_id: str
    word_count: int
    difficulty_distribution: Dict[int, int]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def occurred_on(self) -> datetime:
        return self.timestamp
    
    def event_data(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "block_id": self.block_id,
            "word_count": self.word_count,
            "difficulty_distribution": self.difficulty_distribution,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class UserProgressUpdated(DomainEvent):
    """Event fired when user progress is updated"""
    user_id: str
    word_id: int
    old_repetitions: int
    new_repetitions: int
    old_ease_factor: float
    new_ease_factor: float
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def occurred_on(self) -> datetime:
        return self.timestamp
    
    def event_data(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "word_id": self.word_id,
            "old_repetitions": self.old_repetitions,
            "new_repetitions": self.new_repetitions,
            "old_ease_factor": self.old_ease_factor,
            "new_ease_factor": self.new_ease_factor,
            "timestamp": self.timestamp.isoformat()
        }
