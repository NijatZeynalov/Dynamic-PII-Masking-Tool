from typing import Optional, Dict, Any
import os
import json
from datetime import datetime
import hashlib
from .logger import setup_logger

logger = setup_logger(__name__)

def ensure_dir(directory: str) -> bool:
    """Create directory if it doesn't exist."""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Directory creation error: {e}")
        return False

def load_json(file_path: str) -> Optional[Dict]:
    """Load JSON file safely."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"JSON load error: {e}")
        return None

def save_json(data: Dict, file_path: str) -> bool:
    """Save dictionary to JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"JSON save error: {e}")
        return False

def generate_hash(text: str) -> str:
    """Generate hash for text."""
    return hashlib.md5(text.encode()).hexdigest()

def get_timestamp() -> str:
    """Get formatted timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    try:
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove non-printable characters
        text = ''.join(char for char in text if char.isprintable())
        return text
    except Exception as e:
        logger.error(f"Text cleaning error: {e}")
        return text

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length."""
    try:
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + '...'
    except Exception as e:
        logger.error(f"Text truncation error: {e}")
        return text
