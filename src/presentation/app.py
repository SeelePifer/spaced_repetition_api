from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .controllers.study_controller import StudyController
from ..infrastructure.database.models import create_tables


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application"""
    
    app = FastAPI(
        title="Spaced Repetition Language Learning API",
        version="2.0.0",
        description="API for language learning using spaced repetition with layered architecture and CQRS",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create controllers
    study_controller = StudyController()
    
    # Include routers
    app.include_router(study_controller.get_router())
    
    # Root route
    @app.get("/")
    async def root():
        return {
            "message": "Spaced Repetition Language Learning API",
            "version": "2.0.0",
            "architecture": "Layered Architecture with CQRS",
            "endpoints": {
                "get_study_block": "/api/v1/study-block/{user_id}",
                "submit_answer": "/api/v1/submit-answer",
                "user_progress": "/api/v1/progress/{user_id}",
                "word_stats": "/api/v1/word/{word_id}",
                "global_stats": "/api/v1/stats"
            },
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc"
            }
        }
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": "2.0.0"}
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Creates tables when starting the application"""
        try:
            create_tables()
            print("✅ Database tables verified/created successfully")
            print("✅ Application started with layered architecture and CQRS")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
    
    return app
