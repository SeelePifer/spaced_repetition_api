from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UserId:
    """Value Object para representar un ID de usuario"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("El ID de usuario no puede estar vacío")
        if len(self.value) < 3:
            raise ValueError("El ID de usuario debe tener al menos 3 caracteres")


@dataclass(frozen=True)
class WordId:
    """Value Object para representar un ID de palabra"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("El ID de palabra debe ser un entero")
        if self.value <= 0:
            raise ValueError("El ID de palabra debe ser positivo")
