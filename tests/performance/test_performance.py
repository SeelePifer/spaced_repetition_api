"""
Performance tests for the spaced repetition API
"""
import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from tests.utils.test_helpers import TestDataFactory


@pytest.mark.slow
class TestPerformance:
    """Performance tests for the API"""
    
    def test_api_response_time(self, client: TestClient):
        """Test that API responses are fast enough"""
        start_time = time.time()
        
        response = client.get("/api/v1/study-block/user123")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_concurrent_api_requests(self, client: TestClient):
        """Test API performance under concurrent load"""
        def make_request():
            return client.get("/api/v1/study-block/user123")
        
        # Make 10 concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in futures]
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
    
    def test_large_study_block_performance(self, client: TestClient):
        """Test performance with large study blocks"""
        start_time = time.time()
        
        response = client.get("/api/v1/study-block/user123?limit=100")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0  # Should handle large blocks within 2 seconds
    
    def test_multiple_user_requests(self, client: TestClient):
        """Test performance with multiple different users"""
        user_ids = [f"user{i}" for i in range(20)]
        
        start_time = time.time()
        
        responses = []
        for user_id in user_ids:
            response = client.get(f"/api/v1/study-block/{user_id}")
            responses.append(response)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Should handle 20 users within reasonable time
        assert total_time < 5.0
    
    def test_submit_answer_performance(self, client: TestClient):
        """Test submit answer endpoint performance"""
        session_data = {
            "word_id": 1,
            "user_id": "user123",
            "quality": 4,
            "response_time": 2.5
        }
        
        start_time = time.time()
        
        response = client.post("/api/v1/submit-answer", json=session_data)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_concurrent_submit_answers(self, client: TestClient):
        """Test concurrent submit answer requests"""
        def submit_answer(user_id, word_id):
            session_data = {
                "word_id": word_id,
                "user_id": user_id,
                "quality": 4,
                "response_time": 2.5
            }
            return client.post("/api/v1/submit-answer", json=session_data)
        
        # Make 5 concurrent submit requests
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(submit_answer, f"user{i}", i) 
                for i in range(1, 6)
            ]
            responses = [future.result() for future in futures]
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200


@pytest.mark.slow
class TestDomainPerformance:
    """Performance tests for domain entities"""
    
    def test_word_creation_performance(self, test_data_factory):
        """Test performance of creating many Word entities"""
        start_time = time.time()
        
        words = []
        for i in range(1000):
            word = test_data_factory.create_word(
                word_id=i,
                word=f"word{i}",
                frequency_rank=i,
                difficulty_level=(i % 5) + 1
            )
            words.append(word)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        assert len(words) == 1000
        assert creation_time < 1.0  # Should create 1000 words within 1 second
    
    def test_user_progress_update_performance(self, test_data_factory):
        """Test performance of updating UserProgress entities"""
        progress = test_data_factory.create_user_progress()
        
        start_time = time.time()
        
        # Simulate 100 progress updates
        for i in range(100):
            quality = test_data_factory.create_quality((i % 6))
            events = progress.update_progress(quality)
        
        end_time = time.time()
        update_time = end_time - start_time
        
        assert update_time < 0.5  # Should handle 100 updates within 0.5 seconds
    
    def test_study_session_creation_performance(self, test_data_factory):
        """Test performance of creating many StudySession entities"""
        start_time = time.time()
        
        sessions = []
        for i in range(1000):
            session = test_data_factory.create_study_session(
                session_id=i,
                word_id=i,
                user_id=f"user{i % 10}",
                correct=(i % 2 == 0),
                response_time=i * 0.1,
                quality=(i % 6)
            )
            sessions.append(session)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        assert len(sessions) == 1000
        assert creation_time < 1.0  # Should create 1000 sessions within 1 second
    
    def test_value_object_creation_performance(self, test_data_factory):
        """Test performance of creating value objects"""
        start_time = time.time()
        
        # Create 1000 of each type of value object
        qualities = []
        difficulty_levels = []
        frequency_ranks = []
        
        for i in range(1000):
            qualities.append(test_data_factory.create_quality(i % 6))
            difficulty_levels.append(test_data_factory.create_difficulty_level((i % 5) + 1))
            frequency_ranks.append(test_data_factory.create_frequency_rank(i + 1))
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        assert len(qualities) == 1000
        assert len(difficulty_levels) == 1000
        assert len(frequency_ranks) == 1000
        assert creation_time < 0.5  # Should create 3000 value objects within 0.5 seconds


@pytest.mark.slow
class TestMemoryUsage:
    """Tests for memory usage patterns"""
    
    def test_word_memory_usage(self, test_data_factory):
        """Test memory usage when creating many Word entities"""
        import sys
        
        # Create many words and check memory usage
        words = []
        for i in range(10000):
            word = test_data_factory.create_word(
                word_id=i,
                word=f"word{i}",
                frequency_rank=i,
                difficulty_level=(i % 5) + 1
            )
            words.append(word)
        
        # Check that memory usage is reasonable
        memory_per_word = sys.getsizeof(words) / len(words)
        assert memory_per_word < 1000  # Should use less than 1KB per word on average
    
    def test_user_progress_memory_usage(self, test_data_factory):
        """Test memory usage when creating many UserProgress entities"""
        import sys
        
        # Create many user progress entries
        progress_entries = []
        for i in range(10000):
            progress = test_data_factory.create_user_progress(
                progress_id=i,
                user_id=f"user{i % 100}",
                word_id=i,
                repetitions=i % 10,
                ease_factor=2.0 + (i % 10) * 0.1,
                interval=i % 30 + 1
            )
            progress_entries.append(progress)
        
        # Check that memory usage is reasonable
        memory_per_progress = sys.getsizeof(progress_entries) / len(progress_entries)
        assert memory_per_progress < 1000  # Should use less than 1KB per progress entry on average


@pytest.fixture
def test_data_factory():
    """Provide TestDataFactory instance"""
    return TestDataFactory()
