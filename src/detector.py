import re
from typing import List, Set, Dict
from .llm_handler import LlamaHandler
from .logger import setup_logger

logger = setup_logger(__name__)


class PIIDetector:
    """Detects PII using regex patterns and LLM validation."""

    def __init__(self, llm_handler: LlamaHandler):
        self.llm = llm_handler
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_card': r'\b\d{4}[-. ]?\d{4}[-. ]?\d{4}[-. ]?\d{4}\b',
            'address': r'\b\d+\s+[A-Za-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\.?\b'
        }

    def detect(self, text: str) -> Dict[str, List[str]]:
        """Detect PII in text using patterns and LLM verification."""
        findings = {}

        # Pattern-based detection
        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            findings[pii_type] = [m.group() for m in matches]

        # LLM-based verification
        prompt = f"Identify if this text contains sensitive information: {text}"
        llm_findings = self.llm.get_completion(prompt)

        # Merge findings
        if llm_findings:
            findings['llm_detected'] = llm_findings

        return findings