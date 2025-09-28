"""
Unit tests for domain value objects
"""
import pytest
from src.domain.value_objects.quality import Quality, DifficultyLevel, FrequencyRank
from src.domain.value_objects.identifiers import UserId, WordId


class TestQuality:
    """Test cases for Quality value object"""
    
    def test_valid_quality_values(self):
        """Test that valid quality values (0-5) are accepted"""
        for value in range(6):
            quality = Quality(value)
            assert quality.value == value
    
    def test_invalid_quality_values(self):
        """Test that invalid quality values raise ValueError"""
        with pytest.raises(ValueError, match="Quality must be between 0 and 5"):
            Quality(-1)
        
        with pytest.raises(ValueError, match="Quality must be between 0 and 5"):
            Quality(6)
    
    def test_non_integer_quality(self):
        """Test that non-integer values raise ValueError"""
        with pytest.raises(ValueError, match="Quality must be an integer"):
            Quality("5")
        
        with pytest.raises(ValueError, match="Quality must be an integer"):
            Quality(3.5)
    
    def test_is_correct(self):
        """Test is_correct method"""
        assert Quality(3).is_correct() is True
        assert Quality(4).is_correct() is True
        assert Quality(5).is_correct() is True
        assert Quality(2).is_correct() is False
        assert Quality(1).is_correct() is False
        assert Quality(0).is_correct() is False
    
    def test_is_perfect(self):
        """Test is_perfect method"""
        assert Quality(5).is_perfect() is True
        assert Quality(4).is_perfect() is False
        assert Quality(3).is_perfect() is False
    
    def test_is_poor(self):
        """Test is_poor method"""
        assert Quality(2).is_poor() is True
        assert Quality(1).is_poor() is True
        assert Quality(0).is_poor() is True
        assert Quality(3).is_poor() is False
        assert Quality(4).is_poor() is False
        assert Quality(5).is_poor() is False


class TestDifficultyLevel:
    """Test cases for DifficultyLevel value object"""
    
    def test_valid_difficulty_levels(self):
        """Test that valid difficulty levels (1-5) are accepted"""
        for value in range(1, 6):
            level = DifficultyLevel(value)
            assert level.value == value
    
    def test_invalid_difficulty_levels(self):
        """Test that invalid difficulty levels raise ValueError"""
        with pytest.raises(ValueError, match="Difficulty level must be between 1 and 5"):
            DifficultyLevel(0)
        
        with pytest.raises(ValueError, match="Difficulty level must be between 1 and 5"):
            DifficultyLevel(6)
    
    def test_non_integer_difficulty(self):
        """Test that non-integer values raise ValueError"""
        with pytest.raises(ValueError, match="Difficulty level must be an integer"):
            DifficultyLevel("3")
        
        with pytest.raises(ValueError, match="Difficulty level must be an integer"):
            DifficultyLevel(2.5)
    
    def test_is_beginner(self):
        """Test is_beginner method"""
        assert DifficultyLevel(1).is_beginner() is True
        assert DifficultyLevel(2).is_beginner() is True
        assert DifficultyLevel(3).is_beginner() is False
        assert DifficultyLevel(4).is_beginner() is False
        assert DifficultyLevel(5).is_beginner() is False
    
    def test_is_intermediate(self):
        """Test is_intermediate method"""
        assert DifficultyLevel(1).is_intermediate() is False
        assert DifficultyLevel(2).is_intermediate() is False
        assert DifficultyLevel(3).is_intermediate() is True
        assert DifficultyLevel(4).is_intermediate() is False
        assert DifficultyLevel(5).is_intermediate() is False
    
    def test_is_advanced(self):
        """Test is_advanced method"""
        assert DifficultyLevel(1).is_advanced() is False
        assert DifficultyLevel(2).is_advanced() is False
        assert DifficultyLevel(3).is_advanced() is False
        assert DifficultyLevel(4).is_advanced() is True
        assert DifficultyLevel(5).is_advanced() is True


class TestFrequencyRank:
    """Test cases for FrequencyRank value object"""
    
    def test_valid_frequency_ranks(self):
        """Test that valid frequency ranks are accepted"""
        rank = FrequencyRank(1)
        assert rank.value == 1
        
        rank = FrequencyRank(1000)
        assert rank.value == 1000
    
    def test_invalid_frequency_ranks(self):
        """Test that invalid frequency ranks raise ValueError"""
        with pytest.raises(ValueError, match="Frequency rank must be positive"):
            FrequencyRank(0)
        
        with pytest.raises(ValueError, match="Frequency rank must be positive"):
            FrequencyRank(-1)
    
    def test_non_integer_frequency(self):
        """Test that non-integer values raise ValueError"""
        with pytest.raises(ValueError, match="Frequency rank must be an integer"):
            FrequencyRank("100")
        
        with pytest.raises(ValueError, match="Frequency rank must be an integer"):
            FrequencyRank(100.5)
    
    def test_is_very_common(self):
        """Test is_very_common method"""
        assert FrequencyRank(50).is_very_common() is True
        assert FrequencyRank(100).is_very_common() is True
        assert FrequencyRank(101).is_very_common() is False
        assert FrequencyRank(1000).is_very_common() is False
    
    def test_is_common(self):
        """Test is_common method"""
        assert FrequencyRank(50).is_common() is True
        assert FrequencyRank(100).is_common() is True
        assert FrequencyRank(500).is_common() is True
        assert FrequencyRank(1000).is_common() is True
        assert FrequencyRank(1001).is_common() is False
    
    def test_is_uncommon(self):
        """Test is_uncommon method"""
        assert FrequencyRank(1000).is_uncommon() is False
        assert FrequencyRank(1001).is_uncommon() is True
        assert FrequencyRank(2000).is_uncommon() is True


class TestUserId:
    """Test cases for UserId value object"""
    
    def test_valid_user_ids(self):
        """Test that valid user IDs are accepted"""
        user_id = UserId("user123")
        assert user_id.value == "user123"
        
        user_id = UserId("abc")
        assert user_id.value == "abc"
    
    def test_empty_user_id(self):
        """Test that empty user ID raises ValueError"""
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            UserId("")
        
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            UserId("   ")
    
    def test_short_user_id(self):
        """Test that short user ID raises ValueError"""
        with pytest.raises(ValueError, match="User ID must have at least 3 characters"):
            UserId("ab")
        
        with pytest.raises(ValueError, match="User ID must have at least 3 characters"):
            UserId("a")


class TestWordId:
    """Test cases for WordId value object"""
    
    def test_valid_word_ids(self):
        """Test that valid word IDs are accepted"""
        word_id = WordId(1)
        assert word_id.value == 1
        
        word_id = WordId(100)
        assert word_id.value == 100
    
    def test_invalid_word_ids(self):
        """Test that invalid word IDs raise ValueError"""
        with pytest.raises(ValueError, match="Word ID must be positive"):
            WordId(0)
        
        with pytest.raises(ValueError, match="Word ID must be positive"):
            WordId(-1)
    
    def test_non_integer_word_id(self):
        """Test that non-integer values raise ValueError"""
        with pytest.raises(ValueError, match="Word ID must be an integer"):
            WordId("1")
        
        with pytest.raises(ValueError, match="Word ID must be an integer"):
            WordId(1.5)
