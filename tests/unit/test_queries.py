"""
Unit tests for application queries
"""
import pytest
from src.application.queries.study_queries import (
    Query,
    GetUserProgressQuery,
    GetWordStatsQuery,
    GetGlobalStatsQuery,
    GetStudyBlockQuery,
    GetWordByIdQuery,
    GetWordsByDifficultyQuery
)


class TestQuery:
    """Test cases for Query base class"""
    
    def test_query_is_abstract(self):
        """Test that Query cannot be instantiated directly"""
        with pytest.raises(TypeError):
            Query()


class TestGetUserProgressQuery:
    """Test cases for GetUserProgressQuery"""
    
    def test_get_user_progress_query_creation(self):
        """Test creating GetUserProgressQuery"""
        query = GetUserProgressQuery(user_id="user123")
        
        assert query.user_id == "user123"
        assert isinstance(query, Query)
    
    def test_get_user_progress_query_with_different_user_id(self):
        """Test GetUserProgressQuery with different user ID"""
        query = GetUserProgressQuery(user_id="user456")
        
        assert query.user_id == "user456"


class TestGetWordStatsQuery:
    """Test cases for GetWordStatsQuery"""
    
    def test_get_word_stats_query_creation(self):
        """Test creating GetWordStatsQuery"""
        query = GetWordStatsQuery(word_id=1)
        
        assert query.word_id == 1
        assert isinstance(query, Query)
    
    def test_get_word_stats_query_with_different_word_id(self):
        """Test GetWordStatsQuery with different word ID"""
        query = GetWordStatsQuery(word_id=100)
        
        assert query.word_id == 100


class TestGetGlobalStatsQuery:
    """Test cases for GetGlobalStatsQuery"""
    
    def test_get_global_stats_query_creation(self):
        """Test creating GetGlobalStatsQuery"""
        query = GetGlobalStatsQuery()
        
        assert isinstance(query, Query)


class TestGetStudyBlockQuery:
    """Test cases for GetStudyBlockQuery"""
    
    def test_get_study_block_query_creation(self):
        """Test creating GetStudyBlockQuery with default limit"""
        query = GetStudyBlockQuery(user_id="user123")
        
        assert query.user_id == "user123"
        assert query.limit == 20
        assert isinstance(query, Query)
    
    def test_get_study_block_query_with_custom_limit(self):
        """Test GetStudyBlockQuery with custom limit"""
        query = GetStudyBlockQuery(user_id="user123", limit=50)
        
        assert query.user_id == "user123"
        assert query.limit == 50
    
    def test_get_study_block_query_with_zero_limit(self):
        """Test GetStudyBlockQuery with zero limit"""
        query = GetStudyBlockQuery(user_id="user123", limit=0)
        
        assert query.user_id == "user123"
        assert query.limit == 0


class TestGetWordByIdQuery:
    """Test cases for GetWordByIdQuery"""
    
    def test_get_word_by_id_query_creation(self):
        """Test creating GetWordByIdQuery"""
        query = GetWordByIdQuery(word_id=1)
        
        assert query.word_id == 1
        assert isinstance(query, Query)
    
    def test_get_word_by_id_query_with_different_word_id(self):
        """Test GetWordByIdQuery with different word ID"""
        query = GetWordByIdQuery(word_id=100)
        
        assert query.word_id == 100


class TestGetWordsByDifficultyQuery:
    """Test cases for GetWordsByDifficultyQuery"""
    
    def test_get_words_by_difficulty_query_creation(self):
        """Test creating GetWordsByDifficultyQuery without limit"""
        query = GetWordsByDifficultyQuery(difficulty_level=3)
        
        assert query.difficulty_level == 3
        assert query.limit is None
        assert isinstance(query, Query)
    
    def test_get_words_by_difficulty_query_with_limit(self):
        """Test GetWordsByDifficultyQuery with limit"""
        query = GetWordsByDifficultyQuery(difficulty_level=2, limit=10)
        
        assert query.difficulty_level == 2
        assert query.limit == 10
    
    def test_get_words_by_difficulty_query_with_zero_limit(self):
        """Test GetWordsByDifficultyQuery with zero limit"""
        query = GetWordsByDifficultyQuery(difficulty_level=4, limit=0)
        
        assert query.difficulty_level == 4
        assert query.limit == 0
