"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
import json


@pytest.mark.integration
class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Spaced Repetition Language Learning API"
        assert data["version"] == "2.0.0"
        assert data["architecture"] == "Layered Architecture with CQRS"
        assert "endpoints" in data
        assert "documentation" in data
    
    def test_health_check_endpoint(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"
        assert data["architecture"] == "Layered CQRS"
    
    def test_get_study_block_endpoint(self, client: TestClient):
        """Test get study block endpoint"""
        response = client.get("/api/v1/study-block/user123")
        
        assert response.status_code == 200
        data = response.json()
        assert "block_id" in data
        assert "words" in data
        assert "created_at" in data
        assert "difficulty_distribution" in data
        assert "total_words" in data
        assert data["block_id"].startswith("user123_")
        assert len(data["words"]) > 0
    
    def test_get_study_block_with_custom_limit(self, client: TestClient):
        """Test get study block endpoint with custom limit"""
        response = client.get("/api/v1/study-block/user123?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["words"]) <= 5
    
    def test_submit_answer_endpoint(self, client: TestClient):
        """Test submit answer endpoint"""
        session_data = {
            "word_id": 1,
            "user_id": "user123",
            "quality": 4,
            "response_time": 2.5
        }
        
        response = client.post("/api/v1/submit-answer", json=session_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Answer recorded successfully"
        assert data["word_id"] == 1
        assert data["quality"] == 4
        assert "next_review" in data
        assert "repetitions" in data
        assert "ease_factor" in data
        assert "interval_days" in data
    
    def test_submit_answer_invalid_quality(self, client: TestClient):
        """Test submit answer endpoint with invalid quality"""
        session_data = {
            "word_id": 1,
            "user_id": "user123",
            "quality": 6,  # Invalid quality
            "response_time": 2.5
        }
        
        response = client.post("/api/v1/submit-answer", json=session_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # Check that the error message contains information about the quality validation
        detail = data["detail"]
        assert any("quality" in str(error) for error in detail)
    
    def test_submit_answer_negative_quality(self, client: TestClient):
        """Test submit answer endpoint with negative quality"""
        session_data = {
            "word_id": 1,
            "user_id": "user123",
            "quality": -1,  # Invalid quality
            "response_time": 2.5
        }
        
        response = client.post("/api/v1/submit-answer", json=session_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # Check that the error message contains information about the quality validation
        detail = data["detail"]
        assert any("quality" in str(error) for error in detail)
    
    def test_get_user_progress_endpoint(self, client: TestClient):
        """Test get user progress endpoint"""
        response = client.get("/api/v1/progress/user123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "user123"
        assert "total_words_studied" in data
        assert "words_due_for_review" in data
        assert "progress" in data
        assert isinstance(data["progress"], list)
    
    def test_get_word_info_endpoint(self, client: TestClient):
        """Test get word info endpoint"""
        response = client.get("/api/v1/word/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "word" in data
        assert "statistics" in data
        assert data["word"]["id"] == 1
        assert "total_attempts" in data["statistics"]
        assert "correct_attempts" in data["statistics"]
        assert "accuracy_percentage" in data["statistics"]
        assert "average_response_time" in data["statistics"]
    
    def test_get_global_stats_endpoint(self, client: TestClient):
        """Test get global stats endpoint"""
        response = client.get("/api/v1/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_words" in data
        assert "total_study_sessions" in data
        assert "total_users" in data
        assert "difficulty_distribution" in data
        assert "average_sessions_per_word" in data
        assert isinstance(data["difficulty_distribution"], dict)
    
    def test_invalid_endpoint(self, client: TestClient):
        """Test invalid endpoint returns 404"""
        response = client.get("/api/v1/invalid-endpoint")
        
        assert response.status_code == 404
    
    def test_submit_answer_missing_fields(self, client: TestClient):
        """Test submit answer endpoint with missing fields"""
        session_data = {
            "word_id": 1,
            "user_id": "user123"
            # Missing quality and response_time
        }
        
        response = client.post("/api/v1/submit-answer", json=session_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_submit_answer_invalid_field_types(self, client: TestClient):
        """Test submit answer endpoint with invalid field types"""
        session_data = {
            "word_id": "invalid",  # Should be int
            "user_id": "user123",
            "quality": 4,
            "response_time": 2.5
        }
        
        response = client.post("/api/v1/submit-answer", json=session_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_study_block_different_users(self, client: TestClient):
        """Test study block endpoint with different users"""
        response1 = client.get("/api/v1/study-block/user123")
        response2 = client.get("/api/v1/study-block/user456")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        assert data1["block_id"].startswith("user123_")
        assert data2["block_id"].startswith("user456_")
    
    def test_word_info_different_ids(self, client: TestClient):
        """Test word info endpoint with different word IDs"""
        response1 = client.get("/api/v1/word/1")
        response2 = client.get("/api/v1/word/2")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        assert data1["word"]["id"] == 1
        assert data2["word"]["id"] == 2
    
    def test_progress_different_users(self, client: TestClient):
        """Test progress endpoint with different users"""
        response1 = client.get("/api/v1/progress/user123")
        response2 = client.get("/api/v1/progress/user456")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        assert data1["user_id"] == "user123"
        assert data2["user_id"] == "user456"
