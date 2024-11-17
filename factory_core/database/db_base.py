"""
Base database functionality for ShortFactory.
Implements TinyDB/TinyMongo for document storage and caching.
"""

import threading
from abc import ABC, abstractmethod
import os
from pathlib import Path
import tinydb
import tinymongo as tm
import json
import time
from typing import Any, Optional, Dict, Union

from factory_core.exceptions import (
    DatabaseError, DocumentNotFoundError, SerializationError,
    CacheError, CacheExpiredError, CacheWriteError
)

class TinyMongoClient(tm.TinyMongoClient):
    @property
    def _storage(self):
        return tinydb.storages.JSONStorage

# Initialize database
DB_DIR = Path(".database")
DB_DIR.mkdir(exist_ok=True)
TINY_MONGO_DATABASE = TinyMongoClient(str(DB_DIR))

class AbstractDocument(ABC):
    """Abstract base class for database documents."""
    
    @abstractmethod
    def save(self, key: str, data: Any) -> None:
        """Save data to the document."""
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        """Retrieve data from the document."""
        pass

    @abstractmethod
    def delete(self) -> None:
        """Delete the document."""
        pass

    @abstractmethod
    def get_id(self) -> str:
        """Get document ID."""
        pass

class TinyMongoDocument(AbstractDocument):
    """TinyMongo document implementation with thread-safe operations."""
    
    _lock = threading.Lock()

    def __init__(self, db_name: str, collection_name: str, document_id: str, create: bool = False):
        """Initialize TinyMongo document.
        
        Args:
            db_name: Database name
            collection_name: Collection name
            document_id: Document ID
            create: Whether to create a new document
            
        Raises:
            DatabaseError: If database initialization fails
            DocumentNotFoundError: If document doesn't exist and create is False
        """
        try:
            self.collection = TINY_MONGO_DATABASE[db_name][collection_name]
            self.collection_name = collection_name
            self.document_id = document_id
            
            if create:
                with self._lock:
                    if self.collection.find_one({"_id": document_id}):
                        raise DatabaseError(f"Document {document_id} already exists")
                    self.collection.insert_one({"_id": document_id})
            elif document_id and not self.collection.find_one({"_id": document_id}):
                raise DocumentNotFoundError(f"Document {document_id} not found")
                
        except Exception as e:
            if isinstance(e, (DatabaseError, DocumentNotFoundError)):
                raise
            raise DatabaseError(f"Database initialization failed: {str(e)}")

    def _serialize_data(self, data: Any) -> Any:
        """Serialize data for storage.
        
        Args:
            data: Data to serialize
            
        Returns:
            Serialized data
            
        Raises:
            SerializationError: If data cannot be serialized
        """
        try:
            # Test if data is JSON serializable
            json.dumps(data)
            return data
        except (TypeError, OverflowError, ValueError) as e:
            try:
                # Try to convert to string representation
                if hasattr(data, 'to_dict'):
                    return data.to_dict()
                elif hasattr(data, '__dict__'):
                    return data.__dict__
                return str(data)
            except Exception as e:
                raise SerializationError(f"Data serialization failed: {str(e)}")

    def save(self, key: str, data: Any) -> None:
        """Thread-safe save operation.
        
        Args:
            key: Key to store data under
            data: Data to store
            
        Raises:
            DatabaseError: If save operation fails
            SerializationError: If data cannot be serialized
        """
        try:
            with self._lock:
                serialized_data = self._serialize_data(data)
                self.collection.update_one(
                    {"_id": self.document_id},
                    {"$set": {key: serialized_data}},
                    upsert=True
                )
        except Exception as e:
            if isinstance(e, SerializationError):
                raise
            raise DatabaseError(f"Save operation failed: {str(e)}")

    def get(self, key: str) -> Any:
        """Thread-safe get operation.
        
        Args:
            key: Key to retrieve data for
            
        Returns:
            Retrieved data
            
        Raises:
            DocumentNotFoundError: If document doesn't exist
            DatabaseError: If retrieval fails
        """
        try:
            with self._lock:
                doc = self.collection.find_one({"_id": self.document_id})
                if not doc:
                    raise DocumentNotFoundError(f"Document {self.document_id} not found")
                return doc.get(key)
        except Exception as e:
            if isinstance(e, DocumentNotFoundError):
                raise
            raise DatabaseError(f"Get operation failed: {str(e)}")

    def delete(self) -> None:
        """Thread-safe delete operation.
        
        Raises:
            DatabaseError: If delete operation fails
        """
        try:
            with self._lock:
                result = self.collection.delete_one({"_id": self.document_id})
                if result.deleted_count == 0:
                    raise DocumentNotFoundError(f"Document {self.document_id} not found")
        except Exception as e:
            if isinstance(e, DocumentNotFoundError):
                raise
            raise DatabaseError(f"Delete operation failed: {str(e)}")

    def get_id(self) -> str:
        """Get document ID."""
        return self.document_id

