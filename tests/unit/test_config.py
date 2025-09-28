"""
Unit tests for configuration
"""
import pytest
import os
from unittest.mock import patch

from src.shared.config import Settings, settings


class TestSettings:
    """Test cases for Settings class"""
    
    def test_default_settings(self):
        """Test default settings values"""
        test_settings = Settings()
        
        # Application configuration
        assert test_settings.APP_NAME == "Spaced Repetition Language Learning API"
        assert test_settings.APP_VERSION == "2.0.0"
        assert test_settings.APP_DESCRIPTION == "API for language learning using spaced repetition with layered architecture and CQRS"
        
        # Server configuration
        assert test_settings.HOST == "0.0.0.0"
        assert test_settings.PORT == 8000
        assert test_settings.DEBUG == False
        assert test_settings.RELOAD == True
        
        # CORS configuration
        assert test_settings.CORS_ORIGINS == ["*"]
        
        # Logging configuration
        assert test_settings.LOG_LEVEL == "info"
    
    def test_settings_class_exists(self):
        """Test that Settings class exists and can be instantiated"""
        assert Settings is not None
        assert callable(Settings)
        
        # Test instantiation
        settings_instance = Settings()
        assert settings_instance is not None
        assert isinstance(settings_instance, Settings)
    
    def test_settings_has_required_attributes(self):
        """Test that Settings has all required attributes"""
        test_settings = Settings()
        
        # Check all required attributes exist
        required_attrs = [
            'APP_NAME', 'APP_VERSION', 'APP_DESCRIPTION',
            'DATABASE_URL', 'HOST', 'PORT', 'DEBUG', 'RELOAD',
            'CORS_ORIGINS', 'LOG_LEVEL'
        ]
        
        for attr in required_attrs:
            assert hasattr(test_settings, attr), f"Settings missing attribute: {attr}"
    
    def test_settings_values_are_strings_or_appropriate_types(self):
        """Test that settings values are of appropriate types"""
        test_settings = Settings()
        
        # String attributes
        assert isinstance(test_settings.APP_NAME, str)
        assert isinstance(test_settings.APP_VERSION, str)
        assert isinstance(test_settings.APP_DESCRIPTION, str)
        assert isinstance(test_settings.DATABASE_URL, str)
        assert isinstance(test_settings.HOST, str)
        assert isinstance(test_settings.LOG_LEVEL, str)
        
        # Integer attributes
        assert isinstance(test_settings.PORT, int)
        
        # Boolean attributes
        assert isinstance(test_settings.DEBUG, bool)
        assert isinstance(test_settings.RELOAD, bool)
        
        # List attributes
        assert isinstance(test_settings.CORS_ORIGINS, list)


class TestGlobalSettings:
    """Test cases for global settings instance"""
    
    def test_global_settings_instance(self):
        """Test that global settings instance exists"""
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_global_settings_values(self):
        """Test that global settings has expected values"""
        assert hasattr(settings, 'APP_NAME')
        assert hasattr(settings, 'APP_VERSION')
        assert hasattr(settings, 'APP_DESCRIPTION')
        assert hasattr(settings, 'DATABASE_URL')
        assert hasattr(settings, 'HOST')
        assert hasattr(settings, 'PORT')
        assert hasattr(settings, 'DEBUG')
        assert hasattr(settings, 'CORS_ORIGINS')
        assert hasattr(settings, 'LOG_LEVEL')
        assert hasattr(settings, 'RELOAD')
    
    def test_global_settings_immutable(self):
        """Test that global settings instance is consistent"""
        # Get settings twice
        settings1 = settings
        settings2 = settings
        
        # Should be the same instance
        assert settings1 is settings2
        
        # Values should be consistent
        assert settings1.APP_NAME == settings2.APP_NAME
        assert settings1.APP_VERSION == settings2.APP_VERSION
        assert settings1.DATABASE_URL == settings2.DATABASE_URL
