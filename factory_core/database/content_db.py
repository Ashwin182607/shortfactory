"""
Content database implementation for ShortFactory.
Handles storage and retrieval of content-related data.
"""

from uuid import uuid4
from typing import Optional

from factory_core.database.db_base import TinyMongoDocument, CacheDocument

class ContentManager:
    """Manages content data with both persistent storage and caching."""
    
    def __init__(self, document_id: str, content_type: str, is_new: bool = False):
        """Initialize content manager.
        
        Args:
            document_id: Unique identifier for the content
            content_type: Type of content (e.g., 'video', 'audio', 'script')
            is_new: Whether this is a new content item
        """
        self.content_type = content_type
        self.mongo_doc = TinyMongoDocument("content_db", "content", document_id, is_new)
        self.cache_doc = CacheDocument("content", document_id)
        
        if is_new:
            self.mongo_doc.save("content_type", content_type)
            self.mongo_doc.save("status", "initialized")

    def save_metadata(self, key: str, value: any) -> None:
        """Save metadata to persistent storage."""
        self.mongo_doc.save(key, value)

    def get_metadata(self, key: str) -> any:
        """Get metadata from persistent storage."""
        return self.mongo_doc.get(key)

    def cache_data(self, key: str, value: any, expiry_seconds: int = None) -> None:
        """Cache data with optional expiry.
        
        Args:
            key: Cache key
            value: Data to cache
            expiry_seconds: Optional expiry time in seconds
        """
        self.cache_doc.set_with_expiry(key, value, expiry_seconds)

    def get_cached_data(self, key: str) -> any:
        """Get cached data if not expired."""
        return self.cache_doc.get_if_fresh(key)

    def clear_cache(self) -> None:
        """Clear cached data."""
        self.cache_doc.delete()

    def delete(self) -> None:
        """Delete both persistent and cached data."""
        self.mongo_doc.delete()
        self.cache_doc.delete()

    @property
    def id(self) -> str:
        """Get content ID."""
        return self.mongo_doc.get_id()

class ContentDatabase:
    """Main interface for content database operations."""
    
    def __init__(self):
        """Initialize content database."""
        self.content_collection = TinyMongoDocument("content_db", "content", None)._collection

    def create_content(self, content_type: str) -> ContentManager:
        """Create new content entry.
        
        Args:
            content_type: Type of content to create
            
        Returns:
            ContentManager instance for the new content
        """
        content_id = uuid4().hex[:24]
        return ContentManager(content_id, content_type, True)

    def get_content(self, content_id: str, content_type: str) -> Optional[ContentManager]:
        """Get existing content.
        
        Args:
            content_id: Content identifier
            content_type: Expected content type
            
        Returns:
            ContentManager instance if found, None otherwise
        """
        try:
            content = ContentManager(content_id, content_type)
            stored_type = content.get_metadata("content_type")
            return content if stored_type == content_type else None
        except Exception:
            return None

    def list_content(self, content_type: Optional[str] = None) -> list:
        """List all content of specified type.
        
        Args:
            content_type: Optional type filter
            
        Returns:
            List of content IDs
        """
        query = {"content_type": content_type} if content_type else {}
        return [doc["_id"] for doc in self.content_collection.find(query)]
