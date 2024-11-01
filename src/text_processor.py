from typing import Dict, Tuple
from .detector import PIIDetector
from .masker import PIIMasker
from .entity_extractor import EntityExtractor
from .logger import setup_logger

logger = setup_logger(__name__)


class TextProcessor:
    """Coordinates PII detection and masking process."""

    def __init__(
            self,
            detector: PIIDetector,
            masker: PIIMasker,
            entity_extractor: EntityExtractor
    ):
        self.detector = detector
        self.masker = masker
        self.entity_extractor = entity_extractor

    def process(self, text: str) -> Tuple[str, Dict]:
        """Process text to detect and mask PII."""
        try:
            # Extract named entities
            entities = self.entity_extractor.extract_entities(text)

            # Detect PII
            pii_findings = self.detector.detect(text)

            # Add relevant entities to findings
            relevant_types = {'PERSON', 'ORG', 'GPE', 'DATE'}
            for ent_type, instances in entities.items():
                if ent_type in relevant_types:
                    pii_findings[ent_type.lower()] = instances

            # Mask PII
            masked_text = self.masker.mask(text, pii_findings)

            return masked_text, pii_findings

        except Exception as e:
            logger.error(f"Text processing error: {e}")
            return text, {}