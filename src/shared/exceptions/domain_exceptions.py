"""Custom domain exceptions"""


class DomainException(Exception):
    """Base exception for domain errors"""
    pass


class WordNotFoundException(DomainException):
    """Exception when a word is not found"""
    def __init__(self, word_id: int):
        self.word_id = word_id
        super().__init__(f"Word with ID {word_id} not found")


class UserNotFoundException(DomainException):
    """Exception when a user is not found"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found")


class InvalidQualityException(DomainException):
    """Exception when answer quality is invalid"""
    def __init__(self, quality: int):
        self.quality = quality
        super().__init__(f"Quality {quality} is invalid. Must be between 0 and 5")


class InvalidDifficultyException(DomainException):
    """Exception when difficulty level is invalid"""
    def __init__(self, difficulty: int):
        self.difficulty = difficulty
        super().__init__(f"Difficulty {difficulty} is invalid. Must be between 1 and 5")


class StudySessionException(DomainException):
    """Base exception for study session errors"""
    pass


class NoWordsAvailableException(DomainException):
    """Exception when no words are available for study"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"No words available for user {user_id}")


class InvalidResponseTimeException(DomainException):
    """Exception when response time is invalid"""
    def __init__(self, response_time: float):
        self.response_time = response_time
        super().__init__(f"Response time {response_time} is invalid. Must be positive")
