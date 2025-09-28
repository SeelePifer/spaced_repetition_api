from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.repositories import WordRepository, UserProgressRepository, StudySessionRepository
from ...domain.entities.word import Word, UserProgress, StudySession
from ...domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from ...domain.value_objects.identifiers import UserId, WordId
from ..database.models import WordModel, UserProgressModel, StudySessionModel
from datetime import datetime


class SQLAlchemyWordRepository(WordRepository):
    """Implementación del repositorio de palabras usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def find_by_id(self, word_id: WordId) -> Optional[Word]:
        """Busca una palabra por ID"""
        word_model = self.db.query(WordModel).filter(WordModel.id == word_id.value).first()
        if not word_model:
            return None
        
        return self._to_domain_entity(word_model)
    
    async def find_all(self) -> List[Word]:
        """Obtiene todas las palabras"""
        word_models = self.db.query(WordModel).all()
        return [self._to_domain_entity(model) for model in word_models]
    
    async def find_by_difficulty(self, difficulty_level: int) -> List[Word]:
        """Busca palabras por nivel de dificultad"""
        word_models = self.db.query(WordModel).filter(
            WordModel.difficulty_level == difficulty_level
        ).all()
        return [self._to_domain_entity(model) for model in word_models]
    
    async def find_unstudied_words(self, user_id: UserId, limit: int) -> List[Word]:
        """Busca palabras no estudiadas por un usuario"""
        # Obtener IDs de palabras ya estudiadas por el usuario
        studied_word_ids = self.db.query(UserProgressModel.word_id).filter(
            UserProgressModel.user_id == user_id.value
        ).all()
        
        studied_ids = [word_id[0] for word_id in studied_word_ids]
        
        # Obtener palabras no estudiadas
        if studied_ids:
            word_models = self.db.query(WordModel).filter(
                ~WordModel.id.in_(studied_ids)
            ).limit(limit).all()
        else:
            # Si no hay palabras estudiadas, obtener las primeras palabras
            word_models = self.db.query(WordModel).limit(limit).all()
        
        return [self._to_domain_entity(model) for model in word_models]
    
    async def save(self, word: Word) -> Word:
        """Guarda una palabra"""
        if word.id:
            # Actualizar palabra existente
            word_model = self.db.query(WordModel).filter(WordModel.id == word.id).first()
            if word_model:
                word_model.word = word.word
                word_model.frequency_rank = word.frequency_rank.value
                word_model.difficulty_level = word.difficulty_level.value
        else:
            # Crear nueva palabra
            word_model = WordModel(
                word=word.word,
                frequency_rank=word.frequency_rank.value,
                difficulty_level=word.difficulty_level.value
            )
            self.db.add(word_model)
        
        self.db.commit()
        self.db.refresh(word_model)
        
        return self._to_domain_entity(word_model)
    
    def _to_domain_entity(self, model: WordModel) -> Word:
        """Convierte un modelo SQLAlchemy a entidad de dominio"""
        return Word(
            id=model.id,
            word=model.word,
            frequency_rank=FrequencyRank(model.frequency_rank),
            difficulty_level=DifficultyLevel(model.difficulty_level)
        )


class SQLAlchemyUserProgressRepository(UserProgressRepository):
    """Implementación del repositorio de progreso de usuario usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def find_by_user_and_word(self, user_id: UserId, word_id: WordId) -> Optional[UserProgress]:
        """Busca el progreso de un usuario para una palabra específica"""
        progress_model = self.db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id.value,
            UserProgressModel.word_id == word_id.value
        ).first()
        
        if not progress_model:
            return None
        
        return self._to_domain_entity(progress_model)
    
    async def find_by_user(self, user_id: UserId) -> List[UserProgress]:
        """Busca todo el progreso de un usuario"""
        progress_models = self.db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id.value
        ).all()
        
        return [self._to_domain_entity(model) for model in progress_models]
    
    async def find_words_due_for_review(self, user_id: UserId, limit: int) -> List[Word]:
        """Busca palabras que necesitan repaso para un usuario"""
        now = datetime.now()
        
        # Obtener palabras que necesitan repaso
        words_to_review = self.db.query(WordModel).join(UserProgressModel).filter(
            UserProgressModel.user_id == user_id.value,
            UserProgressModel.next_review <= now
        ).limit(limit).all()
        
        return [self._to_domain_entity(word_model) for word_model in words_to_review]
    
    async def save(self, progress: UserProgress) -> UserProgress:
        """Guarda el progreso de un usuario"""
        if progress.id:
            # Actualizar progreso existente
            progress_model = self.db.query(UserProgressModel).filter(
                UserProgressModel.id == progress.id
            ).first()
            if progress_model:
                progress_model.repetitions = progress.repetitions
                progress_model.ease_factor = progress.ease_factor
                progress_model.interval = progress.interval
                progress_model.next_review = progress.next_review
                progress_model.last_review = progress.last_review
        else:
            # Crear nuevo progreso
            progress_model = UserProgressModel(
                user_id=progress.user_id,
                word_id=progress.word_id,
                repetitions=progress.repetitions,
                ease_factor=progress.ease_factor,
                interval=progress.interval,
                next_review=progress.next_review,
                last_review=progress.last_review
            )
            self.db.add(progress_model)
        
        self.db.commit()
        self.db.refresh(progress_model)
        
        return self._to_domain_entity(progress_model)
    
    async def count_words_studied(self, user_id: UserId) -> int:
        """Cuenta las palabras estudiadas por un usuario"""
        return self.db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id.value
        ).count()
    
    async def count_words_due_for_review(self, user_id: UserId) -> int:
        """Cuenta las palabras que necesitan repaso para un usuario"""
        now = datetime.now()
        return self.db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id.value,
            UserProgressModel.next_review <= now
        ).count()
    
    def _to_domain_entity(self, model: UserProgressModel) -> UserProgress:
        """Convierte un modelo SQLAlchemy a entidad de dominio"""
        return UserProgress(
            id=model.id,
            user_id=model.user_id,
            word_id=model.word_id,
            repetitions=model.repetitions,
            ease_factor=model.ease_factor,
            interval=model.interval,
            next_review=model.next_review,
            last_review=model.last_review
        )


