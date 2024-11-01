from typing import Dict, Any, Optional
import json, hashlib
from datetime import datetime, timedelta
from .logger import setup_logger

logger = setup_logger(__name__)


class CacheManager:
    """Manages caching of masked text and PII mappings."""

    def __init__(self, cache_file: str = "cache/pii_cache.json"):
        self.cache_file = cache_file
        self.cache: Dict[str, Any] = {}
        self.load_cache()

    def add_to_cache(
            self,
            original: str,
            masked: str,
            findings: Dict,
            ttl_hours: int = 24
    ):
        """Add entry to cache with TTL."""
        try:
            self.cache[self._hash(original)] = {
                'masked': masked,
                'findings': findings,
                'expires': (
                        datetime.now() + timedelta(hours=ttl_hours)
                ).isoformat()
            }
            self.save_cache()

        except Exception as e:
            logger.error(f"Cache addition error: {e}")

    def get_from_cache(self, text: str) -> Optional[Dict]:
        """Retrieve cached entry if exists and not expired."""
        try:
            key = self._hash(text)
            if key in self.cache:
                entry = self.cache[key]
                if datetime.now() < datetime.fromisoformat(entry['expires']):
                    return entry
                else:
                    del self.cache[key]
                    self.save_cache()
            return None

        except Exception as e:
            logger.error(f"Cache retrieval error: {e}")
            return None

    def save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.error(f"Cache save error: {e}")

    def load_cache(self):
        """Load cache from file."""
        try:
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.cache = {}
        except Exception as e:
            logger.error(f"Cache load error: {e}")
            self.cache = {}

    @staticmethod
    def _hash(text: str) -> str:
        """Create hash for cache key."""
        return hashlib.md5(text.encode()).hexdigest()
