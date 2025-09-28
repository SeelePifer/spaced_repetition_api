from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Quality:
    """Value Object to represent answer quality (0-5)"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("Quality must be an integer")
        if self.value < 0 or self.value > 5:
            raise ValueError("Quality must be between 0 and 5")
    
    def is_correct(self) -> bool:
        """Determines if the answer is correct (>= 3)"""
        return self.value >= 3
    
    def is_perfect(self) -> bool:
        """Determines if the answer is perfect (= 5)"""
        return self.value == 5
    
    def is_poor(self) -> bool:
        """Determines if the answer is poor (< 3)"""
        return self.value < 3


@dataclass(frozen=True)
class DifficultyLevel:
    """Value Object to represent word difficulty level (1-5)"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("Difficulty level must be an integer")
        if self.value < 1 or self.value > 5:
            raise ValueError("Difficulty level must be between 1 and 5")
    
    def is_beginner(self) -> bool:
        """Determines if it's beginner level (1-2)"""
        return self.value <= 2
    
    def is_intermediate(self) -> bool:
        """Determines if it's intermediate level (3)"""
        return self.value == 3
    
    def is_advanced(self) -> bool:
        """Determines if it's advanced level (4-5)"""
        return self.value >= 4


@dataclass(frozen=True)
class FrequencyRank:
    """Value Object to represent word frequency rank"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("Frequency rank must be an integer")
        if self.value < 1:
            raise ValueError("Frequency rank must be positive")
    
    def is_very_common(self) -> bool:
        """Determines if it's very common (top 100)"""
        return self.value <= 100
    
    def is_common(self) -> bool:
        """Determines if it's common (top 1000)"""
        return self.value <= 1000
    
    def is_uncommon(self) -> bool:
        """Determines if it's uncommon (> 1000)"""
        return self.value > 1000


@dataclass(frozen=True)
class UserId:
    """Value Object to represent a user ID"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("User ID cannot be empty")
        if len(self.value) < 3:
            raise ValueError("User ID must have at least 3 characters")


@dataclass(frozen=True)
class WordId:
    """Value Object to represent a word ID"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("Word ID must be an integer")
        if self.value <= 0:
            raise ValueError("Word ID must be positive")
