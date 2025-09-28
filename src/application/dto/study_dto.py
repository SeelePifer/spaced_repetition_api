from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class WordDto:
    """DTO to represent a word"""
    id: int
    word: str
    frequency_rank: int
    difficulty_level: int


@dataclass
class StudySessionDto:
    """DTO for a study session"""
    word_id: int
    user_id: str
    quality: int
    response_time: float = 0.0


@dataclass
class StudySessionResponseDto:
    """DTO for study session response"""
    message: str
    word_id: int
    quality: int
    next_review: datetime
    repetitions: int
    ease_factor: float
    interval_days: int


@dataclass
class StudyBlockDto:
    """DTO for a study block"""
    block_id: str
    words: List[WordDto]
    created_at: datetime
    difficulty_distribution: Dict[int, int]
    total_words: int


@dataclass
class UserProgressDto:
    """DTO for user progress"""
    word: str
    word_id: int
    repetitions: int
    ease_factor: float
    interval_days: int
    next_review: datetime
    last_review: Optional[datetime]
    difficulty_level: int


@dataclass
class UserProgressResponseDto:
    """DTO for user progress response"""
    user_id: str
    total_words_studied: int
    words_due_for_review: int
    progress: List[UserProgressDto]


@dataclass
class WordStatsDto:
    """DTO for word statistics"""
    word: WordDto
    total_attempts: int
    correct_attempts: int
    accuracy_percentage: float
    average_response_time: float


@dataclass
class GlobalStatsDto:
    """DTO for global statistics"""
    total_words: int
    total_study_sessions: int
    total_users: int
    difficulty_distribution: Dict[int, int]
    average_sessions_per_word: float
