from functools import lru_cache
from sqlalchemy.orm import Session
from .database.models import get_db
from .repositories.sqlalchemy_repositories import (
    SQLAlchemyWordRepository,
    SQLAlchemyUserProgressRepository,
    SQLAlchemyStudySessionRepository
)
from src.application.mediator import CQRSMediator
from src.application.handlers.command_handlers import (
    SubmitAnswerCommandHandler,
    GenerateStudyBlockCommandHandler
)
from src.application.handlers.query_handlers import (
    GetUserProgressQueryHandler,
    GetWordStatsQueryHandler,
    GetGlobalStatsQueryHandler,
    GetWordByIdQueryHandler
)
from src.application.commands.study_commands import (
    SubmitAnswerCommand,
    GenerateStudyBlockCommand
)
from src.application.queries.study_queries import (
    GetUserProgressQuery,
    GetWordStatsQuery,
    GetGlobalStatsQuery,
    GetWordByIdQuery
)


@lru_cache()
def get_word_repository(db: Session = None) -> SQLAlchemyWordRepository:
    """Gets the word repository"""
    if db is None:
        db = next(get_db())
    return SQLAlchemyWordRepository(db)


@lru_cache()
def get_user_progress_repository(db: Session = None) -> SQLAlchemyUserProgressRepository:
    """Gets the user progress repository"""
    if db is None:
        db = next(get_db())
    return SQLAlchemyUserProgressRepository(db)


@lru_cache()
def get_study_session_repository(db: Session = None) -> SQLAlchemyStudySessionRepository:
    """Gets the study session repository"""
    if db is None:
        db = next(get_db())
    return SQLAlchemyStudySessionRepository(db)


@lru_cache()
def get_mediator(db: Session = None) -> CQRSMediator:
    """Gets the configured CQRS mediator"""
    if db is None:
        db = next(get_db())
    
    # Create repositories
    word_repo = get_word_repository(db)
    user_progress_repo = get_user_progress_repository(db)
    study_session_repo = get_study_session_repository(db)
    
    # Create handlers
    submit_answer_handler = SubmitAnswerCommandHandler(
        word_repo, user_progress_repo, study_session_repo
    )
    
    generate_study_block_handler = GenerateStudyBlockCommandHandler(
        word_repo, user_progress_repo
    )
    
    get_user_progress_handler = GetUserProgressQueryHandler(
        user_progress_repo, word_repo
    )
    
    get_word_stats_handler = GetWordStatsQueryHandler(
        word_repo, study_session_repo
    )
    
    get_global_stats_handler = GetGlobalStatsQueryHandler(
        word_repo, study_session_repo, user_progress_repo
    )
    
    get_word_by_id_handler = GetWordByIdQueryHandler(word_repo)
    
    # Create mediator
    mediator = CQRSMediator()
    
    # Register handlers
    mediator.register_command_handler(SubmitAnswerCommand, submit_answer_handler)
    mediator.register_command_handler(GenerateStudyBlockCommand, generate_study_block_handler)
    mediator.register_query_handler(GetUserProgressQuery, get_user_progress_handler)
    mediator.register_query_handler(GetWordStatsQuery, get_word_stats_handler)
    mediator.register_query_handler(GetGlobalStatsQuery, get_global_stats_handler)
    mediator.register_query_handler(GetWordByIdQuery, get_word_by_id_handler)
    
    return mediator
