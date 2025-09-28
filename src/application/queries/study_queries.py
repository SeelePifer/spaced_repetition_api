from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional
from ..dto.study_dto import (
    UserProgressResponseDto, 
    WordStatsDto, 
    GlobalStatsDto, 
    StudyBlockDto
)


class Query(ABC):
    """Base class for all queries"""
    pass


@dataclass
class GetUserProgressQuery(Query):
    """Query to get user progress"""
    user_id: str


@dataclass
class GetWordStatsQuery(Query):
    """Query to get word statistics"""
    word_id: int


@dataclass
class GetGlobalStatsQuery(Query):
    """Query to get global statistics"""
    pass


@dataclass
class GetStudyBlockQuery(Query):
    """Query to get a study block"""
    user_id: str
    limit: int = 20


@dataclass
class GetWordByIdQuery(Query):
    """Query to get a word by ID"""
    word_id: int


@dataclass
class GetWordsByDifficultyQuery(Query):
    """Query to get words by difficulty"""
    difficulty_level: int
    limit: Optional[int] = None