class SQLAlchemyStudySessionRepository(StudySessionRepository):
    """Implementación del repositorio de sesiones de estudio usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def save(self, session: StudySession) -> StudySession:
        """Guarda una sesión de estudio"""
        session_model = StudySessionModel(
            word_id=session.word_id,
            user_id=session.user_id,
            correct=session.correct,
            response_time=session.response_time,
            timestamp=session.timestamp,
            quality=session.quality.value
        )
        
        self.db.add(session_model)
        self.db.commit()
        self.db.refresh(session_model)
        
        return self._to_domain_entity(session_model)
    
    async def find_by_user(self, user_id: UserId) -> List[StudySession]:
        """Busca todas las sesiones de un usuario"""
        session_models = self.db.query(StudySessionModel).filter(
            StudySessionModel.user_id == user_id.value
        ).all()
        
        return [self._to_domain_entity(model) for model in session_models]
    
    async def find_by_word(self, word_id: WordId) -> List[StudySession]:
        """Busca todas las sesiones de una palabra"""
        session_models = self.db.query(StudySessionModel).filter(
            StudySessionModel.word_id == word_id.value
        ).all()
        
        return [self._to_domain_entity(model) for model in session_models]
    
    async def count_total_sessions(self) -> int:
        """Cuenta el total de sesiones en el sistema"""
        return self.db.query(StudySessionModel).count()
    
    async def count_correct_sessions(self, word_id: WordId) -> int:
        """Cuenta las sesiones correctas para una palabra"""
        return self.db.query(StudySessionModel).filter(
            StudySessionModel.word_id == word_id.value,
            StudySessionModel.correct == True
        ).count()
    
    def _to_domain_entity(self, model: StudySessionModel) -> StudySession:
        """Convierte un modelo SQLAlchemy a entidad de dominio"""
        return StudySession(
            id=model.id,
            word_id=model.word_id,
            user_id=model.user_id,
            correct=model.correct,
            response_time=model.response_time,
            timestamp=model.timestamp,
            quality=Quality(model.quality)
        )
