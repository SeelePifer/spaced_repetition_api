from abc import ABC, abstractmethod
from typing import Any
from ..commands.study_commands import Command
from ..dto.study_dto import StudySessionResponseDto, StudyBlockDto
from ...domain.repositories import WordRepository, UserProgressRepository, StudySessionRepository
from ...domain.value_objects.identifiers import UserId, WordId
from ...domain.value_objects.quality import Quality
from ...domain.entities.word import Word, UserProgress, StudySession
from ...shared.exceptions.domain_exceptions import (
    WordNotFoundException, 
    InvalidQualityException,
    InvalidResponseTimeException
)


class CommandHandler(ABC):
    """Clase base para todos los command handlers"""
    
    @abstractmethod
    async def handle(self, command: Command) -> Any:
        """Maneja un comando"""
        pass


class SubmitAnswerCommandHandler(CommandHandler):
    """Handler para el comando SubmitAnswerCommand"""
    
    def __init__(
        self,
        word_repository: WordRepository,
        user_progress_repository: UserProgressRepository,
        study_session_repository: StudySessionRepository
    ):
        self.word_repository = word_repository
        self.user_progress_repository = user_progress_repository
        self.study_session_repository = study_session_repository
    
    async def handle(self, command) -> StudySessionResponseDto:
        """Maneja el comando de enviar respuesta"""
        from ..commands.study_commands import SubmitAnswerCommand
        
        if not isinstance(command, SubmitAnswerCommand):
            raise ValueError("Comando inválido")
        
        session_data = command.session_data
        
        # Validar calidad
        if session_data.quality < 0 or session_data.quality > 5:
            raise InvalidQualityException(session_data.quality)
        
        # Validar tiempo de respuesta
        if session_data.response_time < 0:
            raise InvalidResponseTimeException(session_data.response_time)
        
        # Verificar que la palabra existe
        word_id = WordId(session_data.word_id)
        word = await self.word_repository.find_by_id(word_id)
        if not word:
            raise WordNotFoundException(session_data.word_id)
        
        # Buscar progreso existente
        user_id = UserId(session_data.user_id)
        progress = await self.user_progress_repository.find_by_user_and_word(user_id, word_id)
        
        if not progress:
            # Crear nuevo progreso
            progress = UserProgress(
                id=None,
                user_id=session_data.user_id,
                word_id=session_data.word_id,
                next_review=None
            )
        
        # Actualizar progreso usando algoritmo SM-2
        quality = Quality(session_data.quality)
        events = progress.update_progress(quality)
        
        # Guardar progreso actualizado
        await self.user_progress_repository.save(progress)
        
        # Crear y guardar sesión de estudio
        session = StudySession(
            id=None,
            word_id=session_data.word_id,
            user_id=session_data.user_id,
            correct=quality.is_correct(),
            response_time=session_data.response_time,
            timestamp=progress.last_review,
            quality=quality
        )
        await self.study_session_repository.save(session)
        
        return StudySessionResponseDto(
            message="Respuesta registrada exitosamente",
            word_id=session_data.word_id,
            quality=session_data.quality,
            next_review=progress.next_review,
            repetitions=progress.repetitions,
            ease_factor=progress.ease_factor,
            interval_days=progress.interval
        )


class GenerateStudyBlockCommandHandler(CommandHandler):
    """Handler para el comando GenerateStudyBlockCommand"""
    
    def __init__(
        self,
        word_repository: WordRepository,
        user_progress_repository: UserProgressRepository
    ):
        self.word_repository = word_repository
        self.user_progress_repository = user_progress_repository
    
    async def handle(self, command) -> StudyBlockDto:
        """Maneja el comando de generar bloque de estudio"""
        from ..commands.study_commands import GenerateStudyBlockCommand
        
        if not isinstance(command, GenerateStudyBlockCommand):
            raise ValueError("Comando inválido")
        
        user_id = UserId(command.user_id)
        
        # Obtener palabras que necesitan repaso
        words_to_review = await self.user_progress_repository.find_words_due_for_review(
            user_id, command.limit
        )
        
        # Si no hay suficientes palabras para repaso, agregar palabras nuevas
        if len(words_to_review) < command.limit:
            new_words_needed = command.limit - len(words_to_review)
            new_words = await self.word_repository.find_unstudied_words(
                user_id, new_words_needed
            )
            words_to_review.extend(new_words)
        
        # Limitar al número solicitado
        words_to_review = words_to_review[:command.limit]
        
        if not words_to_review:
            from ...shared.exceptions.domain_exceptions import NoWordsAvailableException
            raise NoWordsAvailableException(command.user_id)
        
        # Crear el bloque de estudio
        from datetime import datetime
        block_id = f"{command.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calcular distribución de dificultad
        difficulty_dist = {}
        word_dtos = []
        for word in words_to_review:
            diff = word.difficulty_level.value
            difficulty_dist[diff] = difficulty_dist.get(diff, 0) + 1
            
            word_dtos.append({
                "id": word.id,
                "word": word.word,
                "frequency_rank": word.frequency_rank.value,
                "difficulty_level": word.difficulty_level.value
            })
        
        return StudyBlockDto(
            block_id=block_id,
            words=word_dtos,
            created_at=datetime.now(),
            difficulty_distribution=difficulty_dist,
            total_words=len(words_to_review)
        )
