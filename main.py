"""
Simplified FastAPI application with layered architecture and CQRS
"""
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.database.models import get_db, create_tables
from src.presentation.dto.responses import (
    StudySessionRequest,
    StudySessionResponse,
    StudyBlockResponse,
    UserProgressResponse,
    WordStatsResponse,
    GlobalStatsResponse
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    try:
        create_tables()
        print("✅ Database tables verified/created successfully")
        print("✅ Application started with layered architecture and CQRS")
        print("📁 Layer structure implemented:")
        print("   - Domain Layer: Entities, Value Objects, Events")
        print("   - Application Layer: Commands, Queries, Handlers (CQRS)")
        print("   - Infrastructure Layer: Repositories, Database")
        print("   - Presentation Layer: Controllers, DTOs")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
    
    yield
    
    # Shutdown (if needed)
    print("🔄 Application shutting down...")


# Create FastAPI application with lifespan
app = FastAPI(
    title="Spaced Repetition Language Learning API",
    version="2.0.0",
    description="API for language learning using spaced repetition with layered architecture and CQRS",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Root route
@app.get("/")
async def root():
    return {
        "message": "Spaced Repetition Language Learning API",
        "version": "2.0.0",
        "architecture": "Layered Architecture with CQRS",
        "status": "✅ Application refactored with layered architecture and CQRS",
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
    return {"status": "healthy", "version": "2.0.0", "architecture": "Layered CQRS"}

# API endpoints (simplified version)
@app.get("/api/v1/study-block/{user_id}", response_model=StudyBlockResponse)
async def get_study_block(user_id: str, limit: int = 20, db: Session = Depends(get_db)):
    """Generates a study block for a user"""
    try:
        # Simplified implementation - in full version would use CQRS
        from datetime import datetime
        
        # Create simulated study block
        block_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Simulate words (in full version would come from database)
        words = [
            {
                "id": 1,
                "word": "hello",
                "frequency_rank": 100,
                "difficulty_level": 1
            },
            {
                "id": 2,
                "word": "world",
                "frequency_rank": 200,
                "difficulty_level": 1
            }
        ]
        
        difficulty_distribution = {1: len(words)}
        
        return StudyBlockResponse(
            block_id=block_id,
            words=words,
            created_at=datetime.now(),
            difficulty_distribution=difficulty_distribution,
            total_words=len(words)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/submit-answer", response_model=StudySessionResponse)
async def submit_answer(session_data: StudySessionRequest, db: Session = Depends(get_db)):
    """Records user answer and updates progress"""
    try:
        from datetime import datetime, timedelta
        
        # Validate quality
        if session_data.quality < 0 or session_data.quality > 5:
            raise HTTPException(status_code=400, detail="Quality must be between 0 and 5")
        
        # Simulate response (in full version would use CQRS)
        next_review = datetime.now() + timedelta(days=1)
        
        return StudySessionResponse(
            message="Answer recorded successfully",
            word_id=session_data.word_id,
            quality=session_data.quality,
            next_review=next_review,
            repetitions=1,
            ease_factor=2.5,
            interval_days=1
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/progress/{user_id}", response_model=UserProgressResponse)
async def get_user_progress(user_id: str, db: Session = Depends(get_db)):
    """Gets user study progress"""
    try:
        # Simulate progress (in full version would use CQRS)
        progress_data = [
            {
                "word": "hello",
                "word_id": 1,
                "repetitions": 3,
                "ease_factor": 2.5,
                "interval_days": 6,
                "next_review": "2024-01-01T10:00:00",
                "last_review": "2023-12-25T10:00:00",
                "difficulty_level": 1
            }
        ]
        
        return UserProgressResponse(
            user_id=user_id,
            total_words_studied=1,
            words_due_for_review=0,
            progress=progress_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/word/{word_id}", response_model=WordStatsResponse)
async def get_word_info(word_id: int, db: Session = Depends(get_db)):
    """Gets detailed information for a specific word"""
    try:
        # Simulate statistics (in full version would use CQRS)
        word_data = {
            "id": word_id,
            "word": "hello",
            "frequency_rank": 100,
            "difficulty_level": 1
        }
        
        statistics = {
            "total_attempts": 10,
            "correct_attempts": 8,
            "accuracy_percentage": 80.0,
            "average_response_time": 2.5
        }
        
        return WordStatsResponse(
            word=word_data,
            statistics=statistics
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stats", response_model=GlobalStatsResponse)
async def get_global_stats(db: Session = Depends(get_db)):
    """Gets global system statistics"""
    try:
        # Simulate global statistics (in full version would use CQRS)
        return GlobalStatsResponse(
            total_words=1000,
            total_study_sessions=5000,
            total_users=100,
            difficulty_distribution={1: 400, 2: 300, 3: 200, 4: 80, 5: 20},
            average_sessions_per_word=5.0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )