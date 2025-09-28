from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UserId:
    """Value Object para representar un ID de usuario"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("User ID cannot be empty")
        if len(self.value) < 3:
            raise ValueError("User ID must have at least 3 characters")


@dataclass(frozen=True)
class WordId:
    """Value Object para representar un ID de palabra"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("Word ID must be an integer")
        if self.value <= 0:
            raise ValueError("Word ID must be positive")
