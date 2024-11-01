from typing import Dict, Any, Optional, Union
import re
from .logger import setup_logger

logger = setup_logger(__name__)


class InputValidator:
    """Validates input text and configuration."""

    def __init__(self):
        self.max_text_length = 10000
        self.min_text_length = 1

    def validate_text(self, text: str) -> bool:
        """Validate input text."""
        try:
            if not isinstance(text, str):
                logger.error("Input must be string type")
                return False

            if not self.min_text_length <= len(text) <= self.max_text_length:
                logger.error("Text length outside allowed range")
                return False

            if not text.strip():
                logger.error("Text is empty or whitespace")
                return False

            return True

        except Exception as e:
            logger.error(f"Text validation error: {e}")
            return False

    def validate_findings(self, findings: Dict[str, Any]) -> bool:
        """Validate PII findings dictionary."""
        try:
            if not isinstance(findings, dict):
                logger.error("Findings must be dictionary type")
                return False

            valid_keys = {
                'email', 'phone', 'ssn', 'credit_card',
                'address', 'person', 'org', 'gpe'
            }

            if not all(k in valid_keys for k in findings.keys()):
                logger.error("Invalid finding types detected")
                return False

            return True

        except Exception as e:
            logger.error(f"Findings validation error: {e}")
            return False

    def validate_mask_pattern(self, pattern: str) -> bool:
        """Validate masking pattern."""
        try:
            if not isinstance(pattern, str):
                return False

            if not 1 <= len(pattern) <= 20:
                return False

            if not re.match(r'^\[[\w-]+\]$', pattern):
                return False

            return True

        except Exception as e:
            logger.error(f"Pattern validation error: {e}")
            return False


class ConfigValidator:
    """Validates configuration settings."""

    @staticmethod
    def validate_llm_config(config: Dict[str, Any]) -> bool:
        """Validate LLM configuration."""
        required_fields = {'model_path', 'max_tokens', 'temperature'}

        try:
            if not all(field in config for field in required_fields):
                logger.error("Missing required LLM config fields")
                return False

            if not isinstance(config['max_tokens'], int):
                logger.error("max_tokens must be integer")
                return False

            if not 0.0 <= config['temperature'] <= 1.0:
                logger.error("temperature must be between 0 and 1")
                return False

            return True

        except Exception as e:
            logger.error(f"LLM config validation error: {e}")
            return False

    @staticmethod
    def validate_cache_config(config: Dict[str, Any]) -> bool:
        """Validate cache configuration."""
        try:
            if 'ttl_hours' in config and not isinstance(config['ttl_hours'], int):
                logger.error("ttl_hours must be integer")
                return False

            if 'max_size' in config and not isinstance(config['max_size'], int):
                logger.error("max_size must be integer")
                return False

            return True

        except Exception as e:
            logger.error(f"Cache config validation error: {e}")
            return False