class CacheDocument(TinyMongoDocument):
    """Cache implementation using TinyMongo."""
    
    def __init__(self, namespace: str, document_id: str):
        """Initialize cache document.
        
        Args:
            namespace: Cache namespace
            document_id: Document ID
            
        Raises:
            CacheError: If cache initialization fails
        """
        try:
            super().__init__("cache_db", namespace, document_id, True)
        except Exception as e:
            raise CacheError(f"Cache initialization failed: {str(e)}")
        
    def set_with_expiry(self, key: str, data: Any, expiry_seconds: Optional[int] = None) -> None:
        """Save data with optional expiry.
        
        Args:
            key: Cache key
            data: Data to cache
            expiry_seconds: Optional expiry time in seconds
            
        Raises:
            CacheWriteError: If cache write fails
            SerializationError: If data cannot be serialized
        """
        try:
            cache_data = {
                "data": data,
                "timestamp": time.time(),
                "expiry": expiry_seconds
            }
            self.save(key, cache_data)
        except Exception as e:
            if isinstance(e, SerializationError):
                raise
            raise CacheWriteError(f"Cache write failed: {str(e)}")
        
    def get_if_fresh(self, key: str) -> Any:
        """Get data if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached data if fresh, None if expired or missing
            
        Raises:
            CacheExpiredError: If data has expired
            CacheError: If cache read fails
        """
        try:
            cache_data = self.get(key)
            if not cache_data:
                return None
                
            if cache_data.get("expiry"):
                age = time.time() - cache_data["timestamp"]
                if age > cache_data["expiry"]:
                    self.delete_key(key)
                    raise CacheExpiredError(f"Cache entry for {key} has expired")
                    
            return cache_data["data"]
            
        except Exception as e:
            if isinstance(e, CacheExpiredError):
                raise
            raise CacheError(f"Cache read failed: {str(e)}")
        
    def delete_key(self, key: str) -> None:
        """Delete specific cache key.
        
        Args:
            key: Key to delete
            
        Raises:
            CacheError: If key deletion fails
        """
        try:
            self.save(key, None)
        except Exception as e:
            raise CacheError(f"Cache key deletion failed: {str(e)}")

    def clear_expired(self) -> None:
        """Clear all expired cache entries.
        
        Raises:
            CacheError: If clearing expired entries fails
        """
        try:
            with self._lock:
                doc = self.collection.find_one({"_id": self.document_id})
                if not doc:
                    return
                    
                current_time = time.time()
                for key, value in doc.items():
                    if key == "_id":
                        continue
                    if isinstance(value, dict) and value.get("expiry"):
                        age = current_time - value["timestamp"]
                        if age > value["expiry"]:
                            self.delete_key(key)
        except Exception as e:
            raise CacheError(f"Cache cleanup failed: {str(e)}")
