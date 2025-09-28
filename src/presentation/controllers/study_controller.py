from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..dto.responses import (
    StudySessionRequest,
    StudySessionResponse,
    StudyBlockResponse,
    UserProgressResponse,
    WordStatsResponse,
    GlobalStatsResponse,
    ErrorResponse
)
from ...infrastructure.database.models import get_db
from ...infrastructure.dependencies import get_mediator
from ...application.mediator import CQRSMediator
from ...application.commands.study_commands import (
    SubmitAnswerCommand,
    GenerateStudyBlockCommand
)
from ...application.queries.study_queries import (
    GetUserProgressQuery,
    GetWordStatsQuery,
    GetGlobalStatsQuery,
    GetWordByIdQuery
)
from ...application.dto.study_dto import StudySessionDto
from ...shared.exceptions.domain_exceptions import (
    WordNotFoundException,
    InvalidQualityException,
    InvalidResponseTimeException,
    NoWordsAvailableException
)


class StudyController:
    """Controller para operaciones de estudio"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/api/v1", tags=["study"])
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura las rutas del controller"""
        
        @self.router.get("/study-block/{user_id}", response_model=StudyBlockResponse)
        async def get_study_block(
            user_id: str,
            limit: int = 20,
            db: Session = Depends(get_db),
            mediator: CQRSMediator = Depends(get_mediator)
        ):
            """Genera un bloque de estudio para un usuario"""
            try:
                command = GenerateStudyBlockCommand(user_id=user_id, limit=limit)
                result = await mediator.send_command(command)
                
                return StudyBlockResponse(
                    block_id=result.block_id,
                    words=[{
                        "id": word["id"],
                        "word": word["word"],
                        "frequency_rank": word["frequency_rank"],
                        "difficulty_level": word["difficulty_level"]
                    } for word in result.words],
                    created_at=result.created_at,
                    difficulty_distribution=result.difficulty_distribution,
                    total_words=result.total_words
                )
                
            except NoWordsAvailableException as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/submit-answer", response_model=StudySessionResponse)
        async def submit_answer(
            session_data: StudySessionRequest,
            db: Session = Depends(get_db),
            mediator: CQRSMediator = Depends(get_mediator)
        ):
            """Registra la respuesta del usuario y actualiza el progreso"""
            try:
                command = SubmitAnswerCommand(
                    session_data=StudySessionDto(
                        word_id=session_data.word_id,
                        user_id=session_data.user_id,
                        quality=session_data.quality,
                        response_time=session_data.response_time
                    )
                )
                result = await mediator.send_command(command)
                
                return StudySessionResponse(
                    message=result.message,
                    word_id=result.word_id,
                    quality=result.quality,
                    next_review=result.next_review,
                    repetitions=result.repetitions,
                    ease_factor=result.ease_factor,
                    interval_days=result.interval_days
                )
                
            except WordNotFoundException as e:
                raise HTTPException(status_code=404, detail=str(e))
            except (InvalidQualityException, InvalidResponseTimeException) as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/progress/{user_id}", response_model=UserProgressResponse)
        async def get_user_progress(
            user_id: str,
            db: Session = Depends(get_db),
            mediator: CQRSMediator = Depends(get_mediator)
        ):
            """Obtiene el progreso de estudio de un usuario"""
            try:
                query = GetUserProgressQuery(user_id=user_id)
                result = await mediator.send_query(query)
                
                return UserProgressResponse(
                    user_id=result.user_id,
                    total_words_studied=result.total_words_studied,
                    words_due_for_review=result.words_due_for_review,
                    progress=[{
                        "word": p.word,
                        "word_id": p.word_id,
                        "repetitions": p.repetitions,
                        "ease_factor": p.ease_factor,
                        "interval_days": p.interval_days,
                        "next_review": p.next_review,
                        "last_review": p.last_review,
                        "difficulty_level": p.difficulty_level
                    } for p in result.progress]
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/word/{word_id}", response_model=WordStatsResponse)
        async def get_word_info(
            word_id: int,
            db: Session = Depends(get_db),
            mediator: CQRSMediator = Depends(get_mediator)
        ):
            """Obtiene información detallada de una palabra específica"""
            try:
                query = GetWordStatsQuery(word_id=word_id)
                result = await mediator.send_query(query)
                
                return WordStatsResponse(
                    word={
                        "id": result.word.id,
                        "word": result.word.word,
                        "frequency_rank": result.word.frequency_rank,
                        "difficulty_level": result.word.difficulty_level
                    },
                    statistics={
                        "total_attempts": result.total_attempts,
                        "correct_attempts": result.correct_attempts,
                        "accuracy_percentage": result.accuracy_percentage,
                        "average_response_time": result.average_response_time
                    }
                )
                
            except WordNotFoundException as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/stats", response_model=GlobalStatsResponse)
        async def get_global_stats(
            db: Session = Depends(get_db),
            mediator: CQRSMediator = Depends(get_mediator)
        ):
            """Obtiene estadísticas globales del sistema"""
            try:
                query = GetGlobalStatsQuery()
                result = await mediator.send_query(query)
                
                return GlobalStatsResponse(
                    total_words=result.total_words,
                    total_study_sessions=result.total_study_sessions,
                    total_users=result.total_users,
                    difficulty_distribution=result.difficulty_distribution,
                    average_sessions_per_word=result.average_sessions_per_word
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self):
        """Retorna el router configurado"""
        return self.router
