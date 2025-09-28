from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..dto.study_dto import StudySessionDto, StudyBlockDto, StudySessionResponseDto


class Command(ABC):
    """Base class for all commands"""
    pass


@dataclass
class SubmitAnswerCommand(Command):
    """Command to submit a study answer"""
    session_data: StudySessionDto


@dataclass
class GenerateStudyBlockCommand(Command):
    """Command to generate a study block"""
    user_id: str
    limit: int = 20


@dataclass
class CreateWordCommand(Command):
    """Command to create a new word"""
    word: str
    frequency_rank: int
    difficulty_level: int


@dataclass
class UpdateUserProgressCommand(Command):
    """Command to update user progress"""
    user_id: str
    word_id: int
    quality: int
    response_time: float
