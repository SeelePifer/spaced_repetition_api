from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class WordResponse(BaseModel):
    """Response DTO for a word"""
    id: int
    word: str
    frequency_rank: int
    difficulty_level: int
    
    class Config:
        from_attributes = True


class StudySessionRequest(BaseModel):
    """Request DTO for a study session"""
    user_id: str = Field(..., min_length=3, description="User ID")
    word_id: int = Field(..., gt=0, description="Word ID")
    quality: int = Field(..., ge=0, le=5, description="Answer quality (0-5)")
    response_time: float = Field(default=0.0, ge=0, description="Response time in seconds")


class StudySessionResponse(BaseModel):
    """Response DTO for a study session"""
    message: str
    word_id: int
    quality: int
    next_review: datetime
    repetitions: int
    ease_factor: float
    interval_days: int


class StudyBlockResponse(BaseModel):
    """Response DTO for a study block"""
    block_id: str
    words: List[WordResponse]
    created_at: datetime
    difficulty_distribution: Dict[int, int]
    total_words: int


class UserProgressDto(BaseModel):
    """DTO for user progress"""
    word: str
    word_id: int
    repetitions: int
    ease_factor: float
    interval_days: int
    next_review: datetime
    last_review: Optional[datetime]
    difficulty_level: int


class UserProgressResponse(BaseModel):
    """Response DTO for user progress"""
    user_id: str
    total_words_studied: int
    words_due_for_review: int
    progress: List[UserProgressDto]


class WordStatsResponse(BaseModel):
    """Response DTO for word statistics"""
    word: WordResponse
    statistics: Dict[str, Any]


class GlobalStatsResponse(BaseModel):
    """Response DTO for global statistics"""
    total_words: int
    total_study_sessions: int
    total_users: int
    difficulty_distribution: Dict[int, int]
    average_sessions_per_word: float


class ErrorResponse(BaseModel):
    """Response DTO for errors"""
    error: str
    detail: str
    status_code: int
