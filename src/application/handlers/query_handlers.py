from abc import ABC, abstractmethod
from typing import Any
from ..queries.study_queries import Query
from ..dto.study_dto import (
    UserProgressResponseDto, 
    WordStatsDto, 
    GlobalStatsDto, 
    StudyBlockDto,
    WordDto,
    UserProgressDto
)
from ...domain.repositories import WordRepository, UserProgressRepository, StudySessionRepository
from ...domain.value_objects.identifiers import UserId, WordId
from ...domain.value_objects.quality import Quality
from ...shared.exceptions.domain_exceptions import WordNotFoundException
from datetime import datetime


class QueryHandler(ABC):
    """Clase base para todos los query handlers"""
    
    @abstractmethod
    async def handle(self, query: Query) -> Any:
        """Maneja una query"""
        pass


class GetUserProgressQueryHandler(QueryHandler):
    """Handler para la query GetUserProgressQuery"""
    
    def __init__(
        self,
        user_progress_repository: UserProgressRepository,
        word_repository: WordRepository
    ):
        self.user_progress_repository = user_progress_repository
        self.word_repository = word_repository
    
    async def handle(self, query) -> UserProgressResponseDto:
        """Maneja la query de obtener progreso de usuario"""
        from ..queries.study_queries import GetUserProgressQuery
        
        if not isinstance(query, GetUserProgressQuery):
            raise ValueError("Query inválida")
        
        user_id = UserId(query.user_id)
        
        # Obtener progreso del usuario
        user_progress = await self.user_progress_repository.find_by_user(user_id)
        
        progress_data = []
        for progress in user_progress:
            word = await self.word_repository.find_by_id(WordId(progress.word_id))
            if word:
                progress_data.append(UserProgressDto(
                    word=word.word,
                    word_id=progress.word_id,
                    repetitions=progress.repetitions,
                    ease_factor=progress.ease_factor,
                    interval_days=progress.interval,
                    next_review=progress.next_review,
                    last_review=progress.last_review,
                    difficulty_level=word.difficulty_level.value
                ))
        
        # Estadísticas generales
        total_words_studied = len(progress_data)
        words_due_for_review = len([p for p in progress_data if p.next_review <= datetime.now()])
        
        return UserProgressResponseDto(
            user_id=query.user_id,
            total_words_studied=total_words_studied,
            words_due_for_review=words_due_for_review,
            progress=progress_data
        )


class GetWordStatsQueryHandler(QueryHandler):
    """Handler para la query GetWordStatsQuery"""
    
    def __init__(
        self,
        word_repository: WordRepository,
        study_session_repository: StudySessionRepository
    ):
        self.word_repository = word_repository
        self.study_session_repository = study_session_repository
    
    async def handle(self, query) -> WordStatsDto:
        """Maneja la query de obtener estadísticas de palabra"""
        from ..queries.study_queries import GetWordStatsQuery
        
        if not isinstance(query, GetWordStatsQuery):
            raise ValueError("Query inválida")
        
        word_id = WordId(query.word_id)
        
        # Verificar que la palabra existe
        word = await self.word_repository.find_by_id(word_id)
        if not word:
            raise WordNotFoundException(query.word_id)
        
        # Estadísticas de la palabra
        word_sessions = await self.study_session_repository.find_by_word(word_id)
        
        total_attempts = len(word_sessions)
        correct_attempts = await self.study_session_repository.count_correct_sessions(word_id)
        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        average_response_time = 0
        if total_attempts > 0:
            total_time = sum(session.response_time for session in word_sessions)
            average_response_time = round(total_time / total_attempts, 2)
        
        word_dto = WordDto(
            id=word.id,
            word=word.word,
            frequency_rank=word.frequency_rank.value,
            difficulty_level=word.difficulty_level.value
        )
        
        return WordStatsDto(
            word=word_dto,
            total_attempts=total_attempts,
            correct_attempts=correct_attempts,
            accuracy_percentage=round(accuracy, 2),
            average_response_time=average_response_time
        )


class GetGlobalStatsQueryHandler(QueryHandler):
    """Handler para la query GetGlobalStatsQuery"""
    
    def __init__(
        self,
        word_repository: WordRepository,
        study_session_repository: StudySessionRepository,
        user_progress_repository: UserProgressRepository
    ):
        self.word_repository = word_repository
        self.study_session_repository = study_session_repository
        self.user_progress_repository = user_progress_repository
    
    async def handle(self, query) -> GlobalStatsDto:
        """Maneja la query de obtener estadísticas globales"""
        from ..queries.study_queries import GetGlobalStatsQuery
        
        if not isinstance(query, GetGlobalStatsQuery):
            raise ValueError("Query inválida")
        
        # Obtener estadísticas básicas
        words = await self.word_repository.find_all()
        total_words = len(words)
        total_sessions = await self.study_session_repository.count_total_sessions()
        
        # Contar usuarios únicos (esto requeriría una implementación específica)
        # Por ahora usaremos un valor estimado
        total_users = 0  # Se implementaría con una query específica
        
        # Distribución de dificultad
        difficulty_dist = {}
        for word in words:
            diff = word.difficulty_level.value
            difficulty_dist[diff] = difficulty_dist.get(diff, 0) + 1
        
        average_sessions_per_word = round(total_sessions / total_words, 2) if total_words > 0 else 0
        
        return GlobalStatsDto(
            total_words=total_words,
            total_study_sessions=total_sessions,
            total_users=total_users,
            difficulty_distribution=difficulty_dist,
            average_sessions_per_word=average_sessions_per_word
        )


class GetWordByIdQueryHandler(QueryHandler):
    """Handler para la query GetWordByIdQuery"""
    
    def __init__(self, word_repository: WordRepository):
        self.word_repository = word_repository
    
    async def handle(self, query) -> WordDto:
        """Maneja la query de obtener palabra por ID"""
        from ..queries.study_queries import GetWordByIdQuery
        
        if not isinstance(query, GetWordByIdQuery):
            raise ValueError("Query inválida")
        
        word_id = WordId(query.word_id)
        word = await self.word_repository.find_by_id(word_id)
        
        if not word:
            raise WordNotFoundException(query.word_id)
        
        return WordDto(
            id=word.id,
            word=word.word,
            frequency_rank=word.frequency_rank.value,
            difficulty_level=word.difficulty_level.value
        )
