from typing import List, Dict
import spacy
from .logger import setup_logger

logger = setup_logger(__name__)


class EntityExtractor:
    """Extracts named entities for additional PII detection."""

    def __init__(self, model: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            raise

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text."""
        try:
            doc = self.nlp(text)
            entities = {}

            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)

            return entities

        except Exception as e:
            logger.error(f"Entity extraction error: {e}")
            return {}