from typing import List, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .logger import setup_logger

logger = setup_logger(__name__)


class LlamaHandler:
    """Handles interactions with Llama 2 7B model."""

    def __init__(self, model_path: str = "meta-llama/Llama-2-7b"):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        except Exception as e:
            logger.error(f"Model initialization error: {e}")
            raise

    def get_completion(
            self,
            prompt: str,
            max_tokens: int = 100
    ) -> Optional[List[str]]:
        """Get completion from Llama model."""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.7,
                do_sample=True
            )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return self._parse_sensitive_info(response)

        except Exception as e:
            logger.error(f"LLM completion error: {e}")
            return None

    def _parse_sensitive_info(self, response: str) -> List[str]:
        """Parse sensitive information from LLM response."""
        # Simple parsing - in practice, would need more sophisticated parsing
        sensitive_items = []
        lines = response.split('\n')

        for line in lines:
            if 'sensitive' in line.lower() or 'personal' in line.lower():
                item = line.split(':')[-1].strip()
                if item:
                    sensitive_items.append(item)

        return sensitive_items
