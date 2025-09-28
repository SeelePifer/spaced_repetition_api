from abc import ABC, abstractmethod
from typing import List, Optional
from .entities.word import Word, UserProgress, StudySession
from .value_objects.identifiers import UserId, WordId


class WordRepository(ABC):
    """Word repository interface"""
    
    @abstractmethod
    async def find_by_id(self, word_id: WordId) -> Optional[Word]:
        """Finds a word by ID"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Word]:
        """Gets all words"""
        pass
    
    @abstractmethod
    async def find_by_difficulty(self, difficulty_level: int) -> List[Word]:
        """Finds words by difficulty level"""
        pass
    
    @abstractmethod
    async def find_unstudied_words(self, user_id: UserId, limit: int) -> List[Word]:
        """Finds unstudied words for a user"""
        pass
    
    @abstractmethod
    async def save(self, word: Word) -> Word:
        """Saves a word"""
        pass


class UserProgressRepository(ABC):
    """User progress repository interface"""
    
    @abstractmethod
    async def find_by_user_and_word(self, user_id: UserId, word_id: WordId) -> Optional[UserProgress]:
        """Finds user progress for a specific word"""
        pass
    
    @abstractmethod
    async def find_by_user(self, user_id: UserId) -> List[UserProgress]:
        """Finds all user progress"""
        pass
    
    @abstractmethod
    async def find_words_due_for_review(self, user_id: UserId, limit: int) -> List[Word]:
        """Finds words that need review for a user"""
        pass
    
    @abstractmethod
    async def save(self, progress: UserProgress) -> UserProgress:
        """Saves user progress"""
        pass
    
    @abstractmethod
    async def count_words_studied(self, user_id: UserId) -> int:
        """Counts words studied by a user"""
        pass
    
    @abstractmethod
    async def count_words_due_for_review(self, user_id: UserId) -> int:
        """Counts words that need review for a user"""
        pass


class StudySessionRepository(ABC):
    """Study session repository interface"""
    
    @abstractmethod
    async def save(self, session: StudySession) -> StudySession:
        """Saves a study session"""
        pass
    
    @abstractmethod
    async def find_by_user(self, user_id: UserId) -> List[StudySession]:
        """Finds all sessions for a user"""
        pass
    
    @abstractmethod
    async def find_by_word(self, word_id: WordId) -> List[StudySession]:
        """Finds all sessions for a word"""
        pass
    
    @abstractmethod
    async def count_total_sessions(self) -> int:
        """Counts total sessions in the system"""
        pass
    
    @abstractmethod
    async def count_correct_sessions(self, word_id: WordId) -> int:
        """Counts correct sessions for a word"""
        pass
