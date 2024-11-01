from typing import Dict, List
import hashlib
from .logger import setup_logger

logger = setup_logger(__name__)


class PIIMasker:
    """Masks detected PII in text."""

    def __init__(self):
        self.mask_patterns = {
            'email': '[EMAIL]',
            'phone': '[PHONE]',
            'ssn': '[SSN]',
            'credit_card': '[CC]',
            'address': '[ADDRESS]',
            'llm_detected': '[SENSITIVE]'
        }
        self.hash_cache = {}

    def mask(self, text: str, findings: Dict[str, List[str]]) -> str:
        """Mask detected PII in text."""
        try:
            masked_text = text

            for pii_type, instances in findings.items():
                mask = self.mask_patterns.get(pii_type, '[MASKED]')

                for instance in instances:
                    masked_text = self.replace_with_consistent_mask(
                        masked_text, instance, mask
                    )

            return masked_text

        except Exception as e:
            logger.error(f"Masking error: {e}")
            return text

    def replace_with_consistent_mask(
            self,
            text: str,
            pii: str,
            mask_pattern: str
    ) -> str:
        """Replace PII with consistent masked value."""
        if pii not in self.hash_cache:
            hash_val = hashlib.md5(pii.encode()).hexdigest()[:6]
            self.hash_cache[pii] = f"{mask_pattern}_{hash_val}"

        return text.replace(pii, self.hash_cache[pii])