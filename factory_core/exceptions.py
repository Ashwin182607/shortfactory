"""
Custom exceptions for ShortFactory.
Provides a hierarchy of exceptions for different error types.
"""

class ShortFactoryError(Exception):
    """Base exception for all ShortFactory errors."""
    pass

# Database Exceptions
class DatabaseError(ShortFactoryError):
    """Base exception for database-related errors."""
    pass

class DocumentNotFoundError(DatabaseError):
    """Raised when a document cannot be found."""
    pass

class SerializationError(DatabaseError):
    """Raised when data cannot be serialized/deserialized."""
    pass

class CacheError(DatabaseError):
    """Base exception for cache-related errors."""
    pass

class CacheExpiredError(CacheError):
    """Raised when cached data has expired."""
    pass

class CacheWriteError(CacheError):
    """Raised when cache write operation fails."""
    pass

# Audio Exceptions
class AudioError(ShortFactoryError):
    """Base exception for audio-related errors."""
    pass

class VoiceGenerationError(AudioError):
    """Raised when voice generation fails."""
    pass

class AudioProcessingError(AudioError):
    """Raised when audio processing fails."""
    pass

class VoiceQuotaError(AudioError):
    """Raised when voice service quota is exceeded."""
    pass

class AudioFileError(AudioError):
    """Raised when there are issues with audio files."""
    pass

# Content Exceptions
class ContentError(ShortFactoryError):
    """Base exception for content-related errors."""
    pass

class ContentTypeError(ContentError):
    """Raised when content type is invalid."""
    pass

class ContentNotFoundError(ContentError):
    """Raised when content cannot be found."""
    pass

class ContentValidationError(ContentError):
    """Raised when content validation fails."""
    pass

# System Exceptions
class SystemError(ShortFactoryError):
    """Base exception for system-related errors."""
    pass

class ResourceError(SystemError):
    """Raised when system resources are insufficient."""
    pass

class ConfigurationError(SystemError):
    """Raised when configuration is invalid."""
    pass

# API Exceptions
class APIError(ShortFactoryError):
    """Base exception for API-related errors."""
    pass

class APIQuotaError(APIError):
    """Raised when API quota is exceeded."""
    pass

class APIAuthenticationError(APIError):
    """Raised when API authentication fails."""
    pass

class APIResponseError(APIError):
    """Raised when API response is invalid."""
    pass
